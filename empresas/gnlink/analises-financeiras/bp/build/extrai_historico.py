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
import sys, os, datetime, base64, json, re, zipfile, html
import openpyxl
from openpyxl.utils import get_column_letter


def read_sheet_formulas(src, display_name):
    """Mapa {(col_1based, row): fórmula-texto} de uma aba, lido do XML (openpyxl com
    data_only=True não expõe fórmulas). Resolve shared formulas pelo master."""
    z = zipfile.ZipFile(src)
    wbxml = z.read("xl/workbook.xml").decode("utf8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf8")
    sheets = re.findall(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wbxml)
    relmap = dict(re.findall(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    name2file = {n: relmap[r] for n, r in sheets}
    tgt = name2file[display_name]
    if not tgt.startswith("xl/"):
        tgt = "xl/" + tgt
    xml = z.read(tgt).decode("utf8")
    z.close()

    def colnum(L):
        n = 0
        for ch in L:
            n = n * 26 + (ord(ch) - 64)
        return n
    frm = {}; shared = {}
    for m in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>]*>(.*?)</c>', xml, re.S):
        coord = (colnum(m.group(1)), int(m.group(2))); inner = m.group(3)
        fb = re.search(r"<f([^>]*)>(.+?)</f>", inner, re.S)
        if fb:
            f = html.unescape(fb.group(2)); frm[coord] = f
            si = re.search(r'si="(\d+)"', fb.group(1))
            if 't="shared"' in fb.group(1) and si:
                shared[si.group(1)] = f
        else:
            sc = re.search(r"<f([^>]*)/>", inner)
            if sc:
                si = re.search(r'si="(\d+)"', sc.group(1))
                if si:
                    frm[coord] = ("SHARED", si.group(1))
    for coord, f in list(frm.items()):
        if isinstance(f, tuple):
            frm[coord] = shared.get(f[1], "")
    return frm

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
    """aba Macro: séries COMPLETAS (realizado + projeção). A projeção macro é PREMISSA
    — valor colado no modelo (SELIC/IPCA/CDI/Brent/HH/Dólar/CPI) que dirige a indexação,
    não é output de fórmula — então vai inteira à planilha. O split realizado/projeção
    continua no flag R/O da aba `meses` (cutoff mantido na assinatura por compat.)."""
    ws = wb["Macro"]
    ym = [(m.year, m.month) for m in months]
    rows = []
    header = ["serie_id", "label", "unidade"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym]
    rows.append(header)
    for (r, sid, label, unit) in MACRO_SERIES:
        vals = row_values(ws, r)
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
            "segmento": (str(rec[28]).strip() if rec[28] else None), # AC segmento (Industrial/Distribuidora/Posto)
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
           or (579 <= i <= 709) or (718 <= i <= 723) or (725 <= i <= 1673) \
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


def extract_sga(orows, n_real):
    """SG&A de planta (OPEX 579-709), 11 componentes por planta — port fiel (sga_ref.py).
    Fórmula paramétrica vale de jan/27 (k48); ago-dez/26 (k43..48) é hardcode (semente).
    Só PREMISSAS + ocupação (driver) + semente do hardcode."""
    def cell(r, col):
        rec = orows.get(r)
        return rec[col - 1] if rec and col - 1 < len(rec) else None
    cfg = {}
    for p in range(1, 7):
        r_sal, r_op, r_eq = 586 + p, 600 + p, 607 + p
        r_as, r_sv, r_vi, r_pj = 614 + p, 621 + p, 628 + p, 635 + p
        r_rg, r_pt, r_oc, r_tr, r_fr = 651 + p, 667 + p, 674 + p, 681 + p, 695 + p
        cfg[p] = {
            "sal_d": _num(cell(r_sal, 4)) or 0.0, "sal_hc": _num(cell(r_sal, 6)) or 0.0,
            "segop_d": _num(cell(r_op, 4)) or 0.0, "segop_e": _num(cell(r_op, 5)) or 0.0,
            "segop_f": _num(cell(r_op, 6)) or 0.0, "segop_ini": _ord(cell(r_op, 7)),
            "segeq_d": _num(cell(r_eq, 4)) or 0.0, "segeq_e": _num(cell(r_eq, 5)) or 0.0,
            "segeq_f": _num(cell(r_eq, 6)) or 0.0, "segeq_ini": _ord(cell(r_eq, 7)),
            "assist_d": _num(cell(r_as, 4)) or 0.0, "assist_mes": _num(cell(r_as, 6)) or 0.0,
            "serv_d": _num(cell(r_sv, 4)) or 0.0, "viag_d": _num(cell(r_vi, 4)) or 0.0,
            "proj_d": _num(cell(r_pj, 4)) or 0.0, "proj_f": _num(cell(r_pj, 6)) or 0.0,
            "proj_g": _num(cell(r_pj, 7)) or 0.0,
            "reg_d": _num(cell(r_rg, 4)) or 0.0, "reg_f": _num(cell(r_rg, 6)) or 0.0,
            "reg_base": _ord(cell(r_rg, 3)),
            "patr_d": _num(cell(r_pt, 4)) or 0.0, "ocup_d": _num(cell(r_oc, 4)) or 0.0,
            "trab_d": _num(cell(r_tr, 4)) or 0.0, "trab_f": _num(cell(r_tr, 6)) or 0.0,
            "trab_base": _ord(cell(r_tr, 3)),
            "cont": _num(cell(688 + p, COL_FIRST + 60)) or 0.0,   # constante (col paramétrica k60)
            "frota_d": _num(cell(r_fr, 4)) or 0.0, "frota_n": _num(cell(r_fr, 6)) or 0.0,
        }
    # ocupação GNL % (rows 644-649) — driver do gatilho de Projetos de Engenharia
    ocup = {p: [_num(cell(643 + p, COL_FIRST + k)) for k in range(N_MONTHS)] for p in range(1, 7)}
    # semente do hardcode: subtotal SG&A (579-584) em k43..48 (ago/26..jan/27); resto None
    seed = {p: [_num(cell(578 + p, COL_FIRST + k)) if (43 <= k <= 48) else None
                for k in range(N_MONTHS)] for p in range(1, 7)}
    reg_base2_ord = 2027 * 12 + 1   # $BF$2 = 2027-02-01 (âncora do regulatório p/ k>=50)
    return cfg, ocup, seed, reg_base2_ord


def extract_comp_term(orows):
    """Compressão (560-565) e Terminal (569-574) por planta — motores simples (port fiel).
    Compressão = (data>=início)?tarifa:0 × op × IPCA. Terminal = tarifa × volume GNL × dias."""
    def cell(r, col):
        rec = orows.get(r)
        return rec[col - 1] if rec and col - 1 < len(rec) else None
    out = {}
    for p in range(1, 7):
        out[p] = {
            "comp_tarifa": _num(cell(559 + p, 4)) or 0.0,       # D560..565
            "comp_ini_ord": _ord(cell(559 + p, 5)),             # E560..565 data de início
            "comp_fim_ord": _ord(cell(559 + p, 6)),             # F560..565 data de fim
            "term_tarifa": _num(cell(568 + p, 4)) or 0.0,       # D569..574
        }
    return out


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
           "refDateOrd": [], "pisoSer": [], "tetoSer": [], "compBaseSer": [], "compBasePrecoSer": [],
           "ajusteExtraSer": []}

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
        comp = []       # base do CUSTO (gás): inclui o fator de desconto acumulado (RN=0,9)
        compP = []      # base do PREÇO (molécula que indexa o preço Brent): SEM o dfac1071
        for k in range(N_MONTHS):
            b = _num(base[k]); dv = _num(desc[k]); df = _num(dfac[k])
            comp.append(None if b is None else b * (1 + (dv or 0)) * (df if df is not None else 1))
            compP.append(None if b is None else b * (1 + (dv or 0)))
        cfg["compBaseSer"].append(comp)
        cfg["compBasePrecoSer"].append(compP)
        # ajuste adicional (Variável 236-241, por posição=planta): fatorExtra=(1+ajuste) DENTRO do
        # fator de reajuste. ≠0 só na banda de orçamento ago-dez/26 (PR/BA); 0 no restante.
        cfg["ajusteExtraSer"].append([_num(v) for v in mrow(236 + p)])
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


