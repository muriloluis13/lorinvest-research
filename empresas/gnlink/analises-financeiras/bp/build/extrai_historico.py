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
import sys, os, datetime, base64, json
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


def real_only(series, n_real):
    """Mantém só os meses realizados (< n_real); zera a PROJEÇÃO (o JS a recalcula
    por fórmula). Base histórica = só o passado medido."""
    return [series[k] if k < n_real else None for k in range(len(series))]


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


def read_receita_rows(wb, rmax=1935):
    """UM passo de streaming pela aba Receita -> {rownum: tuple}. Evita O(n²) de
       chamadas iter_rows por linha (fatal numa aba de 2438 linhas em read_only)."""
    ws = wb["Receita"]
    keep = {}
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=rmax, values_only=True), start=1):
        if (27 <= i <= 340) or (764 <= i <= 782) or (1158 <= i <= 1470) or (1625 <= i <= 1931):
            keep[i] = row
    return keep


def read_variavel_rows(wb):
    """UM passo pela aba Variável -> {rownum: tuple}. Captura macro (10..17),
       molécula (254..259), fator de reajuste (430..584), preço corrigido (586..743)
       e fator IPCA puro (1089..1241)."""
    ws = wb["Variável"]
    keep = {}
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=1245, values_only=True), start=1):
        if (8 <= i <= 20) or (184 <= i <= 268) or (254 <= i <= 259) or (430 <= i <= 584) \
           or (586 <= i <= 743) or (903 <= i <= 1057) or (1071 <= i <= 1076) or (1088 <= i <= 1241):
            keep[i] = row
    return keep


def read_opex_rows(wb):
    """UM passo pela aba OPEX -> {rownum: tuple}. Captura molécula/gás/ajustes e os
       subtotais por categoria/planta (liquefação, compressão, terminal, SG&A,
       distribuição, regás) + CUSTO TOTAL."""
    ws = wb["OPEX"]
    keep = {}
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=2479, values_only=True), start=1):
        if i == 39 or (190 <= i <= 556) or (560 <= i <= 574) \
           or (579 <= i <= 584) or (718 <= i <= 723) or (725 <= i <= 1673) \
           or (1976 <= i <= 1981) or (1983 <= i <= 2473) or i == 2478:
            keep[i] = row
    return keep


# Subtotais de OpEx por categoria -> {planta: linha OPEX}
OPEX_CAT = {
    "liquefacao":   {1: 407, 2: 408, 3: 409, 4: 410, 5: 411, 6: 412},
    "compressao":   {1: 560, 2: 561, 3: 562, 4: 563, 5: 564, 6: 565},
    "terminal":     {1: 569, 2: 570, 3: 571, 4: 572, 5: 573, 6: 574},
    "sga":          {1: 579, 2: 580, 3: 581, 4: 582, 5: 583, 6: 584},
    "distribuicao": {1: 718, 2: 719, 3: 720, 4: 721, 5: 722, 6: 723},
    "regas":        {1: 1976, 2: 1977, 3: 1978, 4: 1979, 5: 1980, 6: 1981},
}


def extract_opex_cat(orows):
    """{categoria: {planta: [192]}} — subtotais de OpEx (ex-gás) por planta."""
    out = {}
    for cat, m in OPEX_CAT.items():
        d = {}
        for p, r in m.items():
            rec = orows.get(r)
            if not rec:
                continue
            d[p] = [rec[COL_FIRST - 1 + k] if COL_FIRST - 1 + k < len(rec) else None
                    for k in range(N_MONTHS)]
        out[cat] = d
    return out


# ---- Logística/Distribuição: config por cliente + planta + globais (port fiel) ----
LOG_ARR_WINDOW = {1: (1526, 1549), 2: (1552, 1574), 3: (1586, 1607),
                  4: (1609, 1629), 5: (1632, 1650), 6: (1653, 1673)}


def _lid(v):
    try:
        return int(round(float(v)))
    except (TypeError, ValueError):
        return None


