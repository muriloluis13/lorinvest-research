# -*- coding: utf-8 -*-
"""Formata a aba 'TIR por Cliente' no padrao visual do modelo GNLink."""
import os, sys
import win32com.client as win32

ARQ = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                      "Modelo - Realizado Jun.26 (v ajust) - TIR por Cliente.xlsx")
ABA = "TIR por Cliente"
C0, C1, NTOT = 9, 200, 78

def rgb(r, g, b): return r + g * 256 + b * 65536
NAVY   = rgb(0x1F, 0x38, 0x64)
GREY   = rgb(0x4D, 0x4D, 0x4E)
LBLUE  = rgb(0xD9, 0xE2, 0xF3)
LGREY  = rgb(0xF2, 0xF2, 0xF2)
TEAL   = rgb(0x0F, 0x3C, 0x4F)
WHITE  = rgb(255, 255, 255)
BLUE   = rgb(0x00, 0x00, 0xC0)
RED    = rgb(0xC0, 0x00, 0x00)
GREEN  = rgb(0x00, 0x60, 0x30)
LRED   = rgb(0xFC, 0xE4, 0xE4)
LGREEN = rgb(0xE2, 0xEF, 0xDA)
MID    = rgb(0x88, 0x88, 0x88)

# ATENCAO: este Excel interpreta os formatos com separadores pt-BR
# (ponto = milhar, virgula = decimal) mas exige nomes de cor em INGLES,
# e codigo de ano "aa" e nao "yy". Verificado empiricamente via Range.Text.
FMT_R    = '#.##0;[Red](#.##0);"–"'
FMT_PCT  = '0,0%;[Red](0,0%);"–"'
FMT_MES  = 'mmm/aa'
FMT_M3   = '#.##0;[Red](#.##0);"–"'
FMT_SH   = '0,0%;[Red](0,0%);"–"'
FMT_TIR  = '0,0%;[Red](0,0%);@'
FMT_IL   = '0,00;[Red](0,00);@'

xl = win32.gencache.EnsureDispatch("Excel.Application")
xl.Visible = True
xl.DisplayAlerts = False
xl.ScreenUpdating = False
wb = xl.Workbooks.Open(ARQ, UpdateLinks=0)
xl.Calculation = -4135
ws = wb.Worksheets(ABA)
ws.Activate()
print("aba aberta")

# ---------- localizar as secoes lendo a coluna B ----------
lastrow = ws.Cells(ws.Rows.Count, 2).End(-4162).Row
colB = ws.Range(ws.Cells(1, 2), ws.Cells(lastrow, 2)).Value
labels = {}
for i, v in enumerate(colB, 1):
    t = (v[0] if isinstance(v, tuple) else v)
    if isinstance(t, str) and t.strip():
        labels.setdefault(t.strip(), i)
def find(pref):
    for k, v in labels.items():
        if k.startswith(pref): return v
    return None

R_PREM = find("WACC (% a.a.)")
PANEL_TIT = find("PAINEL POR PLANTA")
PANEL_H = 22
PLANTAS_R = [PANEL_TIT + 2 + k * PANEL_H for k in range(3)]
ORFAO = [r + 20 for r in PLANTAS_R]
GA_ROW = find("G&A MATRIZ / HOLDING")
IDX_TIT = find("ÍNDICE DE CLIENTES")
IDX0 = IDX_TIT + 2
BLOCOS = sorted([(i, k) for k, i in labels.items()
                 if k.startswith(("VOLUME DO CLIENTE", "CAPACIDADE OCUPADA", "SHARE DE",
                                  "RECEITA LÍQUIDA (", "( − )", "( = )", "( + )", "( ± )",
                                  "SALDO DE PREJUÍZO", "FC DESCONTADO"))])
MET_TIT = find("MÉTRICAS POR CLIENTE")
MET0 = MET_TIT + 3          # linha do cabecalho de colunas
MR0 = MET0 + 1
REC_TIT = find("RECONCILIAÇÃO CONTRA")
REC0 = REC_TIT + 2
NOT_TIT = find("NOTAS METODOLÓGICAS")
print(f"premissas={R_PREM} painel={PANEL_TIT} idx={IDX0} blocos={len(BLOCOS)} met={MET0} rec={REC0} notas={NOT_TIT}")

