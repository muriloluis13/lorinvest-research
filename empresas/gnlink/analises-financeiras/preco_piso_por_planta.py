# -*- coding: utf-8 -*-
"""Acrescenta a secao PRECO-PISO na aba 'TIR por Cliente'."""
import os, sys
import win32com.client as win32

ARQ = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                      "Modelo - Realizado Jun.26 (v ajust) - TIR por Cliente.xlsx")
ABA = "TIR por Cliente"
C0, C1, NTOT = 9, 200, 78

def rgb(r, g, b): return r + g * 256 + b * 65536
NAVY, GREY, LBLUE = rgb(0x1F,0x38,0x64), rgb(0x4D,0x4D,0x4E), rgb(0xD9,0xE2,0xF3)
LGREY, WHITE, RED = rgb(0xF2,0xF2,0xF2), rgb(255,255,255), rgb(0xC0,0x00,0x00)
GREEN, LRED, LGREEN = rgb(0x00,0x60,0x30), rgb(0xFC,0xE4,0xE4), rgb(0xE2,0xEF,0xDA)
MID, AMBER = rgb(0x88,0x88,0x88), rgb(0xFF,0xF2,0xCC)
FMT_R  = '#.##0;[Red](#.##0);"–"'
FMT_M3 = '#.##0;[Red](#.##0);"–"'
FMT_2  = '0,00;[Red](0,00);"–"'
FMT_P  = '0,0%;[Red](0,0%);"–"'

# ---- geometria da aba (mesma do script gerador) ----
R_PREM, PANEL0, PANEL_H = 10, 26, 22
GA_ROW = PANEL0 + 3 * PANEL_H + 1          # 92
IDX0 = GA_ROW + 4                          # 96
BLK0, STEP = IDX0 + NTOT + 4, NTOT + 3     # 178, 81
ORD = ["vol","capat","shvol","shvolmol","shcap","rec","molec","liqvar","dist","regas","mc",
       "fixo","encargo","ga","capex","resid","wc","pf1","ir1","fc1","pf2","ir2","fc2",
       "pf3","ir3","fc3","ac1","ac2","ac3"]
B = {k: BLK0 + i * STEP for i, k in enumerate(ORD)}
def panel(p, off): return PANEL0 + p * PANEL_H + off
W_AM = f"$D${R_PREM+1}"

xl = win32.gencache.EnsureDispatch("Excel.Application")
xl.Visible = True; xl.DisplayAlerts = False; xl.ScreenUpdating = False
wb = xl.Workbooks.Open(ARQ, UpdateLinks=0)
xl.Calculation = -4135
ws = wb.Worksheets(ABA); ws.Activate()

cprem = ws.Cells(R_PREM + 13, 4)
cprem.Font.Color = rgb(0,0,0xC0); cprem.Font.Bold = True
cprem.Interior.Color = LGREY; cprem.HorizontalAlignment = -4108
cprem.NumberFormat = "0"; cprem.Font.Name = "Arial"; cprem.Font.Size = 10
for b in (7,8,9,10): cprem.Borders(b).LineStyle = 1

lastrow = ws.Cells(ws.Rows.Count, 2).End(-4162).Row
S0 = lastrow + 4                     # inicio da nova secao
DISC = S0 + 2                        # linha do fator de desconto
PL0  = S0 + 6                        # cabecalho do resumo por planta
CLI_H = PL0 + 6                      # cabecalho da tabela por cliente
CLI0 = CLI_H + 1
print(f"nova secao a partir da linha {S0} (disc={DISC}, planta={PL0}, clientes={CLI0})")

def R(r1,c1,r2,c2): return ws.Range(ws.Cells(r1,c1), ws.Cells(r2,c2))
def bar(r,c1,c2,fill=GREY,color=WHITE,size=10):
    rg = R(r,c1,r,c2); rg.Interior.Color=fill; rg.Font.Color=color; rg.Font.Bold=True; rg.Font.Size=size
def cl(c):
    s=""
    while c>0: c,m=divmod(c-1,26); s=chr(65+m)+s
    return s

# ---------- titulo + fator de desconto ----------
ws.Cells(S0,2).Value = "PREÇO-PISO — QUANTO PRECISA SER COBRADO POR m³ PARA O CLIENTE SE PAGAR"
bar(S0,1,C1,NAVY,WHITE,12)
ws.Cells(S0+1,2).Value = ("Piso derivado do custo de capacidade da planta, não de regressão. Já embute fator de carga, "
                          "prazo de contrato e custo de carregamento do capex dedicado. Impostos não deslocam o piso "
                          "(no break-even o resultado é zero).")
