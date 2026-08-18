# -*- coding: utf-8 -*-
"""Auditoria estrutural da aba TIR por Cliente."""
import os, re, win32com.client as win32

C0, C1 = 9, 200
NC = [24, 32, 22]
CLI_SRC = [(7, 24), (37, 32), (75, 22)]
SRC = {
    "rec_gnl": ("Receita",(1161,1188,1223)), "rec_gnc": ("Receita",(1318,1345,1380)),
    "rec_alug":("Receita",(1475,1501,1535)), "rec_outr":("Receita",(1627,1653,1687)),
    "rec_serv":("Receita",(1779,1806,1841)), "vol_gnl": ("Receita",(367,394,429)),
    "vol_gnc": ("Receita",(525,552,587)),    "frete_fix":("OPEX",(710,736,770)),
    "frete_var":("OPEX",(861,887,921)),      "alug_log":("OPEX",(1027,1052,1085)),
    "out_dist":("OPEX",(1174,1199,1232)),    "reg_alug":("OPEX",(1992,2017,2050)),
    "reg_mont":("OPEX",(2139,2164,2197)),    "cx_di":("Capex",(65,90,123)),
    "cx_de":("Capex",(213,238,271)),         "cx_ri":("Capex",(364,389,422)),
    "cx_re":("Capex",(511,536,569)),
}
P = {"molec":("OPEX",(372,373,374)),"energia":("OPEX",(398,399,400)),"insumos":("OPEX",(438,439,440)),
     "perdas":("OPEX",(504,505,506)),"om":("OPEX",(496,497,498)),"outliq":("OPEX",(529,530,531)),
     "compr":("OPEX",(543,544,545)),"term":("OPEX",(552,553,554)),"sga":("OPEX",(562,563,564)),
     "dist_t":("OPEX",(701,702,703)),"reg_t":("OPEX",(1959,1960,1961)),"capex_t":("Capex",(677,678,679)),
     "cap_gnl":("Receita",(9,10,11)),"cap_gnc":("Receita",(18,19,20)),
     "vol_gnl_t":("Receita",(365,392,427)),"vol_gnc_t":("Receita",(523,550,585)),
     "mol_unit":("OPEX",(363,364,365))}
ORD = ["vol","capat","shvol","shvolmol","shcap","rec","molec","liqvar","dist","regas","mc",
       "fixo","encargo","ga","capex","resid","wc","pf1","ir1","fc1","pf2","ir2","fc2",
       "pf3","ir3","fc3","ac1","ac2","ac3"]
R_PREM, PANEL0, PANEL_H = 10, 26, 22
GA_ROW = PANEL0 + 3*PANEL_H + 1
IDX0 = GA_ROW + 4

xl = win32.gencache.EnsureDispatch("Excel.Application"); xl.Visible=False; xl.DisplayAlerts=False
wb = xl.Workbooks.Open(os.path.abspath("Modelo - Realizado Jun.26 (v ajust) - TIR por Cliente.xlsx"), UpdateLinks=0)
ws = wb.Worksheets("TIR por Cliente")

ids = ws.Range(ws.Cells(IDX0,1), ws.Cells(IDX0+90,1)).Value
IDS = []
for v in ids:
    x = v[0] if isinstance(v, tuple) else v
    if x is None or str(x).strip()=="": break
    IDS.append(str(int(x)) if isinstance(x,(int,float)) else str(x).strip())
NK = len(IDS)
MAP = [(int(t[0])-1, int(t[1:])-1) for t in IDS]
BLK0, STEP = IDX0 + NK + 4, NK + 3
B = {k: BLK0 + i*STEP for i,k in enumerate(ORD)}
BLKROWS = {}
for k,base in B.items():
    for j in range(NK): BLKROWS[base+j] = (k, j)
MET0 = BLK0 + len(ORD)*STEP + 2
MR0 = MET0 + 1
print("aba: %d clientes | blocos %d..%d | metricas %d..%d" % (NK, BLK0, B["ac3"]+NK-1, MR0, MR0+NK-1))

lastB = ws.Cells(ws.Rows.Count,2).End(-4162).Row
CLI0 = None
for r in range(MR0+NK, lastB+1):
    if str(ws.Cells(r,1).Text).strip()=="ID" and "Vol" in ws.Cells(r,4).Text:
        CLI0 = r+1; break
PISO_OK = set()
if CLI0:
    _t = CLI0 - 13
    PISO_OK = set(range(_t, CLI0))       # titulo, fator de desconto e resumo por planta
print("tabela preco-piso: %s" % (("%d..%d" % (CLI0, CLI0+NK-1)) if CLI0 else "nao localizada"))

# regex unico: captura referencia (com ou sem aba) e o segundo extremo do intervalo
REF = re.compile(r"(?:(?:'([^']+)'|([A-Za-z\u00c0-\u00ff][\w\u00c0-\u00ff.]*))!)?"
                 r"\$?([A-Z]{1,3})\$?(\d+)"
                 r"(?::\$?([A-Z]{1,3})\$?(\d+))?")

def esperado_ext(p, k):
    return set((v[0], v[1][p]+k) for v in SRC.values())
