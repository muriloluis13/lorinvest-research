# -*- coding: utf-8 -*-
"""
Constroi a aba "TIR por Cliente" no modelo GNLink, 100% linkada as abas do modelo.
Escreve via COM (Excel) para nao corromper o arquivo vivo.
"""
import os, sys
import win32com.client as win32
from win32com.client import constants

ARQ = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                      "Modelo - Realizado Jun.26 (v ajust) - TIR por Cliente.xlsx")
ABA = "TIR por Cliente"

C0, C1 = 9, 200                      # colunas I..GR = jan/23..dez/38
NCOL = C1 - C0 + 1                   # 192 meses
NC = [24, 32, 22]                    # clientes por planta (PR, BA, RN)
NTOT = sum(NC)                       # 78
PLANTAS = ["PARANÁ", "BAHIA", "RIO GRANDE DO NORTE"]
CLI_SRC = [(7, 24), (37, 32), (75, 22)]   # aba Clientes: (linha inicial, n)

def cl(c):
    s = ""
    while c > 0:
        c, r = divmod(c - 1, 26)
        s = chr(65 + r) + s
    return s

COLS = [cl(c) for c in range(C0, C1 + 1)]

# ---- blocos por cliente nas abas de origem (linha inicial por planta) ----
SRC = {
    "rec_gnl":   ("Receita", (1161, 1188, 1223)),
    "rec_gnc":   ("Receita", (1318, 1345, 1380)),
    "rec_alug":  ("Receita", (1475, 1501, 1535)),
    "rec_outr":  ("Receita", (1627, 1653, 1687)),
    "rec_serv":  ("Receita", (1779, 1806, 1841)),
    "vol_gnl":   ("Receita", (367, 394, 429)),
    "vol_gnc":   ("Receita", (525, 552, 587)),
    "frete_fix": ("OPEX",    (710, 736, 770)),
    "frete_var": ("OPEX",    (861, 887, 921)),
    "alug_log":  ("OPEX",    (1027, 1052, 1085)),
    "out_dist":  ("OPEX",    (1174, 1199, 1232)),
    "reg_alug":  ("OPEX",    (1992, 2017, 2050)),
    "reg_mont":  ("OPEX",    (2139, 2164, 2197)),
    "cx_di":     ("Capex",   (65, 90, 123)),
    "cx_de":     ("Capex",   (213, 238, 271)),
    "cx_ri":     ("Capex",   (364, 389, 422)),
    "cx_re":     ("Capex",   (511, 536, 569)),
}
# ---- linhas por planta (nivel planta) ----
P = {
    "molec":  ("OPEX", (372, 373, 374)),
    "energia":("OPEX", (398, 399, 400)),
    "insumos":("OPEX", (438, 439, 440)),
    "perdas": ("OPEX", (504, 505, 506)),
    "om":     ("OPEX", (496, 497, 498)),
    "outliq": ("OPEX", (529, 530, 531)),
    "compr":  ("OPEX", (543, 544, 545)),
    "term":   ("OPEX", (552, 553, 554)),
    "sga":    ("OPEX", (562, 563, 564)),
    "dist_t": ("OPEX", (701, 702, 703)),
    "reg_t":  ("OPEX", (1959, 1960, 1961)),
    "capex_t":("Capex",(677, 678, 679)),
    "cap_gnl":("Receita", (9, 10, 11)),
    "cap_gnc":("Receita", (18, 19, 20)),
    "vol_gnl_t":("Receita", (365, 392, 427)),   # volume total da planta, m3
    "vol_gnc_t":("Receita", (523, 550, 585)),
    "mol_unit":("OPEX", (363, 364, 365)),       # custo unitario da molecula, R$/m3
    "rec_t":   ("Receita", (727, 733, 739)),    # receita liquida da planta
}
# capital de giro por planta, direto da DRE mensal (mesmas linhas do FCFF do analista)
WC_T = (482, 557, 631)
DRE_MENSAL = "'Demonstrativo Financeiro Mensal'"
GA_MATRIZ_ROW = 89

def q(sh):
    return f"'{sh}'" if any(ch in sh for ch in " -&") else sh

# ---------------- layout da aba nova ----------------
R_PREM = 10         # primeira linha de premissas (linha 4 = contador de períodos)
PANEL0 = 28         # inicio do painel por planta (premissas vao ate a linha 24)
PANEL_H = 22        # linhas por planta no painel
GA_ROW = PANEL0 + 3 * PANEL_H + 1          # linha do G&A Matriz (global)
IDX0 = GA_ROW + 12                         # GA_ROW+4..+7 = IR, +8 = plantas em operacao
BLK0 = None                                # definidos apos apurar NK
BLK_STEP = None

BLOCOS = [
 ("vol",      "VOLUME DO CLIENTE (m³/mês)"),
 ("capat",    "CAPACIDADE OCUPADA PELO CLIENTE (m³/dia)"),
 ("shvol",    "SHARE DE VOLUME NA PLANTA (%)"),
 ("shvolmol", "SHARE DE VOLUME COM MOLÉCULA (%)"),
 ("shcap",    "SHARE DE CAPACIDADE NA PLANTA (%)"),
 ("rec",      "RECEITA LÍQUIDA (R$)"),
 ("molec",    "( − ) MOLÉCULA (R$)"),
 ("liqvar",   "( − ) LIQUEFAÇÃO / COMPRESSÃO VARIÁVEL (R$)"),
 ("dist",     "( − ) DISTRIBUIÇÃO DIRETA (R$)"),
 ("regas",    "( − ) REGÁS / DESCOMPRESSÃO DIRETO (R$)"),
 ("mc",       "( = ) MARGEM DE CONTRIBUIÇÃO (R$)"),
 ("fixo",     "( − ) CUSTOS FIXOS DE PLANTA RATEADOS POR CAPACIDADE (R$)"),
 ("encargo",  "( − ) ENCARGO DE CAPACIDADE — CAPEX DE PLANTA (R$)"),
 ("ga",       "( − ) G&A MATRIZ RATEADO (R$)"),
 ("capex",    "( − ) CAPEX DEDICADO AO CLIENTE (R$)"),
 ("resid",    "( + ) RESIDUAL DO CAPEX NO FIM DO CONTRATO (R$)"),
 ("wc",       "( ± ) VARIAÇÃO DE CAPITAL DE GIRO (R$)"),
 ("pf1",      "SALDO DE PREJUÍZO FISCAL — NÍVEL 1 (R$)"),
 ("ir1",      "( − ) IR/CSLL — NÍVEL 1 (R$)"),
 ("fc1",      "( = ) FLUXO DE CAIXA — NÍVEL 1 · INCREMENTAL (R$)"),
 ("pf2",      "SALDO DE PREJUÍZO FISCAL — NÍVEL 2 (R$)"),
 ("ir2",      "( − ) IR/CSLL — NÍVEL 2 (R$)"),
 ("fc2",      "( = ) FLUXO DE CAIXA — NÍVEL 2 · COM CAPACIDADE (R$)"),
 ("pf3",      "SALDO DE PREJUÍZO FISCAL — NÍVEL 3 (R$)"),
 ("ir3",      "( − ) IR/CSLL — NÍVEL 3 (R$)"),
 ("fc3",      "( = ) FLUXO DE CAIXA — NÍVEL 3 · FULLY LOADED (R$)"),
 ("ac1",      "FC DESCONTADO ACUMULADO — NÍVEL 1 (R$)"),
 ("ac2",      "FC DESCONTADO ACUMULADO — NÍVEL 2 (R$)"),
 ("ac3",      "FC DESCONTADO ACUMULADO — NÍVEL 3 (R$)"),
]
B = {}
MET0 = None