def extract_logistica(orows):
    """Config da logística (OPEX 725-1673) p/ o motor por-cliente em JS. Validado 1:1
    (logistica_ref.py). Motor: frete_fixo + frete_var + aluguel + cavalo + ociosos + sinergia.
    Volume vem do motor JS (volClienteSerie); aqui só as PREMISSAS por cliente/planta."""
    def cell(r, col):   # col 1-based
        rec = orows.get(r)
        return rec[col - 1] if rec and col - 1 < len(rec) else None

    def scan(r0, r1):   # {id: row} das linhas cujo A é id de cliente (>=11)
        out = {}
        for r in range(r0, r1 + 1):
            cid = _lid(cell(r, 1))
            if cid is not None and cid >= 11:
                out[cid] = r
        return out
    FF = scan(727, 874); FV = scan(878, 1025); AL = scan(1044, 1187); RAWc = scan(1526, 1673)
    clientes = []
    for cid, r in sorted(RAWc.items()):
        planta = int(str(cid)[0])
        tipoC = cell(r, 3)
        tipo = "GNL" if (isinstance(tipoC, str) and tipoC.strip().upper() == "GNL") else "GNC"
        a, b = LOG_ARR_WINDOW.get(planta, (0, -1))
        clientes.append({
            "id": cid, "planta": planta, "tipo": tipo,
            "cap": _num(cell(r, 4)), "descarga": _num(cell(r, 6)),
            "g": _num(cell(r, 7)), "hmax": _num(cell(r, 8)),
            "custo_viagem": (_num(cell(FF[cid], 5)) or 0.0) if cid in FF else 0.0,
            "fob": 1 if (cid in FF and not _num(cell(FF[cid], 8))) else 0,   # H(dist)==0 => guard FOB
            "custo_km": (_num(cell(FV[cid], 5)) or 0.0) if cid in FV else 0.0,
            "aluguel": (_num(cell(AL[cid], 5)) or 0.0) if cid in AL else 0.0,
            "arr_win": 1 if a <= r <= b else 0,
        })
    planta = {}
    for p in range(1, 7):
        planta[p] = {
            "cav_fix": _num(cell(1345 + p, 4)) or 0.0,
            "cav_var": _num(cell(1352 + p, 4)) or 0.0,
            "sin_red": _num(cell(1360 + p, 3)) or 0.0,
            "sin_lim_ord": _ord(cell(1360 + p, 4)),
        }
    globs = {
        "idle_target": _num(cell(1035, 4)), "idle_yearmax": _num(cell(1035, 5)),
        "adic_target": _num(cell(1036, 4)), "prep_cost": _num(cell(1038, 4)),
        "fix_cost": _num(cell(1040, 4)),
    }
    return clientes, planta, globs


# ---- Regás: config por cliente + globais Furui (port fiel) -------------------
REGAS_QTD_WINDOW = {1: (2322, 2345), 2: (2347, 2378), 3: (2380, 2401),
                    4: (2404, 2423), 5: (2425, 2444), 6: (2446, 2465)}
REGAS_ALU_WINDOW = {1: (2009, 2032), 2: (2034, 2065), 3: (2067, 2089),
                    4: (2091, 2110), 5: (2112, 2131), 6: (2133, 2152)}


def extract_regas(orows, n_real):
    """Config da regás (OPEX 1983-2465) p/ o motor por-cliente em JS. Validado 1:1
    (regas_ref.py). Motor: prep_furui + aluguel + montagem(0) + furui_leasing + insumos(0)
    + assistência. Furui recalculado ao vivo (43 USD × dólar × equip × dias). Volume vem
    do motor JS (volClienteSerie / volAgg). Aqui só PREMISSAS."""
    def cell(r, col):
        rec = orows.get(r)
        return rec[col - 1] if rec and col - 1 < len(rec) else None
    # custo/dia por cliente (tabela Aluguel, col E)
    custo_dia = {}
    for p in range(1, 7):
        a, b = REGAS_ALU_WINDOW[p]
        for r in range(a, b + 1):
            cid = _lid(cell(r, 1))
            if cid is not None and cid >= 11:
                custo_dia[cid] = _num(cell(r, 5)) or 0.0
    clientes = []
    for p in range(1, 7):
        a, b = REGAS_QTD_WINDOW[p]
        for r in range(a, b + 1):
            cid = _lid(cell(r, 1))
            if cid is None or cid < 11:
                continue
            cC = cell(r, 3)
            modal = "GNL" if (isinstance(cC, str) and cC.strip().upper() == "GNL") else "GNC"
            fC = cell(r, 6)
            fob = 1 if (isinstance(fC, str) and fC.strip().upper() == "FOB") else 0
            clientes.append({
                "id": cid, "planta": p, "modal": modal,
                "cap": _num(cell(r, 4)), "dias_est": _num(cell(r, 5)),
                "fob": fob, "custo_dia": custo_dia.get(cid, 0.0),
            })
    # semente da variação de frota (row 2001 "Necessidade de Compra" = max(0, frotaGNL-6)):
    # realizado é baked no modelo (o motor JS zera a frota no realizado), então a projeção
    # da preparação (variação mês a mês) precisa do valor realizado no corte como semente.
    necess_real = [_num(cell(2001, COL_FIRST + k)) if k < n_real else None
                   for k in range(N_MONTHS)]
    # dólar Macro (OPEX row 39) — premissa de câmbio que dirige o leasing Furui (≠ dólar
    # da Variável usado na molécula). Série completa (premissa de projeção).
    dolar_macro = [_num(cell(39, COL_FIRST + k)) for k in range(N_MONTHS)]
    globs = {
        "equip": _num(cell(1992, 4)),        # D1992 = 10 equipamentos comprados 18 bar
        "usd_dia": _num(cell(1993, 4)),      # D1993 = 43 USD/dia
        "inicio_ord": _ord(cell(1994, 4)),   # D1994 = 2026-09 início de custo
        "compra_ord": _ord(cell(1995, 4)),   # D1995 = 2029-09 data de compra
        "isos": _num(cell(1996, 4)),         # D1996 = 13000
        "equip_disp": _num(cell(2001, 4)),   # D2001 = 6 disponíveis
        "prep_iso": _num(cell(2003, 4)),     # D2003 = 30000
        "custo_fixo": _num(cell(2005, 4)) or 0.0,   # D2005 = 0
        "assist_valor": _num(cell(2468, 3)) or 1500.0,   # C2468 = 1500 R$
        "assist_por": _num(cell(2468, 4)) or 5000.0,     # D2468 = a cada 5000 m³
    }
    return clientes, globs, necess_real, dolar_macro