def extract_holding_sga(wb):
    """SG&A da holding/matriz (aba Holding, linha 23 = SUM(13:18)). EBITDA = Resultado
    Operacional + Holding23. As 6 componentes são paramétricas: médias/sementes de 2026
    (k36..k47) × corr556 (IPCA, já vivo no HTML) × fatores, com gatilho de escala em r15.
    Saem só as premissas/sementes + a série-driver r32 (proxy de volume da matriz)."""
    ws = wb["Holding"]
    keep = {}
    for i, r in enumerate(ws.iter_rows(min_row=1, max_row=45,
                                       max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1):
        if i in (4, 8, 13, 14, 15, 16, 17, 18, 23, 27, 28, 29, 30, 32, 33):
            keep[i] = r

    def ser(rr):
        row = keep.get(rr)
        return [_num(row[COL_FIRST - 1 + k]) if row and COL_FIRST - 1 + k < len(row) else None
                for k in range(N_MONTHS)]

    def cval(rr, col):   # col 1-based (C=3, D=4)
        row = keep.get(rr)
        return _num(row[col - 1]) if row and col - 1 < len(row) else None

    r13 = ser(13); r14 = ser(14); r15 = ser(15); r16 = ser(16); r17 = ser(17); r32 = ser(32)
    K26 = list(range(36, 48))                              # 2026 = jan..dez (k36..k47)
    seed13 = [(r13[k] or 0.0) for k in K26]                # semente de r13 por mês-calendário

    def avg(rr):
        vals = [(rr[k] or 0.0) for k in K26]
        return sum(vals) / len(vals)

    scal = {
        "C27": cval(27, 3), "C28": cval(28, 3), "C29": cval(29, 3), "C30": cval(30, 3),
        "C32": cval(32, 3), "C33": cval(33, 3), "D18": cval(18, 4),
        "H8": cval(8, 3) if cval(8, 3) is not None else 1.0,
        "SEED15": r15[46] or 0.0, "C34": r32[47] or 0.0,
        "AVG14": avg(r14), "AVG16": avg(r16), "AVG17": avg(r17),
    }
    # semente do Holding23 (SUM 13:18) na banda de orçamento ago-dez/26 (k43..47): r13 é hardcode
    # literal no modelo, então o paramétrico só vale de jan/27 (k48). Guardamos k<48 (realizado+banda).
    r23 = ser(23)
    seed23 = [r23[k] if k < 48 else None for k in range(N_MONTHS)]
    return {"scalars": scal, "seed13": seed13, "r32": r32, "seed23": seed23}


def extract_balanco(wb):
    """MÓDULO CAIXA / FLUXO DE CAIXA + BALANÇO + DCF. O HTML reproduz por fórmula: waterfall de
    caixa, capital de giro (níveis = driver×prazo/30), DFM385 (=Caixa[k-1]×G383×CDI), Div26/resfin,
    máquinas de estado do PL, somas do balanço, VPL/TIR. Aqui saem os INSUMOS COLADOS/de outro
    módulo (pastes voláteis, imposto-caixa, política de dividendos, override de ICMS, sementes,
    geração anual do DCF) + as constantes de prazo/desconto. Validado 1:1 (caixa_balanco_ref.py)."""
    dfm = wb["Demonstrativo Financeiro Mensal"]; dv = wb["Dívida"]; imp = wb["Impostos"]
    dcf = wb["DCF"]; dfa = wb["Demonstrativo Financeiro Anual"]
    def read(ws, rowset, maxr):
        keep = {}
        for i, r in enumerate(ws.iter_rows(min_row=1, max_row=maxr,
                                           max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1):
            if i in rowset:
                keep[i] = r
        return keep
    dfm_rows = {130, 135, 140, 141, 142, 143, 144, 148, 157, 158, 160, 165, 195, 196, 208, 223,
                242, 281, 292, 294, 299, 300, 302, 316, 319, 321, 344, 345, 352, 353, 354, 356,
                360, 362, 363, 364, 368, 374, 383, 385, 349, 351, 355, 357, 359}
    dfmk = read(dfm, dfm_rows, 400)
    # +linhas por bloco do Div26: Seguro (67,76,85,94,103,112) e IOF (64,73,82,91,100,109,118),
    # p/ isolar o "outros" (comissão+taxa, colado) = Div26 − seguros_modelo − IOF_modelo.
    dvk = read(dv, {12, 13, 26, 64, 67, 73, 76, 82, 85, 91, 94, 100, 103, 109, 112, 118}, 120)
    impk = read(imp, {37}, 82)
    dcfk = read(dcf, {5, 15, 19, 20, 21, 22}, 25)
    dfak = read(dfa, {227}, 230)

    def ser(keep, r):
        row = keep.get(r)
        return [_num(row[COL_FIRST - 1 + k]) if row and COL_FIRST - 1 + k < len(row) else None
                for k in range(N_MONTHS)]
    def kc(keep, r, c):   # célula (col 1-based) de uma linha já lida
        row = keep.get(r)
        return _num(row[c - 1]) if row and c - 1 < len(row) else None
    def kdate(keep, r, c):   # célula de DATA -> serial Excel (openpyxl data_only dá datetime)
        row = keep.get(r)
        v = row[c - 1] if row and c - 1 < len(row) else None
        if isinstance(v, datetime.datetime):
            v = v.date()
        if isinstance(v, datetime.date):
            return float((v - datetime.date(1899, 12, 30)).days)
        return _num(v)

    out = {}
    for r in dfm_rows:
        out["dfm%d" % r] = ser(dfmk, r)
    out["div26"] = ser(dvk, 26); out["div12"] = ser(dvk, 12); out["div13"] = ser(dvk, 13)
    # Div26 ("Outros" do resultado financeiro) = Σ_blocos (IOF + Comissão + Taxa + Seguro). O SEGURO é a
    # parcela que depende do SALDO da dívida (reage às premissas) → reproduzido vivo no HTML. As demais
    # (comissão/taxa/IOF = fees de estruturação com cronograma fixo) ficam como baseline COLADO. No HTML:
    #   Div26_vivo = Div26_colado + (seguro_vivo − seguro_modelo). Extraímos o seguro do MODELO (Σ blocos)
    #   para o delta zerar no default (Div26 == colado) e reagir quando uma premissa de dívida muda.
    # só BA (r76) e RN (r85) são reproduzidos vivos (seguro trimestral sobre o saldo do bloco). Outros
    # blocos de seguro (ex.: r103, mensal a partir de 2028) ficam no baseline colado do Div26.
    _segrows = [ser(dvk, r) for r in (76, 85)]
    out["div26_seg"] = [sum((_segrows[j][k] or 0.0) for j in range(len(_segrows))) for k in range(N_MONTHS)]
    out["imp37"] = ser(impk, 37)
    out["const"] = {
        "F349": kc(dfmk, 349, 6), "F357": kc(dfmk, 357, 6), "F359": kc(dfmk, 359, 6),
        "H355": kc(dfmk, 355, 8), "G383": kc(dfmk, 383, 7),
        "F20": kc(dcfk, 20, 6), "F22": kdate(dcfk, 22, 6),
    }
    out["dcf_anos"] = [kc(dcfk, 5, COL_FIRST + j) for j in range(20)]
    out["dfa_gen_cons"] = [kc(dfak, 227, COL_FIRST + j) for j in range(20)]
    # constantes de custo de capital do DCF (col F=6, G=7) — premissas p/ a aba DCF do HTML
    out["dcf_const"] = {
        "growth": kc(dcfk, 15, 6), "kd_pre": kc(dcfk, 19, 6), "ir": kc(dcfk, 19, 7),
        "ke": kc(dcfk, 20, 6), "wacc": kc(dcfk, 21, 6),
    }
    # DCF MENSAL (modelo atualizado): Ke real anual (Painel!F43) + toggle Real/Nominal (Painel!C42).
    # r890: Ke_mensal = ((1+ke_real)^(1/12))·(1+IPCA_mês) − 1  se "Nominal" (grosseia p/ inflação mensal).
    try:
        pn = wb["Painel de Controle"]
        ke_real = pn.cell(43, 6).value            # F43
        modo = str(pn.cell(42, 3).value or "")    # C42: "1 - Real" / "2 - Nominal"
        out["dcf_const"]["ke_real"] = float(ke_real) if ke_real is not None else 0.12
        out["dcf_const"]["ke_real_nominal"] = 0 if modo.strip().startswith("1") else 1
    except Exception:
        out["dcf_const"]["ke_real"] = 0.12
        out["dcf_const"]["ke_real_nominal"] = 1
    # MECÂNICA DE CAIXA MÍNIMO + DÍVIDA ROLLING (do modelo GNLink_Model_2026.09.07, aba Consolidated):
    #   caixa mínimo = C321 meses de custos fixos + retenção BNB; dívida rolling de 1 ano cobre o gap.
    # Params do Dashboard do 09.07 (C321=3, J303=4,5%, J302=IPCA, J304=Quarterly, J300=0). A série de
    # retenção BNB (aba BnbRetencao) é grafada do 09.07 pelo scratchpad/patch_mincash.py (não vem do 09.04).
    out["dcf_const"]["mincash_months"] = 3
    out["dcf_const"]["mincash_spread"] = 0.045
    out["dcf_const"]["mincash_index"] = 0        # 0=IPCA, 1=DI
    out["dcf_const"]["mincash_freq_m"] = 3       # 3=trimestral, 6=semestral, 1=mensal
    out["dcf_const"]["mincash_flatfee"] = 0.0
    out["dcf_const"]["mincash_tenor_m"] = 12     # prazo da dívida rolling (12m = 1 ano)
    return out


def extract_divida(wb, div_formulas):
    """MÓDULO DE DÍVIDA (aba Dívida) — reproduz o cronograma de cada instrumento a partir dos
    TERMOS (premissas): desembolso, tipo (SAC/PRICE), índice (IPCA/CDI), spread, datas/nº de
    amortização, gate de pagamento, comissões, alocação por projeto. Juros = saldo×taxa e o saldo
    devedor saem POR FÓRMULA no HTML. Os blocos BA e RN têm amortização/pagamento COLADOS no Excel
    (fórmula morta = override manual) → entram como VALORES COLADOS (premissa) na planilha."""
    ws = wb["Dívida"]
    # leitura de todas as linhas necessárias num passo (blocos 156..1541 + alocação 1518..1540)
    rows = {}
    for i, r in enumerate(ws.iter_rows(min_row=1, max_row=1545,
                                       max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1):
        rows[i] = r
    def cell(r, c):   # c 1-based
        row = rows.get(r); return row[c - 1] if row and c - 1 < len(row) else None
    def label(r):
        v = cell(r, 2); return (str(v).strip() if v else "")
    def ser(r):
        row = rows.get(r)
        return [_num(row[COL_FIRST - 1 + k]) if row and COL_FIRST - 1 + k < len(row) else None
                for k in range(N_MONTHS)]
    BASES = [156, 215, 274, 333, 389, 445, 501, 560, 615, 670, 729, 788, 847, 906, 965,
             1024, 1083, 1144, 1205, 1266, 1327, 1388, 1449, 1510]
    insts = []
    for bi in range(len(BASES) - 1):
        base, nb = BASES[bi], BASES[bi + 1]
        lab = {}
        for r in range(base, nb):
            t = label(r)
            if t and t not in lab:
                lab[t] = r
        def F(name, col=6):
            r = lab.get(name)
            return (cell(r, col)) if r else None
        def has(name):
            return name in lab
        def _serial(v):   # datetime (openpyxl data_only) OU número -> serial Excel
            if isinstance(v, datetime.datetime):
                v = v.date()
            if isinstance(v, datetime.date):
                return float((v - datetime.date(1899, 12, 30)).days)
            return float(v) if isinstance(v, (int, float)) else None
        def num(name, col=6):
            return _serial(F(name, col))
        name = label(base)
        ini = lab.get("Início do Período")
        amt_row = next((r for r in ("Valor", "Cronograma", "Desembolso Total") if has(r)), "Desembolso Total")
        dt_row = "Data Inicial" if has("Data Inicial") else "Data"
        tr = []
        d_f = _serial(F(dt_row)); a_f = F(amt_row)
        if d_f is not None and isinstance(a_f, (int, float)) and a_f:
            tr.append([int(round(d_f)), float(a_f)])
        d_h = _serial(F(dt_row, 8)); a_h = F(amt_row, 8)
        if d_h is not None and isinstance(a_h, (int, float)) and a_h:
            tr.append([int(round(d_h)), float(a_h)])
        tipo_row = "Cronograma de Amortização" if has("Cronograma de Amortização") else "Pagamento"
        # gate de pagamento: lê do MOD() da fórmula
        pg_period = 0; pg_offset = 0
        for r in range(base, nb):
            f = None
            for c in range(9, 60):
                ff = div_formulas.get((c, r))
                if ff and "MOD(SUM" in ff:
                    f = ff; break
            if f:
                m = re.search(r'MOD\(SUM\([^)]*\)\s*([+-]\s*\d+)?\s*,\s*\$?([A-Z]+)\$?(\d+)\)', f)
                if m:
                    if m.group(1):
                        pg_offset = int(m.group(1).replace(" ", ""))
                    dc = 0
                    for ch in m.group(2):
                        dc = dc * 26 + (ord(ch) - 64)
                    pv = cell(int(m.group(3)), dc)
                    pg_period = int(pv) if isinstance(pv, (int, float)) else 0
                break
        nm = name.lower()
        override = ("bahia" in nm or " ba" in nm or "- ba" in nm or "rio grande" in nm or " rn" in nm or "- rn" in nm)
        rec = {
            "name": name, "tipo": int(F(tipo_row, 5) or 2), "indice": int(F("Índice", 5) or 2),
            "spread": float(F("Spread") or 0.0), "iof": float(F("IOF") or 0.0),
            "comissao": float(F("Comissão") or 0.0), "taxa_comp": float(F("Taxa de Compromisso") or 0.0),
            "inicio_amort": num("Início - Amortização do Principal"),
            "n_amort": num("Período - # Amortização do Principal"),
            "ultima": num("Última Amortização do Principal"),
            "inicio_pgto": num("Início - Pagamento de Juros"),
            "pg_period": pg_period, "pg_offset": pg_offset, "tranches": tr, "override": override,
            "g_rn": _num(cell(1518 + bi, 7)) or 0.0,   # % RN por instrumento (col G) — Imp37 + seguro RN
            "g_ba": _num(cell(1518 + bi, 6)) or 0.0,   # % BA por instrumento (col F) — seguro BA (Div26)
            "g_pr": _num(cell(1518 + bi, 5)) or 0.0,   # % PR por instrumento (col E) — switch de planta
        }
        # sementes do realizado (resumo ini+0..+5) — realizado; para BA/RN também a projeção colada
        if ini:
            rec["seed_desemb"] = ser(ini + 1); rec["seed_amort"] = ser(ini + 2)
            rec["seed_despJ"] = ser(ini + 3); rec["seed_pagJ"] = ser(ini + 4)
            rec["seed_final"] = ser(ini + 5)
        insts.append(rec)
    return insts


def extract_capex(wb):
    """MÓDULO DE CAPEX (aba Capex) — PREMISSAS do plano de investimento, para computar a
    depreciação AO VIVO (não extrair pronta): plano de capex por planta/classe + vidas úteis +
    datas de início. Depreciação linear por vintage (investimento/240 durante 240 meses a partir
    de max(data, início-op)); intangível da holding = amortização em pool (120 meses). O HTML
    reproduz depreciação mensal, capex acumulado e o Ativo Imobilizado do balanço."""
    cx = wb["Capex"]; hd = wb["Holding"]; bp = wb["Base Premissas"]
    pn = wb["Painel de Controle"]; dfm = wb["Demonstrativo Financeiro Mensal"]
    HDR1 = [706, 1039, 1384, 1733, 2088, 2432]; INV1_ROW = [h + 1 for h in HDR1]   # 707..
    HDR2 = [711, 1044, 1389, 1738, 2093, 2437]; INV2_ROW = [h + 1 for h in HDR2]   # 712..
    want = set(INV1_ROW + INV2_ROW + [2])
    cxk = {}
    for i, r in enumerate(cx.iter_rows(min_row=1, max_row=2440,
                                       max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1):
        if i in want:
            cxk[i] = r
    def cser(keep, r):
        row = keep.get(r)
        return [_num(row[COL_FIRST - 1 + k]) if row and COL_FIRST - 1 + k < len(row) else None
                for k in range(N_MONTHS)]
    inv1 = [cser(cxk, INV1_ROW[p]) for p in range(6)]
    inv2 = [cser(cxk, INV2_ROW[p]) for p in range(6)]
    dates_cx = cser(cxk, 2)                       # eixo de datas do Capex (serial 1º do mês)
    hd46 = None; hd54 = None
    for i, r in enumerate(hd.iter_rows(min_row=1, max_row=55,
                                       max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1):
        if i == 46:
            hd46 = [_num(r[COL_FIRST - 1 + k]) if COL_FIRST - 1 + k < len(r) else None
                    for k in range(N_MONTHS)]
        elif i == 54:
            hd54 = [_num(r[COL_FIRST - 1 + k]) if COL_FIRST - 1 + k < len(r) else None
                    for k in range(N_MONTHS)]
    dfmk = {}
    for i, r in enumerate(dfm.iter_rows(min_row=1, max_row=148,
                                        max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1):
        if i in (146, 147):
            dfmk[i] = r
    def dser(r):
        row = dfmk.get(r)
        return [_num(row[COL_FIRST - 1 + k]) if row and COL_FIRST - 1 + k < len(row) else None
                for k in range(N_MONTHS)]
    dfm146 = dser(146); dfm147 = dser(147)
    op_dates = [_num(bp.cell(row=148 + p, column=4).value) for p in range(1, 7)]   # D149..D154
    life = int(round(_num(cx.cell(row=719, column=4).value) or 240))
    holdlife = int(round((_num(hd.cell(row=52, column=4).value) or 10.0) * 12))     # D52 anos -> meses
    flag = _num(pn.cell(row=53, column=2).value) or 0.0
    return {
        "inv1": inv1, "inv2": inv2, "hd46": [(_num(x) if x is not None else 0.0) for x in hd46],
        "dfm147": dfm147, "dates": dates_cx, "op_dates": op_dates,
        "life": life, "holdlife": holdlife, "flag": flag,
        "seed146": (dfm146[42] or 0.0), "seed_hd54": ((hd54[42] if hd54 else 0.0) or 0.0),
        # sementes hardcode de ativos classe-1 lançados direto no cronograma (Bahia/PE/Arg/Sal)
        "extra1": {1: {41: 43764.09, 42: 45658.0}, 3: {42: 45658.0}, 4: {42: 45658.0}, 5: {42: 45658.0}},
    }


def extract_dcfproj(wb):
    """DCF POR PROJETO — insumos que NÃO são reproduzíveis ao vivo pelo motor operacional:
    (1) flags de planta ativa/inativa (Painel!B53..B58 → flag = 1 − B); (2) o Fluxo de Caixa
    Financeiro por projeto (bloco de dívida por planta: Desembolso + Amortização + Juros + Outras),
    que é PLANO DE FINANCIAMENTO (colado). No HTML: EBITDA(p)=RO por planta (vivo), ΔCapital de
    Giro(p)=ΔWC consol × (RL_p/RL_consol) (vivo), Impostos(p)=IR/CSLL consol × (RL_p/RL_consol)
    (vivo), Capex(p)=−(inv1_p+inv2_p) (do módulo de capex), FC Financeiro(p)=este bloco colado.
    Bloco de dívida por planta (base row): PR=60, BA=69, RN=78, PE=87, AR=96, SAL=105;
    +0 Desemb, +2 Amort, +3 Juros, +4 IOF, +5 Comissão, +6 Taxa, +7 Seguros → Outras=IOF+Com+Tx+Seg.
    Só PR/BA/RN têm dívida (PE/AR/SAL = 0). Validado 1:1 (perproj_ref.py)."""
    dfm = wb["Demonstrativo Financeiro Mensal"]; dv = wb["Dívida"]; pn = wb["Painel de Controle"]
    def dser(ws, r):
        return [_num(ws.cell(row=r, column=COL_FIRST + k).value) or 0.0 for k in range(N_MONTHS)]
    flags = {}
    for name, brow in [("PR", 53), ("BA", 54), ("RN", 55), ("PE", 56), ("AR", 57), ("SAL", 58)]:
        flags[name] = 1.0 - (_num(pn.cell(row=brow, column=2).value) or 0.0)
    base = {"PR": 60, "BA": 69, "RN": 78, "PE": 87, "AR": 96, "SAL": 105}
    debt = {}
    for name, b in base.items():
        desemb, amort, juros = dser(dv, b), dser(dv, b + 2), dser(dv, b + 3)
        iof, comis, taxa, seg = dser(dv, b + 4), dser(dv, b + 5), dser(dv, b + 6), dser(dv, b + 7)
        outras = [iof[k] + comis[k] + taxa[k] + seg[k] for k in range(N_MONTHS)]
        debt[name] = {"desemb": desemb, "amort": amort, "juros": juros, "outras": outras}
    # Δ capital de giro (DFM468) e Impostos (DFM470) por planta — REALIZADO (k≤corte) como actual colado;
    # a projeção é fórmula viva no HTML (consol × participação na receita). Só o realizado precisa colar.
    ro_row = {"PR": 465, "BA": 540, "RN": 614, "PE": 688, "AR": 762, "SAL": 837}
    wc_row = {"PR": 468, "BA": 543, "RN": 617, "PE": 691, "AR": 765, "SAL": 840}
    imp_row = {"PR": 470, "BA": 545, "RN": 619, "PE": 693, "AR": 767, "SAL": 842}
    ro = {name: dser(dfm, ro_row[name]) for name in ro_row}
    wc = {name: dser(dfm, wc_row[name]) for name in wc_row}
    imp = {name: dser(dfm, imp_row[name]) for name in imp_row}
    return {"flags": flags, "debt": debt, "ro": ro, "wc": wc, "imp": imp}


def extract_capacidade(wb):
    """Capacidade instalada de liquefação/compressão por planta × produto (m³/dia), da aba Receita
    (CAPACIDADE - GNL r9-14, GNC r18-23; PR/BA/RN/PE/AR/SAL). É uma CURVA DE CAPACIDADE (plano de
    expansão da planta, premissa da aba Base Premissas → 'DEMANDA - CURVA DE CAPACIDADE', 4 fases),
    resolvida na Receita. Vai como série colada (não reage às alavancas operacionais). A UTILIZAÇÃO
    (%) = volume / capacidade é reproduzida AO VIVO no HTML (reage ao volume)."""
    ws = wb["Receita"]
    def dser(r):
        return [_num(ws.cell(row=r, column=COL_FIRST + k).value) for k in range(N_MONTHS)]
    gnl = {1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14}
    gnc = {1: 18, 2: 19, 3: 20, 4: 21, 5: 22, 6: 23}
    resolved = {"GNL": {p: dser(r) for p, r in gnl.items()},
                "GNC": {p: dser(r) for p, r in gnc.items()}}
    # PREMISSA editável — curva de expansão (até 4 fases: capacidade m³/dia + data início) da aba
    # Base Premissas ('DEMANDA - CURVA DE CAPACIDADE'). GNL rows 10-15, GNC 20-25; cap=cols 4/6/8/10,
    # data=cols 5/7/9/11. O HTML monta a função-degrau ao vivo (editável).
    bp = wb["Base Premissas"]
    def phases(r):
        out = []
        for i in range(4):
            cap = _num(bp.cell(row=r, column=4 + 2 * i).value)
            dat = _num(bp.cell(row=r, column=5 + 2 * i).value)
            if cap is not None and dat is not None:
                out += [cap, dat]
        return out
    prem = {"GNL": {p: phases(9 + p) for p in range(1, 7)},
            "GNC": {p: phases(19 + p) for p in range(1, 7)}}
    return {"resolved": resolved, "prem": prem}


def extract_dre_below(wb):
    """Linhas da DRE ABAIXO do EBITDA. Depreciação e Resultado Financeiro são cronogramas dos
    módulos de CAPEX e DÍVIDA (premissas de plano de investimento/financiamento — fixas, não reagem
    às alavancas operacionais); saem como séries-driver (DFM 103 / 108). Receita Bruta / Deduções
    (DFM 33 / 35) idem (módulo de Impostos). IMPOSTOS é computado AO VIVO no HTML (máquina de NOL de
    2 entidades sobre o EBT), então aqui saem só as PREMISSAS: constantes fiscais, imp36/imp37
    (partição inter-CNPJ), sementes do estoque de prejuízo (k47) e a planta da entidade A (RN=3)."""
    dfm = wb["Demonstrativo Financeiro Mensal"]
    imp = wb["Impostos"]

    def read_rows(ws, rowset, maxr):
        keep = {}
        for i, r in enumerate(ws.iter_rows(min_row=1, max_row=maxr,
                                           max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1):
            if i in rowset:
                keep[i] = r
        return keep

    dfmk = read_rows(dfm, {33, 35, 103, 108, 142}, 145)
    impk = read_rows(imp, {13, 14, 15, 16, 17, 18, 30, 31, 32, 33, 34, 36, 37, 45, 70}, 82)

    def ser(keep, r):
        row = keep.get(r)
        return [_num(row[COL_FIRST - 1 + k]) if row and COL_FIRST - 1 + k < len(row) else None
                for k in range(N_MONTHS)]

    def escal(r):   # coluna E (5) da aba Impostos
        row = impk.get(r)
        return _num(row[4]) if row and len(row) > 4 else None

    # alíquotas da Receita Bruta/Deduções (Impostos rows 13-18): D=ICMS por planta, F=PIS, G=COFINS.
    # Bruta = Σ_p ReceitaLíq_p/((1-ICMS_p)(1-PIS-COFINS)); Deduções = ICMS + (Bruta-ICMS)(PIS+COFINS).
    def _cell(r, c):
        row = impk.get(r)
        return _num(row[c - 1]) if row and c - 1 < len(row) else None
    icms = [(_cell(r, 4) or 0.0) for r in (13, 14, 15, 16, 17, 18)]   # coluna D = ICMS por planta
    return {
        "receita_bruta": ser(dfmk, 33), "deducoes": ser(dfmk, 35),
        "icms": icms, "pis": (_cell(13, 6) or 0.0), "cofins": (_cell(13, 7) or 0.0),   # premissas de alíquota
        "imp36": ser(impk, 36), "imp37": ser(impk, 37),   # imp37: alocação RN de juros+comissões da dívida
        "seedA": (ser(impk, 45)[47] or 0.0), "seedB": (ser(impk, 70)[47] or 0.0),
        "seedD": (ser(dfmk, 142)[47] or 0.0),
        "E30": escal(30), "E31": escal(31), "E32": escal(32), "E33": escal(33), "E34": escal(34),
        "entityA": [3],   # planta 3 (RN) = CNPJ da entidade A; B = as demais (DFM 614 vs 465/540/688/762/837)
    }


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
    _mac = wb["Macro"]                              # CDI % a.m. (Macro linha 10) — indexador da dívida
    _macrow = {i: r for i, r in enumerate(_mac.iter_rows(min_row=1, max_row=11,
              max_col=COL_FIRST - 1 + N_MONTHS, values_only=True), start=1)}
    idx_macro["cdi"] = [_num(_macrow[10][COL_FIRST - 1 + k]) if 10 in _macrow and COL_FIRST - 1 + k < len(_macrow[10]) else None
                        for k in range(N_MONTHS)]
    idx_macro["ipca_macro"] = [_num(_macrow[8][COL_FIRST - 1 + k]) if 8 in _macrow and COL_FIRST - 1 + k < len(_macrow[8]) else None
                               for k in range(N_MONTHS)]   # IPCA % a.m. (Macro 8) — indexador da dívida
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
    comp_term = extract_comp_term(orows)
    sga_cfg, sga_ocup, sga_seed, sga_regbase2 = extract_sga(orows, n_real)
    custo_total = extract_custo_total(orows)
    holding_sga = extract_holding_sga(wb)          # SG&A da holding (para o EBITDA = RO + Holding23)
    dre_below = extract_dre_below(wb)              # linhas abaixo do EBITDA (resfin driver + impostos live)
    capex = extract_capex(wb)                      # módulo de capex (depreciação viva + imobilizado)
    divida = extract_divida(wb, read_sheet_formulas(src, "Dívida"))   # módulo de dívida (juros/saldo vivos)
    var_d6 = _num(wb["Variável"]["D6"].value) or 0.0                  # toggle IPCA on/off (lido enquanto wb aberto)
    # premissa do SEGURO da dívida (bloco RN, Dívida!D85/E85) — taxa a.a. + data-fim; alimenta o
    # imp37 vivo (seguro trimestral sobre o principal RN em aberto). Reproduzido por fórmula no HTML.
    _dvsheet = wb["Dívida"]
    def _segrate(rrow):
        return _num(_dvsheet.cell(row=rrow, column=4).value) or 0.0   # coluna D = taxa a.a.
    def _segend(rrow):
        v = _dvsheet.cell(row=rrow, column=5).value                   # coluna E = data-fim
        return (float((v.date() - datetime.date(1899, 12, 30)).days)
                if isinstance(v, (datetime.datetime, datetime.date)) else (_num(v) or 0.0))
    seg_rate_rn, seg_end_rn = _segrate(85), _segend(85)   # bloco RN (Dívida r85)
    seg_rate_ba, seg_end_ba = _segrate(76), _segend(76)   # bloco BA (Dívida r76)
    balanco = extract_balanco(wb)                  # caixa/fluxo de caixa + balanço + DCF (insumos colados)
    dcfproj = extract_dcfproj(wb)                  # flags de planta + FC financeiro por projeto (colado)
    capacidade = extract_capacidade(wb)            # curva de capacidade por planta × produto (m³/dia, colada)
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
               "segmento", "top", "margem", "correcao_mol"]
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

    # (aba IdxMacro REMOVIDA) — as séries de indexação (média m-2/m-3/m-4; acumulado 12m)
    # são FÓRMULAS sobre a aba Macro no modelo, então o HTML as DERIVA ao vivo das 7 séries
    # brutas da aba Macro (deriveIdxFromMacro). A aba Macro é a ÚNICA fonte da verdade macro.

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

    # aba MolCompBasePreco: componente-base da molécula que indexa o PREÇO Brent (rows 254-259).
    # = custo-base(209) × (1+desconto,245), SEM o fator de desconto acumulado (dfac 1071) que só
    # existe no CUSTO do gás (RN=0,9). preço_molécula[p] = MolCompBasePreco[p] × fator_reajuste(macro).
    ws_mbp = out.create_sheet("MolCompBasePreco")
    ws_mbp.append(["planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in range(6):
        ws_mbp.append([p + 1] + mol_prem["compBasePrecoSer"][p])

    # aba MolAjuste: ajuste adicional do fator de reajuste (Variável 236-241) por planta.
    # fatorExtra = 1+ajuste, aplicado DENTRO do fator (composto, todo mês pós-data-base).
    # ≠0 só na banda de orçamento ago-dez/26 (PR/BA); zero no restante da projeção.
    ws_maj = out.create_sheet("MolAjuste")
    ws_maj.append(["planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in range(6):
        ws_maj.append([p + 1] + mol_prem["ajusteExtraSer"][p])

    # aba HoldingSga: premissas/sementes do SG&A da holding (matriz) — EBITDA = RO + Holding23.
    # Escalares + semente 2026 de r13 (por mês) + série-driver r32 (proxy de volume da matriz).
    ws_hs = out.create_sheet("HoldingSga")
    ws_hs.append(["key", "value"])
    for key in ("C27", "C28", "C29", "C30", "C32", "C33", "D18", "H8",
                "SEED15", "C34", "AVG14", "AVG16", "AVG17"):
        ws_hs.append([key, holding_sga["scalars"][key]])
    ws_hs.append(["seed13"] + holding_sga["seed13"])          # 12 valores (jan..dez/26)
    ws_hs.append(["r32"] + holding_sga["r32"])                # 192 (proxy de volume da matriz)
    ws_hs.append(["seed23"] + holding_sga["seed23"])          # Holding23 realizado+banda (k<48)

    # aba DreBelow: linhas abaixo do EBITDA. Drivers dos módulos de capex/dívida/impostos (deprec,
    # resfin, receita bruta, deduções, imp36) + premissas fiscais (constantes, sementes, entidade A).
    # IMPOSTOS é computado ao vivo no HTML (máquina de NOL de 2 entidades) — aqui só as premissas.
    # imp37 (reclass. RN do resultado financeiro) agora é VIVO (módulo de dívida: juros+IOF+seguros
    # RN) — removido daqui. imp36 (deprec RN) segue extraído.
    ws_db = out.create_sheet("DreBelow")
    ws_db.append(["field"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    # receita_bruta/deducoes: só o REALIZADO (semente) — a projeção é FÓRMULA no HTML (grossup por
    # alíquotas ICMS/PIS/COFINS da receita líquida por planta). imp36 (deprec RN) segue extraído.
    for key in ("receita_bruta", "deducoes"):
        ws_db.append([key] + real_only(dre_below[key], n_real))
    ws_db.append(["imp36"] + dre_below["imp36"])
    ws_db.append(["icms"] + dre_below["icms"])                       # alíquota ICMS por planta (premissa)
    ws_db.append(["pis_cofins", dre_below["pis"], dre_below["cofins"]])  # PIS/COFINS (premissa)
    ws_db.append(["taxconst", dre_below["E30"], dre_below["E31"], dre_below["E32"],
                  dre_below["E33"], dre_below["E34"]])
    ws_db.append(["taxseed", dre_below["seedA"], dre_below["seedB"], dre_below["seedD"]])
    ws_db.append(["entityA"] + dre_below["entityA"])

    # aba Capex: PREMISSAS do plano de investimento (inv por planta/classe, datas de início, vidas
    # úteis, semente da depreciação acumulada no corte). Depreciação e imobilizado saem por fórmula.
    ws_cx = out.create_sheet("Capex")
    hdr = ["field"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym]
    ws_cx.append(hdr)
    for p in range(6):
        ws_cx.append(["inv1_%d" % (p + 1)] + capex["inv1"][p])
        ws_cx.append(["inv2_%d" % (p + 1)] + capex["inv2"][p])
    ws_cx.append(["hd46"] + capex["hd46"])
    ws_cx.append(["dfm147"] + capex["dfm147"])
    ws_cx.append(["dates"] + capex["dates"])
    ws_cx.append(["op_dates"] + capex["op_dates"])
    ws_cx.append(["cfg", capex["life"], capex["holdlife"], capex["flag"], capex["seed146"], capex["seed_hd54"]])
    # extra1: sementes hardcode -> linhas "extra1_<planta>_<k>" = valor
    for p, seeds in capex["extra1"].items():
        for k, amt in seeds.items():
            ws_cx.append(["extra1_%d_%d" % (p, k), amt])

    # aba Divida: termos por instrumento (juros/saldo saem por fórmula no HTML) + sementes do
    # realizado; para BA/RN, a amortização/pagamento COLADOS (override manual no Excel) entram como
    # VALORES COLADOS (as únicas séries coladas de projeção na planilha, rotuladas ovr_*).
    ws_dv = out.create_sheet("Divida")
    ws_dv.append(["field"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    ws_dv.append(["cfg_var_d6", var_d6])   # toggle IPCA on/off dos índices (lido na fase de extração)
    ws_dv.append(["cfg_seg_rate_rn", seg_rate_rn])   # taxa a.a. do seguro RN (Dívida!D85) — premissa
    ws_dv.append(["cfg_seg_end_rn", seg_end_rn])     # data-fim do seguro RN (Dívida!E85, serial) — premissa
    ws_dv.append(["cfg_seg_rate_ba", seg_rate_ba])   # taxa a.a. do seguro BA (Dívida!D76) — premissa
    ws_dv.append(["cfg_seg_end_ba", seg_end_ba])     # data-fim do seguro BA (Dívida!E76, serial) — premissa
    for i, d in enumerate(divida):
        term = [d["name"], d["tipo"], d["indice"], d["spread"], d["iof"], d["comissao"],
                d["taxa_comp"], d["inicio_amort"], d["n_amort"], d["ultima"], d["inicio_pgto"],
                d["pg_period"], d["pg_offset"], d["override"] and 1 or 0, d["g_rn"], d["g_ba"]]
        for t in d["tranches"]:
            term += [t[0], t[1]]
        ws_dv.append(["i%d_term" % i] + term)
        if "seed_final" in d:
            ws_dv.append(["i%d_desemb" % i] + real_only(d["seed_desemb"], n_real))
            ws_dv.append(["i%d_final" % i] + real_only(d["seed_final"], n_real))
            ws_dv.append(["i%d_amort" % i] + real_only(d["seed_amort"], n_real))
            ws_dv.append(["i%d_despJ" % i] + real_only(d["seed_despJ"], n_real))
            ws_dv.append(["i%d_pagJ" % i] + real_only(d["seed_pagJ"], n_real))
            if d["override"]:            # BA/RN: amort/pagamento COLADOS (série completa = premissa)
                ws_dv.append(["i%d_ovr_amort" % i] + d["seed_amort"])
                ws_dv.append(["i%d_ovr_pagJ" % i] + d["seed_pagJ"])
    # aba DividaGpr: planta de cada instrumento (1=PR,2=BA,3=RN,0=holding) — p/ o switch de planta gatear a dívida
    ws_dg = out.create_sheet("DividaGpr")
    ws_dg.append(["plant_by_instrument"] + [
        (1 if d.get("g_pr") else 2 if d.get("g_ba") else 3 if d.get("g_rn") else 0) for d in divida])

    # aba Balanco: insumos do módulo caixa/balanço/DCF. Séries COLADAS/de outro módulo (imposto-caixa,
    # dividendos, override de ICMS, seguros/comissões da dívida, sementes, carries) + constantes de
    # prazo/desconto + geração anual do DCF. O waterfall/capital de giro/balanço/VPL/TIR são fórmula no HTML.
    ws_bl = out.create_sheet("Balanco")
    ws_bl.append(["field"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for key, serie in balanco.items():
        if key in ("const", "dcf_anos", "dfa_gen_cons"):
            continue
        ws_bl.append([key] + serie)
    c = balanco["const"]
    ws_bl.append(["const_keys"] + list(c.keys()))
    ws_bl.append(["const_vals"] + list(c.values()))
    ws_bl.append(["dcf_anos"] + balanco["dcf_anos"])
    ws_bl.append(["dfa_gen_cons"] + balanco["dfa_gen_cons"])

    # aba DcfConst: custo de capital do DCF (Ke, custo da dívida, IR, WACC, crescimento) p/ a aba DCF
    ws_dc = out.create_sheet("DcfConst")
    for k, v in balanco["dcf_const"].items():
        ws_dc.append([k, v])

    # aba DcfProj: DRE/DFC por projeto. Flags de planta (Painel B53..B58) + FC financeiro por planta
    # (bloco de dívida = plano de financiamento colado). EBITDA/ΔWC/Impostos/Capex são fórmula viva no HTML.
    ws_dp = out.create_sheet("DcfProj")
    ws_dp.append(["field"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    ws_dp.append(["flags"] + [dcfproj["flags"][p] for p in ("PR", "BA", "RN", "PE", "AR", "SAL")])
    for p in ("PR", "BA", "RN", "PE", "AR", "SAL"):
        for comp in ("desemb", "amort", "juros", "outras"):
            ws_dp.append(["%s_%s" % (p, comp)] + dcfproj["debt"][p][comp])
        # EBITDA/WC/Impostos por planta: só o REALIZADO (projeção é fórmula viva → None)
        ws_dp.append(["%s_ro" % p] + real_only(dcfproj["ro"][p], n_real))
        ws_dp.append(["%s_wc" % p] + real_only(dcfproj["wc"][p], n_real))
        ws_dp.append(["%s_imp" % p] + real_only(dcfproj["imp"][p], n_real))

    # aba Capacidade: curva RESOLVIDA por planta × produto (m³/dia) — usada p/ o realizado + validação.
    ws_cap = out.create_sheet("Capacidade")
    ws_cap.append(["field"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for prod in ("GNL", "GNC"):
        for p in range(1, 7):
            ws_cap.append(["%s_%d" % (prod, p)] + capacidade["resolved"][prod][p])
    # aba CapacidadePrem: PREMISSA editável — fases da curva de expansão (capacidade + data início).
    ws_cpm = out.create_sheet("CapacidadePrem")
    ws_cpm.append(["field", "cap1", "dat1", "cap2", "dat2", "cap3", "dat3", "cap4", "dat4"])
    for prod in ("GNL", "GNC"):
        for p in range(1, 7):
            ws_cpm.append(["%s_%d" % (prod, p)] + capacidade["prem"][prod][p])

    # aba PrecoBrent: preço corrigido por cliente Brent — REALIZADO (k<n_real) + SEMENTE de
    # orçamento ago-dez/26 (k43..47). A banda de transição de 2026 é colada (literal + fórmula
    # legada) no Excel e não é reproduzível pela regra paramétrica; a fórmula viva (molécula da
    # planta) assume em jan/27 (k48). Mesma lógica das sementes de SG&A/Regás.
    BRENT_SEED_CUT = 48   # mantém k0..47 (realizado + 5 meses de orçamento); projeção k>=48 é fórmula
    ws_pb = out.create_sheet("PrecoBrent")
    ws_pb.append(["id"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for cid in sorted(preco_brent):
        ser = preco_brent[cid]
        ws_pb.append([cid] + [ser[k] if k < BRENT_SEED_CUT else None for k in range(N_MONTHS)])

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
    ws_rs = out.create_sheet("OpexRegasSeed")   # semente da variação de frota (Furui)
    ws_rs.append(["serie"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    ws_rs.append(["necess"] + regas_necess)
    # (dólar_macro REMOVIDO) — o dólar do Furui é o dólar BRUTO da aba Macro; o HTML o usa
    # direto de lá (DB.idx.dolar_spot), mantendo a Macro como única fonte da verdade.

    # abas do SG&A: config por planta + ocupação (driver) + semente do hardcode ago-dez/26
    SGA_KEYS = ["sal_d", "sal_hc", "segop_d", "segop_e", "segop_f", "segop_ini",
                "segeq_d", "segeq_e", "segeq_f", "segeq_ini", "assist_d", "assist_mes",
                "serv_d", "viag_d", "proj_d", "proj_f", "proj_g", "reg_d", "reg_f", "reg_base",
                "patr_d", "ocup_d", "trab_d", "trab_f", "trab_base", "cont", "frota_d", "frota_n"]
    ws_sc = out.create_sheet("OpexSgaCfg")
    ws_sc.append(["planta"] + SGA_KEYS)
    for p in range(1, 7):
        ws_sc.append([p] + [sga_cfg[p][k] for k in SGA_KEYS])
    ws_sg = out.create_sheet("OpexSgaGlob")
    ws_sg.append(["key", "value"])
    ws_sg.append(["reg_base2_ord", sga_regbase2])
    ws_sg.append(["reg_switch_k", 50])
    ws_so2 = out.create_sheet("OpexSgaOcup")   # ocupação GNL % por planta (driver de Projetos Eng.)
    ws_so2.append(["planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in range(1, 7):
        ws_so2.append([p] + sga_ocup[p])
    ws_ss = out.create_sheet("OpexSgaSeed")    # semente do hardcode (subtotal SG&A k43..48)
    ws_ss.append(["planta"] + ["%04d-%02d" % (y, mo) for (y, mo) in ym])
    for p in range(1, 7):
        ws_ss.append([p] + sga_seed[p])

    # aba OpexCompTerm: compressão + terminal por planta (motores simples)
    ws_ct2 = out.create_sheet("OpexCompTerm")
    ws_ct2.append(["planta", "comp_tarifa", "comp_ini_ord", "comp_fim_ord", "term_tarifa"])
    for p in range(1, 7):
        ct = comp_term[p]
        ws_ct2.append([p, ct["comp_tarifa"], ct["comp_ini_ord"], ct["comp_fim_ord"], ct["term_tarifa"]])

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
