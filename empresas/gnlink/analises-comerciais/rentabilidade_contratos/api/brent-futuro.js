// Curva de contratos futuros do Brent (root 'CB') via Barchart.
// Substitui /barchart-brent-futuro do proxy_anp.py. TTL de 5 min (preços intraday).
import { fetchBarchartFutures } from '../lib/barchart.js';
import { getCached, setCached } from '../lib/httpcache.js';

const PAGE_URL = 'https://www.barchart.com/futures/quotes/CB*0/futures-prices?page=all';
const TTL = 5 * 60 * 1000;

export const maxDuration = 30;

export default async function handler(req, res) {
  try {
    let payload = getCached('brent_futuro', TTL);
    if (!payload) {
      payload = await fetchBarchartFutures('CB', PAGE_URL);
      setCached('brent_futuro', payload);
    }
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=600');
    return res.status(200).json(payload);
  } catch (e) {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(502).send(String((e && e.message) || e));
  }
}