# ---- Fase "fiel": premissas de OpEx para portar as fórmulas em JS ------------
def _opex_series(orows, row):
    rec = orows.get(row)
    return [rec[COL_FIRST - 1 + k] if rec and COL_FIRST - 1 + k < len(rec) else None
            for k in range(N_MONTHS)] if rec else [None] * N_MONTHS


def _pp(orows, rows, cidx):
    """Escalar por planta (1..6): valores da coluna cidx (0-based) nas 6 `rows`."""
    out = []
    for r in rows:
        rec = orows.get(r)
        v = rec[cidx] if rec and cidx < len(rec) else None
        out.append(v if isinstance(v, (int, float)) else None)
    return out


def _pp_month(orows, rows, cidx):
    """Mês (1-12) por planta a partir de uma data OU inteiro na coluna cidx."""
    out = []
    for r in rows:
        rec = orows.get(r)
        v = rec[cidx] if rec and cidx < len(rec) else None
        if isinstance(v, (datetime.datetime, datetime.date)):
            out.append(v.month)
        elif isinstance(v, (int, float)):
            out.append(int(v))
        else:
            out.append(None)
    return out


def extract_liquef_prem(orows):
    """Premissas de liquefação por planta (energia, insumos, O&M, perdas, purga)."""
    P = {}
    P["precoMWh"] = _pp(orows, [426, 429, 432, 435, 438, 441], 2)   # C
    P["gerador"]  = _pp(orows, [446, 447, 448, 449, 450, 451], 3)   # D
    P["oem"]      = _pp(orows, [513, 514, 515, 516, 517, 518], 3)
    P["perdaFrac"] = _pp(orows, [529, 530, 531, 532, 533, 534], 3)
    P["purga_c"]  = _pp(orows, [537, 538, 539, 540, 541, 542], 2)   # C
    P["purga_start"] = [_ym(orows.get(r)[4]) if orows.get(r) else None
                        for r in [537, 538, 539, 540, 541, 542]]     # E (data início) -> ym
    # insumos: rate (D) por planta + gates (F,G) onde houver
    INS = {"propano": 470, "agua": 477, "oleo": 484, "glycol": 491,
           "residuos": 498, "mercaptano": 505, "outros": 546}
    for name, r0 in INS.items():
        rows = [r0 + i for i in range(6)]
        P[name + "_rate"] = _pp(orows, rows, 3)   # D
    for name, r0 in (("propano", 470), ("mercaptano", 505)):
        rows = [r0 + i for i in range(6)]
        P[name + "_g1"] = _pp_month(orows, rows, 5)   # F
        P[name + "_g2"] = _pp_month(orows, rows, 6)   # G
    return P


LIQUEF_SUB_ROWS = {"energia": 415, "insumos": 455, "oem": 513, "perdas": 521, "outros": 546}


