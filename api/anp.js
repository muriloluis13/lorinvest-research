// Planilha mensal de preços de combustíveis da ANP (por estado, desde 2013).
// Substitui o endpoint /anp.xlsx do proxy_anp.py. Dado é mensal, então cacheamos
// por 6h em memória para não rebaixar ~2,8 MB a cada acesso.
import { getCached, setCached } from '../lib/httpcache.js';

const ANP_URL =
  'https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia' +
  '/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/mensal' +
  '/mensal-estados-desde-jan2013.xlsx';

const TTL = 6 * 60 * 60 * 1000; // 6 horas

// Download da planilha pode passar do timeout padrão de 10s no plano Hobby.
export const maxDuration = 30;

export default async function handler(req, res) {
  try {
    let buf = getCached('anp', TTL);
    if (!buf) {
      const r = await fetch(ANP_URL, {
        headers: {
          'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
          Accept: '*/*',
        },
      });
      if (!r.ok) throw new Error('ANP HTTP ' + r.status);
      buf = Buffer.from(await r.arrayBuffer());
      setCached('anp', buf);
    }
    res.setHeader(
      'Content-Type',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    );
    res.setHeader('Cache-Control', 's-maxage=21600, stale-while-revalidate=86400');
    return res.status(200).send(buf);
  } catch (e) {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(502).send(String((e && e.message) || e));
  }
}
