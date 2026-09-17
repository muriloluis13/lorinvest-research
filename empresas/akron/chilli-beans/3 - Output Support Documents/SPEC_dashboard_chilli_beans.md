# SPEC — Dashboard/Guia de Investimento · Chilli Beans (New Money)

> **Status:** rascunho para aprovação (Spec-Driven Development). Nenhuma linha de HTML será
> escrita antes do seu aceite desta spec.
> **Autor:** Research Lorinvest · **Data:** 17/09/2026
> **Entregável final:** `empresas/akron/chilli-beans/index.html` (arquivo único, autocontido)

---

## 1. Objetivo e enquadramento

Produzir um **guia de investimento HTML de página única**, no mesmo padrão visual e de navegação
dos dashboards **Compass** (`gnlink/analises-setoriais/competidores/compass/index.html`) e **Eneva**,
adaptado a uma operação de **crédito / special situations** da **Akron/Lorinvest** na **Chilli Beans**.

- **Decisão que o material apoia:** aporte de **New Money (R$ 35 mm; parcela Akron R$ 4,375 mm)**
  dentro da **Recuperação Extrajudicial (RE)** da Chilli Beans, com adesão à **Opção B**.
- **Ênfase pedida:** o **plano de reestruturação** da companhia (posição atual → RE → cascata →
  New Money → cenários de retorno).
- **Audiência:** interna (IC/Comitê Akron-Lorinvest). Idioma **pt-BR**. Tom analítico, sóbrio.
- **Natureza:** difere do Compass (equity listado / consenso sell-side). Aqui é **dívida distressed**:
  o fio condutor é sobrevivência da Cia, prioridade na cascata, deságio, garantias e recovery.

---

## 2. Contrato visual (herdado do Compass — replicar fielmente)

Reaproveitar o *design system* do `compass/index.html`, mantendo tokens e componentes:

- **Fonte:** DM Sans (Google Fonts). `font-variant-numeric: tabular-nums`.
- **Paleta Chilli Beans (marca):** o dashboard usa a identidade da Chilli — **preto** e **vermelho Chilli**
  como cores de marca, sobre fundo claro para legibilidade de material analítico. Tokens propostos
  (hex exato a confirmar amostrando o logo no build):
  - `--ink:#1A1A1A` (preto de marca — títulos, valores), `--bg:#F6F6F7`, `--card:#FFFFFF`, `--muted:#6A6A6E`.
  - `--accent3:#E4002B` (**vermelho Chilli** — cor de destaque, KPI-feat, acentos, notas).
  - `--accent:#2B2B2E` (grafite para elementos estruturais), `--line:#E4E4E7`.
  - **Paleta categórica de gráficos (contida):** preto/grafite + vermelho Chilli como par principal,
    com um set neutro de apoio (cinzas) e no máximo 2–3 secundárias sóbrias. Nada de arco-íris —
    o material é buy-side, não vitrine de coleção.
- **Header sticky** com faixa gradiente (slate→vermelho) + **strip de 6 KPIs** (cards `.kpi`, um `.k-feat` escuro em destaque).
- **Sidebar** de navegação por seções (colapsável, com grupos e ícones SVG) + **nav de abas** no topo.
- **Cards** com `.section-head` (ícone + título + tag/cap). Variantes `.tinted`, `.note` (borda vermelha).
- **Gráficos:** SVG gerados em JS inline (sem libs externas), tooltip `#tip` compartilhado, `.legend`.
- **Responsivo:** breakpoints do Compass (860px sidebar vira drawer; chrome-min ao rolar).
- **Sem dependências externas** além da fonte. Dados **inline** no JS (empresa única — não separar em `data/`).
- **Rodapé:** endereço Lorinvest + akroncapital.com.br (como no deck). Marca d'água "Confidencial".

### 2.1 Regra editorial (tom buy-side)

- **Perspectiva buy-side, não sell-side.** Sem *pitch*, sem adjetivação promocional. O leitor é o
  comitê que aloca capital do fundo — quer o fato, a conta e o risco.