R(S0+1,2,S0+1,C1).Font.Italic = True
R(S0+1,2,S0+1,C1).Font.Color = MID
ws.Cells(DISC,2).Value = "Fator de desconto ao WACC mensal (mês zero = 1º mês Orçado)"
R(DISC,1,DISC,C1).Font.Color = MID
ws.Range(ws.Cells(DISC,C0), ws.Cells(DISC,C1)).Formula = \
    tuple([tuple(f"=1/(1+{W_AM})^{cl(c)}$4" for c in range(C0, C1+1))])
R(DISC,C0,DISC,C1).NumberFormat = '0,0000'
D = f"$I${DISC}:$GR${DISC}"

# ---------- tabela por cliente (calculada primeiro; a planta agrega dela) ----------
HDR = ["ID","Cliente","Planta","Vol. Máx (m³/dia)","Prazo (meses)",
       "VP Volume (m³)","VP Capacidade (m³)","Fator de carga",
       "VP Margem contrib. (R$)","VP Custo de capacidade (R$)","VP G&A (R$)","VP Capex líquido (R$)",
       "MARGEM REALIZADA (R$/m³)","PISO EXIGIDO (R$/m³)","FOLGA (R$/m³)","Situação"]
ws.Range(ws.Cells(CLI_H,1), ws.Cells(CLI_H,len(HDR))).Value = tuple([tuple(HDR)])
rows=[]
for i in range(NTOT):
    m = CLI0 + i
    ident = IDX0 + i
    v, mc = B["vol"]+i, B["mc"]+i
    fx, en, ga = B["fixo"]+i, B["encargo"]+i, B["ga"]+i
    cx, rs, cp = B["capex"]+i, B["resid"]+i, B["capat"]+i
    rows.append([
      f"=$A${ident}", f"=$B${ident}", f"=$C${ident}", f"=$E${ident}",
      f'=IFERROR(DATEDIF($F${ident},$G${ident},"m"),0)',
      f"=SUMPRODUCT($I{v}:$GR{v},{D})",
      f"=SUMPRODUCT($I{cp}:$GR{cp},$I$3:$GR$3,{D})",
      f'=IFERROR($F{m}/$G{m},"–")',
      f"=SUMPRODUCT($I{mc}:$GR{mc},{D})",
      f"=-SUMPRODUCT($I{fx}:$GR{fx}+$I{en}:$GR{en},{D})",
      f"=-SUMPRODUCT($I{ga}:$GR{ga},{D})",
      f"=-SUMPRODUCT($I{cx}:$GR{cx}+$I{rs}:$GR{rs},{D})",
      f'=IFERROR($I{m}/$F{m},"–")',
      f'=IFERROR(($J{m}+$K{m}+$L{m})/$F{m},"–")',
      f'=IFERROR($M{m}-$N{m},"–")',
      f'=IF($F{m}<=0,"sem volume",IF($O{m}>=0,"paga-se","abaixo do piso"))',
    ])
ws.Range(ws.Cells(CLI0,1), ws.Cells(CLI0+NTOT-1,len(HDR))).Formula = tuple(tuple(r) for r in rows)
print("tabela por cliente ok")

# ---------- resumo por planta ----------
PH = ["Planta","#","Fator de carga","VP Volume (m³)",
      "Custo de capacidade — pool cheio (R$)","Custo de capacidade — alocado (R$)",
      "PISO N2 · capacidade (R$/m³)","+ G&A (R$/m³)","+ capex dedicado (R$/m³)",
      "PISO N3 · TOTAL (R$/m³)","Margem média realizada (R$/m³)","FOLGA (R$/m³)",
      "PISO DA PLANTA c/ ociosidade (R$/m³)","Preço da ociosidade (R$/m³)",
      "Piso @100% carga","Piso @85%","Piso @70%","Piso @55%"]
