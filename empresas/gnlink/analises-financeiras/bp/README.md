# GNLink · Business Plan — motor de modelo ao vivo

Dashboard de BP da GNLink que **roda as fórmulas de projeção no navegador** (JS) e
lê uma **base histórica em xlsx** separada. Reimplementa a espinha do modelo Excel
(volume → receita → custos → EBITDA), validando cada motor **1:1 contra o Excel**.

Arquitetura (ver `GNLink Inputs para o BP.docx` na pasta `Modelo/`): o modelo mensal
tem só 2 dados brutos — **histórico** (Realizado, vai para o xlsx) e **premissas de
projeção** (viram JS editável). Todo o resto são fórmulas, que vivem no `index.html`.

## Arquivos
```
bp/
  index.html                 # o dashboard (motor + UI) — o entregável
  gnlink-bp-historico.xlsx   # base histórica + drivers (gerada pelo build)
  middleware.js              # Basic Auth (protege o deploy dedicado)
  package.json               # dep: @vercel/functions (só p/ o middleware)
  build/
    extrai_historico.py      # gera o xlsx a partir do modelo Excel
    golden/*.csv             # referência de validação (cache do Excel)
  .gitignore                 # re-inclui o xlsx gerado (o repo ignora *.xlsx)
```

## Como as abas mapeiam o modelo
- **Resumo (EBITDA)** — DRE consolidada do Demonstrativo Financeiro Mensal.
- **Receita** — Receita Líquida por componente (GNL+GNC+serviço+aluguel+outros) + volume.
- **Variável** — custo da molécula (R$/m³, indexado com piso/teto).
- **OPEX** — custos operacionais por categoria (gás, liquefação, compressão, terminal, SG&A, logística, regás).
- **Clientes** — editor de premissas por contrato (curva de volume, preço, indexação) — re-projeta ao vivo.
- **Macro** — SELIC/IPCA/CDI/Brent/Henry Hub/Dólar/CPI.
- **Premissas** — alavancas globais what-if (volume/preço/molécula × base) que cascateiam pela projeção.

Sidebar espelha as abas da planilha; cada aba de modelagem tem **sub-abas por região**
(Consolidado/PR/BA/RN/Terminal PE/Argentina/SAL/Outro). Eixo de 192 meses (jan/23→dez/38),
corte Realizado = jul/26 (`DCF!F22`).

## Regenerar a base histórica
Quando entrar um novo mês/cenário no modelo, aponte o extrator para o novo .xlsx:
```bash
cd build
python extrai_historico.py            # usa o cenário padrão (custos a IPCA)
python extrai_historico.py "<caminho\Modelo - ....xlsx>"
```
Gera `../gnlink-bp-historico.xlsx` e os goldens em `golden/`. Requer `openpyxl`.

## Rodar localmente
Servido por HTTP o dashboard **carrega o xlsx automaticamente**:
```bash
python -m http.server 8777    # dentro da pasta bp/
```
e abra `http://127.0.0.1:8777/index.html`. Abrindo via `file://` o navegador bloqueia
o fetch — use o seletor/drag-drop de arquivo que aparece na tela.

## Validar (motor JS × Excel)
Abra com `?validate` (`http://127.0.0.1:8777/index.html?validate`) e veja o console (F12):

| Motor | Status |
|---|---|
| Volume | **0** divergências (2304 pontos) |
| Receita (IPCA + Brent) | **0** |
| Custo do gás / molécula | **0** (1152 pontos) |
| Custo total (gás + OpEx) | **0** (192 meses) |
| Receita Líquida (composição vs DFM) | projeção **0**; realizado ~1% (reconciliação actual vs bottom-up) |

O golden é o **cache de valores do próprio Excel** (`data_only`), extraído junto com o xlsx.

## Deploy na Vercel (deploy dedicado por pasta)
1. **Novo projeto** apontando para este repositório.
2. **Root Directory** = `empresas/gnlink/analises-financeiras/bp` (Settings → General).
3. **Basic Auth**: env vars `SITE_USER` e `SITE_PASSWORD` (as mesmas do resto do site).
   O `middleware.js` local protege tudo (o da raiz do repo não vem no deploy dedicado).
4. **Deploy** — sem build step; é estático + 1 middleware. Configure as env vars antes do 1º build.

## Notas de fidelidade
- **Realizado = actuals** extraídos; **projeção = fórmulas em JS** — mesma separação do Excel.
- **Indexação de preço:** IPCA 100% é portada em JS (exata, sensível ao preço-base editável);
  a Brent (Bahia/RN/SAL) usa o preço corrigido extraído como driver (acopla o custo da
  molécula com piso/teto).
- **Premissas what-if globais** ajustam Receita e gás na projeção → overlay no EBITDA
  (base do modelo + Δreceita − Δgás). As demais linhas da DRE (OpEx, depreciação, impostos)
  ficam na base — ligar o OpEx volume-dependente às alavancas é refinamento futuro.

## Roadmap
DRE por região; OpEx volume-dependente ligado às alavancas; balanço/dívida/DCF/alavancagem;
chaves de cenário do Painel de Controle (Congelar Realizado, plantas 3/5, funding).
