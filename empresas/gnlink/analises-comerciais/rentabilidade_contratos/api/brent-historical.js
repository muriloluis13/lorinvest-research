// Histórico diário do Brent (BZ=F) via Yahoo Finance v8 chart API.
// Substitui /yahoo-brent-historical do proxy_anp.py. Aceita ?start=YYYY-MM-DD&end=YYYY-MM-DD.
import { getCached, setCached } from '../lib/httpcache.js';

const YAHOO = 'https://query1.finance.yahoo.com/v8/finance/chart/BZ=F';
const TTL = 5 * 60 * 1000;
const DEFAULT_START = 1185768000; // 2007-07-30 UTC

export const maxDuration = 30;

function toTs(s, fallback) {
  if (!s) return fallback;
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
  if (!m) return fallback;
  return Math.floor(Date.UTC(+m[1], +m[2] - 1, +m[3]) / 1000);
}

export default async function handler(req, res) {
  try {
    const q = req.query || {};
    const period1 = toTs(q.start, DEFAULT_START);
    const period2 = toTs(q.end, Math.floor(Date.now() / 1000));
    const key = `brent_hist_${period1}_${period2}`;

    let payload = getCached(key, TTL);
    if (!payload) {
      const url = `${YAHOO}?period1=${period1}&period2=${period2}&interval=1d`;
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

      const timestamps = r0.timestamp || [];
      const closes = (((r0.indicators || {}).quote || [{}])[0] || {}).close || [];
      const points = [];
      for (let i = 0; i < timestamps.length; i++) {
        const close = closes[i];
        if (close == null) continue;
        const date = new Date(timestamps[i] * 1000).toISOString().slice(0, 10);
        points.push({ date, value: close });
      }

      payload = {
        symbol: (r0.meta && r0.meta.symbol) || 'BZ=F',
        currency: r0.meta && r0.meta.currency,
        period1,
        period2,
        count: points.length,
        data: points,
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