ws.Range(ws.Cells(PL0,2), ws.Cells(PL0,1+len(PH))).Value = tuple([tuple(PH)])
NOMES = ["PARANÁ","BAHIA","RIO GRANDE DO NORTE"]
CR = f"$C${CLI0}:$C${CLI0+NTOT-1}"
def col(letter, s): return f"${letter}${CLI0}:${letter}${CLI0+NTOT-1}"
prows=[]
for p in range(3):
    s = PL0 + 1 + p
    pf, pe = panel(p,11), panel(p,16)
    prows.append([
      NOMES[p], p+1,
      f"=IFERROR(SUMIF({CR},$C{s},{col('F',s)})/SUMIF({CR},$C{s},{col('G',s)}),\"–\")",
      f"=SUMIF({CR},$C{s},{col('F',s)})",
      f"=-SUMPRODUCT($I{pf}:$GR{pf}+$I{pe}:$GR{pe},{D})",
      f"=SUMIF({CR},$C{s},{col('J',s)})",
      f'=IFERROR($G{s}/$E{s},"–")',
      f"=IFERROR(SUMIF({CR},$C{s},{col('K',s)})/$E{s},\"–\")",
      f"=IFERROR(SUMIF({CR},$C{s},{col('L',s)})/$E{s},\"–\")",
      f'=IFERROR($H{s}+$I{s}+$J{s},"–")',
      f"=IFERROR(SUMIF({CR},$C{s},{col('I',s)})/$E{s},\"–\")",
      f'=IFERROR($L{s}-$K{s},"–")',
      f'=IFERROR($F{s}/$E{s},"–")',
      f'=IFERROR($N{s}-$H{s},"–")',
      f'=IFERROR($K{s}*$D{s}/1,"–")',
      f'=IFERROR($K{s}*$D{s}/0,85,"–")'.replace("0,85","0.85"),
      f'=IFERROR($K{s}*$D{s}/0.7,"–")',
      f'=IFERROR($K{s}*$D{s}/0.55,"–")',
    ])
ws.Range(ws.Cells(PL0+1,2), ws.Cells(PL0+3,1+len(PH))).Formula = tuple(tuple(r) for r in prows)
print("resumo por planta ok")

# ---------- formatacao ----------
R(S0,1,CLI0+NTOT+1,60).Font.Name = "Arial"
R(S0,1,CLI0+NTOT+1,60).Font.Size = 10
bar(PL0,2,1+len(PH),NAVY,WHITE)
R(PL0,2,PL0,1+len(PH)).WrapText = True
R(PL0,2,PL0,1+len(PH)).HorizontalAlignment = -4108
ws.Rows(PL0).RowHeight = 46
pt = R(PL0+1,2,PL0+3,1+len(PH))
pt.Borders(11).LineStyle = 1; pt.Borders(12).LineStyle = 1
R(PL0+1,2,PL0+3,2).Font.Bold = True
R(PL0+1,2,PL0+3,2).Interior.Color = LBLUE
R(PL0+1,2,PL0+3,2).Font.Color = NAVY
R(PL0+1,4,PL0+3,4).NumberFormat = FMT_P
R(PL0+1,5,PL0+3,7).NumberFormat = FMT_R
R(PL0+1,8,PL0+3,19).NumberFormat = FMT_2
R(PL0+1,11,PL0+3,11).Font.Bold = True      # PISO N3
R(PL0+1,11,PL0+3,11).Interior.Color = AMBER
R(PL0+1,13,PL0+3,13).Font.Bold = True      # folga
R(PL0+1,15,PL0+3,15).Interior.Color = LRED # preco da ociosidade
bar(CLI_H,1,len(HDR),NAVY,WHITE)
R(CLI_H,1,CLI_H,len(HDR)).WrapText = True
R(CLI_H,1,CLI_H,len(HDR)).HorizontalAlignment = -4108
ws.Rows(CLI_H).RowHeight = 46
ct = R(CLI0,1,CLI0+NTOT-1,len(HDR))
ct.Borders(11).LineStyle = 1; ct.Borders(11).Color = rgb(0xD9,0xD9,0xD9)
ct.Borders(12).LineStyle = 1; ct.Borders(12).Color = rgb(0xD9,0xD9,0xD9)
R(CLI0,4,CLI0+NTOT-1,4).NumberFormat = FMT_M3
R(CLI0,5,CLI0+NTOT-1,5).NumberFormat = '0'
R(CLI0,6,CLI0+NTOT-1,7).NumberFormat = FMT_M3
R(CLI0,8,CLI0+NTOT-1,8).NumberFormat = FMT_P
R(CLI0,9,CLI0+NTOT-1,12).NumberFormat = FMT_R
R(CLI0,13,CLI0+NTOT-1,15).NumberFormat = FMT_2
R(CLI0,14,CLI0+NTOT-1,14).Interior.Color = AMBER
R(CLI0,13,CLI0+NTOT-1,15).Font.Bold = True
sit = R(CLI0,16,CLI0+NTOT-1,16)
sit.HorizontalAlignment = -4108
for formula, cor, fundo in ((f'=$P{CLI0}="paga-se"', GREEN, LGREEN),
                            (f'=$P{CLI0}="abaixo do piso"', RED, LRED)):
    try:
        fc = sit.FormatConditions.Add(Type=2, Formula1=formula)
        fc.Font.Color = cor; fc.Interior.Color = fundo
    except Exception as e:
        print("  cf:", str(e)[:50])
