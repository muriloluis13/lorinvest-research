// Curva de contratos futuros do JKM (GNL asiático, root 'JKM') via Barchart.
// Substitui /barchart-jkm-futuro do proxy_anp.py. TTL de 5 min.
import { fetchBarchartFutures } from '../lib/barchart.js';
import { getCached, setCached } from '../lib/httpcache.js';

const PAGE_URL = 'https://www.barchart.com/futures/quotes/JKM*1/futures-prices';
const TTL = 5 * 60 * 1000;

export const maxDuration = 30;

export default async function handler(req, res) {
  try {
    let payload = getCached('jkm_futuro', TTL);
    if (!payload) {
      payload = await fetchBarchartFutures('JKM', PAGE_URL);
      setCached('jkm_futuro', payload);
    }
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=600');
    return res.status(200).json(payload);
  } catch (e) {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(502).send(String((e && e.message) || e));
  }
}