- **Poucos adjetivos.** Frases curtas, orientadas a número. Preferir "TIR base 35% a.a." a
  "retorno atrativo". Evitar superlativos ("excelente", "robusto", "sólido").
- **Viés conservador.** Ancorar no cenário base/conservador; downside e recovery visíveis por padrão,
  não em nota de rodapé. Explicitar a baixa confiabilidade dos números da Cia sempre que citá-los.
- **Rastreável.** Todo número traz origem (via nota/fonte). Divergências de versão ficam explícitas,
  não escondidas.

---

## 3. Arquitetura de informação (sistemática, não narrativa)

**Princípio.** A IA não segue o fio de contação (histórico → crise → o que fizemos → o que ganhamos),
que soa a *storyline* de PPT. Segue **dimensões analíticas** de uma tese de crédito/special-situations
buy-side, cada uma respondendo a uma pergunta do comitê. As sub-histórias antes separadas
(**A Crise + Reestruturação + New Money**) são o **mesmo macro-tópico** — a *situação especial* — e passam
a viver sob uma única aba, com subtabs. **Valuation & Peers** ganha aba própria (destaque).

Estrutura: **8 abas de topo**, cada uma com **subtabs** (componente `.subtabs` do Compass) para os cortes internos.

| # | Aba (macro-tópico) | id | Pergunta que responde | Subtabs |
|---|--------------------|----|-----------------------|---------|
| 1 | **Sumário** | `p-sum` | Qual a decisão e por quê? | — (tese, recomendação, KPIs, racional) |
| 2 | **A Companhia** | `p-cia` | Qual é o ativo / a capacidade de pagar? | Perfil & modelo · Franquia & unit economics · Base & performance |
| 3 | **Setor** | `p-setor` | O mercado sustenta a tese? | Mercado ótico · Óculos de sol · Grau · Óticas & competição |
| 4 | **Notícias** | `p-news` | O que a evidência externa corrobora/contradiz? | Feed cronológico + leitura buy-side |
| 5 | **Situação & Reestruturação** | `p-sit` | Em que situação estamos e como se resolve? | A crise & o passivo · Posição atual · Plano de RE · New Money · Cascata & garantias |
| 6 | **Valuation & Retorno** | `p-val` | Quanto vale e quanto paga? | Valuation & peers · Ponte de EV · Cenários de retorno · Fluxo de caixa · Recovery & breakeven |
| 7 | **Riscos & Assunções** | `p-risco` | O que pode dar errado? | Riscos & mitigantes · Vetor de assunções (A1–A6) |
| 8 | **Fontes & Anexos** | `p-anexo` | De onde vêm os números? | Documentos · Metodologia · Notas de reconciliação |

**Agrupamento na sidebar** (tgrp), 3 blocos:
`TESE` (Sumário) · `FUNDAMENTOS` (A Companhia, Setor, Notícias) · `A OPERAÇÃO` (Situação & Reestruturação, Valuation & Retorno, Riscos, Fontes).

> A ênfase pedida na **reestruturação** é atendida pela aba 4 (a maior, com 5 subtabs) e reforçada no Sumário;
> não precisa ser uma aba "de história" à parte.

---

## 4. Conteúdo por aba (cards, gráficos, tabelas) e fonte dos dados

Legenda de fonte: **[NM]** deck New Money (set/26) · **[MEMO]** Memo IC v3 (mai/26) ·
**[TS]** Resumo Term Sheet RE · **[MOD]** modelos Excel de reestruturação (abas Resumo/Quadros PPT/Visão Valuation) ·
**[GUI]** `Chilli_Beans_Guidance.xlsx` · **[NEWS]** notícias públicas.

### Aba 1 — Sumário (`p-sum`)
- **Strip de KPIs (header, 6):** Investimento Akron **R$ 4,375 mm** · TIR **37% a.a.** (`k-feat`) · MOIC **1,7x** ·
  Payback **23 meses** · Exposição Akron total (pós) **R$ 8,8 mm** · Prazo **30 meses**. [NM]
