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


# ============================================================================
#  VOLUME (Fase B) — a Receita computa o volume de TODOS os 192 meses a partir
#  do cronograma de rampa da aba Clientes (não há série histórica separada).
#  Recipe (Receita!<mes><linhaCliente>):
#    volRampa = estágio S6..S1 cujo [ini,fim] contém o mês (vol>0), senão 0
#    override = Clientes!E184:N332 (jan..dez/26, keyed por id) — só se mes>corte
#    vol = (useOverride ? override : volRampa) * fatorOperacao[planta][mes]
#                                              * fatorSensib[planta][mes]
#  Extraímos os INSUMOS BRUTOS (Clientes + overrides + fatores); o JS recalcula.
# ============================================================================
CLI_ROW0, CLI_ROW1 = 7, 174        # faixa de clientes na aba Clientes (A7:A174)
OVR_ROW0, OVR_ROW1 = 184, 332      # bloco de override (A184:A332)
FATOR_OPER = (767, 772)            # Receita: Início de Operação por planta (1..6)
FATOR_SENS = (775, 780)            # Receita: Fator de Sensibilidade por planta


def _ym(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return "%04d-%02d" % (v.year, v.month)
    return None


def _iso(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return "%04d-%02d-%02d" % (v.year, v.month, v.day)
    return None


def _num(v):
    return v if isinstance(v, (int, float)) else None


def extract_clientes(wb):
    """Cronograma por cliente: id, planta, produto, volmax, estágios S1..S6 (vol/ini/fim)."""
    ws = wb["Clientes"]
    rows = list(ws.iter_rows(min_row=1, max_row=OVR_ROW1, max_col=57, values_only=True))
    def cell(r, idx):  # r = nº de linha 1-based; idx = 0-based na tupla
        return rows[r - 1][idx] if r - 1 < len(rows) else None

    clientes = []
    # estágios: (vol_idx, ini_idx, fim_idx) 0-based
    STG = [(33, 34, 36), (37, 38, 40), (41, 42, 44), (45, 46, 48), (49, 50, 52), (53, 54, 56)]
    for r in range(CLI_ROW0, CLI_ROW1 + 1):
        rec = rows[r - 1]
        cid = rec[0]; num = rec[1]; planta = rec[3]; prod = rec[4]; volmax = rec[6]
        if prod not in ("GNL", "GNC"):    # pula cabeçalhos de seção
            continue
        if not isinstance(num, (int, float)):
            continue
        stages = []
        for (vi, ii, fi) in STG:
            stages.append([_num(rec[vi]), _ym(rec[ii]), _ym(rec[fi])])
        clientes.append({
            "id": str(cid).strip(),
            "nome": (str(rec[2]).strip() if rec[2] else ""),      # C
            "planta": int(planta) if isinstance(planta, (int, float)) else None,
            "produto": prod,                                        # E
            "volmax": _num(volmax),                                 # G
            "preco": _num(rec[7]),                                  # H  Preço de venda
            "aluguel": _num(rec[8]),                                # I  Aluguel fixo
            "custo_mol": _num(rec[9]),                              # J  Custo molécula (0/1)
            "ini_contrato": _iso(rec[10]),                          # K
            "ini_op": _iso(rec[11]),                                # L
            "duracao": _num(rec[12]),                               # M  meses
            "fim_contrato": _iso(rec[13]),                          # N
            "distancia": _num(rec[14]),                             # O  km
            "tipo_transp": (str(rec[15]).strip() if rec[15] else None),   # P
            "tipo_regas": (str(rec[16]).strip() if rec[16] else None),    # Q
            "venda_regas": _num(rec[20]),                           # U
            "entrega": (str(rec[21]).strip() if rec[21] else None), # V  CIF/FOB
            "top": _num(rec[22]),                                   # W  Take-or-Pay
            "margem": _num(rec[30]),                                # AE
            "correcao_mol": _num(rec[31]),                          # AF
            "stages": stages,
        })
    return clientes


def extract_overrides(wb):
    """Override de volume near-term (jan..dez/26): {id, produto, {ym: valor}}."""
    ws = wb["Clientes"]
    rows = list(ws.iter_rows(min_row=183, max_row=OVR_ROW1, max_col=14, values_only=True))
    hdr = rows[0]                       # linha 183
    months = [_ym(hdr[j]) for j in range(4, 14)]   # cols E..N
    out = []
    for rec in rows[1:]:
        cid = rec[0]
        if cid in (None, ""):
            continue
        prod = rec[3]
        vals = {}
        for j, ym in enumerate(months):
            if ym is None:
                continue
            v = rec[4 + j]
            if isinstance(v, (int, float)):
                vals[ym] = v
        if vals:
            out.append({"id": str(cid).strip(), "produto": prod, "vals": vals})
    return out, [m for m in months if m]


def read_receita_rows(wb, rmax=1475):
    """UM passo de streaming pela aba Receita -> {rownum: tuple}. Evita O(n²) de
       chamadas iter_rows por linha (fatal numa aba de 2438 linhas em read_only)."""
    ws = wb["Receita"]
    keep = {}
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=rmax, values_only=True), start=1):
        if (27 <= i <= 340) or (764 <= i <= 782) or (1158 <= i <= 1470):
            keep[i] = row
    return keep