def R(r1, c1, r2, c2): return ws.Range(ws.Cells(r1, c1), ws.Cells(r2, c2))
def bar(r, c1, c2, fill=GREY, color=WHITE, size=10, bold=True):
    rg = R(r, c1, r, c2)
    rg.Interior.Color = fill
    rg.Font.Color = color
    rg.Font.Bold = bold
    rg.Font.Size = size

# ---------- base ----------
used = R(1, 1, NOT_TIT + 25, C1)
used.Font.Name = "Arial"
used.Font.Size = 10
used.Interior.ColorIndex = -4142
used.Font.Color = rgb(0, 0, 0)
used.Font.Bold = False
ws.Cells.VerticalAlignment = -4108
try:
    ws.Cells.FormatConditions.Delete()
except Exception:
    pass
xl.ActiveWindow.DisplayGridlines = False
ws.Tab.Color = rgb(0x10, 0x48, 0x62)
print("base ok")

# larguras
ws.Columns("A").ColumnWidth = 7
ws.Columns("B").ColumnWidth = 46
ws.Columns("C").ColumnWidth = 7
ws.Columns("D").ColumnWidth = 13
ws.Columns("E").ColumnWidth = 12
ws.Columns("F:G").ColumnWidth = 10
ws.Columns("H").ColumnWidth = 9
R(1, C0, 1, C1).EntireColumn.ColumnWidth = 12

# ---------- cabecalho de datas ----------
bar(1, 1, C1, NAVY, WHITE)
bar(2, 1, C1, TEAL, WHITE)
R(2, C0, 2, C1).NumberFormat = FMT_MES
R(3, 1, 3, C1).Font.Color = MID
R(3, C0, 3, C1).NumberFormat = "0"
R(4, 1, 4, C1).Font.Color = MID          # contador de periodos (mes zero = 1o orcado)
R(4, C0, 4, C1).NumberFormat = "0"
R(5, 1, 5, C1).Font.Bold = True          # status Realizado/Orcado
R(5, 1, 5, C1).Font.Color = MID
R(1, C0, 5, C1).HorizontalAlignment = -4108
R(1, 2, 5, 2).HorizontalAlignment = -4131

# ---------- titulo ----------
ttl = find("TIR POR CLIENTE")
bar(ttl, 1, C1, NAVY, WHITE, size=14)
ws.Rows(ttl).RowHeight = 24
R(ttl + 1, 1, ttl + 1, C1).Font.Italic = True
R(ttl + 1, 1, ttl + 1, C1).Font.Color = MID

# ---------- premissas ----------
bar(R_PREM - 1, 1, 4, GREY, WHITE)
prem_end = R_PREM + 14
R(R_PREM, 2, prem_end, 2).IndentLevel = 1
box = R(R_PREM, 4, prem_end, 4)
box.Font.Color = BLUE
box.Font.Bold = True
box.Interior.Color = LGREY
box.HorizontalAlignment = -4108
for b in (7, 8, 9, 10):
    box.Borders(b).LineStyle = 1
    box.Borders(b).Color = rgb(0xBF, 0xBF, 0xBF)
FMT_PREM = ['0,00%', '0,0000%', '0%', '0 "anos"', '0%', '0%',
            '0 "dias"', '0 "dias"', '0', '0', '0', '0,0%', '0%', '0', '0']
for k, f in enumerate(FMT_PREM):
    ws.Cells(R_PREM + k, 4).NumberFormat = f

# ---------- painel por planta ----------
bar(PANEL_TIT, 1, C1, GREY, WHITE)
for pr in PLANTAS_R:
    bar(pr, 1, C1, LBLUE, NAVY)
    R(pr + 1, 2, pr + 20, 2).IndentLevel = 1
    R(pr + 1, C0, pr + 5, C1).NumberFormat = FMT_M3      # capacidades e volumes
    R(pr + 6, C0, pr + 16, C1).NumberFormat = FMT_R      # pools, capex, depreciacao, encargo
    R(pr + 17, C0, pr + 19, C1).NumberFormat = FMT_SH    # somas de share
    R(pr + 20, C0, pr + 20, C1).NumberFormat = FMT_R     # custo orfao
    R(pr + 11, 1, pr + 11, C1).Font.Bold = True          # pool fixo total
    R(pr + 16, 1, pr + 16, C1).Font.Bold = True          # encargo de capacidade
