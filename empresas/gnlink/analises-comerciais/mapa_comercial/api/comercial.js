// ============================================================================
// API do Mapa Comercial GNLink — persiste a base comercial (clientes/leads) e
// as visitas do time num Redis (Upstash / Vercel KV). Mesma proteção do site:
// o middleware.js roda em /:path* (inclui /api/*), então o navegador reenvia o
// Basic Auth automaticamente. As credenciais do banco ficam em variáveis de
// ambiente do Vercel — nunca no cliente.
//
// Duas coleções, uma chave Redis cada:
//   comercial:clientes:v1  -> os pontos do mapa (leads/clientes). Semeados 1x
//                             a partir de data/comercial-seed.js; depois o
//                             banco manda. Cada cliente é um marcador no mapa.
//   comercial:visitas:v1   -> as interações do time (visita/call/proposta…),
//                             cada uma amarrada a um clienteId. É a timeline.
//
//   GET    /api/comercial                 -> { clientes:[...], visitas:[...] }
//   GET    /api/comercial?kind=clientes   -> só a lista de clientes
//   GET    /api/comercial?kind=visitas    -> só a lista de visitas
//   POST   /api/comercial  body{kind:'cliente', nome, ...campos}
//   POST   /api/comercial  body{kind:'visita', clienteId, vendedor, ...}
//                            (se vier estagioDepois, move o cliente no funil)
//   PATCH  /api/comercial  body{kind:'cliente'|'visita', id, ...campos}
//   DELETE /api/comercial?kind=cliente&id=...   (ou ?kind=visita&id=...)
// ============================================================================
import { Redis } from '@upstash/redis';
import SEED_CLIENTES from '../data/comercial-seed.js';

// Encontra a variável de ambiente cujo NOME termina no padrão dado — funciona
// com ou sem "Custom Prefix" na Vercel (KV_REST_API_URL, STORAGE_..., Upstash).
function findEnv(re) {
  const key = Object.keys(process.env).find((k) => re.test(k));
  return key ? process.env[key] : undefined;
}

const redis = new Redis({
  url: findEnv(/REST_API_URL$/) || findEnv(/UPSTASH_REDIS_REST_URL$/),
  token: findEnv(/REST_API_TOKEN$/) || findEnv(/UPSTASH_REDIS_REST_TOKEN$/),
});

const K_CLI = 'comercial:clientes:v1';
const K_VIS = 'comercial:visitas:v1';

// --- Vocabulário do funil -------------------------------------------------
// O estágio comanda o dashboard; a `cat` comanda a cor do pino no mapa. Para
// os leads da base comercial (off_*), os dois andam juntos.
const ESTAGIOS = ['potencial', 'prospeccao', 'negociacao', 'cliente', 'negativa', 'outro'];
const EST2CAT = {
  potencial: 'off_potencial',
  prospeccao: 'off_prospeccao',
  negociacao: 'off_negociacao',
  cliente: 'off_cliente',
  negativa: 'off_negativa',
};
const TIPOS_VISITA = ['visita', 'call', 'email', 'whatsapp', 'proposta', 'reuniao', 'outro'];