def plant_of(i):
    """indice global 0..77 -> (planta 0..2, indice dentro da planta)"""
    if i < NC[0]: return 0, i
    if i < NC[0] + NC[1]: return 1, i - NC[0]
    return 2, i - NC[0] - NC[1]

def src_row(key, i):
    sh, starts = SRC[key]
    p, j = plant_of(i)
    return q(sh), starts[p] + j

# ---------------- abrir Excel ----------------
print("Abrindo Excel...")
xl = win32.gencache.EnsureDispatch("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.ScreenUpdating = False
wb = xl.Workbooks.Open(ARQ, UpdateLinks=0)
xl.Calculation = -4135   # manual
print("Aberto:", wb.Name)

# ---------------- quem entra na aba ----------------
# Le direto do modelo (a aba ainda nem existe): fica quem tem contrato
# alcancando o mes zero E algum financial nos meses Orcados.
_rec = wb.Worksheets("Receita")
_cli = wb.Worksheets("Clientes")
_st = _rec.Range(_rec.Cells(4, C0), _rec.Cells(4, C1)).Value[0]
FIRST_ORC = next(k for k, v in enumerate(_st) if isinstance(v, str) and v.strip().startswith("Or"))
MES_ZERO = _rec.Cells(2, C0 + FIRST_ORC).Value
print(f"mes zero = {MES_ZERO} (coluna {C0+FIRST_ORC})")

def _leia(sheet, r0, n):
    rg = wb.Worksheets(sheet).Range(wb.Worksheets(sheet).Cells(r0, C0),
                                    wb.Worksheets(sheet).Cells(r0 + n - 1, C1)).Value
    return [[x if isinstance(x, (int, float)) else 0 for x in linha] for linha in rg]

_proj = {}
for k in ("vol_gnl", "vol_gnc", "rec_gnl", "rec_gnc", "rec_alug", "rec_outr",
          "rec_serv", "cx_di", "cx_de", "cx_ri", "cx_re"):
    sh, starts = SRC[k]
    _proj[k] = []
    for p in range(3):
        _proj[k].extend(_leia(sh, starts[p], NC[p]))

_fim = []
for p in range(3):
    r0, n = CLI_SRC[p]
    col = _cli.Range(_cli.Cells(r0, 14), _cli.Cells(r0 + n - 1, 14)).Value
    _fim.extend([(x[0] if isinstance(x, tuple) else x) for x in col])

KEEP = []
for i in range(NTOT):
    fim = _fim[i]
    try:
        vivo = fim is not None and fim >= MES_ZERO
    except TypeError:
        vivo = False
    if not vivo:
        continue
    tot = 0.0
    for k in ("vol_gnl", "vol_gnc", "rec_gnl", "rec_gnc", "rec_alug", "rec_outr", "rec_serv"):
        tot += sum(_proj[k][i][FIRST_ORC:])
    for k in ("cx_di", "cx_de", "cx_ri", "cx_re"):
        tot += abs(sum(_proj[k][i][FIRST_ORC:]))
    if abs(tot) > 1e-9:
        KEEP.append(i)
NK = len(KEEP)
NCK = [sum(1 for i in KEEP if plant_of(i)[0] == p) for p in range(3)]
OC = cl(C0 + FIRST_ORC)          # 1a coluna Orcada: toda metrica de VP olha daqui pra frente
print(f"janela do VPL: horizonte completo I..GR (1o mes Orcado = {OC}, t=0)")
print(f"{NK} clientes com financials projetados (de {NTOT} linhas do modelo) -> PR {NCK[0]}, BA {NCK[1]}, RN {NCK[2]}")

# NUNCA apagar a aba: outras abas referenciam ela por nome. A DRE Mensal usa
# 'TIR por Cliente'!$D$11 (WACC mensal) e o contador de periodos nas linhas de
# DCF/EV. Um Delete transformaria todas essas formulas em #REF! silenciosamente.
# Por isso: reaproveita a aba existente e so limpa o conteudo.
ws = None
for _s in list(wb.Worksheets):
    if _s.Name == ABA:
        ws = _s
        break
if ws is None:
    ws = wb.Worksheets.Add(After=wb.Worksheets(wb.Worksheets.Count))
    ws.Name = ABA
    NOVA = True
    print("aba criada")
else:
    try:
        ws.AutoFilterMode = False
    except Exception:
        pass
    try:
        ws.Cells.ClearOutline()
    except Exception:
        pass
    ws.Cells.Clear()
    NOVA = False
    print("aba existente reaproveitada (conteudo limpo, referencias externas preservadas)")

BLK0 = IDX0 + NK + 4
BLK_STEP = NK + 3
for _k, (_key, _) in enumerate(BLOCOS):
    B[_key] = BLK0 + _k * BLK_STEP
MET0 = BLK0 + len(BLOCOS) * BLK_STEP + 2

if NOVA:      # largura de coluna e ajuste manual do analista; so define na criacao
    ws.Columns("A").ColumnWidth = 7
    ws.Columns("B").ColumnWidth = 46
    ws.Columns("C").ColumnWidth = 7
    ws.Columns("D").ColumnWidth = 13
    ws.Columns("E").ColumnWidth = 12
    ws.Columns("F:G").ColumnWidth = 10
    ws.Columns("H").ColumnWidth = 9
    ws.Range(ws.Cells(1, C0), ws.Cells(1, C1)).EntireColumn.ColumnWidth = 12

def put(rng, val):
    ws.Range(rng).Value = val

def putf(rng, f):
    ws.Range(rng).Formula = f

def bulk(r0, rows):
    """rows = lista de listas de strings de formula, cobrindo colunas I..GR"""
    n = len(rows)
    rng = ws.Range(ws.Cells(r0, C0), ws.Cells(r0 + n - 1, C1))
    rng.Formula = tuple(tuple(r) for r in rows)

# ---------------- cabecalho ----------------
put("B1", "Ano"); put("B2", "Mês"); put("B3", "Dias")
put("B4", "Discounting count"); put("B5", "Status")
# t = 0 no primeiro mes Orcado; realizado fica negativo (capitalizado), orcado positivo.
# O ancoramento e dinamico: quando o corte de realizado andar, o contador anda junto.
# Realizado entra com t=0 -> fator 1 -> peso NOMINAL, sem levar a valor futuro.
# Orcado conta 0,1,2,... a partir do primeiro mes Orcado.
CONT = [f'=MAX(0,COLUMN()-IFERROR(MATCH("Orçado",$I$5:$GR$5,0),1)-8)' for _ in COLS]
bulk(1, [[f"=Receita!{c}1" for c in COLS],
         [f"=Receita!{c}2" for c in COLS],
         [f"=Receita!{c}3" for c in COLS],
         CONT,
         [f"=Receita!{c}4" for c in COLS]])
put("B6", "TIR POR CLIENTE — GNLink · fluxo de caixa desalavancado, mensal, por cliente")
put("B7", "Todas as células são fórmulas linkadas às abas do modelo. Nenhum valor digitado, exceto as premissas em azul abaixo.")

# ---------------- premissas ----------------
prem = [
 ("WACC (% a.a.)",                                  "=DCF!$F$21", "0.0%"),
 ("WACC (% a.m.)",                                  f"=(1+$D${R_PREM})^(1/12)-1", "0.000%"),
 ("Alíquota IR/CSLL",                               "='Painel de Controle'!$F$44", "0%"),
 ("Vida útil do capex de planta (anos)",            "=10", "0"),
 ("% Residual do capex — Equipamento",              "=1", "0%"),
 ("% Residual do capex — Infraestrutura",           "=0", "0%"),
 ("Dias de recebimento (DSO) — não utilizado",      "=30", "0"),
 ("Dias de pagamento (DPO) — não utilizado",        "=30", "0"),
 ("Driver do G&A Matriz  (1 = igual por planta | 2 = Receita)", "=1", "0"),
 ("Compensar prejuízo fiscal (1 = sim | 0 = não)",  "=1", "0"),
 ("Capacidade ocupada (1 = só contratada | 2 = máx(contratada, realizada))", "=2", "0"),
 ("Desembolso mínimo para a TIR ser significativa (% das entradas)", "=0.01", "0.0%"),
 ("TIR máxima significativa (% a.a.) — acima disso a TIR não informa", "=5", "0%"),
 ("Nº de plantas p/ rateio do G&A (0 = dinâmico, só as em operação)", "=0", "0"),
 ("Origem do IR (1 = 34% sobre o resultado do cliente | 2 = rateio do IR efetivo do modelo)", "=2", "0"),
]
put("B8", "PREMISSAS  (editáveis)")
for k, (lab, f, fmt) in enumerate(prem):
    r = R_PREM + k
    put(f"B{r}", lab)
    putf(f"D{r}", f)
    ws.Range(f"D{r}").NumberFormat = fmt
    ws.Range(f"D{r}").Font.Color = 0xC00000
W_AA, W_AM, TAX, VIDA, RES_EQ, RES_IN, DSO, DPO, DRV_GA, USA_PF, DRV_CAP, MIN_INV, MAX_TIR, N_PL, DRV_IR = \
    [f"$D${R_PREM+k}" for k in range(15)]

# --- plantas em operacao (Painel de Controle L53-55: D = inicio, F = fim) ---
# Precisa estar definido ANTES do painel por planta, que usa ativa() no custo orfao.
PC = "'Painel de Controle'"
def ativa(c, p):
    # planta EM OPERACAO: usada para dividir o G&A da matriz
    return f"IF(AND({c}$2>={PC}!$D${53+p},{c}$2<{PC}!$F${53+p}),1,0)"
def ate_fim(c, p):
    # planta AINDA NAO ENCERRADA: os custos dela (inclusive o custo de capital
    # do capex em obra) existem desde antes da partida e cessam no encerramento.
    return f"IF({c}$2<{PC}!$F${53+p},1,0)"
N_ATIV = GA_ROW + 8              # linha global: quantas plantas operam no mes

# ---------------- painel por planta ----------------
put(f"B{PANEL0-2}", "PAINEL POR PLANTA — pools de custo, capacidade e ociosidade")
PAN_LAB = [
 "PLANTA",
 "Capacidade nominal (m³/dia)",
 "Capacidade contratada ativa (m³/dia)",
 "Denominador de capacidade (m³/dia)",
 "Volume total da planta (m³)",
 "Volume com molécula (m³)",
 "Pool — Molécula (R$)",
 "Pool — Liquefação/compressão variável (R$)",
 "Pool — Fixo de planta (R$)",
 "Pool — Distribuição indireta (R$)",
 "Pool — Regás indireto (R$)",
 "Pool — Fixo total a ratear por capacidade (R$)",
 "Capex de planta no mês (R$)",
 "Capex de planta — adições acumuladas (R$)",
 "Depreciação econômica do capex de planta (R$)",
 "Saldo do ativo de planta (R$)",
 "Encargo de capacidade = depreciação + custo de capital (R$)",
 "Σ share de capacidade dos clientes (%)",
 "Σ share de volume dos clientes (%)",
 "Σ share de volume com molécula dos clientes (%)",
 "CUSTO ÓRFÃO — OCIOSIDADE E CUSTO NÃO ALOCÁVEL (R$)",
]
for p in range(3):
    r0 = PANEL0 + p * PANEL_H
    put(f"B{r0}", PLANTAS[p])
    put(f"C{r0}", p + 1)
    for k, lab in enumerate(PAN_LAB[1:], start=1):
        put(f"B{r0+k}", lab)
    b_cap, b_vol = B["capat"], B["vol"]
    rows = [[] for _ in range(20)]
    for c in COLS:
        # +1 capacidade nominal
        rows[0].append(f"=Receita!{c}{P['cap_gnl'][1][p]}+Receita!{c}{P['cap_gnc'][1][p]}")
        # +2 capacidade contratada ativa
        rows[1].append(f"=SUMIF($C${b_cap}:$C${b_cap+NK-1},$C${r0},{c}${b_cap}:{c}${b_cap+NK-1})")
        # +3 denominador
        rows[2].append(f"=MAX({c}{r0+1},{c}{r0+2})")
        # +4 volume total
        rows[3].append(f"=Receita!{c}{P['vol_gnl_t'][1][p]}+Receita!{c}{P['vol_gnc_t'][1][p]}")
        # +5 volume com molecula
        rows[4].append(f"=IFERROR(OPEX!{c}{P['molec'][1][p]}/OPEX!{c}{P['mol_unit'][1][p]},0)")
        # +6 pool molecula
        rows[5].append(f"=-OPEX!{c}{P['molec'][1][p]}")
        # +7 pool liquefacao variavel
        rows[6].append(f"=-(OPEX!{c}{P['energia'][1][p]}+OPEX!{c}{P['insumos'][1][p]}+OPEX!{c}{P['perdas'][1][p]})")
        # +8 pool fixo de planta
        rows[7].append(f"=-(OPEX!{c}{P['om'][1][p]}+OPEX!{c}{P['outliq'][1][p]}+OPEX!{c}{P['compr'][1][p]}+OPEX!{c}{P['term'][1][p]}+OPEX!{c}{P['sga'][1][p]})")
        # +9 pool distribuicao indireta = total - diretos
        bd = B["dist"]
        rows[8].append(f"=-OPEX!{c}{P['dist_t'][1][p]}-SUMIF($C${bd}:$C${bd+NK-1},$C${r0},{c}${bd}:{c}${bd+NK-1})")
        # +10 pool regas indireto = total - diretos
        br = B["regas"]
        rows[9].append(f"=-OPEX!{c}{P['reg_t'][1][p]}-SUMIF($C${br}:$C${br+NK-1},$C${r0},{c}${br}:{c}${br+NK-1})")
        # +11 pool fixo total a ratear
        rows[10].append(f"={c}{r0+8}+{c}{r0+9}+{c}{r0+10}")
        # +12 capex de planta no mes = total - capex dos clientes
        bx = B["capex"]
        rows[11].append(f"=Capex!{c}{P['capex_t'][1][p]}+SUMIF($C${bx}:$C${bx+NK-1},$C${r0},{c}${bx}:{c}${bx+NK-1})")
        ci = COLS.index(c)
        prev = COLS[ci - 1] if ci > 0 else None
        # +13 adicoes acumuladas
        rows[12].append(f"={c}{r0+12}" if prev is None else f"={prev}{r0+13}+{c}{r0+12}")
        # +14 depreciacao economica linear por tranche ao longo de VIDA*12 meses
        lag = ci - 120
        ant = f"{COLS[lag]}{r0+13}" if lag >= 0 else "0"
        rows[13].append(f"=-({c}{r0+13}-{ant})/({VIDA}*12)")
        # +15 saldo do ativo
        rows[14].append(f"={c}{r0+12}+{c}{r0+14}" if prev is None
                        else f"={prev}{r0+15}+{c}{r0+12}+{c}{r0+14}")
        # +16 encargo = depreciacao + custo de capital sobre o saldo inicial
        sini = f"{prev}{r0+15}" if prev else "0"
        rows[15].append(f"={c}{r0+14}-MAX(0,{sini})*{W_AM}")
        # +17/+18/+19 somas dos shares (capacidade, volume, volume c/ molecula)
        for kk, bk in enumerate(("shcap", "shvol", "shvolmol")):
            bs = B[bk]
            rows[16+kk].append(f"=SUMIF($C${bs}:$C${bs+NK-1},$C${r0},{c}${bs}:{c}${bs+NK-1})")
        # +20 custo orfao = tudo que os pools carregam e nao foi alocado a nenhum cliente
        _div = f"IF({N_PL}=0,{c}${N_ATIV},{N_PL})"
        rows[19].append(f"={ate_fim(c,p)}*({c}{r0+6}*(1-{c}{r0+19})+{c}{r0+7}*(1-{c}{r0+18})"
                        f"+({c}{r0+11}+{c}{r0+16})*(1-{c}{r0+17}))"
                        f"+{ativa(c,p)}*IF({DRV_GA}=1,IFERROR({c}${GA_ROW}/{_div},0)*(1-{c}{r0+17}),0)")
    bulk(r0 + 1, rows)
    for k in (1, 2, 3, 4, 5):
        ws.Range(ws.Cells(r0+k, C0), ws.Cells(r0+k, C1)).NumberFormat = "#,##0"
    ws.Range(ws.Cells(r0+17, C0), ws.Cells(r0+19, C1)).NumberFormat = "0.0%"

put(f"B{GA_ROW}", "G&A MATRIZ / HOLDING (R$) — consolidado, a ratear")
bulk(GA_ROW, [[f"=-ABS({DRE_MENSAL}!{c}{GA_MATRIZ_ROW})" for c in COLS]])
put(f"B{GA_ROW+1}", "Receita líquida positiva total das 3 plantas (R$) — base do rateio de G&A")
br = B["rec"]
bulk(GA_ROW+1, [[f"=SUMPRODUCT(({c}${br}:{c}${br+NK-1}>0)*({c}${br}:{c}${br+NK-1}))" for c in COLS]])
IR_MOD = GA_ROW + 4
DEN = {"1": GA_ROW + 5, "2": GA_ROW + 6, "3": GA_ROW + 7}
put(f"B{IR_MOD}", "IR/CSLL efetivo do modelo (R$) — base do rateio de imposto")
# sinal preservado: em mes de credito fiscal a linha do modelo e positiva,
# e -ABS() transformaria credito em custo (descolava R$ 24 mil do modelo).
bulk(IR_MOD, [[f"={DRE_MENSAL}!{c}116" for c in COLS]])
def _rng(k, c):
    return f"{c}${B[k]}:{c}${B[k]+NK-1}"
for lvl, comps in (("1", ["mc"]), ("2", ["mc","fixo","encargo"]), ("3", ["mc","fixo","encargo","ga"])):
    put(f"B{DEN[lvl]}", f"Σ base tributável positiva dos clientes — Nível {lvl} (R$)")
    linha = []
    for c in COLS:
        expr = "+".join(_rng(k, c) for k in comps)
        linha.append(f"=SUMPRODUCT((({expr})>0)*({expr}))")
    bulk(DEN[lvl], [linha])

FORA = [i for i in range(NTOT) if i not in set(KEEP)]
put(f"B{GA_ROW+3}", f"Receita líquida dos {len(FORA)} clientes fora do escopo (R$) — só para a reconciliação")
_lin = []
for c in COLS:
    parts = []
    for i in FORA:
        for k2 in ("rec_gnl", "rec_gnc", "rec_alug", "rec_outr", "rec_serv"):
            sh, rr = src_row(k2, i)
            parts.append(f"{sh}!{c}{rr}")
    _lin.append("=" + "+".join(parts) if parts else "=0")
bulk(GA_ROW + 3, [_lin])

put(f"B{N_ATIV}", "Nº de plantas em operação no mês (Painel de Controle, fim de operação)")
bulk(N_ATIV, [["=" + "+".join(ativa(c, p) for p in range(3)) for c in COLS]])
GA_SP = GA_ROW + 9
put(f"B{GA_SP}", "G&A da matriz em meses SEM planta em operação (R$) — não alocável")
bulk(GA_SP, [[f"=IF({c}${N_ATIV}=0,{c}${GA_ROW},0)" for c in COLS]])

put(f"B{GA_ROW+2}", "Capacidade contratada ativa total das 3 plantas (m³/dia)")
bc = B["capat"]
bulk(GA_ROW+2, [[f"=SUM({c}${bc}:{c}${bc+NK-1})" for c in COLS]])

# ---------------- indice de clientes ----------------
put(f"B{IDX0-2}", "ÍNDICE DE CLIENTES")
hdr = ["ID", "Cliente", "Planta", "GNL/GNC", "Vol. Máximo (m³/dia)",
       "Início da Operação", "Fim do Contrato", "Molécula (1=sim)"]
for k, h in enumerate(hdr):
    put(f"{cl(1+k)}{IDX0-1}", h)
idx = []
for i in KEEP:
    p, j = plant_of(i)
    sr = CLI_SRC[p][0] + j
    idx.append([f"=Clientes!A{sr}", f"=Clientes!C{sr}", f"=Clientes!D{sr}",
                f"=Clientes!E{sr}", f"=Clientes!G{sr}", f"=Clientes!L{sr}",
                f"=Clientes!N{sr}", f"=Clientes!J{sr}"])
ws.Range(ws.Cells(IDX0, 1), ws.Cells(IDX0 + NK - 1, 8)).Formula = tuple(tuple(r) for r in idx)
ws.Range(ws.Cells(IDX0, 6), ws.Cells(IDX0 + NK - 1, 7)).NumberFormat = "mmm/aa"
# "No horizonte" = contrato alcanca o mes zero E a linha tem algum numero.
# Exclui os que terminaram antes do 1o mes Orcado e os [Inserir Cliente] em branco.
# "No horizonte" = tem algum financial nos meses ORÇADOS (contador >= 0).
# Pega de uma vez os contratos encerrados antes do mês zero e as linhas em branco.
# ---------------- blocos mensais ----------------
def stub(base):
    """colunas A-H de identificacao repetidas em cada bloco"""
    rows = []
    for j in range(NK):
        r = IDX0 + j
        rows.append([f"=$A${r}", f"=$B${r}", f"=$C${r}", f"=$D${r}",
                     f"=$E${r}", f"=$F${r}", f"=$G${r}", f"=$H${r}"])
    ws.Range(ws.Cells(base, 1), ws.Cells(base + NK - 1, 8)).Formula = tuple(tuple(x) for x in rows)
    ws.Range(ws.Cells(base, 6), ws.Cells(base + NK - 1, 7)).NumberFormat = "mmm/yy"

def panel_row(p, off):
    return PANEL0 + p * PANEL_H + off

print("Escrevendo blocos mensais...")
for key, titulo in BLOCOS:
    base = B[key]
    put(f"B{base-2}", titulo)
    stub(base)
    rows = []
    for jj, i in enumerate(KEEP):
        p, _ = plant_of(i)
        r = base + jj
        line = []
        for ci, c in enumerate(COLS):
            prev = COLS[ci - 1] if ci > 0 else None
            if key == "vol":
                sh, rr = src_row("vol_gnl", i); _, r2 = src_row("vol_gnc", i)
                f = f"={sh}!{c}{rr}+{sh}!{c}{r2}"
            elif key == "capat":
                # planta encerrada nao tem capacidade ocupada, mesmo que o
                # contrato do cliente se estenda alem do fim de operacao.
                f = (f"={ativa(c,p)}*IF(AND({c}$2>=$F{r},{c}$2<$G{r}),"
                     f"IF({DRV_CAP}=2,MAX($E{r},IFERROR({c}{B['vol']+jj}/{c}$3,0)),$E{r}),"
                     f"IF({DRV_CAP}=2,IFERROR({c}{B['vol']+jj}/{c}$3,0),0))")
            elif key == "shvol":
                f = f"=IFERROR({c}{B['vol']+jj}/{c}{panel_row(p,4)},0)"
            elif key == "shvolmol":
                f = f"=IFERROR($H{r}*{c}{B['vol']+jj}/{c}{panel_row(p,5)},0)"
            elif key == "shcap":
                f = f"=IFERROR({c}{B['capat']+jj}/{c}{panel_row(p,3)},0)"
            elif key == "rec":
                parts = []
                for k2 in ("rec_gnl", "rec_gnc", "rec_alug", "rec_outr", "rec_serv"):
                    sh, rr = src_row(k2, i); parts.append(f"{sh}!{c}{rr}")
                f = "=" + "+".join(parts)
            elif key == "molec":
                f = f"={c}{panel_row(p,6)}*{c}{B['shvolmol']+jj}"
            elif key == "liqvar":
                f = f"={c}{panel_row(p,7)}*{c}{B['shvol']+jj}"
            elif key == "dist":
                parts = []
                for k2 in ("frete_fix", "frete_var", "alug_log", "out_dist"):
                    sh, rr = src_row(k2, i); parts.append(f"N({sh}!{c}{rr})")
                f = "=-(" + "+".join(parts) + ")"
            elif key == "regas":
                parts = []
                for k2 in ("reg_alug", "reg_mont"):
                    sh, rr = src_row(k2, i); parts.append(f"N({sh}!{c}{rr})")
                f = "=-(" + "+".join(parts) + ")"
            elif key == "mc":
                f = (f"={c}{B['rec']+jj}+{c}{B['molec']+jj}+{c}{B['liqvar']+jj}"
                     f"+{c}{B['dist']+jj}+{c}{B['regas']+jj}")
            elif key == "fixo":
                f = f"={c}{panel_row(p,11)}*{c}{B['shcap']+jj}"
            elif key == "encargo":
                f = f"={c}{panel_row(p,16)}*{c}{B['shcap']+jj}"
            elif key == "ga":
                div = f"IF({N_PL}=0,{c}${N_ATIV},{N_PL})"
                f = (f"=IF({DRV_GA}=1,"
                     f"{ativa(c,p)}*IFERROR({c}${GA_ROW}/{div},0)*{c}{B['shcap']+jj},"
                     f"{c}${GA_ROW}*IFERROR(MAX(0,{c}{B['rec']+jj})/{c}${GA_ROW+1},0))")
            elif key == "capex":
                parts = []
                for k2 in ("cx_di", "cx_de", "cx_ri", "cx_re"):
                    sh, rr = src_row(k2, i); parts.append(f"N({sh}!{c}{rr})")
                f = "=-(" + "+".join(parts) + ")"
            elif key == "resid":
                she, rre = src_row("cx_de", i); shr, rrr = src_row("cx_re", i)
                shi, rri = src_row("cx_di", i); shn, rrn = src_row("cx_ri", i)
                eq = f"(SUM({she}!$I{rre}:$GR{rre})+SUM({shr}!$I{rrr}:$GR{rrr}))*{RES_EQ}"
                inf = f"(SUM({shi}!$I{rri}:$GR{rri})+SUM({shn}!$I{rrn}:$GR{rrn}))*{RES_IN}"
                f = f"=IF({c}$2=$G{r},{eq}+{inf},0)"
            elif key == "wc":
                # capital de giro do proprio modelo (DRE mensal, por planta),
                # rateado pela participacao do cliente na receita liquida da planta.
                f = (f"=IFERROR({DRE_MENSAL}!{c}{WC_T[p]}*{c}{B['rec']+jj}"
                     f"/Receita!{c}{P['rec_t'][1][p]},0)")
            elif key in ("pf1", "pf2", "pf3"):
                nb = {"pf1": B['mc'], "pf2": B['mc'], "pf3": B['mc']}[key]
                if key == "pf1":
                    base_res = f"{c}{B['mc']+jj}"
                elif key == "pf2":
                    base_res = f"({c}{B['mc']+jj}+{c}{B['fixo']+jj}+{c}{B['encargo']+jj})"
                else:
                    base_res = f"({c}{B['mc']+jj}+{c}{B['fixo']+jj}+{c}{B['encargo']+jj}+{c}{B['ga']+jj})"
                pr = f"{prev}{B[key]+jj}" if prev else "0"
                f = f"=MAX(0,{pr}-MAX(0,{base_res}))+MAX(0,-{base_res})"
            elif key in ("ir1", "ir2", "ir3"):
                lvl = key[-1]
                if lvl == "1":
                    base_res = f"{c}{B['mc']+jj}"
                elif lvl == "2":
                    base_res = f"({c}{B['mc']+jj}+{c}{B['fixo']+jj}+{c}{B['encargo']+jj})"
                else:
                    base_res = f"({c}{B['mc']+jj}+{c}{B['fixo']+jj}+{c}{B['encargo']+jj}+{c}{B['ga']+jj})"
                pf = f"{prev}{B['pf'+lvl]+jj}" if prev else "0"
                proprio = f"-{TAX}*MAX(0,{base_res}-IF({USA_PF}=1,{pf},0))"
                # rateio: o imposto que a companhia de fato paga, distribuido pela
                # base tributavel positiva de cada cliente no mes.
                rateio = f"{c}${IR_MOD}*IFERROR(MAX(0,{base_res})/{c}${DEN[lvl]},0)"
                f = f"=IF({DRV_IR}=1,{proprio},{rateio})"
            elif key == "fc1":
                f = (f"={c}{B['mc']+jj}+{c}{B['capex']+jj}+{c}{B['resid']+jj}"
                     f"+{c}{B['wc']+jj}+{c}{B['ir1']+jj}")
            elif key == "fc2":
                f = (f"={c}{B['mc']+jj}+{c}{B['fixo']+jj}+{c}{B['encargo']+jj}"
                     f"+{c}{B['capex']+jj}+{c}{B['resid']+jj}+{c}{B['wc']+jj}+{c}{B['ir2']+jj}")
            elif key == "fc3":
                f = (f"={c}{B['mc']+jj}+{c}{B['fixo']+jj}+{c}{B['encargo']+jj}+{c}{B['ga']+jj}"
                     f"+{c}{B['capex']+jj}+{c}{B['resid']+jj}+{c}{B['wc']+jj}+{c}{B['ir3']+jj}")
            elif key in ("ac1", "ac2", "ac3"):
                lvl = key[-1]
                disc = f"{c}{B['fc'+lvl]+jj}/(1+{W_AM})^{c}$4"
                f = f"={disc}" if prev is None else f"={prev}{B[key]+jj}+{disc}"
            else:
                f = "=0"
            line.append(f)
        rows.append(line)
    bulk(base, rows)
    fmt = "0.0%" if key.startswith("sh") else ("#,##0" if key != "capat" else "#,##0")
    ws.Range(ws.Cells(base, C0), ws.Cells(base + NK - 1, C1)).NumberFormat = fmt
    print("   bloco", key, "linha", base)


# ---------------- tabela de metricas ----------------
print("Escrevendo metricas...")
put(f"B{MET0-3}", "MÉTRICAS POR CLIENTE")
put(f"B{MET0-2}", "Nível 1 = incremental (decisão comercial)  ·  Nível 2 = + capacidade da planta (precificação)  ·  Nível 3 = + G&A Matriz (portfólio).  TIR mensal anualizada.")
h1 = ["", "", "", "", "", "", "", "", "GERAL", "", "", "", "",
      "NÍVEL 1 — INCREMENTAL", "", "", "", "",
      "NÍVEL 2 — COM CAPACIDADE", "", "", "", "",
      "NÍVEL 3 — FULLY LOADED", "", "", "", ""]
h2 = ["ID", "Cliente", "Planta", "GNL/GNC", "Vol. Máx (m³/dia)", "Início", "Fim", "Prazo (meses)",
      "Volume total (m³)", "Receita (R$)", "Margem contrib. (R$)", "Margem (R$/m³)", "Capex dedicado (R$)",
      "TIR (% a.a.)", "MTIR (% a.a.)", "VPL (R$)", "IL (x)", "Payback desc.",
      "TIR (% a.a.)", "MTIR (% a.a.)", "VPL (R$)", "IL (x)", "Payback desc.",
      "TIR (% a.a.)", "MTIR (% a.a.)", "VPL (R$)", "IL (x)", "Payback desc."]
ws.Range(ws.Cells(MET0-1, 1), ws.Cells(MET0-1, len(h1))).Value = tuple([tuple(h1)])
ws.Range(ws.Cells(MET0, 1), ws.Cells(MET0, len(h2))).Value = tuple([tuple(h2)])
MR0 = MET0 + 1
met = []
for j in range(NK):
    m = MR0 + j
    r_idx = IDX0 + j
    v, mc, cx = B["vol"] + j, B["mc"] + j, B["capex"] + j
    row = [f"=$A${r_idx}", f"=$B${r_idx}", f"=$C${r_idx}", f"=$D${r_idx}",
           f"=$E${r_idx}", f"=$F${r_idx}", f"=$G${r_idx}",
           f'=IFERROR(DATEDIF($F{m},$G{m},"m"),0)',
           f"=SUM($I{v}:$GR{v})",
           f"=SUM($I{B['rec']+j}:$GR{B['rec']+j})",
           f"=SUM($I{mc}:$GR{mc})",
           f"=IFERROR($K{m}/$I{m},0)",
           f"=SUM($I{cx}:$GR{cx})"]
    for lvl, c0 in (("1", 14), ("2", 19), ("3", 24)):
        f = B["fc" + lvl] + j
        a = B["ac" + lvl] + j
        cV = cl(c0 + 2)
        row += [
          (f'=IF(-SUMIF($I{f}:$GR{f},"<0")<={MIN_INV}*SUMIF($I{f}:$GR{f},">0"),"n.a. s/ desembolso",'
           f'IFERROR(IF((1+IRR($I{f}:$GR{f},0.02))^12-1>{MAX_TIR},"n.a. TIR>"&TEXT({MAX_TIR},"0%"),(1+IRR($I{f}:$GR{f},0.02))^12-1),'
           f'IFERROR(IF((1+IRR($I{f}:$GR{f},-0.25))^12-1>{MAX_TIR},"n.a. TIR>"&TEXT({MAX_TIR},"0%"),(1+IRR($I{f}:$GR{f},-0.25))^12-1),"n.a.")))'),
          f'=IF(-SUMIF($I{f}:$GR{f},"<0")<={MIN_INV}*SUMIF($I{f}:$GR{f},">0"),"n.a. s/ desembolso",IFERROR((1+MIRR($I{f}:$GR{f},{W_AM},{W_AM}))^12-1,"n.a."))',
          f"=SUMPRODUCT($I{f}:$GR{f},1/(1+{W_AM})^$I$4:$GR$4)",
          f'=IFERROR(1+{cV}{m}/ABS(SUMPRODUCT($I{cx}:$GR{cx},1/(1+{W_AM})^$I$4:$GR$4)),"n.a.")',
          f'=IFERROR(INDEX($I$2:$GR$2,MATCH(TRUE,INDEX($I{a}:$GR{a}>0,0),0)),"n.a.")']
    met.append(row)
ws.Range(ws.Cells(MR0, 1), ws.Cells(MR0 + NK - 1, len(h2))).Formula = tuple(tuple(r) for r in met)
ws.Range(ws.Cells(MR0, 6), ws.Cells(MR0 + NK - 1, 7)).NumberFormat = "mmm/aa"
ws.Range(ws.Cells(MR0, 9), ws.Cells(MR0 + NK - 1, 11)).NumberFormat = "#,##0"
ws.Range(ws.Cells(MR0, 12), ws.Cells(MR0 + NK - 1, 12)).NumberFormat = "0.00"
ws.Range(ws.Cells(MR0, 13), ws.Cells(MR0 + NK - 1, 13)).NumberFormat = "#,##0"
for c0 in (14, 19, 24):
    ws.Range(ws.Cells(MR0, c0), ws.Cells(MR0 + NK - 1, c0 + 1)).NumberFormat = "0.0%"
    ws.Range(ws.Cells(MR0, c0 + 2), ws.Cells(MR0 + NK - 1, c0 + 2)).NumberFormat = "#,##0"
    ws.Range(ws.Cells(MR0, c0 + 3), ws.Cells(MR0 + NK - 1, c0 + 3)).NumberFormat = "0.00"
    ws.Range(ws.Cells(MR0, c0 + 4), ws.Cells(MR0 + NK - 1, c0 + 4)).NumberFormat = "mmm/aa"

# ---------------- reconciliacao ----------------
REC0 = MR0 + NK + 3
put(f"B{REC0-2}", "RECONCILIAÇÃO CONTRA O MODELO  —  toda linha deve dar zero em todos os meses")
recs = []
def sumblk(k, c):
    b = B[k]; return f"SUM({c}${b}:{c}${b+NK-1})"
def panel_sum(off, c):
    return "+".join(f"{c}{panel_row(p,off)}" for p in range(3))
def panel_sum2(off_pool, off_share, c):
    """parcela do pool que nao foi alocada a nenhum cliente"""
    return "+".join(f"{c}{panel_row(p,off_pool)}*(1-{c}{panel_row(p,off_share)})" for p in range(3))
def opex3(key, c):
    return "+".join(f"OPEX!{c}{P[key][1][p]}" for p in range(3))
recs.append(("Receita líquida: Σ clientes na aba + Σ fora do escopo − modelo",
             lambda c: f"={sumblk('rec',c)}+{c}${GA_ROW+3}-(Receita!{c}727+Receita!{c}733+Receita!{c}739)"))
recs.append(("Molécula: Σ clientes − modelo",
             lambda c: f"=-({sumblk('molec',c)}+({panel_sum2(6,19,c)}))-({opex3('molec',c)})"))
recs.append(("Liquefação/compressão variável: Σ clientes − modelo",
             lambda c: f"=-({sumblk('liqvar',c)}+({panel_sum2(7,18,c)}))-({opex3('energia',c)}+{opex3('insumos',c)}+{opex3('perdas',c)})"))
recs.append(("Distribuição: Σ diretos + Σ pool − modelo",
             lambda c: f"=-({sumblk('dist',c)}+({panel_sum(9,c)}))-({opex3('dist_t',c)})"))
recs.append(("Regás: Σ diretos + Σ pool − modelo",
             lambda c: f"=-({sumblk('regas',c)}+({panel_sum(10,c)}))-({opex3('reg_t',c)})"))
recs.append(("Custos fixos de planta: Σ alocado + Σ órfão − pool",
             lambda c: f"={sumblk('fixo',c)}+{sumblk('encargo',c)}+({panel_sum2(11,17,c)})+({panel_sum2(16,17,c)})-(({panel_sum(11,c)})+({panel_sum(16,c)}))"))
recs.append(("Capex: Σ clientes + Σ planta − modelo",
             lambda c: f"=-{sumblk('capex',c)}+({panel_sum(12,c)})-(Capex!{c}677+Capex!{c}678+Capex!{c}679)"))
recs.append(("G&A Matriz: Σ alocado + Σ órfão + Σ sem planta − consolidado",
             lambda c: f"={sumblk('ga',c)}+IF({DRV_GA}=1,"
                       + "+".join(f"{ativa(c,p)}*IFERROR({c}${GA_ROW}/IF({N_PL}=0,{c}${N_ATIV},{N_PL}),0)*(1-{c}{panel_row(p,17)})"
                                  for p in range(3))
                       + f",0)+{c}${GA_SP}-{c}${GA_ROW}"))
def _naoaloc(c):
    return "+".join(f"IF({c}${DEN[l]}=0,{c}${IR_MOD},0)" for l in ("1","2","3"))
recs.append(("IR/CSLL: Σ clientes + não alocado − modelo (pior dos 3 níveis)",
             lambda c: "=IF(" + DRV_IR + "<>2,0,MAX("
                       + ",".join(
                           f"ABS({sumblk('ir'+l,c)}+IF({c}${DEN[l]}=0,{c}${IR_MOD},0)-{c}${IR_MOD})"
                           for l in ("1","2","3")) + "))"))
recs.append(("Share de capacidade: excedente sobre 100% por planta (deve ser 0)",
             lambda c: "=MAX(0," + ",".join(f"{c}{panel_row(p,17)}-1" for p in range(3)) + ")"))
for k, (lab, fn) in enumerate(recs):
    r = REC0 + k
    put(f"B{r}", lab)
    bulk(r, [[fn(c) for c in COLS]])
    putf(f"D{r}", f'=IF(AND(MAX($I{r}:$GR{r})<1,MIN($I{r}:$GR{r})>-1),"OK","VERIFICAR: "&TEXT(MAX(MAX($I{r}:$GR{r}),-MIN($I{r}:$GR{r})),"#,##0"))')
    ws.Range(ws.Cells(r, C0), ws.Cells(r, C1)).NumberFormat = "#,##0"
ws.Columns("B").ColumnWidth = 52
ws.Columns("A").ColumnWidth = 7

NOT0 = REC0 + len(recs) + 3
notas = [
 ("NOTAS METODOLÓGICAS", ""),
 ("", ""),
 ("Filtro de escopo", f"Entram apenas clientes que (a) têm contrato alcançando o mês zero e (b) têm algum financial nos meses Orçados (volume, receita ou capex de t>=0). Das {NTOT} linhas de cliente do modelo, {NTOT-NK} ficaram de fora: linhas em branco, contratos encerrados antes do mês zero e agregados de histórico sem projeção."),
 ("Denominadores do rateio", "Os shares de volume e de capacidade têm como denominador o total DA PLANTA lido do modelo, não a soma das linhas desta aba. Assim o custo dos clientes fora do escopo não é empurrado para os que ficaram — cai no custo órfão. É isso que mantém a reconciliação fechando."),
 ("Escopo", f"3 plantas operacionais (PR, BA, RN) e {NK} clientes, jan/23 a dez/38 (192 meses). Terminal PE, Argentina e Outro ficam fora."),
 ("Janela de capacidade", "O cliente ocupa capacidade a partir do INÍCIO DA OPERAÇÃO (não da assinatura) até o fim do contrato. Meses entre assinatura e partida não geram rateio."),
 ("Janela do VPL", "Horizonte completo: jan/23 a dez/38. O realizado entra com t=0, ou seja a valor NOMINAL, sem ser capitalizado para o mês zero — decisão do analista, alinhada ao DCF do modelo, que também dá fator 1 ao passado. É o que mantém o capex de construção dentro da conta — restrito ao orçado, a planta apareceria de graça para quem chegou depois e o preço-piso desabaria (cai de 1,11 para 1,05 no PR e a ociosidade de 0,37 para 0,03)."),
 ("Desconto", "Mês zero = primeiro mês Orçado (linha 4, contador dinâmico). O realizado é capitalizado para frente (expoente negativo) e o orçado descontado para trás. O VPL fica em reais do primeiro mês orçado — inclui o custo de oportunidade do que já foi investido. TIR, payback, índice de lucratividade e preço-piso são invariantes à âncora."),
 ("Fluxo", "Desalavancado. A dívida não é rateada por cliente: a TIR do cliente é comparada ao WACC. A alavancagem continua no nível planta/consolidado do DCF."),
 ("Nível 1 — incremental", "Receita − molécula − liquefação/compressão variável − distribuição direta − regás direto − capex dedicado + residual ± capital de giro − IR. Responde 'aceito este contrato a este preço?'."),
 ("Nível 2 — com capacidade", "Nível 1 − custos fixos de planta − encargo de capacidade do capex de planta, ambos rateados por capacidade ocupada. Responde 'este preço paga a planta?'."),
 ("Nível 3 — fully loaded", "Nível 2 − G&A da matriz. O G&A é dividido igualmente pelo nº de plantas operacionais (premissa) e, dentro da planta, distribuído por capacidade ocupada. A parcela da ociosidade vai para o custo órfão, não para os clientes."),
 ("Driver: capacidade", "Custos de capacidade rateados por m³/dia ocupados / capacidade nominal da planta. O que não é alocado vira CUSTO ÓRFÃO da planta (ociosidade) — não é jogado em cliente nenhum."),
 ("Driver: volume", "Molécula e custos variáveis de liquefação rateados por m³ efetivos. Molécula só entra em cliente com a flag Custo Molécula = 1 na aba Clientes."),
 ("Encargo de capacidade", "Depreciação econômica linear (vida útil da premissa) + custo de capital sobre o saldo do ativo. Autoextingue-se — não cobra capex em perpetuidade."),
 ("Residual do capex", "Por decisão do analista: equipamento volta 100% do valor NOMINAL no mês de fim de contrato — sem depreciação, sem probabilidade de reuso, sem custo de desmobilização. Infraestrutura tem residual 0% (fica no site do cliente). Ambos os percentuais são editáveis nas premissas."),
 ("ATENÇÃO — residual", "O residual é um crédito sintético: ele NÃO existe no caixa da companhia. Por isso a soma dos fluxos dos clientes não bate com o DCF da planta — a diferença é exatamente o residual. É premissa deliberada, não erro."),
 ("G&A pré-operacional", "De jan/23 a jul/24 nenhuma planta operava. Nesses meses o G&A da matriz não tem planta para ratear e vai para a linha 'G&A da matriz em meses SEM planta em operação' — R$ 26,1 mi em VP. Sem essa linha o custo simplesmente sumia da conta."),
 ("Planta encerrada", "O custo órfão de cada planta usa DUAS janelas: os custos da própria planta (pools e encargo de capacidade) valem de jan/23 até o fim de operação — o custo de capital do capex em obra é real e existe antes da partida —, enquanto o G&A da matriz só é rateado entre plantas EM OPERAÇÃO. Zerar tudo antes da partida descartava R$ 25 mi de custo de capital de construção. Cada planta para de gerar custo órfão a partir do seu fim de operação (Painel de Controle, coluna F das linhas 53-55: o PR encerra em mar/36). A partir daí o G&A da matriz passa a ser dividido só entre as plantas ainda operando — o divisor é a linha 'Nº de plantas em operação no mês', não um número fixo. Deixar o divisor fixo em 3 jogava um terço do G&A no órfão do PR para sempre."),
 ("Capital de giro", "Vem do próprio modelo — linha (±) Variação de Capital de Giro da DRE mensal, por planta (L482 PR, L557 BA, L631 RN) — rateada pela participação do cliente na receita líquida da planta. As premissas DSO/DPO ficaram sem uso."),
 ("Imposto", "Por padrão (premissa Origem do IR = 2) o IR não é 34% teórico: é o IR/CSLL efetivo do modelo, rateado mês a mês pela base tributável positiva de cada cliente. A companhia mal é pagante no horizonte (EBT acumulado de R$ 19,6 mi), então cobrar 34% cheio de cada cliente inventava imposto e derrubava as TIRs. Com o rateio, a soma dos clientes fecha com o modelo. Origem do IR = 1 volta ao 34% próprio com prejuízo fiscal por cliente."),
 ("Imposto — modo 1 (alternativo)", "34% sobre o resultado do nível, com compensação integral de prejuízo fiscal acumulado do próprio cliente (sem a trava de 30%). Base = resultado operacional, sem depreciação."),
 ("TIR", "Calculada sobre o fluxo mensal e anualizada. Marcada 'n.a. s/ desembolso' quando o desembolso é irrelevante frente às entradas — a TIR não é definida nesses casos. Use VPL, IL e margem R$/m³ nesses clientes."),
 ("Reconciliação", "Todas as linhas do bloco de reconciliação devem marcar OK. A única exceção esperada é o G&A da matriz em meses pré-operacionais, quando não há cliente para receber o rateio."),
 ("Observação", "O capex por cliente é o efetivamente lançado na aba Capex (dimensionado pelo volume), que difere do campo 'CAPEX utilizado' da aba Clientes — este último é referência de input, não o valor contabilizado."),
]
for k, (a, b) in enumerate(notas):
    put(f"B{NOT0+k}", a); put(f"C{NOT0+k}", b)
ws.Columns("C").ColumnWidth = 130

print("Calculando...")
xl.Calculation = -4105          # automatico
xl.CalculateUntilAsyncQueriesDone()
ws.Calculate()
wb.Save()
print("Blocos gravados e salvos.")
wb.Close(SaveChanges=False)
xl.Quit()
print("OK")
