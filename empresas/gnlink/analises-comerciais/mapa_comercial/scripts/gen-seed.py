"""Regenera data/comercial-seed.js a partir dos POINTS comerciais do index.html.

Rode a partir da pasta mapa_comercial:
    python scripts/gen-seed.py

Requer: pip install json5
O seed é a carga inicial da base comercial — só entra no banco na 1ª leitura
(GET /api/comercial). Depois disso o Upstash/Redis manda; regenerar NÃO
sobrescreve o banco em produção.
"""
import json5, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # .../mapa_comercial
html = open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8").read()

i = html.index("const POINTS =")
start = html.index("[", i)
depth = 0; in_str = False; q = ""; esc = False; end = -1; k = start
while k < len(html):
    c = html[k]
    if in_str:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == q: in_str = False
    else:
        if c == '"' or c == "'": in_str = True; q = c
        elif c == "[": depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0: end = k; break
    k += 1
POINTS = json5.loads(html[start:end + 1])

COM = {"off_cliente", "off_negociacao", "off_prospeccao", "off_potencial",
       "off_negativa", "cdl", "comp", "cliente_comp"}
CAT2EST = {
    "off_potencial": "potencial", "off_prospeccao": "prospeccao",
    "off_negociacao": "negociacao", "off_cliente": "cliente",
    "off_negativa": "negativa",
}

def norm(p):
    cat = p.get("cat")
    return {
        "id": p.get("id"),
        "cat": cat,
        "estagio": CAT2EST.get(cat, "outro"),
        "nome": p.get("nome", ""),
        "sub": p.get("sub", ""),
        "lat": p.get("lat"),
        "lng": p.get("lng"),
        "aprox": bool(p.get("aprox", False)),
        "regiao": p.get("regiao", ""),
        "segmento": p.get("segmento", ""),
        "combustivel": p.get("combustivel", ""),
        "modal": p.get("modal", ""),
        "cdl": p.get("cdl", ""),
        "tipo": p.get("tipo", ""),
        "cap": p.get("cap", ""),
        "status": p.get("status", ""),
        "responsavel": p.get("responsavel", ""),
        "probabilidade": None,
        "proximoContato": "",
        "notas": p.get("notas", ""),
        "origem": "seed",
    }

seed, seen = [], set()
for p in POINTS:
    if p.get("cat") in COM and p.get("id") and p["id"] not in seen:
        seen.add(p["id"]); seed.append(norm(p))

out = os.path.join(ROOT, "data", "comercial-seed.js")
os.makedirs(os.path.dirname(out), exist_ok=True)
header = (
    "// AUTO-GERADO por scripts/gen-seed.py (extraido dos POINTS comerciais do\n"
    "// index.html). Carga inicial da base comercial: so entra no banco na 1a\n"
    "// vez (GET /api/comercial). Depois disso o banco (Upstash/Redis) manda.\n"
    "export default "
)
with open(out, "w", encoding="utf-8") as f:
    f.write(header + json.dumps(seed, ensure_ascii=False, indent=0) + ";\n")

print("registros:", len(seed))
print("por estagio:", dict(Counter(r["estagio"] for r in seed)))
print("arquivo:", os.path.relpath(out, ROOT))
