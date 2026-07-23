// Cotação mais recente da ação da Compass (PASS3.SA) via Yahoo Finance v8 chart API.
// Versão AUTOSSUFICIENTE (cache inline) para quando esta pasta é o Root Directory de
// um projeto Vercel dedicado à análise da Compass. Espelha /api/pass3 da raiz do repo.
// Retorna { symbol, currency, price, previousClose, marketTime, fetched_at }.

const YAHOO = 'https://query1.finance.yahoo.com/v8/finance/chart/PASS3.SA';
const TTL = 5 * 60 * 1000; // 5 min

// Cache simples em memória de módulo (sobrevive entre invocações "quentes").
const _cache = new Map();
function getCached(key, ttlMs) {
  const e = _cache.get(key);
  if (e && Date.now() - e.t < ttlMs) return e.v;
  return null;
}
function setCached(key, value) { _cache.set(key, { t: Date.now(), v: value }); }

export const maxDuration = 30;

export default async function handler(req, res) {
  try {
    const key = 'pass3_last';
    let payload = getCached(key, TTL);
    if (!payload) {
      const url = `${YAHOO}?range=5d&interval=1d&includePrePost=false`;
      const r = await fetch(url, {
        headers: {
          'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          Accept: 'application/json,*/*',
          'Accept-Language': 'en-US,en;q=0.9',
        },
      });
      if (!r.ok) throw new Error('Yahoo HTTP ' + r.status);
      const j = await r.json();
      const chart = j.chart || {};
      if (chart.error) throw new Error('Yahoo retornou erro: ' + JSON.stringify(chart.error));
      const r0 = (chart.result || [])[0];
      if (!r0) throw new Error('Yahoo retornou resultado vazio.');
      const meta = r0.meta || {};

      let price = meta.regularMarketPrice;
      const closes = (((r0.indicators || {}).quote || [{}])[0] || {}).close || [];
      let lastClose = null;
      for (let i = closes.length - 1; i >= 0; i--) {
        if (closes[i] != null) { lastClose = closes[i]; break; }
      }
      if (price == null) price = lastClose;
      if (price == null) throw new Error('Yahoo não retornou preço.');

      payload = {
        symbol: meta.symbol || 'PASS3.SA',
        currency: meta.currency || 'BRL',
        price,
        previousClose: meta.chartPreviousClose ?? lastClose ?? null,
        marketTime: meta.regularMarketTime ? new Date(meta.regularMarketTime * 1000).toISOString() : null,
        marketState: meta.marketState || null,
        fetched_at: new Date().toISOString(),
      };
      setCached(key, payload);
    }
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=600');
    return res.status(200).json(payload);
  } catch (e) {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(502).send(String((e && e.message) || e));
  }
}
