# -*- coding: utf-8 -*-
"""Repara as referencias que o delete da aba quebrou e compara com o arquivo original."""
import os, win32com.client as win32
def cl(c):
    s=""
    while c>0: c,m=divmod(c-1,26); s=chr(65+m)+s
    return s
def erros(wbk):
    d={}
    for sh in wbk.Worksheets:
        try: rg = sh.Cells.SpecialCells(-4123, 16)
        except Exception: continue
        d[sh.Name] = rg.Count
    return d
xl = win32.gencache.EnsureDispatch("Excel.Application"); xl.Visible=False; xl.DisplayAlerts=False
wb = xl.Workbooks.Open(os.path.abspath("Modelo - Realizado Jun.26 (v ajust) - TIR por Cliente.xlsx"), UpdateLinks=0)
orig = xl.Workbooks.Open(os.path.abspath("Modelo - Realizado Jun.26 (v ajust).xlsx"), UpdateLinks=0)
ea, eo = erros(wb), erros(orig)
print("=== ERROS: minha copia x original (o que eu causei) ===")
print("  %-40s %10s %10s %10s" % ("aba","copia","original","causado"))
for k in sorted(set(ea)|set(eo)):
    a, o = ea.get(k,0), eo.get(k,0)
    if a or o:
        print("  %-40s %10d %10d %10d" % (k[:40], a, o, a-o))
orig.Close(SaveChanges=False)

d = wb.Worksheets("Demonstrativo Financeiro Mensal")
print("\n=== REPARO ===")
d.Range(d.Cells(4,9), d.Cells(4,200)).Formula = tuple([tuple(
    "='TIR por Cliente'!%s4" % cl(c) for c in range(9,201))])
print("  L4 (contador de periodos) religada a 'TIR por Cliente'!linha 4")
for r, src in ((241,234),(242,235),(243,236),(244,237),(245,238)):
    d.Range(d.Cells(r,9), d.Cells(r,200)).Formula = tuple([tuple(
        "=%s%d/(1+'TIR por Cliente'!$D$11)^%s$4" % (cl(c), src, cl(c)) for c in range(9,201))])
    print("  L%d reescrita (fonte L%d)" % (r, src))
xl.Calculation = -4105
xl.CalculateFullRebuild()
print("\n=== CONFERENCIA ===")
print("  contador L4: I=%s AY=%s GR=%s" % (d.Cells(4,9).Text, d.Cells(4,51).Text, d.Cells(4,200).Text))
for r,nome in ((234,"FCFF PR"),(238,"FCFF TOTAL"),(241,"DCF PR"),(242,"DCF BA"),(243,"DCF RN"),(244,"DCF Holding"),(245,"EV TOTAL")):
    v = d.Range(d.Cells(r,9), d.Cells(r,200)).Value[0]
    s = sum(x for x in v if isinstance(x,(int,float)))
    print("  %-14s soma = %18s   jul/26 = %s" % (nome, format(s,",.0f"), d.Cells(r,51).Text))
ea2 = erros(wb)
print("\n  erros na DRE Mensal apos reparo: %d (era %d)" % (ea2.get("Demonstrativo Financeiro Mensal",0), ea.get("Demonstrativo Financeiro Mensal",0)))
p = wb.Worksheets("Painel de Controle")
print("  integridade:", " | ".join(p.Cells(r,1).Text+"="+p.Cells(r,2).Text for r in (6,7,8,9)))
wb.Save(); print("\n  salvo")
wb.Close(SaveChanges=False); xl.Quit()
