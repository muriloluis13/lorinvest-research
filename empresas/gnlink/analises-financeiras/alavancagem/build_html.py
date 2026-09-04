# -*- coding: utf-8 -*-
"""Gera index-2026-09-04.html a partir do index.html (24/07) + dados dos 16 modelos de 04/set/2026.

Diferenças em relação à versão de julho:
  - novo switch de escopo: 3 plantas (Plantas atuais) x 5 plantas (Plantas atuais + Projetos)
  - séries de volume e receita por planta passam a incluir AR e SAL
  - Fontes & Usos e textos atualizados para a base jul/2026
"""
import json, re, io

SRC = 'index.html'
DST = 'index-2026-09-04.html'
DATA_JSON = '_data_2026-09-04.json'

PLANT_KEYS = ['pr', 'ba', 'rn', 'ar', 'sal']
KEEP_SERIES = ['gas_price', 'ebitda', 'ebitda_mg', 'net_income', 'net_mg', 'fcfe', 'eop_cash',
               'eop_debt', 'net_debt_ebitda', 'equity_issue', 'dividends', 'principal', 'interest',
               'fcfe_accum_annual', 'fcff'] + ['rev_' + p for p in PLANT_KEYS] + ['vol_' + p for p in PLANT_KEYS]


def rnd(v, n=6):
    return None if not isinstance(v, (int, float)) else round(v, n)


def slim(raw):
    out = {}
    for pl, funds in raw.items():
        out[pl] = {}
        for fu, blk in funds.items():
            o = {'years_full': blk['years_full']}
            for cx in ('on', 'off'):
                st = blk[cx]
                k = {kk: (rnd(vv) if isinstance(vv, (int, float)) else vv)
                     for kk, vv in st['kpi'].items() if not kk.startswith('_')}
                s = {kk: [rnd(v) for v in st['series_full'][kk]] for kk in KEEP_SERIES}
                o[cx] = {'kpi': k, 'series_full': s}
            out[pl][fu] = o
    return out


def uop_block(raw):
    """Fontes & Usos: bloco histórico do modelo (idêntico nos 16 arquivos)."""
    src = raw['p3']['equity']['on']['uop']
    want_f = ['Equity', 'Dívida líquida', 'Fontes']
    want_u = ['CapEx', 'Serviço da dívida', 'SG&A Holding', 'OpEx e outros', 'Usos']
    f = {k: v for k, v in src['fontes'] if k in want_f}
    u = {k: v for k, v in src['usos'] if k in want_u}
    return f, u


def mi(v):
    return ('R$ %.1f mi' % v).replace('.', ',')


