// Histórico diário do JKM (GNL asiático, contrato perpetual 'JKM*1') via Barchart timeseries.
// Substitui /barchart-jkm-historical do proxy_anp.py. Aceita ?start=YYYY-MM-DD&end=YYYY-MM-DD.
import { fetchBarchartEod } from '../lib/barchart.js';
import { getCached, setCached } from '../lib/httpcache.js';

const PAGE_URL = 'https://www.barchart.com/futures/quotes/JKM*1/price-history/historical';
const TTL = 5 * 60 * 1000;

export const maxDuration = 30;

export default async function handler(req, res) {
  try {
    const q = req.query || {};
    const start = q.start || null;
    const end = q.end || null;
    const key = `jkm_hist_${start}_${end}`;

    let payload = getCached(key, TTL);
    if (!payload) {
      let points = await fetchBarchartEod('JKM*1', PAGE_URL);
      if (start) points = points.filter((p) => p.date >= start);
      if (end) points = points.filter((p) => p.date <= end);
      payload = {
        symbol: 'JKM*1',
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
