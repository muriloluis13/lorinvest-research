// ============================================================================
// API do To-Do Tracker — persiste as tarefas num Redis (Upstash / Vercel KV).
// Protegida pela mesma senha do site: o middleware.js roda em /:path* (inclui
// /api/*), e o navegador reenvia o Basic Auth automaticamente nas chamadas.
// As credenciais do banco ficam em variáveis de ambiente do Vercel — nunca no
// cliente. Aceita as duas convenções de nome que o add-on pode injetar.
//
//   GET    /api/todos          -> lista todas as tarefas (semeia na 1ª vez)
//   POST   /api/todos          -> body {analista, empresa, empresaLogo?, projeto?, texto, comentario?}
//   PATCH  /api/todos          -> body {id, done?, projeto?, texto?, comentario?}
//   PUT    /api/todos          -> body {order:[id,...], moved?:{id, projeto?}} (reordena)
//   DELETE /api/todos?id=...   -> remove a tarefa
// ============================================================================
import { Redis } from '@upstash/redis';

// Encontra a variável de ambiente cujo NOME termina no padrão dado — assim
// funciona com ou sem "Custom Prefix" na Vercel (ex.: KV_REST_API_URL ou
// STORAGE_KV_REST_API_URL). Cobre as convenções Vercel KV e Upstash.
function findEnv(re) {
  const key = Object.keys(process.env).find((k) => re.test(k));
  return key ? process.env[key] : undefined;
}

const redis = new Redis({
  url: findEnv(/REST_API_URL$/) || findEnv(/UPSTASH_REDIS_REST_URL$/),
  token: findEnv(/REST_API_TOKEN$/) || findEnv(/UPSTASH_REDIS_REST_TOKEN$/),
});

const KEY = 'todos:v1';

// Semente: os to-dos que estavam chumbados no HTML (extraídos 1:1). Só entram
// no banco se ainda não houver nada gravado — depois disso o banco manda.
const SEED = [
  { id: 'seed_01', analista: 'Murilo Nunes', empresa: 'BioRen', empresaLogo: 'logos/bioren-logo.jpg', texto: 'Terminar modelo de valuation para PRIO' },
  { id: 'seed_02', analista: 'Murilo Nunes', empresa: 'BioRen', empresaLogo: 'logos/bioren-logo.jpg', texto: 'Comparação economics vs. tinta barata + raspagem' },
  { id: 'seed_03', analista: 'Murilo Nunes', empresa: 'BioRen', empresaLogo: 'logos/bioren-logo.jpg', texto: 'Comparação mercante vs. sonda' },
  { id: 'seed_04', analista: 'Murilo Nunes', empresa: 'GNLink', empresaLogo: 'logos/gnlink-logo.jpg', texto: 'Atualizar modelo com informações de Maio/2026' },
  { id: 'seed_05', analista: 'Murilo Nunes', empresa: 'GNLink', empresaLogo: 'logos/gnlink-logo.jpg', texto: 'Fazer HTML com as apresentações de conselho' },
  { id: 'seed_06', analista: 'Murilo Nunes', empresa: 'GNLink', empresaLogo: 'logos/gnlink-logo.jpg', texto: 'Valuation EDGE' },
  { id: 'seed_07', analista: 'Murilo Nunes', empresa: 'GNLink', empresaLogo: 'logos/gnlink-logo.jpg', texto: 'Apresentação de alavancagem: incluir Use of Proceeds e todos os gráficos (EBITDA, Lucro, CapEx, FCFF, Dívida, Juros, FCFE)' },
  { id: 'seed_08', analista: 'Murilo Nunes', empresa: 'GNLink', empresaLogo: 'logos/gnlink-logo.jpg', texto: 'Testar IA com as planilhas do comercial do Silvino (clientes, raios de atuação da planta, gasodutos de distribuição por UF)' },
  { id: 'seed_09', analista: 'Murilo Nunes', empresa: 'Novas Águas', empresaLogo: '', texto: 'Modelo interno' },
  { id: 'seed_10', analista: 'Murilo Nunes', empresa: 'Novas Águas', empresaLogo: '', texto: 'Analisar valuation TGA' },
  { id: 'seed_11', analista: 'Murilo Nunes', empresa: 'Novas Águas', empresaLogo: '', texto: 'Apresentação setorial' },
  { id: 'seed_12', analista: 'Murilo Nunes', empresa: 'GBS', empresaLogo: 'logos/gbs-logo.jpg', texto: 'Refazer os cálculos de tributos sobre o lucro do modelo GBS' },
  { id: 'seed_13', analista: 'Murilo Nunes', empresa: 'GBS', empresaLogo: 'logos/gbs-logo.jpg', texto: 'Ver quando acaba o prejuízo fiscal de R$ 34 mi' },
  { id: 'seed_14', analista: 'Murilo Nunes', empresa: 'GBS', empresaLogo: 'logos/gbs-logo.jpg', texto: 'Avaliar quanto do prejuízo fiscal da Tann (R$ 50 mi) seria aproveitável' },
].map(function (t) { return Object.assign({ done: false, criadoEm: '2026-07-20T00:00:00.000Z' }, t); });

