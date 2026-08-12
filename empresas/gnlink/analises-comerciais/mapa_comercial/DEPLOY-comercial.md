# Deploy — Mapa Comercial GNLink (backend `api/comercial.js`)

Plataforma de inteligência comercial embutida no mapa. O `index.html` continua
sendo o entregável; a base comercial deixa de ser chumbada no HTML e passa a
viver num banco (Upstash/Redis) exposto por `api/comercial.js`.

## Estrutura da pasta (deploy dedicado)
```
mapa_comercial/
  index.html              # o mapa (entregável)
  middleware.js           # Basic Auth do site (protege tudo, inclui /api/*)
  package.json            # deps: @upstash/redis, @vercel/functions
  api/comercial.js        # backend (clientes + visitas)
  data/comercial-seed.js  # carga inicial: 865 leads extraidos dos POINTS
  scripts/gen-seed.py     # regenera o seed a partir do index.html
```

## Passo a passo na Vercel
1. **Novo projeto** apontando para este repositório.
2. **Root Directory** = `empresas/gnlink/analises-comerciais/mapa_comercial`
   (Settings → General → Root Directory). É o padrão de deploy dedicado por
   pasta já usado na casa.
3. **Provisionar o banco** (Storage → criar um **Upstash Redis / KV**) e
   conectá-lo a ESTE projeto. Isso injeta as env vars
   `KV_REST_API_URL` / `KV_REST_API_TOKEN` (ou `UPSTASH_REDIS_REST_URL/TOKEN`).
   O `api/comercial.js` aceita as duas convenções automaticamente.
   > É um banco separado do To-Do Tracker — use um store novo (chaves
   > `comercial:*`), ou reaproveite um store existente (as chaves não colidem).
4. **Basic Auth**: defina `SITE_USER` e `SITE_PASSWORD` nas env vars (mesmas do
   restante do site). O `middleware.js` já protege `/api/*`.
5. **Deploy.** Configure as env vars ANTES do 1º build.

## Verificar
- `GET /api/comercial` → `{ clientes:[...865...], visitas:[] }` (semeia na 1ª vez).
- `GET /api/comercial?kind=clientes` → só os clientes.
- `POST /api/comercial` com `{ "kind":"visita", "clienteId":"cdl-batalha-al",
  "vendedor":"Marco", "resumo":"...", "estagioDepois":"negociacao" }`
  → cria a visita e move o cliente no funil (muda a cor do pino no mapa).

## Contrato da API (resumo)
| Método | Rota | Corpo / query | Faz |
|---|---|---|---|
| GET | `/api/comercial` | — | `{clientes, visitas}` |
| GET | `/api/comercial?kind=clientes\|visitas` | — | uma coleção |
| POST | `/api/comercial` | `{kind:'cliente', nome, ...}` | novo lead |
| POST | `/api/comercial` | `{kind:'visita', clienteId, vendedor, estagioDepois?, ...}` | nova visita (+ move funil) |
| PATCH | `/api/comercial` | `{kind, id, ...campos}` | edita cliente/visita |
| DELETE | `/api/comercial?kind=cliente&id=` | — | remove (visitas órfãs junto) |

## Modelo de dados
- **cliente**: `id, cat, estagio, nome, sub, lat, lng, regiao, segmento,
  combustivel, modal, cdl, cap(volume), status, responsavel, probabilidade,
  proximoContato, notas`. `cat` dá a cor do pino; `estagio` alimenta o funil.
- **visita**: `id, clienteId, data, vendedor, tipo, resumo, proximosPassos,
  proximoContato, estagioAntes, estagioDepois, concorrente, volumeInformado,
  combustivelAtual`.

## Regenerar o seed
```bash
pip install json5
python scripts/gen-seed.py
```
Só afeta a carga inicial. Em produção, o banco já semeado NÃO é sobrescrito.