function normEstagio(v) {
  const s = String(v == null ? '' : v).trim();
  return ESTAGIOS.includes(s) ? s : 'outro';
}
function normTipoVisita(v) {
  const s = String(v == null ? '' : v).trim();
  return TIPOS_VISITA.includes(s) ? s : 'visita';
}
function toNum(v) {
  if (v === '' || v == null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}
function novoId(prefix) {
  return prefix + '_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 7);
}

// Registros antigos/parciais ganham os campos que faltam na leitura.
function migrarCliente(c) {
  const estagio = normEstagio(c.estagio);
  return Object.assign(
    {
      id: c.id,
      cat: c.cat || EST2CAT[estagio] || '',
      estagio,
      nome: c.nome || '',
      sub: c.sub || '',
      lat: typeof c.lat === 'number' ? c.lat : toNum(c.lat),
      lng: typeof c.lng === 'number' ? c.lng : toNum(c.lng),
      aprox: !!c.aprox,
      regiao: c.regiao || '',
      segmento: c.segmento || '',
      combustivel: c.combustivel || '',
      modal: c.modal || '',
      cdl: c.cdl || '',
      tipo: c.tipo || '',
      cap: c.cap || '',
      status: c.status || '',
      responsavel: c.responsavel || '',
      probabilidade: toNum(c.probabilidade),
      proximoContato: c.proximoContato || '',
      notas: c.notas || '',
      origem: c.origem || 'manual',
      criadoEm: c.criadoEm || '',
      atualizadoEm: c.atualizadoEm || '',
    },
    {}
  );
}
function migrarVisita(v) {
  return {
    id: v.id,
    clienteId: v.clienteId || '',
    data: v.data || v.criadoEm || '',
    vendedor: v.vendedor || '',
    tipo: normTipoVisita(v.tipo),
    resumo: v.resumo || '',
    proximosPassos: v.proximosPassos || '',
    proximoContato: v.proximoContato || '',
    estagioAntes: v.estagioAntes || '',
    estagioDepois: v.estagioDepois || '',
    concorrente: v.concorrente || '',
    volumeInformado: v.volumeInformado || '',
    combustivelAtual: v.combustivelAtual || '',
    criadoEm: v.criadoEm || '',
  };
}

async function loadClientes() {
  const list = await redis.get(K_CLI);
  if (Array.isArray(list)) return list.map(migrarCliente);
  const seeded = (SEED_CLIENTES || []).map((c) =>
    Object.assign({}, c, { criadoEm: '2026-08-12T00:00:00.000Z', atualizadoEm: '' })
  );
  await redis.set(K_CLI, seeded);
  return seeded.map(migrarCliente);
}
async function loadVisitas() {
  const list = await redis.get(K_VIS);
  if (Array.isArray(list)) return list.map(migrarVisita);
  await redis.set(K_VIS, []);
  return [];
}

// Aplica os campos de um POST/PATCH de cliente sobre um objeto-base.
function aplicarCamposCliente(alvo, b) {
  const set = (k, f) => {
    if (Object.prototype.hasOwnProperty.call(b, k)) alvo[k] = f(b[k]);
  };
  set('nome', (v) => String(v || '').trim());
  set('sub', (v) => String(v || '').trim());
  set('lat', toNum);
  set('lng', toNum);
  set('aprox', (v) => !!v);
  set('regiao', (v) => String(v || '').trim());
  set('segmento', (v) => String(v || '').trim());
  set('combustivel', (v) => String(v || '').trim());
  set('modal', (v) => String(v || '').trim());
  set('cdl', (v) => String(v || '').trim());
  set('tipo', (v) => String(v || '').trim());
  set('cap', (v) => String(v || '').trim());
  set('status', (v) => String(v || '').trim());
  set('responsavel', (v) => String(v || '').trim());
  set('probabilidade', toNum);
  set('proximoContato', (v) => String(v || '').trim());
  set('notas', (v) => String(v || '').trim());
  // Estágio: quando muda, arrasta a cat (cor do pino) para os leads off_*.
  if (Object.prototype.hasOwnProperty.call(b, 'estagio')) {
    alvo.estagio = normEstagio(b.estagio);
    if (EST2CAT[alvo.estagio]) alvo.cat = EST2CAT[alvo.estagio];
  }
  if (Object.prototype.hasOwnProperty.call(b, 'cat') && String(b.cat).trim()) {
    alvo.cat = String(b.cat).trim();
  }
  return alvo;
}

export default async function handler(req, res) {
  try {
    const kind = (req.query && req.query.kind) || (req.body && req.body.kind) || '';

    // ---------------- GET ----------------
    if (req.method === 'GET') {
      if (kind === 'clientes') return res.status(200).json(await loadClientes());
      if (kind === 'visitas') return res.status(200).json(await loadVisitas());
      const [clientes, visitas] = await Promise.all([loadClientes(), loadVisitas()]);
      return res.status(200).json({ clientes, visitas });
    }

    // ---------------- POST ----------------
    if (req.method === 'POST') {
      const b = req.body || {};

      if (kind === 'visita') {
        if (!b.clienteId || !String(b.vendedor || '').trim()) {
          return res.status(400).json({ error: 'clienteId e vendedor são obrigatórios' });
        }
        const clientes = await loadClientes();
        const cli = clientes.find((c) => c.id === b.clienteId);
        if (!cli) return res.status(404).json({ error: 'cliente não encontrado' });

        const agora = new Date().toISOString();
        const visita = migrarVisita({
          id: novoId('v'),
          clienteId: b.clienteId,
          data: (b.data && String(b.data)) || agora,
          vendedor: String(b.vendedor).trim(),
          tipo: b.tipo,
          resumo: String(b.resumo || '').trim(),
          proximosPassos: String(b.proximosPassos || '').trim(),
          proximoContato: String(b.proximoContato || '').trim(),
          estagioAntes: cli.estagio,
          estagioDepois: b.estagioDepois ? normEstagio(b.estagioDepois) : '',
          concorrente: String(b.concorrente || '').trim(),
          volumeInformado: String(b.volumeInformado || '').trim(),
          combustivelAtual: String(b.combustivelAtual || '').trim(),
          criadoEm: agora,
        });

        // Cola de inteligência: a visita atualiza o cliente (estágio→cor no
        // mapa, responsável, próximo contato) — o mapa relê e reflete tudo.
        let mudouCliente = false;
        if (visita.estagioDepois && visita.estagioDepois !== cli.estagio) {
          cli.estagio = visita.estagioDepois;
          if (EST2CAT[cli.estagio]) cli.cat = EST2CAT[cli.estagio];
          mudouCliente = true;
        }
        if (visita.proximoContato) { cli.proximoContato = visita.proximoContato; mudouCliente = true; }
        if (!cli.responsavel && visita.vendedor) { cli.responsavel = visita.vendedor; mudouCliente = true; }
        if (visita.combustivelAtual && !cli.combustivel) { cli.combustivel = visita.combustivelAtual; mudouCliente = true; }
        if (mudouCliente) {
          cli.atualizadoEm = agora;
          await redis.set(K_CLI, clientes);
        }

        const visitas = await loadVisitas();
        visitas.push(visita);
        await redis.set(K_VIS, visitas);
        return res.status(201).json({ visita, cliente: mudouCliente ? cli : undefined });
      }

      // POST cliente (novo lead)
      if (!String(b.nome || '').trim()) {
        return res.status(400).json({ error: 'nome é obrigatório' });
      }
      const agora = new Date().toISOString();
      const base = migrarCliente({ id: novoId('c'), estagio: 'prospeccao', origem: 'manual', criadoEm: agora });
      aplicarCamposCliente(base, b);
      base.atualizadoEm = agora;
      const clientes = await loadClientes();
      clientes.push(base);
      await redis.set(K_CLI, clientes);
      return res.status(201).json(base);
    }

    // ---------------- PATCH ----------------
    if (req.method === 'PATCH') {
      const b = req.body || {};
      if (!b.id) return res.status(400).json({ error: 'id é obrigatório' });

      if (kind === 'visita') {
        const visitas = await loadVisitas();
        const v = visitas.find((x) => x.id === b.id);
        if (!v) return res.status(404).json({ error: 'visita não encontrada' });
        const setV = (k, f) => { if (Object.prototype.hasOwnProperty.call(b, k)) v[k] = f(b[k]); };
        setV('data', (x) => String(x || ''));
        setV('vendedor', (x) => String(x || '').trim());
        setV('tipo', normTipoVisita);
        setV('resumo', (x) => String(x || '').trim());
        setV('proximosPassos', (x) => String(x || '').trim());
        setV('proximoContato', (x) => String(x || '').trim());
        setV('concorrente', (x) => String(x || '').trim());
        setV('volumeInformado', (x) => String(x || '').trim());
        setV('combustivelAtual', (x) => String(x || '').trim());
        await redis.set(K_VIS, visitas);
        return res.status(200).json(v);
      }

      // PATCH cliente
      const clientes = await loadClientes();
      const cli = clientes.find((c) => c.id === b.id);
      if (!cli) return res.status(404).json({ error: 'cliente não encontrado' });
      aplicarCamposCliente(cli, b);
      cli.atualizadoEm = new Date().toISOString();
      await redis.set(K_CLI, clientes);
      return res.status(200).json(cli);
    }

    // ---------------- DELETE ----------------
    if (req.method === 'DELETE') {
      const id = (req.query && req.query.id) || (req.body && req.body.id);
      if (!id) return res.status(400).json({ error: 'id é obrigatório' });

      if (kind === 'visita') {
        const visitas = await loadVisitas();
        const next = visitas.filter((v) => v.id !== id);
        await redis.set(K_VIS, next);
        return res.status(200).json({ ok: true, removidas: visitas.length - next.length });
      }
      // DELETE cliente: remove o cliente e as visitas órfãs dele.
      const clientes = await loadClientes();
      const nextCli = clientes.filter((c) => c.id !== id);
      await redis.set(K_CLI, nextCli);
      const visitas = await loadVisitas();
      const nextVis = visitas.filter((v) => v.clienteId !== id);
      if (nextVis.length !== visitas.length) await redis.set(K_VIS, nextVis);
      return res.status(200).json({
        ok: true,
        removidas: clientes.length - nextCli.length,
        visitasRemovidas: visitas.length - nextVis.length,
      });
    }

    res.setHeader('Allow', 'GET, POST, PATCH, DELETE');
    return res.status(405).json({ error: 'método não permitido' });
  } catch (e) {
    return res.status(500).json({ error: String((e && e.message) || e) });
  }
}