def read_variavel_rows(wb):
    """UM passo pela aba Variável -> {rownum: tuple}. Captura macro (10..17),
       fator de reajuste (430..584) e fator IPCA puro (1089..1241)."""
    ws = wb["Variável"]
    keep = {}
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=1245, values_only=True), start=1):
        if (8 <= i <= 20) or (430 <= i <= 584) or (1088 <= i <= 1241):
            keep[i] = row
    return keep


# ---- Fase C: Receita R$ = preço indexado × volume × dias ----------------------
IDX_ROWS = {"ipca_m": 10, "ipca12": 11, "brent": 13, "hh": 15, "dolar": 17}  # Variável
PRECO_BLOCK = (432, 584)   # Variável "Fator de Reajuste": D=precoBase E=dataBase F=indicador G=residual
CORR_BLOCK = (1089, 1241)  # Variável "Fator IPCA puro": E=dataBase H=correcao(1=sem indexação)
REV_BLOCKS = {"GNL": (1161, 1313), "GNC": (1318, 1470)}  # Receita R$ (líquida)


def extract_idx_macro(vrows):
    """Séries macro de indexação (Variável): ipca_m, ipca12, brent, hh, dolar (192 meses)."""
    out = {}
    for key, r in IDX_ROWS.items():
        rec = vrows.get(r)
        out[key] = [rec[COL_FIRST - 1 + k] if rec and COL_FIRST - 1 + k < len(rec) else None
                    for k in range(N_MONTHS)] if rec else [None] * N_MONTHS
    return out


def extract_preco(vrows):
    """Config de preço por cliente: precoBase, dataBase, indicador, residual, correcao."""
    out = {}
    for r in range(PRECO_BLOCK[0], PRECO_BLOCK[1] + 1):
        rec = vrows.get(r)
        if not rec:
            continue
        cid = rec[0]
        if cid in (None, ""):
            continue
        out[str(cid).strip()] = {
            "precoBase": _num(rec[3]),     # D
            "dataBase": _ym(rec[4]),       # E
            "indicador": (str(rec[5]).strip() if rec[5] else None),  # F
            "residual": _num(rec[6]),      # G
        }
    # correcao (H) do bloco IPCA puro
    for r in range(CORR_BLOCK[0], CORR_BLOCK[1] + 1):
        rec = vrows.get(r)
        if not rec:
            continue
        cid = rec[0]
        if cid in (None, ""):
            continue
        c = out.get(str(cid).strip())
        if c is not None:
            c["correcao"] = _num(rec[7])   # H (1 = sem indexação)
    return out


def extract_revenue_golden(rrows, id2planta):
    """Golden de receita (cache do Excel) por planta/produto: GNL 1161-1313, GNC 1318-1470."""
    gold = {}
    for prod, (r0, r1) in REV_BLOCKS.items():
        for r in range(r0, r1 + 1):
            rec = rrows.get(r)
            if not rec:
                continue
            cid = rec[0]
            if cid in (None, ""):
                continue
            p = id2planta.get(str(cid).strip())
            if p is None:
                continue
            arr = gold.setdefault((p, prod), [0.0] * N_MONTHS)
            for k in range(N_MONTHS):
                v = rec[COL_FIRST - 1 + k]
                if isinstance(v, (int, float)):
                    arr[k] += v
    return gold


def extract_fatores(rrows):
    """Fatores por planta (1..6) x 192 meses: operacao (Y/N) e sensibilidade."""
    def block(r0, r1):
        res = {}
        for r in range(r0, r1 + 1):
            rec = rrows.get(r)
            if not rec:
                continue
            pid = rec[0]
            if not isinstance(pid, (int, float)):
                continue
            res[int(pid)] = [rec[COL_FIRST - 1 + k] if COL_FIRST - 1 + k < len(rec) else None
                             for k in range(N_MONTHS)]
        return res
    return block(*FATOR_OPER), block(*FATOR_SENS)


