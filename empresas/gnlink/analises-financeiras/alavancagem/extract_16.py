# -*- coding: utf-8 -*-
"""Extrai os 16 workbooks GNLink_Model_2026.09.04 para o JSON do dashboard de alavancagem."""
import openpyxl, json, glob, os, re, datetime

PLANTS = ['PR', 'BA', 'RN', 'AR', 'SAL']
Y0, Y1 = 2026, 2045


def matrix(ws, maxcol=None):
    mc = maxcol or ws.max_column
    return [list(r) for r in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=mc, values_only=True)]


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


class Sheet:
    def __init__(self, ws, maxcol=None):
        self.M = matrix(ws, maxcol)

    def lab(self, i):
        v = self.M[i - 1][1] if 0 < i <= len(self.M) else None
        return str(v) if v is not None else None

    def find(self, name, after=1):
        for i in range(after, len(self.M) + 1):
            if self.lab(i) == name:
                return i
        return None

    def find_all(self, pred):
        return [i for i in range(1, len(self.M) + 1) if pred(self.lab(i) or '')]

    def cell(self, row, col):
        try:
            return self.M[row - 1][col - 1]
        except (IndexError, TypeError):
            return None

    def row(self, r):
        return self.M[r - 1] if r and r - 1 < len(self.M) else []


def _flag_row(dsh):
    """Linha dos flags Y/N de projeto ativo: a de cima do cabeçalho PR|BA|RN|... do Dashboard."""
    for r in range(1, 60):
        if str(dsh.cell(r, 4) or '') == 'PR' and str(dsh.cell(r, 2) or '') == 'Outputs':
            return r - 1
    return 36


def annual_block(sh):
    hdr = sh.find('Financials | Annual')
    colof = {}
    for c, v in enumerate(sh.row(hdr), 1):
        if isinstance(v, int) and 2000 < v < 2100:
            colof[v] = c
    return hdr, colof


def series(sh, hdr, colof, label, scale=1.0):
    r = sh.find(label, after=hdr)
    if r is None:
        return [None] * (Y1 - Y0 + 1)
    row = sh.row(r)
    out = []
    for y in range(Y0, Y1 + 1):
        c = colof.get(y)
        v = num(row[c - 1]) if c and c - 1 < len(row) else None
        out.append(None if v is None else v * scale)
    return out


