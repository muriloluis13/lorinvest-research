// Estrutura a Termo das Taxas de Juros (ETTJ) da ANBIMA — curva de juros diária.
// Fonte: sistema legado est-termo. O "Consultar" da tela pública só encaminha para
// CZ-down.asp, que aceita POST com Dt_Ref (dd/mm/aaaa), saida (csv) e Idioma (PT).
// A ANBIMA só mantém os últimos ~5 dias úteis, então varremos para trás até achar
// um pregão com dado. Resposta em ISO-8859-1; datas sem pregão vêm vazias.
import { getCached, setCached } from '../lib/httpcache.js';

const ENDPOINT = 'https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp';
const TTL = 30 * 60 * 1000; // 30 min — dado é de fechamento, muda 1x/dia
const MAX_LOOKBACK = 8; // dias corridos para trás (cobre feriado + fim de semana)

export const maxDuration = 30;

function pad(n) { return String(n).padStart(2, '0'); }
function fmtBR(d) { return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear(); }
function toISO(br) { const [d, m, y] = br.split('/'); return y + '-' + m + '-' + d; }

// Decimal por vírgula, milhar por ponto (só nos vértices inteiros). Notação
// científica (E-02) usa vírgula como decimal. Remover pontos e trocar vírgula
// por ponto cobre todos os casos.
function num(s) {
  s = String(s || '').trim();
  if (!s) return null;
  const v = parseFloat(s.replace(/\./g, '').replace(',', '.'));
  return Number.isFinite(v) ? v : null;
}

async function fetchDate(brDate) {
  const body = new URLSearchParams({ Idioma: 'PT', Dt_Ref: brDate, saida: 'csv' });
  const r = await fetch(ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
    },
    body,
  });
  if (!r.ok) throw new Error('ANBIMA HTTP ' + r.status);
  const buf = Buffer.from(await r.arrayBuffer());
  return buf.toString('latin1'); // ISO-8859-1
}

// Estrutura do CSV:
//   linha 1:  DD/MM/AAAA;Beta 1;Beta 2;Beta 3;Beta 4;Lambda 1;Lambda 2
//   linha 2:  PREFIXADOS;<6 params>
//   linha 3:  IPCA;<6 params>
//   (linha em branco)
//   ETTJ Inflação Implicita (IPCA)
//   Vertices;ETTJ IPCA;ETTJ PREF;Inflação Implícita
//   126;8,4755;13,9065;5,0066  ...
function parse(text) {
  const lines = text.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  if (!lines.some((l) => /^Vertices;/i.test(l))) return null;

  const params = {};
  const paramKeys = ['beta1', 'beta2', 'beta3', 'beta4', 'lambda1', 'lambda2'];
  for (const l of lines) {
    const m = /^(PREFIXADOS|IPCA);(.+)$/.exec(l);
    if (!m) continue;
    const vals = m[2].split(';').map(num);
    params[m[1] === 'PREFIXADOS' ? 'pre' : 'ipca'] = Object.fromEntries(
      paramKeys.map((k, i) => [k, vals[i]])
    );
  }

  const start = lines.findIndex((l) => /^Vertices;/i.test(l)) + 1;
  const curve = [];
  for (let i = start; i < lines.length; i++) {
    const c = lines[i].split(';');
    const vertice = num(c[0]);
    if (vertice == null) continue;
    curve.push({
      vertice,                         // prazo em dias corridos
      anos: +(vertice / 252).toFixed(2), // aproximação em anos úteis
      ipca: num(c[1]),                 // juro real (NTN-B / IPCA+), % a.a.
      pre: num(c[2]),                  // juro nominal pré-fixado (DI/LTN), % a.a.
      implicita: num(c[3]),            // inflação implícita (breakeven), % a.a.
    });
  }
  if (!curve.length) return null;
  return { params, curve };
}

export default async function handler(req, res) {
  try {
    const asked = (req.query && (req.query.date || req.query.dt)) || null;
    const cacheKey = 'anbima_ettj_' + (asked || 'latest');

    let payload = getCached(cacheKey, TTL);
    if (!payload) {
      const candidates = [];
      if (asked) {
        candidates.push(asked); // dd/mm/aaaa explícito
      } else {
        const base = new Date();
        for (let i = 0; i < MAX_LOOKBACK; i++) {
          const d = new Date(base);
          d.setDate(base.getDate() - i);
          const wd = d.getDay();
          if (wd === 0 || wd === 6) continue; // pula sáb/dom
          candidates.push(fmtBR(d));
        }
      }

      let parsed = null, usedDate = null;
      for (const br of candidates) {
        const text = await fetchDate(br);
        const p = parse(text);
        if (p) { parsed = p; usedDate = br; break; }
      }
      if (!parsed) throw new Error('Sem dado de ETTJ nos últimos dias úteis');

      payload = {
        date: usedDate,
        dateISO: toISO(usedDate),
        source: 'ANBIMA — Estrutura a Termo das Taxas de Juros (ETTJ)',
        params: parsed.params,
        curve: parsed.curve,
      };
      setCached(cacheKey, payload);
    }

    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 's-maxage=1800, stale-while-revalidate=3600');
    return res.status(200).json(payload);
  } catch (e) {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(502).send(String((e && e.message) || e));
  }
}