- **Card "Tese" (SCR, 1 frase + recomendação):** o New Money de R$ 35 mm cobre a necessidade de caixa da Cia
  em 2026; a adesão dá à Akron prioridade na cascata, aceleração e deságio menor sobre o Old Money.
  Recomendação buy-side objetiva (aderir / não aderir), sem adjetivação. [NM]
- **Card "Racional da adesão" (4 blocos):** prioridade na cascata · aceleração (Roll-Up 1:1) ·
  deságio menor (50% vs 40%) · garantias reforçadas (AF 100% das ações + marca). [NM]
- **Card "Snapshot da Cia" (kv):** 872 lojas · 26% share sol (vol.) · R$ 368 mm faturamento 2025 ·
  R$ 997 mm sell-out · asset-light · 256 franqueados. [NM]
- **Card "Retorno em uma tela" (3 cenários resumidos):** Base c/M&A 65%/3,0x · Base s/M&A 35%/2,2x ·
  Conservador 16%/1,3x — ancorar no conservador. [NM]
- **Nota de confiabilidade do dado:** números da Cia pouco confiáveis (KPMG; práticas contábeis não seguidas). [NM][MEMO]

### Aba 2 — A Companhia (`p-cia`) — subtabs
**2a · Perfil & modelo**
- Card "Visão geral" (lead + kv: 28 anos, 872 lojas, +2,2 mm óculos/ano). [NM]
- Card "Linha do tempo" (timeline `.tml`: 1998→1999→2000-04→2013 Gávea→2016 Ótica→2018 saída Gávea→2020-21 pandemia→2024-26 inadimplência→2026 Akron/RE). [NM]
- Card "O sócio — Caito Maia" com **risco de pessoa-chave** explícito (sócio ≈ marca; interdependência). [NM]
- Card "Estrutura societária" (organograma SVG: Caito 99,99% → Fortuna/Sonic 2503 → Casa Firme (Holding) → Mustang 25 (**emissora**) → Super 25; Santa Mônica; Luz Franquias (avalista)). [NM][TS]
- Card "Modelo de negócio" (fluxo China → markup ~3x → franqueado → markup ~3x → consumidor; e-commerce, taxa de franquia, rebate de lentes; sem royalties). [NM]
- Card "Ciclo financeiro" (285 dias D0→D285; descasamento de caixa de 120 dias). [NM]

**2b · Franquia & unit economics**
- Card "Modelos de franquia" (tabela Quiosque/Rua/Shopping/Eco + Ótica: investimento, área, payback, markup, margem). [NM]
- Card "Economics da franqueadora" (payback 24-36m, margem 12-15%, markup 2,74-3x, FNP 3%; sem royalties sobre receita). [NM]

**2c · Base & performance**
- Card "Evolução da base de lojas" (barras empilhadas Vermelhas/Óticas/Eco-Intl 2021→mai/26 + churn 9%). [NM]
- Card "Performance financeira" (Receita líquida; EBITDA & margem; nota write-off R$ 88,5 mm). [NM][MOD]
- Card "Sell-out e composição" (sell-out da rede; mix Verm 66% / Ótica 23% / Outros 11%). [NM]

### Aba 3 — Setor (`p-setor`) — subtabs
**3a · Mercado ótico** — faturamento por segmento 2020→2030E; CAGR +8,0%→+5,1%; volumes; share do mercado. [NM]
**3b · Óculos de sol** — share em volume Chilli 26% vs Ray-Ban 8%; sell-out & ticket médio; diferenciais (marca, escassez programada, capilaridade). [NM]
**3c · Grau** — armações & lentes: sell-out & volume; drivers (envelhecimento, tempo de tela, 45% fora do oftalmo); pulverização das armações. [NM]
**3d · Óticas & competição** — tabela redes (Chilli, Carol, Diniz: economics comparados); nota smart glasses Ray-Ban/Meta. [NM]

### Aba 4 — Notícias (`p-news`) · evidência externa
Fonte única: **[NEWS]** `chilli_beans_noticias.docx` (14 matérias, fev/23 → set/26). A aba serve à leitura
buy-side: o que a imprensa **corrobora**, **contradiz** ou **acrescenta** à narrativa da Cia.

