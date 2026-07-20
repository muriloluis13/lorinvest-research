// Helpers de scraping do Barchart, portados de proxy_anp.py para Node (fetch/undici).
// Fluxo de 2 etapas para contornar a tabela renderizada via JS:
//   1) GET na página de quotes -> captura o cookie XSRF-TOKEN (+ demais cookies de sessão)
//   2) chamada à API interna enviando o token no header X-XSRF-TOKEN e reenviando os cookies
// A `fetch` do Node (undici) já descomprime gzip/br/deflate automaticamente, desde que
// NÃO fixemos o header Accept-Encoding manualmente — por isso ele é omitido aqui.

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
  'AppleWebKit/537.36 (KHTML, like Gecko) ' +
  'Chrome/120.0.0.0 Safari/537.36';

const FIELDS = [
  'symbol', 'contractSymbol', 'contractName', 'contractNameHistorical',
  'lastPrice', 'priceChange', 'percentChange', 'bidPrice', 'askPrice',
  'volume', 'openInterest', 'previous', 'open', 'high', 'low',
  'tradeTime', 'contractExpirationDate', 'symbolCode', 'symbolType',
].join(',');

const API_BASE = 'https://www.barchart.com/proxies/core-api/v1/quotes/get';
const TIMESERIES_URL = 'https://www.barchart.com/proxies/timeseries/queryeod.ashx';

// Etapa 1: abre a página para obter os cookies de sessão e o token XSRF decodificado.
async function getSession(pageUrl) {
  const res = await fetch(pageUrl, {
    headers: {
      'User-Agent': UA,
      Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8',
      Referer: 'https://www.barchart.com/',
      'Upgrade-Insecure-Requests': '1',
    },
  });
  await res.arrayBuffer(); // drena o corpo; só interessam os cookies

  const setCookies =
    typeof res.headers.getSetCookie === 'function'
      ? res.headers.getSetCookie()
      : (res.headers.get('set-cookie') ? [res.headers.get('set-cookie')] : []);

  let token = null;
  for (const c of setCookies) {
    const m = /^XSRF-TOKEN=([^;]+)/.exec(c);
    if (m) { token = decodeURIComponent(m[1]); break; }
  }
  if (!token) throw new Error('Cookie XSRF-TOKEN não recebido do Barchart.');

  // Reenvia TODOS os cookies (laravel_session etc.) na etapa 2, como faz o CookieJar do Python.
  const cookieHeader = setCookies.map((c) => c.split(';')[0]).join('; ');
  return { token, cookieHeader };
}

// Curva de contratos futuros (Brent 'CB', JKM 'JKM', ...). Retorno espelha o do proxy Python.
export async function fetchBarchartFutures(root, pageUrl) {
  const { token, cookieHeader } = await getSession(pageUrl);

  const all = [];
  let total = null;
  let page = 1;
  const limit = 200;

  while (true) {
    const params = new URLSearchParams({
      lists: 'futures.contractInRoot',
      root,
      fields: FIELDS,
      orderBy: 'contractExpirationDate',
      orderDir: 'asc',
      meta: 'field.shortName,field.type,field.description',
      hasOptions: 'true',
      page: String(page),
      limit: String(limit),
      raw: '1',
    });
    const res = await fetch(API_BASE + '?' + params.toString(), {
      headers: {
        'User-Agent': UA,
        Accept: 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        Referer: pageUrl,
        'X-XSRF-TOKEN': token,
        'X-Requested-With': 'XMLHttpRequest',
        Cookie: cookieHeader,
      },
    });
    if (!res.ok) throw new Error('Barchart core-api HTTP ' + res.status);
    const j = await res.json();

    const items = j.data || [];
    all.push(...items);
    total = j.total != null ? j.total : all.length;

    if (all.length >= total || !items.length) break;
    page += 1;
    if (page > 20) break; // salvaguarda contra loop infinito
  }

  return {
    total: total != null ? total : all.length,
    count: all.length,
    data: all,
    fetched_at: new Date().toISOString(),
  };
}

// Histórico end-of-day (CSV: symbol,date,open,high,low,close,volume,openinterest).
export async function fetchBarchartEod(symbol, pageUrl) {
  const { token, cookieHeader } = await getSession(pageUrl);

  const params = new URLSearchParams({
    symbol,
    data: 'daily',
    maxrecords: '20000',
    volume: 'contract',
    order: 'asc',
    dividends: 'false',
    backadjust: 'false',
    daystoexpiration: '1',
    contractroll: 'expiration',
  });
  const res = await fetch(TIMESERIES_URL + '?' + params.toString(), {
    headers: {
      'User-Agent': UA,
      Accept: 'text/plain,*/*',
      'Accept-Language': 'en-US,en;q=0.9',
      Referer: pageUrl,
      'X-XSRF-TOKEN': token,
      'X-Requested-With': 'XMLHttpRequest',
      Cookie: cookieHeader,
    },
  });
  if (!res.ok) throw new Error('Barchart timeseries HTTP ' + res.status);
  const body = await res.text();

  const points = [];
  for (const line of body.split('\n')) {
    const l = line.trim();
    if (!l) continue;
    const parts = l.split(',');
    if (parts.length < 6) continue;
    const date = parts[1].trim();
    const close = parseFloat(parts[5]);
    if (!isFinite(close) || close <= 0) continue;
    points.push({ date, value: close });
  }
  if (!points.length) throw new Error('Nenhum ponto retornado pelo timeseries para ' + symbol);
  points.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));
  return points;
}