def extract_liquef_golden(orows):
    """Golden das sub-linhas de liquefação por planta (para depurar o port)."""
    out = {}
    for sub, r0 in LIQUEF_SUB_ROWS.items():
        d = {}
        for p in range(1, 7):
            rec = orows.get(r0 + (p - 1))
            if not rec:
                continue
            d[p] = [rec[COL_FIRST - 1 + k] if COL_FIRST - 1 + k < len(rec) else None
                    for k in range(N_MONTHS)]
        out[sub] = d
    return out


def extract_custo_total(orows):
    """CUSTO TOTAL (OPEX 2478) — gás + todas as categorias — para validação."""
    rec = orows.get(2478)
    if not rec:
        return None
    return [rec[COL_FIRST - 1 + k] if COL_FIRST - 1 + k < len(rec) else None
            for k in range(N_MONTHS)]


# ---- Fase E: DRE / EBITDA (Demonstrativo Financeiro Mensal, consolidado) ------
DRE_ROWS = {
    "receita_bruta": 33, "deducoes": 35, "receita_liquida": 37,
    "receita_gnl": 40, "receita_gnc": 41, "aluguel": 42, "outros": 43, "servico": 44,
    "custos": 51, "resultado_operacional": 85, "ebitda_recorrente": 91, "ebitda": 98,
    "depreciacao": 103, "ebit": 105, "resultado_financeiro": 108, "lucro_liquido": 118,
}


def read_dfm_rows(wb):
    """UM passo pela aba Demonstrativo Financeiro Mensal -> {rownum: tuple} (DRE)."""
    ws = wb["Demonstrativo Financeiro Mensal"]
    keep = {}
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=125, values_only=True), start=1):
        if 30 <= i <= 120:
            keep[i] = row
    return keep


def extract_dre(drows):
    """Linhas-chave da DRE consolidada (R$/mês) x 192 meses."""
    out = {}
    for key, r in DRE_ROWS.items():
        rec = drows.get(r)
        out[key] = [rec[COL_FIRST - 1 + k] if rec and COL_FIRST - 1 + k < len(rec) else None
                    for k in range(N_MONTHS)] if rec else [None] * N_MONTHS
    return out


# ---- Fase C: Receita R$ = preço indexado × volume × dias ----------------------
IDX_ROWS = {"ipca_m": 10, "ipca12": 11, "brent": 13, "hh": 15, "dolar": 17,
            "ipca_anual": 19, "dolar_spot": 16}  # Variável
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


def _ord(v):
    """Ordinal ano*12+(mês-1), compatível com monthsOrd do JS (ord(ym)=y*12+m-1)."""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.year * 12 + (v.month - 1)
    return None


def extract_molecula_prem(vrows, wb):
    """Premissas do motor de reajuste da molécula (fator IPCA/Brent/Dólar/composto) por planta.

    O modelo compõe custo_molécula[p] = base(209) × fator_reajuste(227) × descontos.
    Só o FATOR depende de macro (Brent/IPCA/Dólar) — é ele que reproduzimos ao vivo no JS.
    O restante (base + descontos) entra como componente-base = golden/fator_base no HTML.
    Aqui exportamos a config por planta (ordinais year*12+mês-1) + escalares macro."""
    def row(r):
        return vrows.get(r)
    cfg = {"custoBase": [], "indicador": [], "dataBaseOrd": [], "ocorrencia": [],
           "refDateOrd": [], "pisoSer": [], "tetoSer": [], "compBaseSer": []}

    def mrow(r):   # série mensal (192) da linha r, cache do Excel
        rec = row(r)
        return [rec[COL_FIRST - 1 + k] if rec and COL_FIRST - 1 + k < len(rec) else None
                for k in range(N_MONTHS)] if rec else [None] * N_MONTHS
    for p in range(6):
        # COMPONENTE-BASE da molécula (PREMISSA, sem macro): custo-base(209) × (1+desconto,245)
        # × fator-de-desconto-acumulado(1071). É a parte não-macro de
        # custo_molécula = compBase × fator_reajuste(Brent/IPCA/Dólar). Verificado 1:1 c/ o modelo.
        base = mrow(209 + p)     # 209-214: custo-base com resets
        desc = mrow(245 + p)     # 245-250: desconto série (SUMPRODUCT do cronograma)
        dfac = mrow(1071 + p)    # 1071-1076: fator de desconto acumulado (RN=0,9)
        comp = []
        for k in range(N_MONTHS):
            b = _num(base[k]); dv = _num(desc[k]); df = _num(dfac[k])
            comp.append(None if b is None else b * (1 + (dv or 0)) * (df if df is not None else 1))
        cfg["compBaseSer"].append(comp)
        c = row(184 + p)    # config: C custoBase, D indicador, E dataBase, G ocorrência
        cfg["custoBase"].append(_num(c[2]) if c else None)
        cfg["indicador"].append((str(c[3]).strip() if c and c[3] else None))
        cfg["dataBaseOrd"].append(_ord(c[4]) if c else None)
        cfg["ocorrencia"].append(int(_num(c[6])) if c and _num(c[6]) else None)
        e2 = row(209 + p)   # E209..214 = data de referência Brent (aniversário rolado até E6)
        cfg["refDateOrd"].append(_ord(e2[4]) if e2 else None)
        # piso/teto são SÉRIES mensais (192-197 / 200-205): valor onde ativo, "-"/None onde inativo
        cfg["pisoSer"].append([_num(v) for v in mrow(192 + p)])
        cfg["tetoSer"].append([_num(v) for v in mrow(200 + p)])
    # escalares macro da aba Base Premissas (motores Argentina/Projeto Sal)
    bp = wb["Base Premissas"]
    cfg["dolarBaseAR"] = _num(bp["Q34"].value)      # dólar-base Argentina
    cfg["fixaSAL"] = _num(bp["R35"].value)          # parcela fixa Projeto Sal
    cfg["pctBrentSAL"] = _num(bp["S35"].value)      # % Brent Projeto Sal
    cfg["divisorSAL"] = _num(bp["Q42"].value)       # divisor Brent→R$/m³
    return cfg


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