for orow in ORFAO:
    rg = R(orow, 1, orow, C1)
    rg.Font.Bold = True
    rg.Font.Color = RED
    rg.Interior.Color = LRED
for r in range(GA_ROW, GA_ROW + 8):
    R(r, 1, r, C1).Font.Bold = True
    R(r, C0, r, C1).NumberFormat = FMT_R
print("painel ok")

# ---------- indice de clientes ----------
_ci = ws.Range(ws.Cells(IDX0, 3), ws.Cells(IDX0 + 90, 3)).Value
PLC = []
for _v in _ci:
    _x = _v[0] if isinstance(_v, tuple) else _v
    if _x is None or str(_x).strip() == "": break
    PLC.append(int(_x))
NTOT = len(PLC)                       # clientes efetivamente na aba
CUTS = [k for k in range(1, NTOT) if PLC[k] != PLC[k-1]]
print(f"   clientes na aba: {NTOT} | quebras de planta em {CUTS}")
bar(IDX_TIT, 1, 8, GREY, WHITE)
bar(IDX0 - 1, 1, 8, NAVY, WHITE)
R(IDX0 - 1, 1, IDX0 - 1, 8).HorizontalAlignment = -4108
R(IDX0 - 1, 1, IDX0 - 1, 8).WrapText = True
idx = R(IDX0, 1, IDX0 + NTOT - 1, 8)
idx.Borders(11).LineStyle = 1
idx.Borders(11).Color = rgb(0xD9, 0xD9, 0xD9)
idx.Borders(12).LineStyle = 1
idx.Borders(12).Color = rgb(0xD9, 0xD9, 0xD9)
R(IDX0, 5, IDX0 + NTOT - 1, 5).NumberFormat = FMT_M3

# ---------- blocos mensais ----------
TOTAIS = ("( = )",)
ws.Outline.SummaryRow = 0     # xlSummaryAbove
for r, nome in BLOCOS:
    b0 = r + 2
    b1 = b0 + NTOT - 1
    bar(r, 1, C1, GREY, WHITE)
    stub = R(b0, 1, b1, 8)
    stub.Interior.Color = LGREY
    stub.Font.Color = rgb(0x40, 0x40, 0x40)
    R(b0, 6, b1, 7).NumberFormat = FMT_MES
    if nome.startswith("SHARE"):
        R(b0, C0, b1, C1).NumberFormat = FMT_SH
    else:
        R(b0, C0, b1, C1).NumberFormat = FMT_R
    if nome.startswith(TOTAIS):
        rg = R(b0, 1, b1, C1)
        rg.Font.Bold = True
        top = R(b0, 1, b0, C1).Borders(8)
        top.LineStyle = 1
        top.Weight = 2
        top.Color = NAVY
        stub.Interior.Color = LBLUE
        stub.Font.Color = NAVY
    else:
        ws.Rows(f"{b0}:{b1}").Group()
    # separadores entre plantas
    for cut in (b0 + k for k in CUTS):
        bd = R(cut, 1, cut, C1).Borders(8)
        bd.LineStyle = 1
        bd.Color = rgb(0xA6, 0xA6, 0xA6)
print("blocos ok")

# ---------- metricas ----------
NCOLM = 28
# a tabela de metricas so traz clientes no horizonte -> descobrir quantas linhas tem
_col = ws.Range(ws.Cells(MR0, 1), ws.Cells(MR0 + 90, 1)).Value
NMET = 0
for _v in _col:
    _x = _v[0] if isinstance(_v, tuple) else _v
    if _x is None or str(_x).strip() == "": break
    NMET += 1