async function load() {
  const list = await redis.get(KEY); // @upstash/redis já entrega o JSON parseado
  if (Array.isArray(list)) return list;
  await redis.set(KEY, SEED);        // primeira vez: semeia
  return SEED.slice();
}

function novoId() {
  return 't_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 7);
}

export default async function handler(req, res) {
  try {
    if (req.method === 'GET') {
      return res.status(200).json(await load());
    }

    if (req.method === 'POST') {
      const b = req.body || {};
      const texto = (b.texto || '').trim();
      if (!b.analista || !b.empresa || !texto) {
        return res.status(400).json({ error: 'analista, empresa e texto são obrigatórios' });
      }
      const item = {
        id: novoId(),
        analista: String(b.analista),
        empresa: String(b.empresa),
        empresaLogo: b.empresaLogo ? String(b.empresaLogo) : '',
        projeto: b.projeto ? String(b.projeto).trim() : '',
        texto: texto,
        comentario: b.comentario ? String(b.comentario).trim() : '',
        done: false,
        criadoEm: new Date().toISOString(),
      };
      const list = await load();
      list.push(item);
      await redis.set(KEY, list);
      return res.status(201).json(item);
    }

    if (req.method === 'PATCH') {
      const b = req.body || {};
      const list = await load();
      const it = list.find(function (t) { return t.id === b.id; });
      if (!it) return res.status(404).json({ error: 'tarefa não encontrada' });
      if (Object.prototype.hasOwnProperty.call(b, 'done')) it.done = !!b.done;
      if (Object.prototype.hasOwnProperty.call(b, 'projeto')) it.projeto = String(b.projeto || '').trim();
      if (Object.prototype.hasOwnProperty.call(b, 'comentario')) it.comentario = String(b.comentario || '').trim();
      if (Object.prototype.hasOwnProperty.call(b, 'texto') && String(b.texto).trim()) it.texto = String(b.texto).trim();
      await redis.set(KEY, list);
      return res.status(200).json(it);
    }

    if (req.method === 'PUT') {
      const b = req.body || {};
      const list = await load();
      // Atualiza o projeto do item arrastado (quando muda de seção de projeto).
      if (b.moved && b.moved.id) {
        const m = list.find(function (t) { return t.id === b.moved.id; });
        if (m && Object.prototype.hasOwnProperty.call(b.moved, 'projeto')) {
          m.projeto = String(b.moved.projeto || '').trim();
        }
      }
      // Reordena a lista inteira conforme a ordem de ids enviada pelo cliente.
      let next = list;
      if (Array.isArray(b.order)) {
        const pos = {};
        b.order.forEach(function (id, i) { pos[String(id)] = i; });
        next = list.slice().sort(function (a, c) {
          const pa = pos[a.id] != null ? pos[a.id] : Infinity;
          const pc = pos[c.id] != null ? pos[c.id] : Infinity;
          return pa - pc;
        });
      }
      await redis.set(KEY, next);
      return res.status(200).json({ ok: true });
    }

    if (req.method === 'DELETE') {
      const id = (req.query && req.query.id) || (req.body && req.body.id);
      if (!id) return res.status(400).json({ error: 'id é obrigatório' });
      const list = await load();
      const next = list.filter(function (t) { return t.id !== id; });
      await redis.set(KEY, next);
      return res.status(200).json({ ok: true, removidas: list.length - next.length });
    }

    res.setHeader('Allow', 'GET, POST, PATCH, PUT, DELETE');
    return res.status(405).json({ error: 'método não permitido' });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}