def _sum_by_planta(rows, r0, r1, id2planta):
    """Soma linhas de cliente (r0..r1) por planta a partir do cache -> {planta: [192]}."""
    out = {}
    for r in range(r0, r1 + 1):
        rec = rows.get(r)
        if not rec:
            continue
        cid = rec[0]
        if cid in (None, ""):
            continue
        p = id2planta.get(str(cid).strip())
        if p is None:
            continue
        arr = out.setdefault(p, [0.0] * N_MONTHS)
        for k in range(N_MONTHS):
            v = rec[COL_FIRST - 1 + k]
            if isinstance(v, (int, float)):
                arr[k] += v
    return out


def extract_rev_extra(rrows, vrows, id2planta):
    """Componentes extras de receita por planta (R$/mês): outros, serviço, aluguel fixo."""
    return {
        "outros":  _sum_by_planta(rrows, 1627, 1774, id2planta),   # Receita OUTROS
        "servico": _sum_by_planta(rrows, 1779, 1931, id2planta),   # Receita SERVIÇO s/ molécula
        "aluguel": _sum_by_planta(vrows, 905, 1057, id2planta),    # Variável ALUGUEL FIXO
    }


# ---- Fase D: custo da molécula / custo do gás --------------------------------
MOLEC_ROWS = {380: 1, 381: 2, 382: 3, 383: 4, 384: 5, 385: 6}  # OPEX -> planta (o q o gás usa)
PRECO_CORR = (589, 743)     # Variável "Preço Variável Corrigido"
GAS_ROWS = {389: 1, 390: 2, 391: 3, 392: 4, 393: 5, 394: 6}    # OPEX -> planta


def extract_molecula(orows):
    """Custo atualizado da molécula por planta (R$/m³) — exatamente a série que o
       custo do gás usa (OPEX 380-385), já com piso/teto e o toggle nominal/real."""
    out = {}
    for r, p in MOLEC_ROWS.items():
        rec = orows.get(r)
        out[p] = [rec[COL_FIRST - 1 + k] if rec and COL_FIRST - 1 + k < len(rec) else None
                  for k in range(N_MONTHS)] if rec else [None] * N_MONTHS
    return out


def extract_preco_brent(vrows, preco):
    """Preço corrigido (indexado) por cliente Brent — projeção exata (acopla molécula)."""
    brent_ids = {cid for cid, p in preco.items()
                 if (p.get("indicador") or "").startswith("Brent")}
    out = {}
    for r in range(PRECO_CORR[0], PRECO_CORR[1] + 1):
        rec = vrows.get(r)
        if not rec:
            continue
        cid = rec[0]
        if cid in (None, ""):
            continue
        cid = str(cid).strip()
        if cid not in brent_ids:
            continue
        out[cid] = [rec[COL_FIRST - 1 + k] if COL_FIRST - 1 + k < len(rec) else None
                    for k in range(N_MONTHS)]
    return out