print(f"   tabela de metricas: {NMET} linhas")
bar(MET_TIT, 1, NCOLM, NAVY, WHITE, size=12)
R(MET_TIT + 1, 1, MET_TIT + 1, NCOLM).Font.Italic = True
R(MET_TIT + 1, 1, MET_TIT + 1, NCOLM).Font.Color = MID
bar(MET0 - 1, 1, NCOLM, WHITE, NAVY)
for c0, tint in ((9, LGREY), (14, LBLUE), (19, rgb(0xFF, 0xF2, 0xCC)), (24, rgb(0xE2, 0xEF, 0xDA))):
    n = 5
    rg = R(MET0 - 1, c0, MET0 - 1, c0 + n - 1)
    rg.Interior.Color = tint
    rg.Font.Color = NAVY
    rg.Font.Bold = True
    rg.HorizontalAlignment = -4108
    rg.Merge()
    R(MET0, c0, MR0 + NMET - 1, c0 + n - 1).Borders(7).LineStyle = 1
    R(MET0, c0, MR0 + NMET - 1, c0 + n - 1).Borders(10).LineStyle = 1
bar(MET0, 1, NCOLM, NAVY, WHITE)
hdr = R(MET0, 1, MET0, NCOLM)
hdr.WrapText = True
hdr.HorizontalAlignment = -4108
ws.Rows(MET0).RowHeight = 42
tab = R(MR0, 1, MR0 + NMET - 1, NCOLM)
tab.Borders(11).LineStyle = 1
tab.Borders(11).Color = rgb(0xD9, 0xD9, 0xD9)
tab.Borders(12).LineStyle = 1
tab.Borders(12).Color = rgb(0xD9, 0xD9, 0xD9)
R(MR0, 6, MR0 + NMET - 1, 7).NumberFormat = FMT_MES
R(MR0, 5, MR0 + NMET - 1, 5).NumberFormat = FMT_M3
R(MR0, 9, MR0 + NMET - 1, 11).NumberFormat = FMT_R
R(MR0, 12, MR0 + NMET - 1, 12).NumberFormat = '0,00;[Red](0,00);"–"'
R(MR0, 13, MR0 + NMET - 1, 13).NumberFormat = FMT_R
for c0 in (14, 19, 24):
    R(MR0, c0, MR0 + NMET - 1, c0 + 1).NumberFormat = FMT_TIR
    R(MR0, c0 + 2, MR0 + NMET - 1, c0 + 2).NumberFormat = FMT_R
    R(MR0, c0 + 3, MR0 + NMET - 1, c0 + 3).NumberFormat = FMT_IL
    R(MR0, c0 + 4, MR0 + NMET - 1, c0 + 4).NumberFormat = FMT_MES
    # texto "n.a." em cinza claro
    rg = R(MR0, c0, MR0 + NMET - 1, c0 + 1)
    try:
        col = chr(64 + c0) if c0 < 27 else "A" + chr(64 + c0 - 26)
        fc = rg.FormatConditions.Add(Type=2, Formula1=f'=ISTEXT(${col}{MR0})')
        fc.Font.Color = rgb(0xA6, 0xA6, 0xA6)
        fc.Font.Italic = True
    except Exception as e:
        print("   cf texto falhou:", str(e)[:60])
# barras de dados no VPL de cada nivel
for c0 in (16, 21, 26):
    rg = R(MR0, c0, MR0 + NMET - 1, c0)
    try:
        db = rg.FormatConditions.AddDatabar()
    except Exception as e:
        print("   databar falhou:", str(e)[:60]); continue
    db.BarColor.Color = rgb(0x9D, 0xC3, 0xE6)
    db.BarFillType = 1
    try:
        db.NegativeBarFormat.ColorType = 0
        db.NegativeBarFormat.Color.Color = rgb(0xF4, 0xB1, 0x83)
    except Exception:
        pass
try:
    ws.AutoFilterMode = False
except Exception:
    pass
for tentativa in (lambda: R(MET0, 1, MR0 + NMET - 1, NCOLM).AutoFilter(1),
                  lambda: R(MET0, 1, MET0, NCOLM).AutoFilter(1)):
    try:
        tentativa(); print("   autofilter ok"); break
    except Exception as e:
        print("   autofilter falhou:", str(e)[:60])
