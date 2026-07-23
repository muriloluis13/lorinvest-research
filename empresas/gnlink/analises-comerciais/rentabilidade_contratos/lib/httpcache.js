// Cache TTL simples em memória de módulo. Numa serverless function da Vercel o
// escopo de módulo sobrevive entre invocações "quentes" (mesma instância), então
// funciona como o dicionário _cache do proxy_anp.py: evita rebuscar a fonte a cada
// request. Em cold start o cache é perdido — comportamento aceitável.
const store = new Map();

export function getCached(key, ttlMs) {
  const e = store.get(key);
  if (e && Date.now() - e.t < ttlMs) return e.v;
  return null;
}

export function setCached(key, value) {
  store.set(key, { t: Date.now(), v: value });
}
