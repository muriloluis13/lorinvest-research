// Curva de contratos futuros do Brent via Yahoo Finance.
//
// Fonte anterior: Barchart (root 'CB'), abandonada porque o site passou a ficar
// atrás do AWS WAF Bot Control — ver o cabeçalho de lib/yahoo.js.
//
// Aqui a curva é montada enumerando os contratos mensais do Brent Last Day
// Financial na NYMEX (símbolo Yahoo BZ<código do mês><ano>.NYM, ex.: BZX26.NYM
// = novembro/2026) e pedindo o último fechamento de cada um em lotes, via spark.
// Contratos sem negociação são omitidos pelo Yahoo e simplesmente não entram na
// curva. O payload sai já normalizado em {date, value, mes}, formato que o
// parseBarchartFuturoJSON do index.html aceita direto.
import { fetchYahooSparkLast } from '../lib/yahoo.js';
import { getCached, setCached } from '../lib/httpcache.js';

const MONTH_CODES = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'];
const MES_PT = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
const MESES_A_FRENTE = 48; // 4 anos de curva
const TTL = 10 * 60 * 1000;

export const maxDuration = 30;

// Gera os símbolos dos próximos N contratos mensais a partir do mês corrente.
function contractSymbols(root, suffix) {
  const now = new Date();
  const out = [];
  for (let i = 0; i < MESES_A_FRENTE; i++) {
    const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + i, 1));
    const y = d.getUTCFullYear();
    const m = d.getUTCMonth();
    out.push({
      symbol: `${root}${MONTH_CODES[m]}${String(y).slice(-2)}${suffix}`,
      year: y,
      month: m,
    });
  }
  return out;
}

export default async function handler(req, res) {
  try {
    let payload = getCached('brent_futuro', TTL);
    if (!payload) {
      const contracts = contractSymbols('BZ', '.NYM');
      const last = await fetchYahooSparkLast(contracts.map((c) => c.symbol));

      const data = [];
      for (const c of contracts) {
        const p = last.get(c.symbol);
        if (!p || !isFinite(p.value) || p.value <= 0) continue;
        data.push({
          symbol: c.symbol,
          // Meio-dia evita que o new Date() do navegador jogue o contrato para o
          // mês anterior em fusos a oeste de Greenwich (Brasil é UTC-3).
          date: `${c.year}-${String(c.month + 1).padStart(2, '0')}-01T12:00:00`,
          value: p.value,
          mes: `${MES_PT[c.month]} '${String(c.year).slice(-2)}`,
          tradeDate: p.date,
        });
      }
      if (!data.length) throw new Error('Nenhum contrato de Brent retornado pelo Yahoo.');

      payload = {
        source: 'yahoo',
        root: 'BZ',
        total: data.length,
        count: data.length,
        data,
        fetched_at: new Date().toISOString(),
      };
      setCached('brent_futuro', payload);
    }
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 's-maxage=600, stale-while-revalidate=1200');
    return res.status(200).json(payload);
  } catch (e) {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(502).send(String((e && e.message) || e));
  }
}