print("metricas ok")

# ---------- reconciliacao ----------
bar(REC_TIT, 1, C1, GREY, WHITE)
nrec = 9
rec = R(REC0, 1, REC0 + nrec - 1, C1)
R(REC0, C0, REC0 + nrec - 1, C1).NumberFormat = FMT_R
st = R(REC0, 4, REC0 + nrec - 1, 4)
st.HorizontalAlignment = -4108
st.Font.Bold = True
try:
    st.FormatConditions.Delete()
except Exception:
    pass
for formula, cor, fundo in ((f'=$D{REC0}="OK"', GREEN, LGREEN),
                            (f'=$D{REC0}<>"OK"', RED, LRED)):
    try:
        fc = st.FormatConditions.Add(Type=2, Formula1=formula)
        fc.Font.Color = cor
        fc.Interior.Color = fundo
    except Exception as e:
        print("   cf reconciliacao falhou:", str(e)[:60])
ws.Rows(f"{REC0}:{REC0+nrec-1}").Group()

# ---------- notas ----------
bar(NOT_TIT, 1, 3, GREY, WHITE, size=11)
notas = R(NOT_TIT + 2, 2, NOT_TIT + 20, 3)
notas.WrapText = True
notas.VerticalAlignment = -4160
R(NOT_TIT + 2, 2, NOT_TIT + 20, 2).Font.Bold = True
R(NOT_TIT + 2, 2, NOT_TIT + 20, 2).Font.Color = NAVY
ws.Columns("C").ColumnWidth = 118
ws.Rows(f"{NOT_TIT+2}:{NOT_TIT+20}").AutoFit()

# ---------- navegacao ----------
nav = ttl + 1
ws.Range("F6").Value = ""
alvos = [("Premissas", f"B{R_PREM-1}"), ("Painel por planta", f"B{PANEL_TIT}"),
         ("Índice de clientes", f"B{IDX_TIT}"), ("MÉTRICAS", f"B{MET_TIT}"),
         ("Reconciliação", f"B{REC_TIT}"), ("Notas", f"B{NOT_TIT}")]
c = 6
for nome, ref in alvos:
    cell = ws.Cells(ttl + 1, c)
    ws.Hyperlinks.Add(Anchor=cell, Address="", SubAddress=f"'{ABA}'!{ref}", TextToDisplay="▸ " + nome)
    cell.Font.Size = 10
    cell.Font.Name = "Arial"
    cell.Font.Bold = True
    c += 1
R(ttl + 1, 6, ttl + 1, 11).HorizontalAlignment = -4131

# ---------- congelar paineis ----------
xl.ScreenUpdating = True
ws.Activate()
try:
    w = wb.Windows(1)          # a janela DESTE workbook (ActiveWindow pode ser outra)
    w.FreezePanes = False
    w.ScrollColumn = 1
    w.ScrollRow = 1
    w.SplitColumn = 8          # congela A:H (identificacao do cliente)
    w.SplitRow = 5             # congela as 5 linhas de cabecalho (inclui o contador)
    w.FreezePanes = True
    w.Zoom = 85
    print(f"   congelado em col={w.SplitColumn} row={w.SplitRow}")
except Exception as e:
    print("   congelamento falhou (nao critico):", str(e)[-70:])

xl.Calculation = -4105
xl.Calculate()
print("--- como o Excel renderiza (Text):")
for ref in ("D9", "D10", "D11", "D12", "D13", "D20", "D21"):
    print(f"   premissa {ref:4s} -> {ws.Range(ref).Text}")
for ref in (f"N{MR0+1}", f"P{MR0+1}", f"Q{MR0+1}", f"R{MR0+1}", f"I{MR0+1}"):
    print(f"   metrica  {ref:8s} -> {ws.Range(ref).Text}")
print(f"   orfao PR -> {ws.Cells(ORFAO[0], 60).Text} | BA -> {ws.Cells(ORFAO[1], 60).Text} | RN -> {ws.Cells(ORFAO[2], 60).Text}")
wb.Save()
print("salvo")
wb.Close(SaveChanges=False)
xl.Quit()
print("OK")