def extract_golden_volume(rrows, id2planta):
    """Golden de validação: soma dos volumes computados (cache do Excel) por planta/produto/mês.
       GNL block = Receita 30..182 ; GNC block = 188..340."""
    gold = {}   # (planta, produto) -> [192]
    def add(r0, r1, produto):
        for r in range(r0, r1 + 1):
            rec = rrows.get(r)
            if not rec:
                continue
            cid = rec[0]
            if cid in (None, ""):
                continue
            p = id2planta.get(str(cid).strip())
            if p is None:
                continue
            arr = gold.setdefault((p, produto), [0.0] * N_MONTHS)
            for k in range(N_MONTHS):
                v = rec[COL_FIRST - 1 + k]
                if isinstance(v, (int, float)):
                    arr[k] += v
    add(30, 182, "GNL")
    add(188, 340, "GNC")
    return gold


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

    # ---- Volume (Fase B) ----
    clientes = extract_clientes(wb)
    id2planta = {c["id"]: c["planta"] for c in clientes if c["planta"]}
    overrides, ovr_months = extract_overrides(wb)
    rrows = read_receita_rows(wb)
    fator_oper, fator_sens = extract_fatores(rrows)
    golden = extract_golden_volume(rrows, id2planta)

    # ---- Receita R$ (Fase C) ----
    vrows = read_variavel_rows(wb)
    idx_macro = extract_idx_macro(vrows)
    preco = extract_preco(vrows)
    rev_golden = extract_revenue_golden(rrows, id2planta)
    print("Clientes: %d | overrides: %d (%s..%s) | fatores plantas: %s | preços: %d" % (
        len(clientes), len(overrides), ovr_months[0], ovr_months[-1], sorted(fator_oper), len(preco)))
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

    # aba Clientes: premissas por cliente (insumo do motor de volume + parametrização)
    ws_c = out.create_sheet("Clientes")
    CFIELDS = ["id", "nome", "planta", "produto", "volmax", "preco", "aluguel",
               "custo_mol", "ini_contrato", "ini_op", "duracao", "fim_contrato",
               "distancia", "tipo_transp", "tipo_regas", "venda_regas", "entrega",
               "top", "margem", "correcao_mol"]
    hdr = list(CFIELDS)
    for s in range(1, 7):
        hdr += ["S%d_vol" % s, "S%d_ini" % s, "S%d_fim" % s]
    ws_c.append(hdr)
    for c in clientes:
        row = [c.get(k) for k in CFIELDS]
        for st in c["stages"]:
            row += [st[0], st[1], st[2]]
        ws_c.append(row)

    # aba Overrides: override near-term (jan..dez/26)
    ws_o = out.create_sheet("Overrides")
    ws_o.append(["id", "produto"] + ovr_months)
    for o in overrides:
        ws_o.append([o["id"], o["produto"]] + [o["vals"].get(m) for m in ovr_months])

    # aba VolumeHist: volume REALIZADO (actuals hardcoded no Excel) por planta/produto.
    # Meses realizados (<=corte) vêm daqui; projeção (>corte) o JS recalcula por rampa.
    ws_vh = out.create_sheet("VolumeHist")
    ws_vh.append(["planta", "produto"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for (p, prod) in sorted(golden):
        arr = golden[(p, prod)]
        ws_vh.append([p, prod] + [arr[k] if k < n_real else None for k in range(N_MONTHS)])

    # aba Fatores: operacao / sensib por planta (1..6) x 192 meses
    ws_f = out.create_sheet("Fatores")
    ws_f.append(["tipo", "planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for tipo, blk in (("operacao", fator_oper), ("sensib", fator_sens)):
        for pid in sorted(blk):
            ws_f.append([tipo, pid] + blk[pid])

    # aba Preco: config de indexação de preço por cliente (Fase C)
    ws_p = out.create_sheet("Preco")
    ws_p.append(["id", "precoBase", "dataBase", "indicador", "residual", "correcao"])
    for cid, p in sorted(preco.items()):
        ws_p.append([cid, p.get("precoBase"), p.get("dataBase"), p.get("indicador"),
                     p.get("residual"), p.get("correcao")])

    # aba IdxMacro: séries de indexação (Variável): ipca_m, ipca12, brent, hh, dolar
    ws_i = out.create_sheet("IdxMacro")
    ws_i.append(["serie"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for key in ("ipca_m", "ipca12", "brent", "hh", "dolar"):
        ws_i.append([key] + idx_macro[key])

    # aba ReceitaHist: receita R$ REALIZADA (actuals) por planta/produto
    ws_rh = out.create_sheet("ReceitaHist")
    ws_rh.append(["planta", "produto"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for (p, prod) in sorted(rev_golden):
        arr = rev_golden[(p, prod)]
        ws_rh.append([p, prod] + [arr[k] if k < n_real else None for k in range(N_MONTHS)])

    out.save(OUT)
    print("OK ->", OUT)

    # ---- golden de validação (fora do xlsx de runtime) ----
    gdir = os.path.join(HERE, "golden")
    os.makedirs(gdir, exist_ok=True)
    gpath = os.path.join(gdir, "volume_por_planta.csv")
    with open(gpath, "w", encoding="utf-8", newline="") as fh:
        fh.write("planta;produto;" + ";".join("%04d-%02d" % (y, mo) for (y, mo) in ym) + "\n")
        for (p, prod) in sorted(golden):
            arr = golden[(p, prod)]
            fh.write("%d;%s;" % (p, prod) + ";".join(repr(round(x, 6)) for x in arr) + "\n")
    print("golden ->", gpath)

    rpath = os.path.join(gdir, "receita_por_planta.csv")
    with open(rpath, "w", encoding="utf-8", newline="") as fh:
        fh.write("planta;produto;" + ";".join("%04d-%02d" % (y, mo) for (y, mo) in ym) + "\n")
        for (p, prod) in sorted(rev_golden):
            arr = rev_golden[(p, prod)]
            fh.write("%d;%s;" % (p, prod) + ";".join(repr(round(x, 4)) for x in arr) + "\n")
    print("golden receita ->", rpath)


if __name__ == "__main__":
    main()