def extract_gas_golden(orows):
    """Custo do gás por planta (R$/mês) — cache do Excel (OPEX 389-394)."""
    gold = {}
    for r, p in GAS_ROWS.items():
        rec = orows.get(r)
        if not rec:
            continue
        gold[p] = [rec[COL_FIRST - 1 + k] if COL_FIRST - 1 + k < len(rec) else None
                   for k in range(N_MONTHS)]
    return gold


# Ajustes que o custo do gás soma por planta: p1 += Reversão(400), p2 += Venda Gasoduto BA(402)
GAS_ADJ_ROWS = {1: 400, 2: 402}


def extract_gas_adj(orows):
    """Ajustes do custo do gás por planta (reversão/venda no gasoduto) x 192 meses."""
    out = {}
    for p, r in GAS_ADJ_ROWS.items():
        rec = orows.get(r)
        if not rec:
            continue
        out[p] = [rec[COL_FIRST - 1 + k] if COL_FIRST - 1 + k < len(rec) else None
                  for k in range(N_MONTHS)]
    return out


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
    mol_prem = extract_molecula_prem(vrows, wb)
    preco = extract_preco(vrows)
    rev_golden = extract_revenue_golden(rrows, id2planta)
    rev_extra = extract_rev_extra(rrows, vrows, id2planta)

    # ---- Custo da molécula / gás (Fase D) ----
    orows = read_opex_rows(wb)
    molecula = extract_molecula(orows)
    preco_brent = extract_preco_brent(vrows, preco)
    gas_golden = extract_gas_golden(orows)
    gas_adj = extract_gas_adj(orows)
    opex_cat = extract_opex_cat(orows)
    log_cli, log_planta, log_glob = extract_logistica(orows)
    regas_cli, regas_glob, regas_necess, regas_dolar = extract_regas(orows, n_real)
    custo_total = extract_custo_total(orows)
    liquef_prem = extract_liquef_prem(orows)
    liquef_gold = extract_liquef_golden(orows)
    corr556 = _opex_series(orows, 556)
    vol192 = _opex_series(orows, 192)

    # ---- DRE / EBITDA (Fase E) ----
    dre = extract_dre(read_dfm_rows(wb))
    print("Clientes: %d | overrides: %d | preços: %d | molécula plantas: %s | preço Brent: %d | gás plantas: %s" % (
        len(clientes), len(overrides), len(preco), sorted(molecula), len(preco_brent), sorted(gas_golden)))
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

    # aba IdxMacro: séries de indexação (Variável): ipca_m, ipca12, brent, hh, dolar,
    # ipca_anual, dolar_spot (estes 2 alimentam o motor da molécula Argentina/piso-teto)
    ws_i = out.create_sheet("IdxMacro")
    ws_i.append(["serie"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for key in ("ipca_m", "ipca12", "brent", "hh", "dolar", "ipca_anual", "dolar_spot"):
        ws_i.append([key] + idx_macro[key])

    # aba ReceitaHist: receita R$ REALIZADA (actuals) por planta/produto
    ws_rh = out.create_sheet("ReceitaHist")
    ws_rh.append(["planta", "produto"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for (p, prod) in sorted(rev_golden):
        arr = rev_golden[(p, prod)]
        ws_rh.append([p, prod] + [arr[k] if k < n_real else None for k in range(N_MONTHS)])

    # aba RevExtra: componentes extras de receita por planta (outros/serviço/aluguel)
    # — SÓ REALIZADO (a projeção sai por fórmula quando esta categoria for portada)
    ws_re = out.create_sheet("RevExtra")
    ws_re.append(["componente", "planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for comp in ("outros", "servico", "aluguel"):
        for p in sorted(rev_extra.get(comp, {})):
            ws_re.append([comp, p] + real_only(rev_extra[comp][p], n_real))

    # aba MolCompBase: PREMISSA (componente-base) do custo da molécula por planta.
    # custo_molécula = MolCompBase × fator_reajuste(macro) — a molécula é 100% dirigida por
    # fórmula no JS; não há mais série de molécula PROJETADA no xlsx (só a premissa-base).
    ws_mb = out.create_sheet("MolCompBase")
    ws_mb.append(["planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in range(6):
        ws_mb.append([p + 1] + mol_prem["compBaseSer"][p])

    # aba PrecoBrent: preço corrigido por cliente Brent — SÓ REALIZADO (projeção portada depois)
    ws_pb = out.create_sheet("PrecoBrent")
    ws_pb.append(["id"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for cid in sorted(preco_brent):
        ws_pb.append([cid] + real_only(preco_brent[cid], n_real))

    # aba GasHist: custo do gás REALIZADO por planta (R$/mês)
    ws_gh = out.create_sheet("GasHist")
    ws_gh.append(["planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in sorted(gas_golden):
        arr = gas_golden[p]
        ws_gh.append([p] + [arr[k] if k < n_real else None for k in range(N_MONTHS)])

    # aba GasAdj: ajustes do custo do gás por planta (reversão/venda gasoduto) — projeção
    ws_ga = out.create_sheet("GasAdj")
    ws_ga.append(["planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in sorted(gas_adj):
        ws_ga.append([p] + gas_adj[p])

    # aba Opex: subtotais de OpEx (ex-gás) por categoria/planta — SÓ REALIZADO
    # (a projeção de cada categoria vem por fórmula à medida que é portada; liquefação já)
    ws_ox = out.create_sheet("Opex")
    ws_ox.append(["categoria", "planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for cat in OPEX_CAT:
        for p in sorted(opex_cat.get(cat, {})):
            ws_ox.append([cat, p] + real_only(opex_cat[cat][p], n_real))

    # abas da Logística: config por cliente + por planta + globais (premissas do motor JS)
    ws_lc = out.create_sheet("OpexLogCli")
    LOG_FIELDS = ["id", "planta", "tipo", "cap", "descarga", "g", "hmax",
                  "custo_viagem", "fob", "custo_km", "aluguel", "arr_win"]
    ws_lc.append(LOG_FIELDS)
    for c in log_cli:
        ws_lc.append([c[k] for k in LOG_FIELDS])
    ws_lp = out.create_sheet("OpexLogPlanta")
    ws_lp.append(["planta", "cav_fix", "cav_var", "sin_red", "sin_lim_ord"])
    for p in range(1, 7):
        lp = log_planta[p]
        ws_lp.append([p, lp["cav_fix"], lp["cav_var"], lp["sin_red"], lp["sin_lim_ord"]])
    ws_lg = out.create_sheet("OpexLogGlob")
    ws_lg.append(["key", "value"])
    for k in ("idle_target", "idle_yearmax", "adic_target", "prep_cost", "fix_cost"):
        ws_lg.append([k, log_glob[k]])

    # abas da Regás: config por cliente + globais Furui (premissas do motor JS)
    ws_rc = out.create_sheet("OpexRegasCli")
    REGAS_FIELDS = ["id", "planta", "modal", "cap", "dias_est", "fob", "custo_dia"]
    ws_rc.append(REGAS_FIELDS)
    for c in regas_cli:
        ws_rc.append([c[k] for k in REGAS_FIELDS])
    ws_rg = out.create_sheet("OpexRegasGlob")
    ws_rg.append(["key", "value"])
    for k in ("equip", "usd_dia", "inicio_ord", "compra_ord", "isos", "equip_disp",
              "prep_iso", "custo_fixo", "assist_valor", "assist_por"):
        ws_rg.append([k, regas_glob[k]])
    ws_rs = out.create_sheet("OpexRegasSeed")   # semente da variação + dólar Macro (Furui)
    ws_rs.append(["serie"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    ws_rs.append(["necess"] + regas_necess)
    ws_rs.append(["dolar_macro"] + regas_dolar)

    # aba PremLiquef: premissas de liquefação por planta (para portar em JS)
    ws_pl = out.create_sheet("PremLiquef")
    ws_pl.append(["key", "p1", "p2", "p3", "p4", "p5", "p6"])
    for k in sorted(liquef_prem):
        ws_pl.append([k] + list(liquef_prem[k]))

    # (golden de validação — GoldenLiquef, fator da molécula — vive em build/golden/*.csv,
    #  fora do xlsx de runtime, que carrega SÓ histórico + premissas)

    # aba do motor de reajuste da molécula: config por planta (fator IPCA/Brent/Dólar/composto)
    ws_mc = out.create_sheet("MolPremCfg")
    ws_mc.append(["key", "p1", "p2", "p3", "p4", "p5", "p6"])
    for k in ("custoBase", "indicador", "dataBaseOrd", "ocorrencia", "refDateOrd"):
        ws_mc.append([k] + list(mol_prem[k]))
    # escalares macro (mesmos p/ todas as plantas) no rótulo, cols p1..
    for k in ("dolarBaseAR", "fixaSAL", "pctBrentSAL", "divisorSAL"):
        ws_mc.append([k, mol_prem[k]])
    # aba MolPisoTeto: séries mensais de piso/teto do Brent por planta (clamp do reajuste)
    ws_pt = out.create_sheet("MolPisoTeto")
    ws_pt.append(["kind_planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in range(6):
        ws_pt.append(["piso_%d" % (p + 1)] + mol_prem["pisoSer"][p])
    for p in range(6):
        ws_pt.append(["teto_%d" % (p + 1)] + mol_prem["tetoSer"][p])

    # aba SeriesOpex: séries mensais de apoio (fator correção IPCA, vol GNC row192)
    ws_so = out.create_sheet("SeriesOpex")
    ws_so.append(["key"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    ws_so.append(["corr556"] + corr556)
    ws_so.append(["vol192"] + vol192)

    # aba CustoTotal: CUSTO TOTAL consolidado — SÓ REALIZADO (projeção = fórmula no JS)
    if custo_total:
        ws_ct = out.create_sheet("CustoTotal")
        ws_ct.append(["linha"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
        ws_ct.append(["custo_total"] + real_only(custo_total, n_real))

    # aba DRE: linhas-chave da DRE consolidada — SÓ REALIZADO (projeção = fórmula no JS)
    ws_dre = out.create_sheet("DRE")
    ws_dre.append(["linha"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for key in DRE_ROWS:
        ws_dre.append([key] + real_only(dre[key], n_real))

    out.save(OUT)
    print("OK ->", OUT)

    # espelho .js (base64) do xlsx: permite auto-load via file:// (duplo-clique no HTML),
    # onde o navegador bloqueia fetch de arquivo irmão. Carregado por <script> como fallback.
    with open(OUT, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    jspath = os.path.splitext(OUT)[0] + ".js"
    with open(jspath, "w", encoding="utf-8") as fh:
        fh.write("window.__BP_XLSX_B64=" + json.dumps(b64) + ";\n")
    print("mirror ->", jspath)

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

    gaspath = os.path.join(gdir, "gas_por_planta.csv")
    with open(gaspath, "w", encoding="utf-8", newline="") as fh:
        fh.write("planta;" + ";".join("%04d-%02d" % (y, mo) for (y, mo) in ym) + "\n")
        for p in sorted(gas_golden):
            arr = gas_golden[p]
            fh.write("%d;" % p + ";".join(repr(round(x or 0, 4)) for x in arr) + "\n")
    print("golden gás ->", gaspath)

    if custo_total:
        ctpath = os.path.join(gdir, "custo_total.csv")
        with open(ctpath, "w", encoding="utf-8", newline="") as fh:
            fh.write("linha;" + ";".join("%04d-%02d" % (y, mo) for (y, mo) in ym) + "\n")
            fh.write("custo_total;" + ";".join(repr(round(x or 0, 4)) for x in custo_total) + "\n")
        print("golden custo total ->", ctpath)

    # golden (full, projeção incluída) das séries que saíram do xlsx: OpEx por categoria,
    # fator da molécula e DRE. Usados só pelo ?validate (build/golden/*.csv).
    hdr = ";".join("%04d-%02d" % (y, mo) for (y, mo) in ym)
    oxpath = os.path.join(gdir, "opex_por_cat.csv")
    with open(oxpath, "w", encoding="utf-8", newline="") as fh:
        fh.write("categoria;planta;" + hdr + "\n")
        for cat in OPEX_CAT:
            for p in sorted(opex_cat.get(cat, {})):
                fh.write("%s;%d;" % (cat, p) + ";".join(repr(round(x or 0, 4)) for x in opex_cat[cat][p]) + "\n")
    print("golden opex ->", oxpath)

    mfpath = os.path.join(gdir, "mol_fator.csv")
    with open(mfpath, "w", encoding="utf-8", newline="") as fh:
        fh.write("planta;" + hdr + "\n")
        for p in range(6):
            rec = vrows.get(227 + p)
            ser = [rec[COL_FIRST - 1 + k] if rec and COL_FIRST - 1 + k < len(rec) else None
                   for k in range(N_MONTHS)] if rec else [None] * N_MONTHS
            fh.write("%d;" % (p + 1) + ";".join(repr(round(_num(v) or 0, 6)) for v in ser) + "\n")
    print("golden mol fator ->", mfpath)

    drepath = os.path.join(gdir, "dre.csv")
    with open(drepath, "w", encoding="utf-8", newline="") as fh:
        fh.write("linha;" + hdr + "\n")
        for key in DRE_ROWS:
            fh.write("%s;" % key + ";".join(repr(round(x or 0, 4)) for x in dre[key]) + "\n")
    print("golden dre ->", drepath)


if __name__ == "__main__":
    main()