def extract(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    con = Sheet(wb['Consolidated'])
    hdr, colof = annual_block(con)

    S = {}
    S['gas_price'] = series(con, hdr, colof, 'Gas Price')
    S['ebitda'] = series(con, hdr, colof, 'EBITDA')
    S['ebitda_mg'] = series(con, hdr, colof, 'EBITDA Mg')
    S['net_income'] = series(con, hdr, colof, 'Net Income')
    S['net_mg'] = series(con, hdr, colof, 'Net Mg')
    S['fcff'] = series(con, hdr, colof, 'FCFF')
    S['fcfe'] = series(con, hdr, colof, 'FCFE')
    S['equity_issue'] = series(con, hdr, colof, 'Equity issue')
    S['dividends'] = series(con, hdr, colof, 'Dividends')
    S['eop_cash'] = series(con, hdr, colof, 'EoP Cash')
    S['eop_debt'] = series(con, hdr, colof, 'EoP Debt')
    S['principal'] = series(con, hdr, colof, 'Principal')
    S['interest'] = series(con, hdr, colof, 'Interest')
    S['net_debt_ebitda'] = series(con, hdr, colof, 'Net Debt/EBITDA')
    eq_cap = series(con, hdr, colof, 'Equity Capital')
    prof_re = series(con, hdr, colof, 'Profit Reserves')

    acc, accum = 0.0, []
    for v in S['fcfe']:
        acc += (v or 0.0)
        accum.append(acc)
    S['fcfe_accum_annual'] = accum

    # Flags Y/N de projeto ativo (D..H = PR, BA, RN, AR, SAL). As abas AR e SAL continuam
    # calculando mesmo quando o projeto está desligado — quem manda é o flag do Dashboard.
    dsh0 = Sheet(wb['Dashboard'], 12)
    frow = _flag_row(dsh0)
    active = [p for i, p in enumerate(PLANTS) if str(dsh0.cell(frow, 4 + i)) == 'Y']

    for p in PLANTS:
        ps = Sheet(wb[p])
        ph, pc = annual_block(ps)
        on = p in active
        S['vol_' + p.lower()] = series(ps, ph, pc, 'Total Volume', 1 / 1000.0) if on else [0.0] * (Y1 - Y0 + 1)
        S['rev_' + p.lower()] = series(ps, ph, pc, 'Net Revenues') if on else [0.0] * (Y1 - Y0 + 1)

    # conferência: receita consolidada = soma das plantas ativas
    con_rev = series(con, hdr, colof, 'Net Revenues')
    chk = []
    for i in range(len(con_rev)):
        tot = sum((S['rev_' + p.lower()][i] or 0) for p in PLANTS)
        ref = con_rev[i] or 0
        if abs(tot - ref) > max(0.5, abs(ref) * 0.01):
            chk.append((Y0 + i, round(ref, 1), round(tot, 1)))

    # ---------------- KPIs: bloco Outputs do Dashboard (saída do próprio modelo) ----------------
    dsh = Sheet(wb['Dashboard'], 12)

    def dlab(name, col=4, after=1):
        r = dsh.find(name, after=after)
        return num(dsh.cell(r, col)) if r else None

    def dside(name):
        """KPIs da coluna direita do bloco Outputs: rótulo em F, valor em H."""
        for r in range(1, 40):
            if str(dsh.cell(r, 6) or '') == name:
                return num(dsh.cell(r, 8))
        return None

    ev = dlab('Enterprise Value')
    lev = dlab('Nominal IRR')                       # None quando o modelo devolve "n/a"
    eq_dur = dlab('Equity Duration')
    equity_needs = dlab('Equity needs')
    debt_dur = dside('Debt Duration')
    debt_irr = dside('Debt IRR')
    max_debt = dside('Max Debt')
    avg_nde = dside('Avg. ND/EBITDA')

    # Breakeven definitivo: último mês em que o FCFE acumulado ainda é negativo.
    # (O modelo reporta o PRIMEIRO cruzamento, que pode ser um pico transitório de
    #  captação de dívida; aqui interessa o ponto a partir do qual não volta mais.)
    months = con.row(con.find('Month'))
    status = con.row(con.find('Status'))
    accm = con.row(con.find('FCFE Accum. All Projects'))
    base_i = next((i for i, s in enumerate(status) if str(s) == 'Forecast'), None)
    last_neg = None
    for i in range(base_i or 0, len(accm)):
        v = num(accm[i])
        if v is not None and isinstance(months[i], datetime.datetime) and v < 0:
            last_neg = i
    bk_i = (last_neg + 1) if (last_neg is not None and last_neg + 1 < len(months)
                              and isinstance(months[last_neg + 1], datetime.datetime)) else None
    bk_month = months[bk_i] if bk_i is not None else None
    ttb = ((bk_i - base_i) / 12.0) if (bk_i is not None and base_i is not None) else None

    n10 = 2035 - Y0 + 1
    i2035 = 2035 - Y0

    kpi = dict(
        ev=ev,
        equity_needs=equity_needs,
        max_debt=max_debt,
        avg_nd_ebitda=avg_nde,
        debt_irr=debt_irr,
        breakeven_month=(bk_month.isoformat() if isinstance(bk_month, datetime.datetime) else None),
        time_to_breakeven=ttb,
        equity_duration=eq_dur,
        debt_duration=debt_dur,
        levered_irr=lev,
        first_pos_fcfe=next((Y0 + i for i, v in enumerate(S['fcfe']) if v is not None and v > 0), None),
        sc2035_equity_capital=eq_cap[i2035],
        sc2035_profit_reserves=prof_re[i2035],
        sc2035_total=(eq_cap[i2035] or 0) + (prof_re[i2035] or 0),
    )

    kpi['active_plants'] = [p.lower() for p in active]

    # switches do cenário, para auditoria
    kpi['_rev_check'] = chk
    kpi['_switches'] = dict(
        min_cash_debt=str(dsh.cell(dsh.find_all(lambda s: s.startswith('Use debt to fund min'))[0], 3)),
        maint_capex=str(dsh.cell(dsh.find('Maintenance CapEx?'), 3)),
        base=str(dsh.cell(dsh.find('Model database'), 3))[:10],
        plants=''.join(str(dsh.cell(_flag_row(dsh), c))[:1] for c in range(4, 11)),
    )
    r_ev = con.find('Enterprise Value')

    # ------------- Fontes & Usos (bloco Outputs) -------------
    uop = {'fontes': [], 'usos': []}
    for r in range(r_ev - 4, r_ev + 12):
        ql, qv = con.cell(r, 17), num(con.cell(r, 18))
        tl, tv = con.cell(r, 20), num(con.cell(r, 21))
        if ql and qv is not None:
            uop['fontes'].append([str(ql), qv])
        if tl and tv is not None:
            uop['usos'].append([str(tl), tv])

    wb.close()
    return {'kpi': kpi, 'series_full': S, 'uop': uop}


FUND = {'Equity': 'equity', 'DI+2,5%': 'di25', 'DI': 'di100', 'IPCA+4,5%': 'ipca45'}


def parse(name):
    m = re.match(r'GNLink_Model_2026\.09\.04 (\d) plantas (.+?) CapExM (ON|OFF)\.xlsx$', name)
    return 'p' + m.group(1), FUND[m.group(2)], m.group(3).lower()


def main():
    out = {}
    files = sorted(glob.glob('GNLink_Model_2026.09.04 *.xlsx'))
    assert len(files) == 16, files
    for f in files:
        p, fu, cx = parse(os.path.basename(f))
        print('...', os.path.basename(f), flush=True)
        d = extract(f)
        out.setdefault(p, {}).setdefault(fu, {'years_full': list(range(Y0, Y1 + 1))})[cx] = d
    with open('_data_2026-09-04.json', 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('ok', {k: sorted(v) for k, v in out.items()})


if __name__ == '__main__':
    main()
