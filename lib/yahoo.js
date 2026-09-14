// Helpers do Yahoo Finance usados como fonte de preços de Brent e JKM.
//
// Por que Yahoo e não Barchart: desde set/2026 o Barchart passou a servir TODO o
// site atrás do AWS WAF Bot Control (CloudFront devolve HTTP 202 com o header
// `x-amzn-waf-action: challenge` e um desafio JavaScript no corpo, em vez da
// página). Sem executar esse desafio não há cookie XSRF-TOKEN, e as APIs internas
// (`core-api` e `queryeod.ashx`) respondem 403. O scraping de 2 etapas que
// alimentava esses cards ficou inviável, então as séries vêm do Yahoo.
//
// Dois endpoints públicos são usados:
//   - v8/finance/chart/<symbol>  -> série diária completa de um símbolo
//   - v7/finance/spark?symbols=  -> último fechamento de VÁRIOS símbolos num só
//     request (usado para montar a curva de futuros sem disparar 1 request por
//     contrato). O limite prático é ~20 símbolos por chamada; acima disso o Yahoo
//     responde 400.

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
  'AppleWebKit/537.36 (KHTML, like Gecko) ' +
  'Chrome/120.0.0.0 Safari/537.36';

const CHART_BASE = 'https://query1.finance.yahoo.com/v8/finance/chart/';
const SPARK_BASE = 'https://query1.finance.yahoo.com/v7/finance/spark';

export const SPARK_BATCH = 20;

async function yahooJson(url) {
  const res = await fetch(url, {
    headers: {
      'User-Agent': UA,
      Accept: 'application/json,*/*',
      'Accept-Language': 'en-US,en;q=0.9',
    },
  });
  if (!res.ok) throw new Error('Yahoo HTTP ' + res.status);
  return res.json();
}

// Extrai [{date:'YYYY-MM-DD', value:<close>}] de um resultado do chart/spark.
function pointsFromResult(r0) {
  const timestamps = r0.timestamp || [];
  const closes = (((r0.indicators || {}).quote || [{}])[0] || {}).close || [];
  const points = [];
  for (let i = 0; i < timestamps.length; i++) {
    const close = closes[i];
    if (close == null) continue;
    const date = new Date(timestamps[i] * 1000).toISOString().slice(0, 10);
    points.push({ date, value: close });
  }
  return points;
}

// Série diária de um símbolo. `period1`/`period2` em segundos (epoch UTC).
export async function fetchYahooDaily(symbol, period1, period2) {
  const url =
    CHART_BASE + encodeURIComponent(symbol) +
    `?period1=${period1}&period2=${period2}&interval=1d`;
  const j = await yahooJson(url);
  const chart = j.chart || {};
  if (chart.error) throw new Error('Yahoo retornou erro: ' + JSON.stringify(chart.error));
  const r0 = (chart.result || [])[0];
  if (!r0) throw new Error('Yahoo retornou resultado vazio para ' + symbol);
  const points = pointsFromResult(r0);
  if (!points.length) throw new Error('Nenhum ponto retornado pelo Yahoo para ' + symbol);
  points.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));
  return { points, meta: r0.meta || {} };
}

// Último fechamento de vários símbolos. Devolve um Map symbol -> {value, date}.
// Símbolos inexistentes simplesmente não aparecem no Map (o Yahoo os omite), e um
// lote que falhe inteiro é ignorado em vez de derrubar a curva toda.
export async function fetchYahooSparkLast(symbols, range = '5d') {
  const out = new Map();
  for (let i = 0; i < symbols.length; i += SPARK_BATCH) {
    const batch = symbols.slice(i, i + SPARK_BATCH);
    let results;
    try {
      const j = await yahooJson(
        `${SPARK_BASE}?symbols=${batch.map(encodeURIComponent).join(',')}` +
        `&range=${range}&interval=1d`
      );
      results = ((j.spark || {}).result) || [];
    } catch (_) {
      continue; // lote indisponível: segue com os demais
    }
    for (const r of results) {
      const r0 = (r.response || [])[0];
      if (!r0) continue;
      const points = pointsFromResult(r0);
      if (!points.length) continue;
      out.set(r.symbol, points[points.length - 1]);
    }
  }
  return out;
}
