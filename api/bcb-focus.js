// Expectativas de mercado do Focus (BCB) via API Olinda — medianas anuais.
// Substitui a raspagem do PDF semanal: a mesma base que alimenta o relatório
// está no OData ExpectativasMercadoAnuais (baseCalculo 0 = agregado 30 dias).
// Puxamos IPCA, PIB, Câmbio, Selic e IGP-M para o ano corrente + 3 seguintes,
// pegando a mediana mais recente ("hoje") e a de ~1 semana antes (comparativo).
import { getCached, setCached } from '../lib/httpcache.js';

const ODATA =
  'https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais';
const TTL = 60 * 60 * 1000; // 1h — Focus roda 1x/dia útil de manhã
export const maxDuration = 30;

// Ordem de exibição + nome exato do Indicador na API.
const INDICADORES = [
  { key: 'ipca',   api: 'IPCA',      label: 'IPCA (%)' },
  { key: 'pib',    api: 'PIB Total', label: 'PIB (%)' },
  { key: 'cambio', api: 'Câmbio',    label: 'Câmbio (R$/US$)' },
  { key: 'selic',  api: 'Selic',     label: 'Selic (% a.a.)' },
  { key: 'igpm',   api: 'IGP-M',     label: 'IGP-M (%)' },
];

function round2(v) { return v == null ? null : Math.round(v * 100) / 100; }
function minusDays(iso, n) {
  const d = new Date(iso + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() - n);
  return d.toISOString().slice(0, 10);
}

export default async function handler(req, res) {
  try {
    let payload = getCached('bcb_focus', TTL);
    if (!payload) {
      const nowY = new Date().getFullYear();
      const years = [nowY, nowY + 1, nowY + 2, nowY + 3].map(String);

      const indFilter = INDICADORES.map((i) => `Indicador eq '${i.api}'`).join(' or ');
      const yrFilter = years.map((y) => `DataReferencia eq '${y}'`).join(' or ');
      const desde = minusDays(new Date().toISOString().slice(0, 10), 25); // janela p/ o comparativo
      const filter =
        `(${indFilter}) and (${yrFilter}) and baseCalculo eq 0 and Data ge '${desde}'`;

      const url =
        ODATA +
        '?$format=json&$orderby=Data desc&$top=4000' +
        '&$select=Indicador,DataReferencia,Data,Mediana' +
        '&$filter=' + encodeURIComponent(filter);

      const r = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0', Accept: 'application/json' },
      });
      if (!r.ok) throw new Error('Olinda HTTP ' + r.status);
      const rows = (await r.json()).value || [];
      if (!rows.length) throw new Error('Sem dados do Focus');

      // Agrupa por indicador+ano, já em ordem decrescente de Data.
      const byInd = {};
      let latest = '';
      for (const row of rows) {
        if (row.Data > latest) latest = row.Data;
        const apiToKey = INDICADORES.find((i) => i.api === row.Indicador);
        if (!apiToKey) continue;
        const g = (byInd[apiToKey.key] = byInd[apiToKey.key] || {});
        (g[row.DataReferencia] = g[row.DataReferencia] || []).push(row);
      }

      const indicators = INDICADORES.map((ind) => {
        const g = byInd[ind.key] || {};
        const values = {};
        for (const y of years) {
          const arr = (g[y] || []).sort((a, b) => (a.Data < b.Data ? 1 : -1));
          if (!arr.length) { values[y] = null; continue; }
          const hoje = arr[0];
          const corte = minusDays(hoje.Data, 6);
          const ant = arr.find((x) => x.Data <= corte);
          values[y] = {
            hoje: round2(hoje.Mediana),
            ant: ant ? round2(ant.Mediana) : null,
          };
        }
        return { key: ind.key, label: ind.label, values };
      });

      payload = {
        date: latest,
        source: 'BCB — Sistema de Expectativas de Mercado (Focus)',
        years,
        indicators,
      };
      setCached('bcb_focus', payload);
    }

    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=7200');
    return res.status(200).json(payload);
  } catch (e) {
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(502).send(String((e && e.message) || e));
  }
}