PLROWS = {}
for sh in ("Receita","OPEX","Capex"):
    d = {}
    for s2,st in P.values():
        if s2==sh:
            for pp in range(3): d.setdefault(st[pp], pp)
    PLROWS[sh] = d

problemas = []
def chk_ext(ctx,row,p,k,sh,rr,esp):
    if sh == "Clientes":
        r0,n = CLI_SRC[p]
        if rr != r0+k: problemas.append((ctx,row,"Clientes!%d deveria ser %d" % (rr, r0+k)))
        return
    if sh in ("Receita","OPEX","Capex"):
        if (sh,rr) in esp: return
        if rr in PLROWS[sh]:
            if PLROWS[sh][rr] != p:
                problemas.append((ctx,row,"%s!%d e da planta %d, cliente e da %d" % (sh,rr,PLROWS[sh][rr]+1,p+1)))
            return
        outras = [(pp,kk) for pp in range(3) for kk in range(NC[pp]) if (sh,rr) in esperado_ext(pp,kk)]
        if outras:
            problemas.append((ctx,row,"%s!%d aponta p/ planta %d cliente %d, esperado planta %d cliente %d"
                              % (sh,rr,outras[0][0]+1,outras[0][1]+1,p+1,k+1)))
        elif rr not in (1,2,3,4,5,727,733,739):
            problemas.append((ctx,row,"%s!%d fora de bloco conhecido" % (sh,rr)))
        return
    if "Demonstrativo" in sh or sh=="DCF" or "Painel" in sh: return
    problemas.append((ctx,row,"aba inesperada: %s!%d" % (sh,rr)))

def chk_int(ctx,row,p,k,j,rr):
    if rr <= 5 or R_PREM <= rr <= R_PREM+13: return
    if PANEL0 <= rr < PANEL0 + 3*PANEL_H:
        pp = (rr - PANEL0)//PANEL_H
        if pp != p: problemas.append((ctx,row,"painel L%d e da planta %d, cliente da %d" % (rr,pp+1,p+1)))
        return
    if GA_ROW <= rr <= GA_ROW+3: return
    if IDX0 <= rr < IDX0+NK:
        if rr != IDX0+j: problemas.append((ctx,row,"indice L%d deveria ser %d" % (rr, IDX0+j)))
        return
    if rr in BLKROWS:
        kk, jj2 = BLKROWS[rr]
        if jj2 != j: problemas.append((ctx,row,"bloco '%s' L%d e do cliente pos %d, deveria ser %d" % (kk,rr,jj2,j)))
        return
    if MR0 <= rr < MR0+NK:
        if rr != MR0+j: problemas.append((ctx,row,"metricas L%d deveria ser %d" % (rr, MR0+j)))
        return
    if rr in PISO_OK: return
    if CLI0 and CLI0 <= rr < CLI0+NK:
        if rr != CLI0+j: problemas.append((ctx,row,"preco-piso L%d deveria ser %d" % (rr, CLI0+j)))
        return
    problemas.append((ctx,row,"linha interna %d nao reconhecida" % rr))

def audita(row, p, k, j, ctx, formula):
    if not isinstance(formula,str) or not formula.startswith("="): return
    esp = esperado_ext(p,k)
    for m in REF.finditer(formula):
        sh = m.group(1) or m.group(2)
        linhas = [int(m.group(4))]
        if m.group(6): linhas.append(int(m.group(6)))
        for rr in linhas:
            if sh: chk_ext(ctx,row,p,k,sh,rr,esp)
            else:  chk_int(ctx,row,p,k,j,rr)

COLA = 60
for key in ORD:
    base = B[key]
    fs = ws.Range(ws.Cells(base,COLA), ws.Cells(base+NK-1,COLA)).Formula
    for j in range(NK):
        p,k = MAP[j]
        audita(base+j, p, k, j, "bloco "+key, fs[j][0] if isinstance(fs[j],tuple) else fs[j])
for col in range(1, 29):
    fs = ws.Range(ws.Cells(MR0,col), ws.Cells(MR0+NK-1,col)).Formula
    for j in range(NK):
        p,k = MAP[j]
        audita(MR0+j, p, k, j, "metricas c%d" % col, fs[j][0] if isinstance(fs[j],tuple) else fs[j])
if CLI0:
    for col in range(1, 17):
        fs = ws.Range(ws.Cells(CLI0,col), ws.Cells(CLI0+NK-1,col)).Formula
        for j in range(NK):
            p,k = MAP[j]
            audita(CLI0+j, p, k, j, "piso c%d" % col, fs[j][0] if isinstance(fs[j],tuple) else fs[j])
fs = ws.Range(ws.Cells(IDX0,1), ws.Cells(IDX0+NK-1,8)).Formula
for j in range(NK):
    p,k = MAP[j]
    for col in range(8):
        audita(IDX0+j, p, k, j, "indice c%d" % (col+1), fs[j][col])

print("\n" + "="*72)
print("%d PROBLEMAS" % len(problemas))
print("="*72)
from collections import Counter
cnt = Counter("%s :: %s" % (c,msg) for c,_,msg in problemas)
for txt,n in cnt.most_common(60):
    print("  %4dx  %s" % (n, txt[:115]))
wb.Close(SaveChanges=False); xl.Quit()