def main():
    raw = json.load(open(DATA_JSON, encoding='utf-8'))
    html = io.open(SRC, encoding='utf-8').read()
    data = slim(raw)
    fon, uso = uop_block(raw)

    # ---------- 1. bloco DATA + descrições ----------
    html = re.sub(r'const DATA = \{.*?\};\n',
                  'const DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n',
                  html, count=1, flags=re.S)
    html = re.sub(r'const YEARS = DATA\.equity\.years;\n',
                  "const PLDESC = {p3:'3 plantas (Plantas atuais)', p5:'5 plantas (Plantas atuais + Projetos)'};\n"
                  "const PLABEL = {pr:'PR',ba:'BA',rn:'RN',ar:'AR (projeto)',sal:'SAL (projeto)'};\n",
                  html, count=1)

    # ---------- 2. paleta das plantas ----------
    html = html.replace(
        "const PLANT={pr:'#002D5C', ba:'#28477E', rn:'#4880A8'};",
        # plantas atuais na família navy/azul; projetos (AR, SAL) em teal/laranja queimado,
        # este último distinto do âmbar da linha de preço médio
        "const PLANT={pr:'#002D5C', ba:'#28477E', rn:'#4880A8', ar:'#5A9B87', sal:'#C55A17'};\n"
        "const PKEYS=['pr','ba','rn','ar','sal'];")

    # ---------- 3. estado: escopo de plantas ----------
    html = html.replace("let cur='equity';", "let plants='p3';\nlet cur='equity';")

    # ---------- 4. seletor de cenário no build() ----------
    html = html.replace("const F=DATA[cur], St=F[capex], k=St.kpi;",
                        "const F=DATA[plants][cur], St=F[capex], k=St.kpi;")
    html = html.replace(
        "document.getElementById('scDesc').textContent='Cenário ativo: '+SCDESC[cur]+' · CapEx de manutenção '+(capex==='on'?'ligado':'desligado');",
        "document.getElementById('scDesc').textContent='Cenário ativo: '+PLDESC[plants]+' · '+SCDESC[cur]+' · CapEx de manutenção '+(capex==='on'?'ligado':'desligado');")

    # ---------- 5. séries por planta: 3 ou 5 ----------
    html = html.replace(
        "  const vol_pr=Z('vol_pr'),vol_ba=Z('vol_ba'),vol_rn=Z('vol_rn');\n"
        "  const rev_pr=Z('rev_pr'),rev_ba=Z('rev_ba'),rev_rn=Z('rev_rn'),gas=Z('gas_price');",
        "  // plantas ligadas no escopo selecionado (flag Y/N do Dashboard do modelo)\n"
        "  const live=(k.active_plants&&k.active_plants.length)?PKEYS.filter(p=>k.active_plants.indexOf(p)>=0):PKEYS;\n"
        "  const gas=Z('gas_price');")

    html = html.replace(
        "  charts.vol=new Chart(document.getElementById('cVol'),{data:{labels:YR,datasets:[\n"
        "    {type:'bar',label:'PR',data:vol_pr,backgroundColor:PLANT.pr,stack:'v',yAxisID:'y',datalabels:barLbl('#fff')},\n"
        "    {type:'bar',label:'BA',data:vol_ba,backgroundColor:PLANT.ba,stack:'v',yAxisID:'y',datalabels:barLbl('#fff')},\n"
        "    {type:'bar',label:'RN',data:vol_rn,backgroundColor:PLANT.rn,stack:'v',yAxisID:'y',datalabels:barLbl('#fff')},\n"
        "  ]},options:",
        "  charts.vol=new Chart(document.getElementById('cVol'),{data:{labels:YR,datasets:\n"
        "    live.map(p=>({type:'bar',label:PLABEL[p],data:Z('vol_'+p),backgroundColor:PLANT[p],stack:'v',yAxisID:'y',datalabels:barLbl('#fff')}))\n"
        "  },options:")

    html = html.replace(
        "  charts.rev=new Chart(document.getElementById('cRev'),{data:{labels:YR,datasets:[\n"
        "    {type:'bar',label:'PR',data:rev_pr,backgroundColor:PLANT.pr,stack:'r',yAxisID:'y',order:2,datalabels:barLbl('#fff')},\n"
        "    {type:'bar',label:'BA',data:rev_ba,backgroundColor:PLANT.ba,stack:'r',yAxisID:'y',order:2,datalabels:barLbl('#fff')},\n"
        "    {type:'bar',label:'RN',data:rev_rn,backgroundColor:PLANT.rn,stack:'r',yAxisID:'y',order:2,datalabels:barLbl('#fff')},\n"
        "    {type:'line',label:'Preço médio (R$/m³)',data:gas,borderColor:AMBER,backgroundColor:AMBER,yAxisID:'y2',order:0,tension:.3,borderWidth:2.5,pointRadius:2,datalabels:lineLbl(AMBER,D1)},\n"
        "  ]},options:",
        "  charts.rev=new Chart(document.getElementById('cRev'),{data:{labels:YR,datasets:\n"
        "    live.map(p=>({type:'bar',label:PLABEL[p],data:Z('rev_'+p),backgroundColor:PLANT[p],stack:'r',yAxisID:'y',order:2,datalabels:barLbl('#fff')}))\n"
        "    .concat([{type:'line',label:'Preço médio (R$/m³)',data:gas,borderColor:AMBER,backgroundColor:AMBER,yAxisID:'y2',order:0,tension:.3,borderWidth:2.5,pointRadius:2,datalabels:lineLbl(AMBER,D1)}])\n"
        "  },options:")

    # ---------- 6. chips: novo switch de escopo ----------
    html = html.replace(
        '  <div class="chips">\n    <span class="lab">Cenário de funding</span>',
        '  <div class="chips">\n'
        '    <span class="lab">Escopo de plantas</span>\n'
        '    <button class="pbtn pl active" data-p="p3">3 plantas (Plantas atuais)</button>\n'
        '    <button class="pbtn pl" data-p="p5">5 plantas (Plantas atuais + Projetos)</button>\n'
        '  </div>\n'
        '  <div class="chips">\n    <span class="lab">Cenário de funding</span>')

    html = html.replace(
        "document.querySelectorAll('.pbtn[data-s]').forEach(b=>b.addEventListener('click',()=>{",
        "document.querySelectorAll('.pbtn[data-p]').forEach(b=>b.addEventListener('click',()=>{\n"
        "  document.querySelectorAll('.pbtn[data-p]').forEach(x=>x.classList.remove('active'));\n"
        "  b.classList.add('active'); plants=b.dataset.p; build();\n"
        "}));\n"
        "document.querySelectorAll('.pbtn[data-s]').forEach(b=>b.addEventListener('click',()=>{", 1)

    # ---------- 7. rótulos dos KPIs de breakeven ----------
    html = html.replace(
        "add('kpi-rose','Mês de breakeven',fmtDate(k.breakeven_month),'caixa acionista ≥ 0');",
        "add('kpi-rose','Mês de breakeven',fmtDate(k.breakeven_month),'FCFE acumulado ≥ 0 em definitivo');")
    html = html.replace(
        "add('kpi-sand','Tempo até breakeven',fmtY(k.time_to_breakeven),'a partir da base');",
        "add('kpi-sand','Tempo até breakeven',fmtY(k.time_to_breakeven),'a partir de jul/2026');")

    # ---------- 8. textos ----------
    html = html.replace(
        'horizonte selecionável (até 2035 ou até 2045)</div>',
        'horizonte selecionável (até 2035 ou até 2045)</div>')
    html = html.replace(
        'Distribuição de gás (GNL/GNC) · sub-projetos PR, BA, RN e Holding · valores em R$ milhões, salvo indicação · Lorinvest — Análise de Investimentos · base do modelo: mai/2026 · horizonte selecionável (até 2035 ou até 2045)',
        'Distribuição de gás (GNL/GNC) · sub-projetos PR, BA, RN e Holding, mais os projetos AR e SAL no escopo de 5 plantas · valores em R$ milhões, salvo indicação · Lorinvest — Análise de Investimentos · base do modelo: jul/2026 · horizonte selecionável (até 2035 ou até 2045)')

    html = html.replace(
        'Fontes &amp; Usos — Use of Proceeds (base mai/2026)',
        'Fontes &amp; Usos — Use of Proceeds (base jul/2026)')

    # Fontes & Usos com os números de 04/set/2026
    html = html.replace('<b>R$ 206,1 mi</b><span>Capital próprio</span>', '<b>%s</b><span>Capital próprio</span>' % mi(fon['Equity']))
    html = html.replace('<b>R$ 284,2 mi</b><span>Dívida líquida</span>', '<b>%s</b><span>Dívida líquida</span>' % mi(fon['Dívida líquida']))
    html = html.replace('<b>R$ 490,3 mi</b><span>Capital Investido</span>', '<b>%s</b><span>Capital Investido</span>' % mi(fon['Fontes']))
    html = html.replace('<b>R$ 321,6 mi</b><span>CapEx</span>', '<b>%s</b><span>CapEx</span>' % mi(uso['CapEx']))
    html = html.replace('<b>R$ 56,8 mi</b><span>Serviço da dívida</span>', '<b>%s</b><span>Serviço da dívida</span>' % mi(uso['Serviço da dívida']))
    html = html.replace('<b>R$ 77,4 mi</b><span>SG&amp;A</span>', '<b>%s</b><span>SG&amp;A</span>' % mi(uso['SG&A Holding']))
    html = html.replace('<b>R$ 34,5 mi</b><span>OpEx e outros</span>', '<b>%s</b><span>OpEx e outros</span>' % mi(uso['OpEx e outros']))
    html = html.replace('<b>R$ 490,3 mi</b><span>Capital utilizado</span>', '<b>%s</b><span>Capital utilizado</span>' % mi(uso['Usos']))

    html = html.replace(
        'Reproduz os workbooks <i>GNLink_Model_2026.07.09</i> (um arquivo por cenário de funding). '
        'Os valores das tabelas e KPIs vêm diretamente das abas Dashboard e Consolidated de cada arquivo.',
        'Reproduz os 16 workbooks <i>GNLink_Model_2026.09.04</i> (um arquivo por combinação de escopo de plantas × cenário de funding × CapEx de manutenção). '
        'Os valores das tabelas e KPIs vêm diretamente das abas Dashboard e Consolidated de cada arquivo. '
        'O <i>mês de breakeven</i> é o primeiro mês a partir do qual o FCFE acumulado não volta a ficar negativo — critério mais restritivo que o do bloco Outputs do modelo, que registra o primeiro cruzamento (que pode ser um pico transitório de captação).')

    html = re.sub(r'<title>.*?</title>',
                  '<title>GNLink · Modelo Financeiro — Endividamento &amp; Alavancagem (04/set/2026)</title>',
                  html, count=1, flags=re.S)

    io.open(DST, 'w', encoding='utf-8').write(html)
    print('gerado', DST, len(html), 'bytes')


if __name__ == '__main__':
    main()