- **Card "Leitura buy-side" (destaque, topo) — o que as notícias mudam na tese:**
  1. **Confiabilidade / governança:** narrativa pública oscilante — negação enfática de RJ ("recuperação judicial
     é uma coisa, extrajudicial é outra"), versões conflitantes sobre o cargo de Dela Togna (co-CEO × VP) em ~70 min,
     reclamação de vazamento. Reforça a bandeira de confiabilidade dos números. [NEWS]
  2. **Corrobora a deterioração:** faturamento dos franqueados −12,3% jan-jul/26 (R$ 380 mm vs R$ 423 mm);
     linha vermelha −9,3%; dívida ~R$ 600 mm no fim de 2025; balanços 2025 não auditados. [NEWS]
  3. **Contexto do valuation / gatilho de M&A:** UBS BB contratado (nov/25) para vender 30% @ EV R$ 1,5 bi;
     conversas **paralisadas** com a escalada da crise. Liga direto à aba Valuation. [NEWS]
  4. **Estratégia e competição:** dependência 100% China (virada USD→yuan), expansão internacional (Caribe, Miami),
     ChilliPay/embedded finance com a Zoop, novo rival Yoface (óculos 3D sob demanda, ex-executivo da Chilli). [NEWS]
- **Card "Linha do tempo de notícias" (feed cronológico):** cada matéria = item com **data · fonte · título ·
  takeaway de 1 linha · tag temática**. Tags/filtros (chips): `Marca & Estratégia` · `Internacional` ·
  `Crise & Reestruturação` · `Governança` · `Competição` · `Financeiro`. Itens marcados como *corrobora* /
  *contradiz* / *contexto* com um selo. Links preservados (abrem em nova aba). [NEWS]
- **Nota:** conteúdo público (não-NDA) — pode ser citado com fonte/link; separa-se visualmente do material confidencial.

### Aba 5 — Situação & Reestruturação (`p-sit`) — subtabs · **macro-tópico central**
**4a · A crise & o passivo**
- Card "5 fatores da crise" (grid): endividamento pandemia + avais · retiradas do sócio · crédito flexível a franqueados · mercado estagnado · gestão financeira amadora. [NM]
- Card "Cronologia" (timeline: 2025 UBS → jan/26 inadimplência → fev/26 quebra de covenants → jun/26 Akron → em curso RE). [NM]
- Card "Composição da dívida" (waterfall: Financeira 424 · Aval 36 · Fiscal 71 · Fornecedores 20 = **551**; credores BB 96,4 / Caixa 71,6 / Deb. Vert 87,0; DL/EBITDA **10,4x**). [NM]

**4b · Posição atual (como a Akron chegou aqui)**
- Card "Aquisição das debêntures": consórcio Akron 25% / Jazz 25% / Vega 50% comprou 73% (Kinea @27,5% VF) + 3% (XP @20% VF) → **84%**, controle da emissão (>75%). VF total R$ 87 mm; exposição Akron R$ 4,6→4,4 mm. [NM][MEMO]

**4c · Plano de RE**
- Card "Opções A / B / C" (tabela comparativa — peça central): New Money, Roll-Up, Tranche 1 (operacional), Tranche 2 (holding/quase-equity); prazos, carências, deságio (40/50/60%), indexadores. Adesão = **Opção B**. [NM]
  - *Nota de reconciliação:* deck (set/26) vs Term Sheet (conceito "Credor Parceiro", deságio 70%) — usar deck como primário; TS numa nota.
- Card "Racional da Opção B" (4 blocos). [NM]
- Card "Reestruturação operacional" (do TS): políticas comerciais, substituição de franqueados problemáticos, corte de G&A/marketing, watchdog independente. [TS]

**4d · New Money**
- Card "Resumo da estrutura" (kv): Nota Comercial Pública; emissora Mustang 25; líquido R$ 35 mm (Akron R$ 4,375 mm); 2,5% a.m. + fee 3%; prazo 30m (venc. mar/29); carência 6m juros / 12m principal (SAC); MOIC mín. 1,5x; aval Caito Maia. [NM]
- Card "Roll-Up 1:1" (diagrama): cada R$ 1 de New Money realoca R$ 1 do crédito antigo para a Tranche Roll-Up (48m vs 60m; deságio 50% vs 60%). [NM]
- Card "Cash sweep" (diagrama): caixa > R$ 35 mm em verificações trimestrais → 100% do excedente, 75% ao New Money. [NM]

**4e · Cascata & garantias**
- Card "Cascata de excussão" (diagrama de prioridade): New Money → Tranche Roll-Up → 1ª Tranche A/B → 2ª Tranche A/B. [NM]
- Card "Garantias e proteções": cessão fiduciária de recebíveis + AF de marcas e de ações/quotas; sênior; cobertura 100% do saldo em até 180 dias. [NM]

### Aba 6 — Valuation & Retorno (`p-val`) — subtabs · **destaque**
**5a · Valuation & peers**
- Card "Valuation de referência (UBS BB)": EV total R$ 1,5 bi; equity implícito ~R$ 1,14 bi; M&A 30% → proceeds ~R$ 343 mm. Múltiplos implícitos (EV/Receita, EV/EBITDA em diferentes bases de EBITDA). [MEMO][GUI]
- Card "Peers" (tabela EV/Sales, EV/EBITDA: EssilorLuxottica, Warby Parker, Safilo, Boticário, Restoque; comentário). [MEMO][GUI]
- Card "EBITDA — qual número?": Cia ~R$ 125 mm vs Akron-realista R$ 53 mm (base) / R$ 40 mm (conservador); efeito nos múltiplos. [MEMO][MOD]

**5b · Ponte de EV**
- Card "Ponte de valor" (2026 As-Is → 2026 Pós-Reestr → 2028): EBITDA, múltiplo 8,0x, EV, caixa, dívida operacional/holding, equity; DL/EBITDA 10,4x → 4,8x → 3,3x. **Números limpos de [MOD]** (não usar OCR). [MOD]

**5c · Cenários de retorno** (estático, 3 colunas)
- Base c/M&A 65%/3,0x/R$ 18 mm (M&A dez/28) · Base s/M&A 35%/2,2x/R$ 11 mm · Conservador 16%/1,3x/R$ 3 mm; premissas por coluna. [NM]
- Card "New Money isolado": 37% / 1,7x / 23m / R$ 2,9 mm. [NM]

**5d · Fluxo de caixa** (tabela 2026–2031, Base + Conservador) — **números limpos de [MOD]/[GUI]**. [MOD]

**5e · Recovery & breakeven**
- Card "Matriz de recovery" (do memo): recovery de face × recebido × MOIC, da cura a RJ 25% (breakeven). [MEMO]

### Aba 7 — Riscos & Assunções (`p-risco`) — subtabs
**6a · Riscos & mitigantes**
- Card "Principais riscos" (grid `.risk`): operacional (base de franqueados pós-RE) · confiabilidade dos números · garantias dependem de performance futura · aval frágil (sócio sem patrimônio relevante no Brasil) · DFs 2025 não emitidas · dependência BB+Caixa · DIP. [NM][MEMO]
- Card "Mitigantes": preço de entrada baixo · co-investimento · posição relevante em assembleia · garantias reforçadas · gatilho de M&A. [MEMO]

**6b · Vetor de assunções** — tabela A1–A6 (assunção · confidence · threshold-de-reversão). [MEMO]

### Aba 8 — Fontes & Anexos (`p-anexo`) — subtabs
**7a · Documentos** — lista dos inputs + nota de confidencialidade (NDA Itaú BBA; material restrito à Akron). [todos]
**7b · Metodologia** — múltiplo 8x, indexadores, hurdle, base de EBITDA. [MOD][GUI]
**7c · Notas de reconciliação** — divergências de versão e escolhas de fonte (ver §6). [todos]

---

## 5. Inventário de gráficos SVG (a construir em JS, estilo Compass)

1. Barras empilhadas — evolução base de lojas por formato (2021–mai/26).
2. Barras + linha — Receita líquida e EBITDA/margem (2021–2030E).
3. Barras — sell-out da rede.
4. Waterfall — composição da dívida (551 mm) e ponte de EV (As-Is→Pós→2028).
5. Diagrama de fluxo — modelo de negócio (China→franqueado→consumidor).
6. Timeline — ciclo financeiro 285 dias; linha do tempo da Cia; cronologia da crise.
7. Diagrama — estrutura societária (organograma).
8. Diagrama — cascata de excussão + roll-up + cash sweep.
9. Barras — setor (faturamento por segmento, share, volumes, ticket).
10. Tabelas estilizadas — Opções A/B/C, franquias, fluxo de caixa, cenários, peers, recovery.
11. Feed de notícias — lista cronológica de cards com data/fonte/tag + filtro por chips (aba Notícias).

Todos na paleta Chilli (preto + vermelho Chilli), com tooltip e legenda; sem bibliotecas.

---

## 6. Reconciliação de dados (a resolver no build, antes de publicar números)

1. **Tabelas embaralhadas no OCR** do deck (ponte de EV pp. 28–29; fluxos pp. 33–34; resumo p. 32):
   **não usar o texto do OCR** — extrair os valores limpos das abas `Resumo` / `Quadros PPT` / `Visão Valuation`
   / `Retornos` dos Excels [MOD]/[GUI].
2. **Opções A/B/C (deck) vs Credor Parceiro (TS):** versões diferentes; deck = primário; TS numa nota.
3. **Métricas Old Money:** memo (mai/26) fala em MOIC ~6,7x @25% face (compra da debênture); deck (set/26)
   consolida New+Old em 2,2x–3,0x. São instrumentos/datas distintos — separar claramente "compra da debênture (mai/26)"
   de "New Money + reperfilamento (set/26)" para não confundir o leitor.
4. **EBITDA "ajustado":** Cia reporta ~R$ 125 mm; Akron trabalha com R$ 53 mm (base) / R$ 40 mm (conservador).
   Usar os números do deck/modelo e sinalizar o ajuste.

---

## 7. Plano de arquivos e build

- **Saída:** `empresas/akron/chilli-beans/index.html` (único, autocontido; espelha `compass/index.html`).
- **Apoio:** esta spec + extrações em `3 - Output Support Documents/`.
- **Passos do build (após aprovação):**
  1. Extrair números limpos dos Excels (Resumo, Quadros PPT, Visão Valuation, Retornos, Peers) → JSON inline.
  2. Portar o shell do Compass (header, KPIs, sidebar, nav, CSS, tooltip, roteador de abas + subtabs),
     recolorindo para a **paleta Chilli** (preto + vermelho Chilli).
  3. Construir seção a seção conforme §4, começando pela aba **Situação & Reestruturação** (ênfase) e **Sumário**.
  4. Implementar os SVGs do §5.
  5. Revisão de consistência (§6) + checagem responsiva (mobile/desktop) + validação dos totais.
  6. Commit no `main` (padrão do repositório: subir direto após cada ajuste).

---

## 8. Fora de escopo (nesta versão)

- Modelo interativo com sliders / recálculo ao vivo (escolhido: **estático**).
- Página `resultados.html` separada (escolhido: **página única**).
- Comparável dedicado com TOKY3/Mobly (pasta `akron/toky3`) — pode virar card/aba futura se desejado.
- Geração de PDF/PPTX a partir do dashboard.

---

## 9. Decisões travadas (feedback do usuário)

1. **Paleta:** identidade **Chilli Beans** (preto + vermelho Chilli), não a slate/navy Lorinvest. (§2)
2. **Valuation & Peers:** **aba própria de destaque** (aba 5), com o EV UBS BB R$ 1,5 bi. (§4)
3. **Tom:** **buy-side**, poucos adjetivos, **conservador**; risco de pessoa-chave (Caito Maia) tratado de forma
   direta e factual. (§2.1)
4. **IA:** **sistemática por dimensão analítica** (não narrativa/PPT); Crise + Reestruturação + New Money
   consolidados na aba única **Situação & Reestruturação** com subtabs. (§3)
