# -*- coding: utf-8 -*-
"""
Extrai a base HISTÓRICA (Realizado) do modelo GNLink para um xlsx que o
dashboard de BP (../index.html) lê em runtime via SheetJS.

Arquitetura (ver plano): o xlsx carrega SÓ dados brutos históricos; todas as
fórmulas de projeção vivem no JS do index.html. Meses <= corte (DCF!F22) = Realizado.

Formato de saída (fácil de ler com XLSX.utils.sheet_to_json(sh,{header:1})):
  - aba `meses`   : idx | ym (YYYY-MM) | flag (R/O)
  - aba `regioes` : id | codigo | nome
  - aba `Macro`   : serie_id | label | unidade | <192 colunas YYYY-MM>
  - abas por domínio (Receita/Variavel/OPEX/Holding): + coluna `regiao` antes dos meses
    (adicionadas nas próximas fases; ver REGISTRY)

Uso:
    python extrai_historico.py            # usa o cenário padrão (custos a IPCA)
    python extrai_historico.py <src.xlsx>

Referência de estilo de extração: alavancagem/Modelos/extract_16.py (openpyxl, data_only=True).
"""
import sys, os, datetime
import openpyxl
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
BP_DIR = os.path.dirname(HERE)
MODELO_DIR = os.path.join(os.path.dirname(BP_DIR), "Modelo")
DEFAULT_SRC = os.path.join(
    MODELO_DIR, "Modelo - Realizado Jul.26 v2 - CENARIO custos a IPCA 2026.09.04.xlsx"
)
OUT = os.path.join(BP_DIR, "gnlink-bp-historico.xlsx")

# Eixo de tempo do modelo (confirmado): 192 meses, col 9 (jan/2023) .. col 200 (dez/2038)
COL_FIRST = 9
N_MONTHS = 192

# Catálogo de região = Planta (aba Clientes). ids 1..6 nomeados + Outro.
# Sub-abas do dashboard: Consolidado, PR, BA, RN, Terminal PE, Argentina, SAL, Outro.
REGIOES = [
    (1, "PR",          "Paraná"),
    (2, "BA",          "Bahia"),
    (3, "RN",          "Rio Grande do Norte"),
    (4, "Terminal PE", "Terminal PE"),
    (5, "Argentina",   "Argentina"),
    (6, "SAL",         "Projeto SAL"),
    (7, "Outro",       "Outro"),
]

# Séries Macro (globais, sem região). row -> (serie_id, label, unidade)
MACRO_SERIES = [
    (6,  "selic",     "SELIC",       "% a.m."),
    (8,  "ipca",      "IPCA",        "% a.m."),
    (10, "cdi",       "CDI",         "% a.m."),
    (14, "brent",     "Brent",       "US$/bbl"),
    (16, "henryhub",  "Henry Hub",   "US$/MMBtu"),
    (20, "dolar",     "Dólar (PTAX)","BRL/USD"),
    (24, "cpi",       "CPI (EUA)",   "% a.m."),
]


def read_month_axis(wb):
    """Retorna lista de 192 datetimes lendo a linha de datas da aba Macro (r2)."""
    ws = wb["Macro"]
    r2 = next(ws.iter_rows(min_row=2, max_row=2, values_only=True))
    months = []
    for k in range(N_MONTHS):
        v = r2[COL_FIRST - 1 + k]
        if not isinstance(v, (datetime.datetime, datetime.date)):
            raise RuntimeError("Célula de data inesperada na Macro r2 col %d: %r" % (COL_FIRST + k, v))
        months.append(v)
    return months


def read_cutoff(wb, months):
    """Mês de corte do Realizado = DCF!F22 (autoritativo). Fallback: jul/2026."""
    try:
        v = wb["DCF"]["F22"].value
        if isinstance(v, (datetime.datetime, datetime.date)):
            return datetime.date(v.year, v.month, 1)
    except Exception:
        pass
    return datetime.date(2026, 7, 1)


def row_values(ws, row):
    """192 valores de uma linha, a partir de COL_FIRST."""
    r = next(ws.iter_rows(min_row=row, max_row=row, values_only=True))
    out = []
    for k in range(N_MONTHS):
        idx = COL_FIRST - 1 + k
        out.append(r[idx] if idx < len(r) else None)
    return out


def extract_macro(wb, months, cutoff):
    """aba Macro: mantém só o Realizado (meses <= cutoff); projeção fica em branco."""
    ws = wb["Macro"]
    ym = [(m.year, m.month) for m in months]
    keep = [ (datetime.date(y, mo, 1) <= cutoff) for (y, mo) in ym ]
    rows = []
    header = ["serie_id", "label", "unidade"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym]
    rows.append(header)
    for (r, sid, label, unit) in MACRO_SERIES:
        vals = row_values(ws, r)
        vals = [ (v if keep[i] else None) for i, v in enumerate(vals) ]
        rows.append([sid, label, unit] + vals)
    return rows


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.exists(src):
        sys.exit("Fonte não encontrada: %s" % src)
    print("Fonte:", os.path.basename(src))
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)

    months = read_month_axis(wb)
    cutoff = read_cutoff(wb, months)
    ym = [(m.year, m.month) for m in months]
    n_real = sum(1 for (y, mo) in ym if datetime.date(y, mo, 1) <= cutoff)
    print("Eixo: %s .. %s (%d meses); corte Realizado=%s (%d meses R / %d O)" % (
        "%04d-%02d" % ym[0], "%04d-%02d" % ym[-1], N_MONTHS,
        cutoff.strftime("%Y-%m"), n_real, N_MONTHS - n_real))

    macro = extract_macro(wb, months, cutoff)
    wb.close()

    # ---- monta o xlsx de saída ----
    out = openpyxl.Workbook()
    out.remove(out.active)

    ws_m = out.create_sheet("meses")
    ws_m.append(["idx", "ym", "flag"])
    for i, (y, mo) in enumerate(ym):
        flag = "R" if datetime.date(y, mo, 1) <= cutoff else "O"
        ws_m.append([i, "%04d-%02d" % (y, mo), flag])

    ws_r = out.create_sheet("regioes")
    ws_r.append(["id", "codigo", "nome"])
    for rid, cod, nome in REGIOES:
        ws_r.append([rid, cod, nome])

    ws_ma = out.create_sheet("Macro")
    for row in macro:
        ws_ma.append(row)

    out.save(OUT)
    print("OK ->", OUT)


if __name__ == "__main__":
    main()