try:
    R(CLI_H,1,CLI0+NTOT-1,len(HDR)).AutoFilter(1)
except Exception as e:
    print("  autofilter:", str(e)[:50])
ws.Rows(f"{DISC}:{DISC}").Group()

ws.Cells(PL0,20).Value = "PISO PLENO DA PLANTA c/ ociosidade (R$/m³)"
ws.Cells(PL0,21).Value = "FOLGA contra o piso pleno (R$/m³)"
for p in range(3):
    s2 = PL0+1+p
    ws.Cells(s2,20).Formula = f'=IFERROR($N{s2}+$I{s2}+$J{s2},"–")'
    ws.Cells(s2,21).Formula = f'=IFERROR($L{s2}-$T{s2},"–")'
rgp = R(PL0+1,20,PL0+3,21)
rgp.NumberFormat = FMT_2; rgp.Font.Bold = True; rgp.Interior.Color = AMBER
hdp = R(PL0,20,PL0,21)
hdp.Interior.Color = NAVY; hdp.Font.Color = WHITE; hdp.Font.Bold = True
hdp.WrapText = True; hdp.HorizontalAlignment = -4108
hdp.Font.Name = "Arial"; hdp.Font.Size = 10

xl.Calculation = -4105
xl.Calculate(); ws.Calculate()
print("\n=== PISO POR PLANTA ===")
for p in range(3):
    s = PL0 + 1 + p
    print(f"  {ws.Cells(s,2).Text:22s} carga={ws.Cells(s,4).Text:>7s} | pisoN2={ws.Cells(s,8).Text:>7s} "
          f"+G&A={ws.Cells(s,9).Text:>6s} +capex={ws.Cells(s,10).Text:>6s} | PISO N3={ws.Cells(s,11).Text:>7s} "
          f"| realizada={ws.Cells(s,12).Text:>7s} folga={ws.Cells(s,13).Text:>7s} "
          f"| piso planta={ws.Cells(s,14).Text:>7s} ociosidade={ws.Cells(s,15).Text:>6s}")
    print(f"     PISO PLENO={ws.Cells(s,20).Text:>7s}  folga plena={ws.Cells(s,21).Text:>7s}  |  "
          f"carga 100%={ws.Cells(s,16).Text:>6s}  85%={ws.Cells(s,17).Text:>6s}  "
          f"70%={ws.Cells(s,18).Text:>6s}  55%={ws.Cells(s,19).Text:>6s}")
print("")
print("=== POR CLIENTE (ordenado pela folga) ===")
lst=[]
for i in range(NTOT):
    r = CLI0+i
    nome = ws.Cells(r,2).Text; vv = ws.Cells(r,6).Value
    if not nome or not isinstance(vv,(int,float)) or vv<=0: continue
    lst.append((ws.Cells(r,15).Value, nome, ws.Cells(r,3).Text, ws.Cells(r,5).Text,
                ws.Cells(r,8).Text, ws.Cells(r,13).Text, ws.Cells(r,14).Text,
                ws.Cells(r,15).Text, ws.Cells(r,16).Text))
lst.sort(key=lambda x: x[0] if isinstance(x[0],(int,float)) else -9e9, reverse=True)
PLN={"1":"PR","2":"BA","3":"RN"}
print(f"{'Cliente':32s} {'Pl':3s} {'mes':>4s} {'carga':>7s} {'margem':>7s} {'piso':>7s} {'folga':>7s}  situacao")
for _,nome,pl,pz,cg,mg,pi,fo,si in lst:
    print(f"{nome[:31]:32s} {PLN.get(pl,pl):3s} {pz:>4s} {cg:>7s} {mg:>7s} {pi:>7s} {fo:>7s}  {si}")
print("")
print(f"resumo: {sum(1 for x in lst if x[8]=='paga-se')} pagam-se de {len(lst)} clientes com volume")
wb.Save()
print("\nsalvo")
wb.Close(SaveChanges=False); xl.Quit()
print("OK")
