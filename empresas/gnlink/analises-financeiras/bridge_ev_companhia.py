# -*- coding: utf-8 -*-
"""Bridge: Sigma VPL dos clientes (Nivel 3) -> EV da companhia.

Derivacao (tudo em VP, mesmo fator de desconto da linha 4):
  Sigma fc3 = Sigma mc + Sigma fixo + Sigma encargo + Sigma ga
            + Sigma capex_cliente + Sigma resid + Sigma wc + Sigma ir3
  EV        = receita + pools variaveis + pool fixo + G&A holding
            + capex total + WC total + IR total + nao operacionais
  Como o custo orfao ja e, por construcao, a parcela NAO alocada de cada pool
  (molecula, liquefacao, fixo, encargo e G&A), a diferenca colapsa em:
  EV - Sigma fc3 = orfao - encargo_total + capex_de_planta
                 + receita dos clientes fora do escopo + WC nao alocado
                 - residual sintetico + nao operacionais
"""
import os, win32com.client as win32
xl = win32.gencache.EnsureDispatch("Excel.Application"); xl.Visible=False; xl.DisplayAlerts=False
wb = xl.Workbooks.Open(os.path.abspath("Modelo - Realizado Jun.26 (v ajust) - TIR por Cliente.xlsx"), UpdateLinks=0)
ws = wb.Worksheets("TIR por Cliente"); d = wb.Worksheets("Demonstrativo Financeiro Mensal")
rc = wb.Worksheets("Receita"); cxs = wb.Worksheets("Capex")
C0, C1 = 9, 200
N = C1 - C0 + 1
def lin(sh, r):
    v = sh.Range(sh.Cells(r, C0), sh.Cells(r, C1)).Value[0]
    return [x if isinstance(x, (int, float)) else 0.0 for x in v]
lab = {}
for r in range(1, 1900):
    t = ws.Cells(r, 2).Text
    if t.strip(): lab.setdefault(t.strip(), r)
IDX0 = lab["ÍNDICE DE CLIENTES"] + 2
NK = 0
while ws.Cells(IDX0 + NK, 1).Text.strip(): NK += 1
BLK0, STEP = IDX0 + NK + 4, NK + 3
ORD = ["vol","capat","shvol","shvolmol","shcap","rec","molec","liqvar","dist","regas","mc",
       "fixo","encargo","ga","capex","resid","wc","pf1","ir1","fc1","pf2","ir2","fc2",
       "pf3","ir3","fc3","ac1","ac2","ac3"]
B = {k: BLK0 + i*STEP for i, k in enumerate(ORD)}
P0 = lab["PARANÁ"]
O_ENC, O_ORF = 16, 20
for o, txt in ((O_ENC, "Encargo"), (O_ORF, "ÓRFÃO")):
    assert txt.lower() in ws.Cells(P0+o, 2).Text.lower(), "offset %d nao bate" % o
w = ws.Range("D11").Value
FD = [1.0/((1.0+w)**t) for t in lin(ws, 4)]
def vp(sh, r): return sum(a*b for a, b in zip(lin(sh, r), FD))
def vpb(k):    return sum(vp(ws, B[k]+j) for j in range(NK))
def vpp(off):  return sum(vp(ws, P0+p*22+off) for p in range(3))

# planta em operacao mes a mes (Painel de Controle L53-55, colunas D e F)
pc = wb.Worksheets("Painel de Controle")
mes = ws.Range("I2:GR2").Value[0]
ATV, ATF = [], []
for p in range(3):
    ini = pc.Cells(53+p, 4).Value; fim = pc.Cells(53+p, 6).Value
    # ATV = planta em operacao (janela do G&A) | ATF = ainda nao encerrada (janela do orfao)
    ATV.append([1.0 if (ini is not None and fim is not None and ini <= m < fim) else 0.0 for m in mes])
    ATF.append([1.0 if (fim is not None and m < fim) else 0.0 for m in mes])
GA_ROW = lab["G&A MATRIZ / HOLDING (R$) — consolidado, a ratear"]
gaSP = lin(ws, GA_ROW + 9)                      # G&A em meses sem planta operando
# encargo EFETIVAMENTE cobrado = o que entrou nos clientes + o que entrou no orfao
encAloc = [0.0]*N
for j in range(NK):
    encAloc = [a+b for a, b in zip(encAloc, lin(ws, B["encargo"]+j))]
encOrf = [0.0]*N
for p in range(3):
    e = lin(ws, P0+p*22+O_ENC); sh = lin(ws, P0+p*22+17)
    for k in range(N):
        encOrf[k] += ATF[p][k]*e[k]*(1-sh[k])
encCobrado = [a+b for a, b in zip(encAloc, encOrf)]

N3     = vpb("fc3")
resid  = vpb("resid")
encT   = sum(a*b for a, b in zip(encCobrado, FD))
encFull = vpp(O_ENC)
orf    = vpp(O_ORF)
capexP = -sum(vp(cxs, r) for r in (677, 678, 679)) - vpb("capex")
recExc = sum(vp(rc, r) for r in (727, 733, 739)) - vpb("rec")
wcNA   = sum(vp(d, r) for r in (482, 557, 631)) - vpb("wc")
nop    = vp(d, 96)
EV     = sum(lin(d, 245))
barras = [
  ("1  Σ VPL dos clientes (Nível 3)",                 N3),
  ("2  ( − ) Residual sintético do capex",            -resid),
  ("3  ( + ) Encargo de capacidade (não é caixa)",    -encT),
  ("4  ( − ) Capex de planta (real)",                 capexP),
  ("5  ( − ) Custo órfão / ociosidade",               orf),
  ("6  ( + ) Receita dos clientes fora do escopo",    recExc),
  ("7  ( ± ) Capital de giro não alocado",            wcNA),
  ("8  ( − ) G&A da matriz sem planta em operação",   sum(a*b for a,b in zip(gaSP, FD))),
  ("9  ( ± ) Não operacionais",                       nop),
]
print("=== BRIDGE: VPL DOS CLIENTES -> EV DA COMPANHIA (VP, R$) ===")
print("")
tot = 0.0
for nome, v in barras:
    tot += v
    print("  %-46s %18s" % (nome, format(v, ",.0f")))
print("  %-46s %18s" % ("-"*34, "-"*18))
print("  %-46s %18s" % ("   SOMA DAS BARRAS", format(tot, ",.0f")))
print("  %-46s %18s" % ("   EV DA COMPANHIA (modelo, L245)", format(EV, ",.0f")))
r = EV - tot
print("  %-46s %18s   (%.2f%% do EV)" % ("   RESÍDUO", format(r, ",.0f"), abs(r/EV)*100 if EV else 0))
print("")
print("=== memo ===")
print("  %-46s %18s" % ("encargo total do painel", format(encFull, ",.0f")))
print("  %-46s %18s" % ("encargo efetivamente cobrado", format(encT, ",.0f")))
print("  %-46s %18s" % ("  diferenca = encargo apos o encerramento", format(encFull-encT, ",.0f")))
print("")
print("=== custo órfão por planta (VP) ===")
for p, n in enumerate(("PR", "BA", "RN")):
    print("  %-4s %18s" % (n, format(vp(ws, P0+p*22+O_ORF), ",.0f")))
wb.Close(SaveChanges=False); xl.Quit()
