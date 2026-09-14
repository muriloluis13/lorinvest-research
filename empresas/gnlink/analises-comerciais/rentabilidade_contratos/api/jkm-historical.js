// Histórico diário do JKM (marcador de GNL Japão/Coreia) via Yahoo Finance.
//
// Fonte anterior: Barchart timeseries do contrato perpétuo 'JKM*1', abandonada
// porque o site passou a ficar atrás do AWS WAF Bot Control — ver o cabeçalho de
// lib/yahoo.js. O símbolo JKM=F do Yahoo é o mesmo marcador (série validada
// contra os extremos conhecidos: pico de US$ 69,96 em 25/08/2022 e mínima de
// US$ 2,00 em 27/04/2020) e cobre desde 29/07/2014 — histórico mais longo que o
// que vinha do Barchart.
//
// Aceita ?start=YYYY-MM-DD&end=YYYY-MM-DD.
import { fetchYahooDaily } from '../lib/yahoo.js';
import { getCached, setCached } from '../lib/httpcache.js';

const SYMBOL = 'JKM=F';
const TTL = 5 * 60 * 1000;
const DEFAULT_START = 1406592000; // 2014-07-29 UTC (primeiro pregão da série)

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
    const start = q.start || null;
    const end = q.end || null;
    const key = `jkm_hist_${start}_${end}`;

    let payload = getCached(key, TTL);
    if (!payload) {
      const period1 = toTs(start, DEFAULT_START);
      const period2 = toTs(end, Math.floor(Date.now() / 1000));
      const { points, meta } = await fetchYahooDaily(SYMBOL, period1, period2);

      // O Yahoo já respeita period1/period2, mas o filtro por string garante o
      // recorte exato nas bordas (o intervalo vem em fuso do pregão).
      let data = points;
      if (start) data = data.filter((p) => p.date >= start);
      if (end) data = data.filter((p) => p.date <= end);

      payload = {
        source: 'yahoo',
        symbol: meta.symbol || SYMBOL,
        currency: meta.currency || 'USD',
        count: data.length,
        data,
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
