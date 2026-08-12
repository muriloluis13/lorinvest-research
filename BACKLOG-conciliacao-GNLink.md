# Conciliação GNLink_Model × Modelo Referência — backlog

Conciliação entre `GNLink_Model_2026.07.31.xlsx` (modelo por segmento) e
`Modelo - Realizado Jun.26 (v ajust).xlsx` (modelo referência, por cliente).

Última atualização: 10/08/2026

**Estado do modelo em 10/08** — 0 células de erro · os 7 checks de balanço em **0,000000** ·
dívida zerada no último mês nas 7 abas · nenhuma célula de `EoP Debt` não-nula após a quitação.

> **Flags da linha 37 no estado atual: `PR=Y · BA=Y · RN=Y · AR=N · SAL=N · Corredor Azul=N ·
> Holding=Y`.** Com AR e SAL desligados o EBITDA consolidado de 2030 é **R$47,65 mi** (volume
> 94,6 mi m³); com os dois ligados, **R$152,77 mi** (180,8 mi m³). Confira os flags antes de
> ler qualquer output — os números do trabalho de dívida foram medidos com AR e SAL em "N".

---

## Convenção de edição (definida em 05/08)

Toda modificação daqui em diante:

1. **Cria linha nova** em vez de reaproveitar linha em branco — o espaçamento visual dos
   blocos é preservado.
2. **Replica em todas as abas de projeto** — hoje **sete**: `PR`, `BA`, `RN`, `AR`, `SAL`,
   `Holding` e `Consolidated` (eram cinco quando a convenção foi escrita; `AR` e `SAL`
   entraram nos itens 31 e 34) — na mesma numeração, mesmo quando a linha fica zerada
   (caso do `Holding`), para manter as abas alinhadas linha a linha.

---

## Concluído

| # | Item | Efeito |
|---|---|---|
| 1 | **Desacoplamento preço × custo no PR.** A molécula renegociada (2,2237 → 1,655 em nov/26) era repassada integralmente ao preço de venda. Criada linha `PR!79` (*Gas cost (pricing)*) com o custo contratual indexado a Brent; linhas 51/61 passam a lê-la; linha 83 segue como custo efetivo na DRE (linha 115 ajustada). | +R$11 mi/ano de receita e EBITDA no PR, custo inalterado |
| 2 | **Recalibração dos preços-base de segmento.** 13 células em `Dashboard!D133:F148` ajustadas por mínimos quadrados ponderados por volume contra a referência (2028-2031). | Δ de preço por bucket caiu de ±0,22 para ±0,02 R$/m³ |
| 3 | **Volume de serviço sem molécula removido das linhas de frete.** Linhas 93/96/98/100 das abas PR/BA/RN somavam a linha 47 (volume de serviço, majoritariamente FOB) no cálculo de frota e frete GNL. Normalizada também `PR!AI103`. | +R$0,6-0,7 mi/ano de EBITDA (BA e RN; PR não tem contrato de serviço) |
| 4 | **Aluguel fixo criado.** Premissa `Dashboard!140` (R$/mês por planta; BA = 57.854,74 = Petyan 45.924,94 + Petrobahia 11.929,80), com o cálculo direto na linha 111 (*Fixed Rent*) de cada aba de projeto, de AI em diante. Histórico D:AH preservado. | +R$0,74-0,85 mi/ano; bate com a referência em ±R$0,01 mi |
| 5 | **Energia da liquefação — correções estruturais.** (i) A potência era lida de `Dashboard!$D$167` nas três abas, com `E167`/`F167` vazias — BA e RN herdavam a potência do PR. Cada aba passou a ler sua coluna. (ii) O número de trens era `ROUNDUP(volume / Dashboard!$C$333)`, onde `C333` é o **tamanho do ISO container** (24.000 m³) — driver conceitualmente trocado. Criada premissa `Dashboard!C335` = *Liquefaction train capacity* = 22.000 m³/dia. | +R$2,5-2,9 mi/ano de custo |
| 6 | **Tarifa de energia alinhada à referência.** `Dashboard!164`: PR 243,95 → **390,00**; BA 306,05 → **426,02**; RN 358,40 → **565,42**. Como a referência não tem crédito de ICMS (custo = tarifa cheia × MWh), o crédito de `Dashboard!165` foi a zero (PR 19% → 0, BA 20,5% → 0) para o custo efetivo bater. | Gap de EBITDA 2028 de +19,3 para +4,6 mi |
| 7 | **Indexação removida da energia.** Retirado o `*AI6` do fim das linhas 86 (eletricidade) e 117 (compressão) das três abas. A referência mantém a tarifa constante em termos nominais. | Gap passou a ser estável no horizonte em vez de divergir |
| 8 | **Gerador a diesel do PR criado.** Premissa `Dashboard!169` (*Diesel Generator*, R$/mês; PR = 86.000, demais 0) e linha 90 (*Diesel Generator*) em cada aba de projeto, sem indexação. Linha 116 passou de `SUM(86:89)` para `SUM(86:90)`. | +R$1,03 mi/ano no PR |
| 9 | **Método de consumo alinhado (cenário C).** Trocado o degrau `ROUNDUP(vol/22.000) × 0,70 MW × 24 × dias` pela curva linear da referência × 1.000 h/mês. `Dashboard!167` mudou de significado (era *LNG Equipments, Mw/Equip* = 0,70; virou *LNG load per train, MW* = 0,48) e foram criadas as premissas de carga base (0,35 MW), carga mínima (0,55 MW) e horas (1.000 h/mês). No RN o driver passou a incluir o volume de serviço (`AI35+AI47`). | **Eletricidade do PR e da BA bate exatamente**; RN fica +R$0,30 mi/ano (ver P8) |
| 10 | **Utilities deixou de escalar por equipamento.** A fórmula era `(ROUNDUP(vol/21.000)+1) × R$/equip` — com o `21.000` hardcoded (nem a capacidade do trem, nem o ISO) e uma unidade extra somada. Como o valor é a **cesta completa de consumíveis da planta** (propano, água, óleo, resíduo, mercaptano), virou um R$/mês por planta: `IF(vol>0, −Dashboard!$D$177, 0)/10^3 × infl`. Rótulo da unidade corrigido de *R$/equipment* para *R$/month*. | Custo caiu de +1,74 para −1,78 mi vs. referência |
| 11 | **Utilities calibrado no total da referência.** `Dashboard!177`: PR 32.766 → **47.812**; BA 15.330 → **69.350**; RN 24.874 → **87.472** R$/mês (mínimos quadrados 2028-2031, base em jul/26). | Desvio de ±R$0,03 mi/ano |
| 12 | **Perdas reestruturadas.** Três mudanças: (i) base de valoração passou de 2% do custo de *processamento* para **5% valorizado ao custo da molécula** (`custo_gás/(1−5%)×5%`) — o gás que evapora foi comprado; (ii) criadas as premissas de **recuperação de purga** (`Dashboard!179` = 20% do volume de GNC no PR; `180` = 2.300 m³/dia na BA; RN nenhuma); (iii) **Losses separado de Others** em linhas distintas. Histórico realizado (que era o item combinado) migrou para a linha de Others. | Perdas batem na casa decimal nas 3 plantas |
| 13 | **"Others" da liquefação alinhado ao realizado.** `Dashboard!177`: PR 108.561 → **5.000**; BA 283.503 → **15.000**; RN 170.707 → **15.000** R$/mês. A premissa projetava 17× a 1.700× o realizado (que roda a ~R$5-6 mil/mês, idêntico nas duas bases). | −R$7 mi/ano; **liquefação fechou em ±R$0,05 mi** |
| 14 | **Distâncias médias ponderadas por volume.** As seis células de distância recalculadas a partir dos contratos CIF da aba `Clientes` (horizonte 2027-2038): GNL PR 410 → **454,40**, BA **120 → 296,32**, RN 540 → **557,25**; GNC PR 244 → **250,08**, BA **139 → 377,00**, RN 120 → **115,20**. Os 120 km da BA não correspondiam a nenhum contrato (o mais próximo está a 174 km). | BA saiu de −5,2 para −1,8 mi (2028) |
| 15 | **Nº de ISOs calibrado pelo custo.** `Dashboard!192`: PR 6,93 → **2,8148**; BA **−1,19 → 3,0794**; RN 7,76 → **2,2408**. O valor da BA era **negativo**, transformando a linha de aluguel em receita. Calibrados para reproduzir o *Aluguel de Equipamento* da referência (mínimos quadrados 2028-2031). | PR bate exato; BA/RN oscilam (ver P11) |
| 16 | **Capacidade de transporte corrigida.** `Dashboard!190` (GNL): BA e RN **34.000 → 24.000 m³**; `198` (GNC): **7.100 → 6.500**. Os 34.000 vinham de *Trailer size* (o cavalo mecânico), não da carga útil por viagem. A referência usa 24.000 para todo cliente GNL e 6.500 para GNC (`Premissas Gerais` 97-98 e fórmula `OPEX!1867`). | Frete variável do RN saiu de −2,46 para −0,58 mi |
| 17 | **Ciclo de transporte parametrizado por planta.** `Dashboard!187` (distância diária) e `189` (carga/descarga) só tinham a coluna do PR preenchida, e as três abas liam `$D$187`/`$D$189`. Preenchidas: distância diária BA **790** e RN **805** km/dia (calibradas pelo frete fixo da referência; o 450 do PR foi validado — o ótimo dá 435 com erro idêntico); carga/descarga replicada em 9 h. `BA!95` e `RN!95` passaram a ler suas próprias colunas. | Frete fixo da BA e do RN voltou ao alvo |
| 18 | **Cavalo mecânico criado.** Premissas `Dashboard!200` (*Yard tractor*: 39.000 / 37.143 / 39.000) e `201` (*Handling cost*: 11.600 / 18.900 / 18.900) R$/mês, e linha **103** (*Yard & handling*) nas cinco abas. São custos de pátio — não escalam com distância nem volume. Total de logística passou a `SUM(98:104)`. | +R$2,1 a 2,4 mi/ano |
| 19 | **Sinergia de equipamentos — mecanismo criado e desligado.** Premissas `Dashboard!202` (%) e `203` (data de início) e linha **104** (*Equipment synergy*) nas cinco abas, aplicando redução sobre o aluguel de equipamento. **Percentuais zerados espelhando a referência** — ver P12. | Zero (mecanismo pronto, desligado) |
| 20 | **Regás — compra de equipamentos modelada.** A referência compra 10 ISOs em out/2029 e para de alugá-los (desconto de R$130 mil/mês, rateado 32,26% PR · 38,71% BA · 29,03% RN). Criadas as premissas `Dashboard!210` (*ISOs purchased*: 1,7786 / 0,1181 / 1,7258) e `211` (*Purchase date* = out/2029); a linha 107 (*LNG Regas*) passou a descontar a quantidade comprada a partir da data. Quantidade base (`208`) recalibrada: PR 8,966 → **5,7897**; BA 10,628 → **8,6667**; RN 5,656 → **6,9935**. **CapEx não lançado**, espelhando a referência (ver P14). | Regás saiu de +0,56/+1,92 para **±R$0,4 mi** e passou a acompanhar a inflexão de 2029 |
| 21 | **Tarifa de ISO do regás parametrizada por planta.** `Dashboard!E206`/`F206` estavam **vazias** e as três abas liam `$D$206`. Preenchidas com a mesma tarifa (R$550,78/dia). Erro pego na verificação: ao apontar as fórmulas para as colunas próprias, o regás de BA e RN foi a zero. | Correção estrutural, sem efeito numérico |
| 22 | **Compressão — trocada de energia para aluguel flat.** Bloco novo `Dashboard!213-215` (*OpEx \| Compression*): **R$20 mil/mês** nas três plantas e data de início (**jul/26 · jan/27 · nov/26**). Linha **121** das cinco abas virou `IF(AI$3>=data, -custo, 0)/10^3` — sem inflação e sem volume, como a referência. | **Δ zero** de 2027 a 2032 |
| 23 | **Semente do IRR alavancado da BA.** `BA!D309` usava `IRR(...,-10%)`, fora da bacia de convergência — virou `#DIV/0!` quando o fluxo mudou. Trocada para `0%`, igual ao RN. Resultado: **11,236%**. | Corrige célula de erro; ver P16 |
| 24 | **Resíduo histórico de compressão na BA.** `BA!D121:AH121` ainda rodava a fórmula antiga de energia (o item 22 só reescreveu `AI:LP`) e gerava **R$231 mil de custo fantasma** em fev, mai e jun/26 — meses em que a BA teve volume de GNC. Não era realizado contábil. Zerado, alinhando à convenção de PR e RN (zero cravado em `D:AH`). | **Δ zero também no realizado**, 2024 a 2032 |
| 25 | **SG&A de planta conciliado.** Mapeamento acordado: Payroll←Salários · Insurance←Seguros · HSEQ←Segurança+Regulatório · Part Maintenance←Assist. Técnica+Serviços Gerais+Frota · Studies&Permits←Projetos de Engenharia · **Travel (linha nova 133)**←Viagens e Hospedagens · Contingency←zero. Premissas recalibradas por mínimos quadrados sobre 2027-2032 (`Dashboard!220, 226, 228, 229, 230, 231, 232`); `PR!132`, `PR!133` e `RN!132` religadas às premissas (tinham valor colado por cima); seguro deixou de inflar. | **±R$0,06 mi por planta** de 2027 a 2032 (era +0,37 / −0,71 / +0,14) |
| 26 | **Mês de pagamento do seguro do PR.** `Dashboard!D225` de dez → **maio**, espelhando a apólice única do PR na referência. | Gap da projeção de jul-dez/26 no PR: +571 → **−64 mil** |
| 30 | **Distância média do GNL em dois estágios.** Criadas `Dashboard!169` (*Avg. Distance \| phase 2*) e `170` (*Phase 2 start* = jan/2030). As linhas **95** (nº de caminhões → frete fixo) e **100** (frete variável) das três abas passaram a escolher a fase pela data. **RN: 557,2 → 355,5 km a partir de jan/2030** (cliente de longa distância sai — o nº de caminhões cai de 6 para 3,75). **PR: nível recalibrado de 454,4 → 380,5 km**, sem degrau. BA sem degrau. Calibragem por busca numérica replicando as fórmulas em Python, porque o `ROUNDUP` do nº de caminhões torna a relação não-linear. | RN 2030-33 de −3,80/−4,91 para **±0,09**; PR de −1,2/ano para **+0,2**; logística consolidada **≤ +1,5** |
| 29 | **SG&A de Holding — dois outliers calibrados.** `Dashboard!D250` (*Backoffice \| Administrative costs*) de **R$324.959 → R$143.341/mês**, contra *Administrativo + Comunicação + Opex ERP* da referência. `D246` e `D247` (*Personnel mobilization* e *Projects and Engineering*) escalados por **3,28×** como grupo, contra *Viagens*. Calibragem por mínimos quadrados sobre 2027-2033, contra a **soma correta 13:18** da referência, não contra o total dela (ver o bug em P23). Pessoal e *Prestação de serviço* deixados como estão. | Admin de −2,30 para **−0,10**; Viagens de +1,18 para **+0,14**; bloco de −2,95 para **−1,78** (2028) |
| 28 | **Seguro da dívida do RN e IOF do desembolso.** `Dashboard!F310` (*Debt Guarantee Cost*) de **0,606% → 1,300% a.a.**, igual à BA e à referência — o RN vinha cobrando metade. E o IOF pontual de **−R$3,0 mi em jun/2027** sobre o desembolso do PR, que não existia no nosso modelo, entrou cravado somando na fórmula de `PR!AT141`. | *Outras taxas*: 2028-2032 de +0,64/+0,41 para **±0,05**; 2027 de +2,99 para −0,65 |
| 27 | **Realizado de SG&A colado em jan-jun/26.** O bloco virava fórmula de projeção em mar/26 (PR, BA) e jan/26 (RN), antes da data-base. Colado o realizado da referência **por componente** (linhas 127-134, colunas `AC:AH`) nas três abas, pelo mesmo mapeamento do item 25 — com `134 Contingency` recebendo *Contigência + Outros*, as duas linhas de sobra. Conferido: a soma dos componentes fecha com o total da referência nos **18 pares mês/planta**. | Realizado jan-jun/26 bate **ao centavo** nos três |

| 31 | **Projeto Argentina criado.** Aba `AR` (cópia da `RN`, remapeada para a coluna **G** do Dashboard), premissas populadas da referência, `AR` somada em 68 linhas do `Consolidated`. A coluna G vinha populada como planta de liquefação própria (R$100 mi de equipamento, dívida, SG&A de planta) — descartada por decisão do usuário. Estrutura: só molécula + logística + regás, sem dívida. | AR isolada dentro de **±0,53** contra a referência |
| 32 | **Molécula da Argentina em dois estágios.** A referência não "declina" — dá um **degrau de contrato**: sobe 0,19%/trimestre de jul/28 a ago/30 e cai para R$1,8200/m³ em set/2030, flat até o fim. Usado o mecanismo de renegociação que já existia (`Scenario` / `Negotiated Price` / `Month of negotiation`), sem criar linhas. | EBITDA da AR de −3,01 para **−0,39** em 2033; **zero** de 2031 em diante |
| 33 | **CapEx da Argentina por fase, no tempo certo.** Medido na referência: logística **15 meses antes** da operação (parcela única), regás **nos 6 primeiros meses** da rampa (13,16/21,44/21,44/20,18/11,90/11,90 %). Mesmo intervalo aplicado à fase 2. Premissas condicionadas ao switch `Dashboard!C32` (Model / Phase 1 / Phase 1+2) e CapEx da fase 2 em **termos reais**. | Cenário `Model` bate a referência **mês a mês** |
| 34 | **Projeto SAL criado.** Aba `SAL` (cópia da `AR`, remapeada para a coluna **H**), somada em 68 linhas do `Consolidated`. Não existe na referência — especificação do usuário: Brumado/BA, cliente único Bahiagás, molécula liquefeita comprada da Eneva, **106.000 m³/dia sem rampa**, mar/2027 a fev/2037, preço **flat R$3,6359/m³**, molécula **12,75% do Brent**, logística com parâmetros da BA a **368 km**, CapEx da Argentina escalado por volume nos **3 meses anteriores** ao início, sem SG&A de planta e sem dívida. | EBITDA de R$56,6 mi (2027) a R$47,9 mi (2033) |
| 35 | **Fórmulas órfãs `#REF!` reconstruídas** nas colunas G (AR) e H (SAL) do resumo do Dashboard — 8 e 10 fórmulas. Estavam quebradas desde antes, escondidas pelo flag em "N". | — |
| 36 | **Todas as fórmulas de TIR protegidas por `IFERROR`.** 12 células em PR, BA, RN, AR e SAL estavam expostas; AR e SAL erravam porque não têm dívida. Valores existentes preservados. | Erros do modelo: **28 → 3** |
| 37 | **Premissa que faltava: distância diária do GNC.** A linha 96 (nº de caminhões GNC) dividia a distância por uma premissa da coluna do PR porque **o bloco GNC não tinha distância diária** — o de GNL tinha (linha 175), o GNC não. Criada `Dashboard!186` *Average daily distance* = **450 km/dia** em D:H, e a 96 repontada nas 5 abas. **Não era vazamento de coluna** — ver a armadilha abaixo. | Implica ~5 caminhões GNC na BA, consistente com a referência |
| 38 | **Botões Y/N da linha 37 ligados ao consolidado.** 68 linhas do `Consolidated` passaram a multiplicar cada termo pelo flag do projeto: `SUM(PR!D10*(Dashboard!$D$37="Y"), …)`. Mapa: **D=PR · E=BA · F=RN · G=AR · H=SAL · J=Holding**. Também as 60 células do bloco de NPV (`Consolidated!297-306`, colunas H:N) e as 6 do Exit no `Dashboard` (`F5:F11`). | Desligar um projeto o remove de volume, receita, EBITDA, NPV e Exit EV |
| 39 | **Comissão de emissão virou despesa.** Estava saindo do caixa (linha 175) e reduzindo o passivo, **sem passar pelo resultado** — desconto de emissão que nunca amortizava. Movida para a linha 141 (`Debt Guarantee Cost`), que já alimenta a 176 no fluxo; o passivo ficou pelo valor de face. Mesmo tratamento no `Consolidated!169`. | Check do PR: **4.548,50 → 0**; do Consolidated: **4.245,00 → 0** |
| 40 | **Última parcela de amortização aparada pelo saldo.** A fórmula repetia parcela fixa enquanto `amort.acum < emissão.acum`, sem aparar a última — ultrapassava. Agora `-MIN(parcela, MAX(0, BoP+emissão+juros−pagos))`. | RN: resíduo de **−811,39 → 0**; corrige defeito latente da BA (amortizava R$740 a mais) |
| 41 | **Resíduo de ponto flutuante no `EoP Debt` eliminado.** `BA!FB259` ficava em 1,6e-11 e propagava até 2050. `=IF(ABS(SUM(...))<0.001, 0, SUM(...))` nas 10 linhas de EoP. Checks uniformizados com `ROUND(...,2)`. | **Todos os 7 balanços em 0,000000**; zero células de dívida após a quitação |

### ⚠️ Arredondar saldo acumulado piora o resíduo

Tentei `ROUND(EoP, 2)` antes do `IF/ABS` e **piorou muito**: checks foram a 0,56 e surgiram 898 células residuais. Arredondar um saldo que alimenta o BoP do mês seguinte injeta erro a cada período, e a cadeia acumula por 325 meses — quanto mais grosso o arredondamento, pior. **Em série recursiva, zere o resíduo com `IF(ABS(x)<ε,0,x)`; nunca arredonde o elo da cadeia.**

### ⚠️ Como verificar sem se enganar

Três erros de *verificação* — não de modelagem — custaram tempo nesta rodada:

- **Tolerância frouxa esconde defeito.** Varri os saldos de dívida com `1e-9` e afirmei que a BA
  estava "totalmente zerada". Não estava: `BA!FB259` carregava `1,61e-11`, propagado até 2050 —
  foi o usuário que apontou. Para saldo que **deve** zerar, use **tolerância zero** e conte
  células, em vez de olhar o máximo.
- **Varrer colunas fora do período modelado gera falso positivo.** Reportei o balanço da Holding
  quebrado em R$15.615,59; era a varredura lendo células além dos meses modelados, num check
  que (ao contrário dos outros) não tinha `ROUND`. **A Holding estava correta**, e `-BH255` na
  linha 145 é competência, não erro. Os checks agora estão uniformizados com `ROUND(...,2)`.
- **`Evaluate` não serve para diagnosticar `#DIV/0!`.** Testando semente de TIR, `Evaluate`
  devolveu `-2146826273` (= `#VALUE!` gerado pelo próprio `Evaluate`), não o erro da célula.
  **Teste na célula real**, escrevendo e recalculando.

### Projetos novos — o que não vem da referência

**Argentina**: existe na referência e foi conciliado (ver itens 31-33). O switch `Dashboard!C32`
controla três cenários — `Model` (130.000 m³/dia, replica a referência), `Phase 1` (150.000) e
`Phase 1+2` (300.000, com CapEx dobrado em termos reais e desembolso deslocado para 2030).
**Sempre confira em qual cenário o switch está antes de comparar com a referência.**

**SAL**: **não existe na referência** — é especificação do usuário, então não há alvo de
conciliação. Pontos que merecem revisão:

- **Preço flat em contrato de 10 anos.** Receita fica em R$140,7 mi/ano, mas molécula (Brent),
  logística e regás sobem. O EBITDA cai de **R$60,6 mi (2028) para R$47,9 mi (2033)** — 21% de
  perda de margem. Se o contrato tiver reajuste, é trocar uma fórmula.
- **ISOs de transporte = 3,829**: escalado da BA por volume. A instrução foi "logística igual à
  BA", que li como as tarifas; a quantidade precisava vir de algum lugar.
- **Pátio e movimentação = zero**: a BA tem R$56 mil/mês, mas são custos de pátio de planta e o
  SAL recebe o GNL já liquefeito. Se houver pátio em Brumado, preencher `Dashboard!H190/H191`.
- **Base da molécula = R$2,3806/m³**, não R$1,9708. O `Factor Index` indexa relativo a
  `Dashboard!C24` (jun/2026), não à data-base contratual. Conferido: o resultado é 12,75% do
  Brent na quarta casa em todo mês.

### ⚠️ Armadilha ao duplicar abas

`Cells.Replace("Dashboard!$G", "Dashboard!$H")` **quebra intervalos de duas pontas**:
`SUM(Dashboard!$G$288:$G$289)` vira `SUM(Dashboard!$H$288:$G$289)`, que o Excel normaliza para
o retângulo G:H — somando dois projetos. Aconteceu em 4 linhas do `SAL` (10, 11, 29 e 235), e a
29 é a do volume: a aba nasceu com volume zero. **Depois de duplicar uma aba, varrer as
fórmulas atrás de intervalos com colunas diferentes.**

Duas outras heranças que só aparecem quando a aba nova usa uma linha que a original não usava:

- `AR!80` (*Factor Index*) veio da `RN` com **colar de Brent de piso/teto zerados**. A Argentina
  tem molécula flat e nunca usou; o SAL usa. Reescrito sem colar.
- `AR!76` (*Adjustment date*) apontava para `Dashboard!$D$141` — a frequência do **PR**.

### Mapa de linhas — situação em 05/08/2026

Inserções acumuladas: *Diesel Generator* (87), *Yard & handling* + *Equipment synergy*
(103/104) e *Travel and lodging* (133, só nas plantas). **Referências de linha de conversas
anteriores estão defasadas** — sempre remapear antes de editar.

> ⚠️ **As abas deixam de ser alinhadas a partir da linha 127.** Só 1-126 é comum. Da 127 em
> diante cada aba tem estrutura própria — ver a tabela específica abaixo. Comparar
> `PR!135` com `Consolidated!135` não faz sentido.

| Abas de planta / `Consolidated` — **só até 126** | Linha |
|---|---|
| LNG / CNG total volume · Service (m³) | 22 · 23 · 24 |
| LNG Volume (segmentos) · CNG Volume · Service (m³/dia) | 35 · 45 · 47 |
| Preços por segmento GNL · GNC | 53-58 · 63-68 |
| Gas cost (pricing, só PR) · Gas cost (custo efetivo) | 79 · 83 |
| **Liquefação**: Electricity · Diesel Generator · Utilities · O&M · Losses · Others | 86 · 87 · 88 · 89 · 90 · 91 |
| **Logística**: LNG/CNG Trucks | 95 · 96 |
| Fixed Freight LNG/CNG · Variable LNG/CNG · ISO Cost | 98 · 99 · 100 · 101 · 102 |
| **Yard & handling** · **Equipment synergy** | **103** · **104** |
| **Regás**: header · LNG Regas · CNG Decompression · Others | 106 · 107 · 108 · 109 |
| **DRE** (header 111): LNG · CNG · Fixed Rent · Service · Other | 113 · 114 · 115 · 116 · 117 |
| Net Revenue · Molecule · Liquefaction · Compression · Logistics · Regas · COGS | 118 · 119 · 120 · 121 · 122 · 123 · 124 |
| Gross Profit · Gross mg. (%) | 125 · 126 |

**Da linha 127 em diante — uma tabela por aba:**

| `PR` · `BA` · `RN` | Linha |
|---|---|
| Payroll · Profit Sharing Plan · Insurance | 127 · 128 · 129 |
| HSEQ · Part Maintenance · Studies And Permits | 130 · 131 · 132 |
| **Travel and lodging** · Contingency · **SG&A** · **EBITDA** | **133** · 134 · **135** · **136** |
| D&A · Financial result · EBT · Income taxes · Net Income | 138 · 142 · 143 · 144 · 145 |
| FCFE | 191 |
| Nominal Levered IRR | BA **310** · RN **321** · PR **323** |

| `Consolidated` | Linha |
|---|---|
| SG&A Plants · SG&A Holding · SG&A · **EBITDA** | 127 · 128 · 129 · **130** |
| D&A · Financial result · EBT · Income taxes · Net Income | 132 · 136 · 137 · 138 · 139 |

| `Holding` | Linha |
|---|---|
| Componentes próprios (CEO/Executives/Managers, Backoffice…) | 127-139 |
| **SG&A** · **EBITDA** | **140** · **141** |

🔴 **O `Dashboard` já foi reindexado quatro vezes.** Linhas removidas pelo usuário e inseridas
por mim (rampa da Argentina, datas do SAL). **O mapa abaixo é de 07/08/2026 e vale só até a
próxima inserção — confira uma âncora antes de qualquer edição.**

| `Dashboard` — âncoras verificadas em 10/08 | Linha |
|---|---|
| Resumo do topo (PR·BA·RN·**AR**·**SAL**·Corredor Azul·Holding·Consolidado) | 5-12 |
| `Assumptions` · **`Argentina phase`** (switch de cenário) | 23 · **32** |
| Flags Y/N · nomes dos projetos (D=PR … J=Holding, K=Consolidado) | **37** · **38** |
| `Capacity` (header) · `Volume` (header) | 56 · 74 |
| Tabela de volume LNG (incrementos por data) | **84-105** |
| `LNG Pricing` (header) · Industrial CIF | **120** · **121** |
| `CNG Pricing` (header) | 130 |
| `OpEx \| Molecule` (header) · Data-base · Frequency · Index | **139** · 140 · 141 · 142 |
| Contractual cost · Actual cost | 143 · **144** |
| Scenario · Negotiated Price · Month of negotiation | 147 · 148 · 149 |
| `OpEx \| Electricity` · `OpEx \| Liquefaction` | **151** · **162** |
| `OpEx \| Distribution` (header) | **170** |
| Fixed Freight · Variable Freight · daily distance · **Avg. Distance** | 173 · 174 · 175 · **176** |
| Avg. Distance phase 2 · Phase 2 start · carga/descarga · capacidade | 177 · 178 · 179 · 180 |
| Trailers · ISOs | 181 · 182 |
| `CNG` (sub-header) · Fixed · Variable · **daily distance** · Avg. Distance | 183 · 184 · 185 · **186** · 187 |
| carga/descarga · capacidade · Trailers · Yard tractor · Handling | 188 · 189 · 190 · 191 · 192 |
| Equipment synergy % · Synergy start | 193 · 194 |
| `OpEx \| Regasification` · LNG ISO Rent · CNG ISO Rent | **196** · 197 · 198 |
| LNG ISO Qty · CNG ISO Qty · ISOs purchased · Purchase date | 199 · 200 · 201 · 202 |
| `OpEx \| Compression` · Compression cost · Compression start | **204** · 205 · 206 |
| `Plant SG&A` · Employees · Avg. Salary · **Travel** · Contingencies | **208** · 210 · 211 · **222** · 223 |
| `Holding SG&A` · `CapEx` (headers) | **225** · **244** |
| Regas Infra · Avg. Infra Price · Regas Equip · Avg. Equip Price | 277 · 278 · 279 · 280 |
| Logistic/Operations · Contingencies | 289 · 290 |
| `Long Term Debt` (header) · % financiado · **Issued Value** | **296** · 297 · **298** |
| Maturity · Flat Fee · **Debt Guarantee Cost** · Frequency of payment | 299 · 300 · **301** · **304** |
| Conversion units: **MMBtu to m³ = 26,8081** · USD-BRL = 5,5 | C334 · C332 |

**Abas de projeto** (`PR`·`BA`·`RN`·`AR`·`SAL`): alinhadas até a **linha 78**; a 79 (*Gas cost*)
só existe no PR. DRE em 111-145 (118 Net Revenue · 124 COGS · 135 SG&A · **136 EBITDA** ·
142 Financial result · 145 Net Income). Bloco anual: **330 Net Revenues · 339 EBITDA** —
mas o do `PR` fica em **342 · 351**, dois acima. Fluxo de caixa 166-190 idêntico em todas.

*Mapa antigo, defasado pela reindexação — mantido só para leitura de conversas anteriores:*

| `Dashboard` (defasado) | Linha |
|---|---|
| Preços por segmento GNL · GNC | 133-139 · 142-148 |
| Fixed Rent (aluguel de equipamento a clientes) | 140 |
| **Energia**: Energy Cost · ICMS Credit | 164 · 165 |
| base load 0,35 MW · min load 0,55 MW · horas 1.000 | 167 · 168 · 169 |
| LNG load per train 0,48 MW · CNG Equipments · Diesel Generator | 170 · 171 · 172 |
| **Liquefação**: O&M · Utilities · Others · Losses % | 175 · 176 · 177 · 178 |
| Purge recovery (% do GNC) · Purge recovery (fixo) | 179 · 180 |
| **Distribuição GNL**: Fixed Freight · Variable Freight · distância diária | 185 · 186 · 187 |
| Avg. Distance · carga/descarga · capacidade · Trailers · ISOs | 188 · 189 · 190 · 191 · 192 |
| **Distribuição GNC**: Fixed · Variable · Avg. Distance | 194 · 195 · 196 |
| carga/descarga · capacidade · Trailers | 197 · 198 · 199 |
| **Yard tractor · Handling cost · Equipment synergy % · Synergy start** | **200 · 201 · 202 · 203** |
| **Regás** (header 205): LNG ISO Rent · CNG ISO Rent · quantidades | 206 · 207 · 208 · 209 |
| **ISOs purchased · Purchase date** | **210 · 211** |
| **Compressão** (header 213): Compression cost · Compression start | **214 · 215** |
| **Plant SG&A** (header 217): Employees · Avg. Salary · Benefits · Bonus | 219 · 220 · 221 · 222 |
| Insurance (on CapEx) · Month of Payment · Insurance coverage | 224 · 225 · 226 |
| HSEQ · Part Maintenance · Studies and Permits · **Travel** · Contingencies | 228 · 229 · 230 · **231** · 232 |
| Holding SG&A (header) · CapEx (header) | 234 · 253 |
| Liquefaction train capacity · ISO Container size (bloco *Others*) | 350 · 351 |

### Status da receita após esses ajustes

| Ex-serviço sem molécula | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| Δ vs. referência (R$ mi) | −4,99 | −1,00 | −0,53 | +0,23 | +0,17 |
| Δ % | −2,3% | −0,4% | −0,2% | +0,1% | +0,1% |

Volume, custo da molécula e D&A já batiam antes destes ajustes.

---

## Pendências

### P1 — Resíduo do PR em 2027 (−R$4,2 mi, pontual)

O GNL do PR fica −R$4,18 mi abaixo da referência em 2027, contra −R$0,32 mi em 2028
e ~−0,3 depois. É a janela de transição nov/26–jan/27: a referência reajusta o preço no
aniversário contratual de **cada cliente**, o nosso modelo reajusta trimestralmente em
fev/mai/ago/nov para o segmento inteiro.

**Recomendação: não corrigir.** Exigiria coortes de preço por data-base de contrato
(a "Opção C" descartada), multiplicando as 12 linhas de segmento por N safras em cada
aba de planta. Efeito restrito a um ano.

### P2 — ~~Serviço sem molécula~~ ✅ RESOLVIDO em 06/08 pelo usuário, no modelo referência

**O usuário corrigiu a indexação do serviço na referência em 06/08.** O gap saiu de **+R$9,0
mi** para **+R$0,81 mi** em 2028. O volume de serviço é idêntico nos dois modelos (12,37
milhões de m³ em 2028), então o resíduo é preço.

| Serviço s/ molécula (R$ mi) | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 |
|---|---|---|---|---|---|---|---|
| Referência | 10,94 | 15,03 | 15,55 | 9,45 | 9,15 | 9,49 | 9,79 |
| Nosso | 12,15 | 15,84 | 16,37 | 7,86 | 7,26 | 7,53 | 7,78 |
| **Δ** | +1,22 | +0,81 | +0,82 | **−1,59** | −1,89 | −1,96 | −2,02 |

**O sinal inverte em 2030** — exatamente quando a Bahiagás-BRU sai. É o P3 (mix de serviço
congelado na BA), não mais o erro de indexação.

O diagnóstico original está preservado abaixo, para registro do que era o erro.

---

*Diagnóstico original (03/08):*

O fator de reajuste da referência (`Variável!434`) é:

```
fator = (mol_base/preço) × fator_Brent + (1 − mol_base/preço) × fator_IPCA
```

Ele pressupõe que o preço embute a molécula. Em contratos de serviço isso é falso — o
preço cobre só logística e regás e fica **abaixo** do custo da molécula da planta. Resultado:
`mol_base/preço > 1`, com peso acima de 100% no Brent e peso **negativo** no IPCA.

| Contrato | preço | mol. base | alavancagem | fator jun/27 | jun/28 | jun/29 |
|---|---|---|---|---|---|---|
| BA Bahiagás-BRU GNC | 0,89 | 2,095 | **2,35×** | 0,665 | 0,263 | **0,190** |
| BA Algás - Serviço | 1,81 | 2,095 | 1,16× | 0,782 | 0,632 | 0,650 |
| RN Petroconcavo GNC | 1,00 | 1,525 | 1,53× | 0,783 | 0,679 | 0,697 |
| RN PetroReconcavo GNL | 1,3155 | 1,525 | 1,16× | 0,835 | 0,767 | 0,790 |

No Bahiagás-BRU o preço cai de R$0,89 para R$0,157/m³ — 82% de queda num contrato de
pura prestação de serviço, com volume constante em 600.000 m³/mês.

Nosso modelo fica dentro de 2-4% do cenário economicamente limpo (preço de contrato + IPCA),
então o gap de ~R$9 mi/ano em 2028-29 é distorção da referência.

**Ação sugerida:** reportar a quem mantém o modelo referência. A correção lá é simples —
usar fator IPCA puro quando `Custo Molécula = 0`, flag que já existe na coluna J da aba
`Clientes`.

### P3 — Mix de serviço congelado na BA (~R$2 mi/ano a partir de 2030)

Erro **nosso**, ainda não corrigido. O preço de serviço é um único blend por planta,
fixado em jun/26:

```
BA = (7.800 × 1,81 + 20.000 × 0,89) / 27.800 = 1,148
```

Quando o Bahiagás-BRU (contrato barato, 20.000 m³/d) sai em jan/30 e sobra só o Algás
a 1,81, o preço deveria subir para ~2,10 e fica em 1,36.

**Correção proposta:** separar o serviço por entrega (CIF/FOB). Algás é CIF e Bahiagás-BRU
é FOB, então separam perfeitamente; no RN os dois são FOB e o blend de 1,2103 continua
correto, sem introduzir erro. Linhas **46, 48, 70 e 72 livres** nas abas de planta
(o aluguel fixo acabou ficando na própria linha 111, sem linha auxiliar).

Não foi feito porque aumentaria o gap contra a referência (que está distorcida, ver P2).

### P4 — Degrau de mix na BA em 2030 nos preços de segmento

Dos 13 buckets recalibrados, 11 ficaram dentro de ±0,02 R$/m³. Os dois da BA oscilam ±0,10
porque um preço-base constante não captura a troca de mix de jan/30 (substituição do
Bahiagás-BRU, com os substitutos reclassificados entre Industrial e Distribuidora).

| Bucket | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|
| BA GNL Industrial CIF | −0,098 | −0,098 | +0,031 | +0,039 |
| BA GNL Distribuidora CIF | +0,013 | +0,024 | −0,049 | −0,060 |

**Correção proposta ("Opção B"):** curva de preço com degraus datados por segmento,
espelhando o padrão que o Dashboard já usa para volume (linhas 79-110). ~35 células novas
e fórmula nova nas linhas 53-58/63-68 das três abas. Vale ~R$0,5 mi/ano.

**Nota de premissa:** conciliar a BA em 2030 significa importar uma premissa da referência
que é questionável — lá os contratos que substituem o Bahiagás-BRU entram a R$3,64
**nominais**, o mesmo preço nominal de hoje, ou seja ~15% de queda real até 2030.

### P5 — Bloco de preços do Dashboard desconectado da Modelagem contratual

As células `Dashboard!D133:F148` eram fórmulas matriciais
`Σ(volume contratado × preço) / Σ(volume contratado)` puxando da aba `Modelagem contratual`.
Foram substituídas por valores fixos na recalibração (item 2), com colagem de valores
confirmada pelo usuário.

**Consequência:** editar um contrato na `Modelagem contratual` **não** atualiza mais os
preços de segmento. É preciso rodar a calibração de novo.

A ponderação original também tinha um defeito próprio: pesava pelo **volume nominal do
contrato**, sem considerar quando cada contrato entra ou termina — por isso Compagás-Lapa
(20.000 m³/d, encerra dez/27) pesava igual em 2031, e Industrial e Distribuidora do PR
saíam praticamente idênticos (3,7245 vs 3,7215). Testei reponderar por duração e **não
resolve** — em vários buckets move na direção errada.

### P6 — Inconsistência na contagem de caminhões entre abas

`PR!93` calcula a frota a partir de `(AO29+AO31+AO33)` — só volume CIF.
`BA!93` e `RN!93` usam `AO35`, que é **todo** o volume GNL, CIF e FOB.

Hoje sem efeito: verificado que BA e RN têm volume GNL FOB **zero** em 2029 (todo o GNL é
CIF nas três plantas). Mas se entrar um cliente GNL FOB em BA ou RN, elas vão dimensionar
frota para volume que o cliente retira sozinho.

**Ação:** alinhar as três fórmulas quando mexermos em logística.

### P8 — Volume de serviço GNL fora do driver de energia da liquefação

A linha 86 (*Electricity*) usa `AO35` (volume GNL dos segmentos), que **exclui** a linha 47
(serviço sem molécula). Mas a GNLink liquefaz esse volume — o cliente só não compra a
molécula.

A referência inclui: o driver de energia dela (`OPEX!104` para o RN) marca **74.419 m³/dia**
em 2029 contra 70.419 do nosso `RN!35`. A diferença de 4.000 m³/dia é exatamente o
PetroReconcavo FOB GNL. PR e BA batem (o PR não tem contrato de serviço e o serviço da BA
é todo GNC, que vai para compressão, não liquefação).

**Correção proposta:** trocar `AO35` por `AO35 + AO47` na linha 86 — ou, mais preciso, somar
só a parcela GNL do serviço, o que exigiria separar a linha 47 por molécula.

Efeito em regime: ~zero, porque com o divisor de 22.000 tanto 70.419 quanto 74.419 arredondam
para 4 trens. Importa nos anos de rampa e conceitualmente. Baixa prioridade, mas fica
registrado porque é o mesmo tipo de erro de driver do item 5.

Nota: isso **não** contradiz o item 3 (remoção do serviço do frete). Serviço FOB é liquefeito
pela GNLink mas retirado pelo cliente — consome energia, não consome frete.

### P7 — Diferenças no realizado do 1S26

Duas linhas divergem só na parte histórica (valores hardcoded, não premissas):

- **Custo da molécula:** mai/26 e jun/26 diferem (PR 2,370 vs 2,224; BA e RN com dispersão
  maior). De jul/26 em diante as trajetórias são idênticas.
- **Aluguel fixo:** nosso histórico jan-jun/26 soma ~R$0,58 mi contra ~R$0,35 mi da
  referência (que registra um pico pontual de R$46,7 mil no Petrobahia em jun/26).

Efeito: 2026 fica +R$0,22 mi acima na receita de aluguel fixo. Não é premissa — é
back-solve de realizado. Baixa prioridade.

---

## Gaps ainda não investigados (custos e financeiro)

Decomposição do gap de EBITDA remanescente (~R$21 mi em 2028, nosso modelo **acima** da
referência):

### Onde a conciliação está (2028)

⚠️ **A tabela abaixo é dos três projetos brasileiros.** Argentina entrou depois (itens 31-33) e
está conciliada em separado; **SAL não existe na referência** e não tem alvo. Ao comparar o
consolidado, confirme antes que o switch `Dashboard!C32` está em `Model`.

| Bloco | Gap vs. referência | Status |
|---|---|---|
| Volume · Custo da molécula · D&A · Saldo de dívida | 0 | ✅ já batiam |
| Receita GNL/GNC (ex-serviço) | −0,4% | ✅ itens 1-2 |
| Aluguel fixo | ±R$0,01 mi | ✅ item 4 |
| **Liquefação** | **±R$0,05 mi** | ✅ itens 5-13 |
| **Logística** | **+R$0,19 mi** | ✅ itens 14-19 |
| **Regás** | **−R$0,28 mi** | ✅ itens 20-21 |
| **Compressão** | **zero, inclusive no realizado** | ✅ itens 22-24 |
| **SG&A de planta** | **−R$0,03 mi** | ✅ itens 25-27; realizado ao centavo |
| CapEx (CFI) | −R$0,15 mi | ✅ ver P14 |
| SG&A de Holding | não medido | ❌ R$27-35 mi/ano, não investigado |
| **Serviço sem molécula** | **+R$0,8 mi** | ✅ P2 — resolvido pelo usuário na referência em 06/08 |
| **Logística** | **+R$1,5 mi** | ✅ item 30 (degrau no RN + nível do PR) |
| Despesa de juros | +R$0,6 mi | ✅ já batia |
| **Outras taxas da dívida** | **±R$0,05 mi** | ✅ item 28; 2026-27 em P21 |
| **Resultado financeiro** | **+R$1,4 mi** | ✅ P19 — resolvido pelo usuário na referência em 06/08 |
| **SG&A de Holding** | **−R$1,8 mi** | ✅ item 29; resíduo e bug da referência em P23 |
| **Argentina** (EBITDA da aba) | **−0,34 a +0,53** | ✅ itens 31-33 |
| SAL | sem alvo | — não existe na referência |

**Consolidado dos 5 projetos, EBITDA 2030 = R$152,8 mi** · volume 516.444 m³/dia. Por projeto:
PR 25,4 · BA 22,3 · RN 31,3 · **AR 48,7** · **SAL 56,4** · Holding −31,3.

### P24 — Pendências abertas do modelo (não são gaps de conciliação)

1. **`Consolidated!251`** — teto de Net Debt/EBITDA para caixa mínimo. Ficou fora das duas
   varreduras automáticas (a fórmula não é `SUM` de plantas), então **não inclui AR nem SAL
   e não responde aos flags Y/N**. Precisa de decisão manual.
2. **Corredor Azul** (coluna I do Dashboard) — **8** `#REF!` órfãos, não 3 como esta nota dizia:
   linhas **41, 42, 45, 46, 49, 50, 52 e 53**. Piorando, **`I52` e `I53` testam `G37`** (o flag da
   AR) em vez de `I37` — se a AR estiver ligada, o Corredor Azul desligado ainda tenta calcular
   dívida. Só aparece quando o projeto for ligado. Reconstruir espelhando a coluna G, como foi
   feito para AR e SAL no item 35.
3. **P15 continua** — premissas com só a coluna do PR preenchida. Já corrigidos: 170, 187/189,
   206, 171. Ainda não varridos: frete e capacidade de GNC.
4. **`Dashboard!D301`** (*Debt Guarantee Cost* do PR) **= 0**, enquanto BA e RN estão em 1,30%.
   O PR é justamente quem tem dívida. Pode ser premissa deliberada — não mexi. Note que
   G301 e H301 estão em 2,0% herdados da cópia da RN, mas são inertes (AR e SAL são 100% equity).
5. **Linhas de flag do cronograma de dívida** ficam em 1 para sempre, mesmo após a quitação.
   5 células, sem efeito numérico — a amortização já é aparada pelo saldo (item 39).
| IR/CSLL | +R$2,4 mi, subindo a +6,1 | ❌ ver P22 |
| Saldo de dívida | −R$8 mi persistente | ❌ ver P20 |

O realizado da BA foi conferido linha a linha contra a referência em fev, mai e jun/26 —
molécula, liquefação, logística e regás batem **ao real**, nos três meses. A referência tem
um bloco de conferência próprio (`OPEX!2479-2481`) confirmando que o realizado de compressão
dela é zero nas seis regiões.

**SG&A de planta**: conciliado nos itens 25-27. Realizado jan-jun/26 ao centavo; projeção
dentro de ±R$0,06 mi por planta de 2027 a 2032. O único resíduo é jul-dez/26 (−R$0,27 mi
consolidado), de descasamento de mês do seguro — ver P18.

**SG&A de Holding ainda não foi conciliado**: R$27-35 mi/ano, quase quatro vezes o de
planta. Nunca foi comparado com a referência.

> Correção: uma versão anterior desta nota comparava `127` (só *Payroll*) contra o SG&A
> total da referência. As abas **não são alinhadas a partir da linha 127** — nas plantas o
> total de SG&A é a **linha 134** e o EBITDA a **135**; no `Consolidated`, 129 e 130. Ver
> o mapa corrigido abaixo.

**EBITDA consolidado 2028: R$46,5 mi contra R$40,1 mi da referência** — gap de +6,5,
praticamente todo o serviço sem molécula (P2).

Trajetória do gap de EBITDA em 2028 ao longo do trabalho: +19,3 (após receita) → +4,6
(tarifa de energia) → +7,9 (sem indexação) → +6,9 (gerador) → +6,5 (cenário C) → +13,7
(Others da liquefação) → +6,5 (logística).

### Gap de logística por ano — o que ainda abre

| Δ vs. referência (R$ mi) | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| PR | +1,47 | +0,60 | +1,18 | +1,19 | +1,32 |
| BA | +0,28 | +0,15 | +0,54 | −0,59 | −0,57 |
| RN | −1,47 | −0,94 | −0,35 | **+3,80** | **+4,50** |
| **Consolidado** | −0,29 | **+0,19** | −1,38 | **−4,40** | **−5,26** |

### P9 — Energia: premissas adotadas da referência, a validar

Os itens 6 a 9 alinharam a energia à referência. **A eletricidade do PR e da BA agora bate
exatamente**, e o RN fica +R$0,30 mi/ano (causa em P8). Mas três premissas foram importadas
da referência e merecem validação de negócio:

**1. Tarifa.** Adotamos R$390,00 (PR), R$426,02 (BA) e R$565,42 (RN) por MWh, contra os
R$243,95 / R$306,05 / R$358,40 que estavam no modelo. Se os valores originais vinham de
contrato assinado ou de fatura, **estávamos certos e a referência está cara** — nesse caso
o item 6 deve ser revertido.

**2. Crédito de ICMS zerado.** Era 19% (PR) e 20,5% (BA). A referência não tem esse conceito.
Se a GNLink de fato recupera ICMS sobre energia, o certo seria manter o crédito e usar tarifas
brutas de R$481,48 (PR) e R$535,87 (BA) para chegar no mesmo líquido.

**3. Sem indexação.** A energia ficou constante em termos nominais até 2038 — queda de ~30%
em termos reais no horizonte. Replica a referência, mas num modelo nominal é uma premissa
conservadora na receita e agressiva no custo.

**4. Convenção de 1.000 h/mês.** Um mês tem ~730 h. Na referência o par (MW linear, 1.000 h)
funciona como parametrização conjunta: os 0,35 e 0,48 MW não são potência de placa, são
coeficientes calibrados. Adotamos o mesmo — fecha o gap, mas a leitura física se perde.

### P14 — Regás: a referência reduz OpEx sem lançar CapEx

A referência declara a compra de 10 ISOs de 18 bar em **out/2029** (`OPEX` 1974-1988:
*Equipamentos Comprados* = 10, *Custo Leasing/dia* = US$43, *Data de Compra* = set/2029) e
a partir daí credita **R$130 mil/mês** de aluguel evitado, mais um lançamento pontual de
−R$854 mil em set/2029.

**Mas o CapEx dela em 2029 é zero**, nas três plantas (conferido no fluxo de investimentos
do `Demonstrativo Financeiro Anual`, linhas 200-208). Ou seja: o custo de aluguel some sem
que a compra apareça como desembolso.

Por decisão do usuário (05/08), **replicamos o efeito no OpEx e também não lançamos CapEx**
— espelhando a referência. Se a compra for real na operação, o certo é modelá-la nos dois
lados, e aí divergimos da referência de propósito.

Comparativo de CapEx entre os modelos (CFI consolidado, R$ mi):

| | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| Referência | −44,53 | −5,48 | −2,47 | 0,00 | −1,79 |
| Nosso | −43,72 | −7,93 | −2,62 | 0,00 | 0,00 |
| Δ | +0,81 | **−2,45** | −0,15 | 0,00 | **+1,79** |

Sobram dois desvios não investigados: adiantamos R$2,45 mi de investimento em 2027 e não
temos o CapEx de R$1,79 mi da BA em 2030.

### P15 — Varredura: premissas com só a coluna do PR preenchida

Padrão recorrente — uma premissa existe só na coluna D e as três abas de planta a leem,
herdando o parâmetro do PR. Já corrigidos:

| Premissa | Onde | Item |
|---|---|---|
| Potência de liquefação | `Dashboard!170` | 5 |
| Distância diária · carga/descarga | `187` · `189` | 17 |
| Tarifa de ISO do regás | `206` | 21 |
| Potência do equipamento de GNC | `171` | 22 (linha eliminada) |

O caso do `171` foi o pior: só a **coluna da BA** estava preenchida (0,254 MW), PR e RN em
zero. A compressão de PR e RN dava zero apesar de 17.496 e 15.496 m³/dia de GNC, e a BA
gerava R$0,95 mi/ano sozinha a partir de 2030. Passou despercebido porque o resultado era
zero, não erro. A linha foi substituída no item 22, então o `171` ficou órfão.

**Ainda não varridos.** Candidatos visíveis: `194`/`195` (frete fixo e variável do GNC),
`197`/`198` (carga/descarga e capacidade do GNC), `207` (tarifa de ISO do GNC) — todos com
só a coluna D preenchida e lidos pelas três abas. Vale uma varredura sistemática antes de
mexer em qualquer coisa nesses blocos.

### P20 — Saldo de dívida: PR e RN tomam menos que a referência

Depois do item 28, sobra a diferença de principal. A BA bate; PR e RN não:

| Saldo fim de ano (R$ mi) | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 |
|---|---|---|---|---|---|---|
| PR Δ | −4,5 | −4,5 | −4,5 | −3,4 | −3,4 | −3,4 |
| BA Δ | +0,2 | −0,1 | −0,3 | −0,4 | −0,4 | −0,3 |
| RN Δ | −3,1 | −3,1 | −4,2 | −4,8 | −5,1 | −5,1 |

É **desembolso menor**, não amortização diferente — o perfil de amortização acompanha. O PR
desembolsa R$95,5 mi contra R$100,0 mi da referência; o RN, R$92,5 contra R$95,6.

Suspeita não confirmada: `Dashboard!306` (*% of CapEx financed* = 98,73%) aplicado sobre um
CapEx que difere um pouco do da referência — e o CapEx tem os desvios do P14 (−2,45 mi em
2027, +1,79 em 2030). Mexer em desembolso de dívida sem entender a origem é arriscado.

Há também **diferença de timing em 2026**: a referência desembolsa os R$100 mi do PR em 2027;
nós, em 2026. Não afeta 2027 em diante.

### P21 — Encargos de 2026-2027: dívida-ponte tratada de forma diferente

Resíduo de *Outras Taxas* depois do item 28: **+0,36 em 2026 e −0,65 em 2027**, zerando de
2028 em diante.

Nosso lado: a Holding tem dívida-ponte (`Holding!258`, média de R$56,5 mi em 2026 e R$33,2 mi
em 2027, zero depois) com custo de garantia de **2% a.a.** (`Dashboard!I310`) — dá −1,12 e
−0,66. A referência não tem essa linha; ela tem **comissões** (`Dívida!65`: −R$62 mil/mês de
jan a jun/26 e −R$1,0 mi em jul/26) e uma comissão de −R$295 mil em jun/26 no projeto do RN.

São encargos diferentes sobre o mesmo financiamento-ponte, de ordem de grandeza semelhante e
restritos a 2026-2027. Não perseguido.

### P19 — ~~Resultado financeiro~~ ✅ RESOLVIDO em 06/08 pelo usuário, no modelo referência

**Histórico.** A referência calculava receita financeira sobre caixa negativo
(`'Demonstrativo Financeiro Mensal'!385 = Caixa(mês anterior) × %CDI`), o que produzia uma
"receita" de −8,29 mi em 2028 caindo a −14,06 em 2032, e um gap de **+R$8,4 a +15,0 mi/ano**.
A causa não era taxa nem encargo: os cronogramas de dívida batiam (saldo Δ de −4 a −9 mi,
fluxo líquido dentro de ±3,5 mi/ano). Era estrutura de capital — o nosso modelo tem um plug
de aporte (`Consolidated!176`, piso de caixa de ~R$10,3 mi em `292`) que injeta **R$113 mi em
2027 e R$143 mi acumulados** até 2033; a referência deixava o déficit descoberto e cobrava CDI.

**Em 06/08 o usuário zerou essa linha na referência.** Resultado:

| Resultado financeiro (R$ mi) | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 |
|---|---|---|---|---|---|---|---|---|
| Referência | −37,77 | −40,75 | −29,63 | −27,80 | −25,32 | −21,61 | −18,09 | −14,37 |
| Nosso | −37,68 | −39,57 | −28,26 | −26,14 | −24,30 | −21,12 | −17,50 | −13,88 |
| **Δ** | +0,08 | +1,17 | +1,37 | +1,66 | +1,02 | +0,49 | +0,59 | +0,49 |

Resíduo: **receita financeira +0,74 a +0,85/ano** (nosso caixa positivo rende 90% do CDI; o
dela, negativo, não rende nada) e **despesa de juros oscilando ±1**, que é o P20 se propagando.

⚠️ **O caixa da referência continua negativo** — −86 mi em 2027 a −126 mi em 2033. Ela apenas
parou de cobrar juros, ou seja, passou a assumir financiamento gratuito e ilimitado do
déficit. As linhas ficaram comparáveis, mas o requisito de capital continua invisível do lado
dela, enquanto do nosso está explícito em R$143 mi. **Para comitê, é essa a diferença que
importa, não a linha de resultado financeiro.**

### P23 — SG&A de Holding: bug de dupla correção na referência + gap estável de R$3 mi

🔴 **O bug contamina a comparação de EBITDA.** `'Demonstrativo Financeiro Anual'!187` (*Matriz*)
puxa `Holding!23`, e o EBITDA da referência (`98`) puxa dali. Ou seja, **a referência subestima
o próprio EBITDA** pelo valor do bug, e isso vem favorecendo a nossa comparação:

| EBITDA (R$ mi) | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 |
|---|---|---|---|---|---|---|---|
| Referência como está | 22,95 | 48,23 | 52,63 | 45,99 | 50,69 | 53,90 | 55,85 |
| Referência sem o bug | 23,45 | 49,79 | 55,24 | 49,96 | 55,78 | 60,31 | 63,70 |
| Nosso | 16,65 | 47,65 | 51,82 | 42,33 | 46,13 | 49,31 | 51,65 |
| Δ como está | −6,30 | **−0,59** | −0,81 | −3,65 | −4,56 | −4,59 | −4,21 |
| **Δ se corrigir** | −6,80 | **−2,14** | −3,42 | −7,62 | −9,65 | −11,01 | **−12,06** |

Em 2033 a diferença entre as duas leituras é de R$7,9 mi. **Qualquer conclusão sobre EBITDA
tirada da referência como está é otimista a nosso favor.**

**Bug na referência (o 5º encontrado).** `Holding!23` (*Total SG&A*) é `=SUM(13:18)*21`, onde
`21` é o fator de correção de IPCA. Mas as linhas **13, 14, 16, 17 e 18 já trazem `*21` dentro
da própria fórmula** — só *Viagens* (15) escapa, porque usa fórmula de elasticidade a volume.
O total é corrigido duas vezes:

| R$ mi | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 |
|---|---|---|---|---|---|---|---|---|
| Total da referência (23) | −25,87 | −26,50 | −28,76 | −31,17 | −34,10 | −36,03 | −38,29 | −40,67 |
| Soma correta (13:18) | −25,87 | −26,00 | −27,21 | −28,56 | −30,13 | −30,94 | −31,87 | −32,82 |
| **Efeito do bug** | 0,00 | −0,50 | −1,55 | −2,61 | −3,97 | −5,09 | −6,42 | **−7,85** |

Em 2033 o bug infla o bloco em **24%**. Como `Holding!65` e a linha *Matriz* do fluxo de caixa
puxam de `23`, o erro se propaga para o EBITDA e o fluxo consolidados da referência.

**Contra o total corrigido**, somos R$2,3 a 3,4 mi/ano mais caros, de forma estável — não é
problema de crescimento, é de nível:

| Grupo (Δ = nosso − ref, 2028) | Δ | Situação |
|---|---|---|
| Pessoal (`127-134` ← *Pessoal - Matriz*) | −0,74 | quase bate; nossa folha cresce 5,2% a.a. contra 4,5% |
| Administrativo + Comunicação + ERP (`138`) | **−2,30** | nosso R$3,94 mi contra R$1,64 mi — maior item |
| Prestação de serviço (`137`+`139`) | −1,09 | nosso 3,15 contra 2,06 |
| Viagens (`135`+`136`) | **+1,18** | nosso 0,45 contra 1,63 — subdimensionado |

Nossa estrutura é bottom-up (CEO · Executives · Managers · Payroll, cada um com headcount,
salário e bônus); a da referência é um lump de *Pessoal - Matriz* dirigido por headcount ×
custo médio de R$12 mil/mês. A nossa é mais granular e provavelmente melhor fundamentada —
por isso o Pessoal não foi calibrado contra ela.

**Situação após o item 29** (Δ contra a soma correta 13:18):

| R$ mi | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 |
|---|---|---|---|---|---|---|---|
| Total | −1,91 | −1,78 | −1,58 | −1,20 | −1,63 | −2,00 | −2,40 |
| ↳ Pessoal | −1,05 | −0,74 | −0,51 | −0,17 | −0,57 | −0,93 | −1,32 |
| ↳ Prestação de serviço | −1,11 | −1,09 | −1,07 | −1,04 | −1,03 | −1,01 | −0,98 |
| ↳ Admin+Com+ERP | −0,15 | −0,10 | −0,05 | 0,00 | +0,05 | +0,09 | +0,14 |
| ↳ Viagens | +0,40 | +0,14 | +0,06 | 0,00 | −0,09 | −0,16 | −0,24 |

⚠️ **Efeito colateral da calibragem de Viagens.** O grupo foi escalado uniformemente, então
`Dashboard!D247` (*Projects and Engineering*) foi de R$22.229 para **R$72.926/mês** — 3,3× —
para representar despesa de viagem. **O rótulo dessa linha não descreve mais o conteúdo.**

A causa é que a Holding não tem linha de viagem no nosso modelo. O certo seria criar uma
*Travel and lodging* na Holding, como foi feito nas plantas no item 25, e devolver o `D247`
ao valor original. Uma linha, na aba `Holding` e no `Dashboard`.

**Sobra R$1,8 mi/ano**, quase todo em *Prestação de serviço* (−1,09) e *Pessoal* (−0,74).

### P22 — IR/CSLL: a referência paga imposto sobre prejuízo

| IR/CSLL (R$ mi) | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 |
|---|---|---|---|---|---|---|---|
| Referência | −1,45 | −2,70 | −3,39 | −4,48 | −7,77 | −9,16 | −10,50 |
| Nosso | 0,00 | −0,34 | −1,72 | −0,25 | −1,71 | −3,64 | −5,35 |
| **Δ** | +1,45 | +2,35 | +1,67 | +4,22 | +6,07 | +5,52 | +5,14 |

Em 2028 a referência recolhe R$2,70 mi com **EBT de −R$7,03 mi**. Alíquota efetiva dela em
2031-2033: **97% / 63% / 52%**, contra 26% / 27% / 28% nossa.

Causa provável, não investigada: apuração **por empresa** e não consolidada — uma planta
lucrativa recolhe mesmo com o consolidado no prejuízo — possivelmente somada a lucro presumido
ou ausência de compensação de prejuízo fiscal.

### P17 — ~~SG&A: o realizado do 1S26 não é realizado~~ ✅ RESOLVIDO (item 27)

O bloco de SG&A trocava para fórmula de projeção em **mar/2026** (PR, BA) e **jan/2026**
(RN), antes da data-base de jul/2026. Colado o realizado da referência por componente.

**Fica registrado o motivo de não termos estendido para 2024-2025**: naquele período os
**componentes da própria referência não fecham com o total dela** em 9 pares mês/planta —
PR set/24 +11,8 mil, fev/25 +17,4, mar/25 +24,8, jul/25 −34,5, e RN out/25 +44,5. O bloco
de conferência dela (`OPEX!2483-2496`) valida só o agregado das seis regiões, onde as
diferenças se cancelam. Como nosso total anual de 2024/2025 já bate (PR exato, BA −0,01),
colar ali importaria inconsistência sem ganho.

Resíduo remanescente do RN: **+0,04 em 2024 e −0,11 em 2025** — deslocamento de um item de
R$0,11 mi entre os dois anos. Não perseguido.

### P18 — Seguro: uma apólice por planta × várias na referência

A referência tem **cinco apólices** na BA (mar, jun, jul, set, dez) e cinco no RN (jan, abr,
mai, jul, out). O nosso modelo tem uma premissa única de mês de pagamento por planta.

O **anual bate exato** (PR 636 · BA 997 · RN 972, constantes) e o PR foi alinhado no item 26
porque lá a referência tem apólice única. BA e RN não têm como bater no mês sem modelar
múltiplas apólices.

Depois do item 27, **este é o único resíduo de 2026**, e é inteiramente de jul-dez (meio ano
de projeção): PR −0,06 · BA −0,72 · RN +0,51 · consolidado **−0,27**. BA e RN quase se
cancelam. Não vale modelar cinco apólices por planta a menos que o fluxo de caixa mensal de
2026 importe para alguma decisão.

### P16 — IRR alavancado do PR não converge

`PR!D322` = `IFERROR((1+IRR(E190:LP190,-10%))^12-1,"n/a")` devolve **"n/a"** — testei as
sementes −10%, −5%, 0%, 1%, 2%, 5% e 10% e nenhuma converge. **É anterior às nossas
mudanças**, e o `IFERROR` vinha escondendo isso.

Duas causas prováveis, não investigadas:

1. O FCFE do PR soma **−R$56,0 mi** em termos nominais no horizonte inteiro (BA soma
   +R$232,5 mi e RN +R$402,7 mi). Fluxo com soma negativa pode simplesmente não ter TIR real.
2. A fórmula do PR começa em **`E190`**, e não em `D190` como BA e RN. Pode ser proposital
   (pular dez/23) ou pode ser erro de digitação.

Vale checar se o FCFE negativo do PR é real ou sintoma de outro problema — é a planta com
o gap de GNL do P1.

### P11 — Débito estrutural: premissa única × mix variável no tempo

**É a causa raiz de quase todo o resíduo que sobrou.** Nosso modelo usa um número por
planta onde a referência calcula por cliente — e o mix de clientes muda ao longo do
horizonte, então um número único erra nas pontas.

O caso mais visível é a **saída do Bahiagás-BRU do RN em jan/2030** (16.000 m³/dia a
1.400 km), que move três coisas de uma vez na referência:

| RN | Referência 2029 → 2030 | Nosso |
|---|---|---|
| Distância média | 704 → ~490 km | fixo em 557 |
| Frete variável | 7,38 → 4,66 | 6,80 → 6,63 |
| Aluguel de equipamento | 0,92 → 0,17 | 0,52 → 0,53 |

Custa **+R$3,8 a +4,5 mi/ano no RN em 2030-31**. O mesmo mecanismo já aparecia em P4
(preços de segmento da BA em 2030) e explica a oscilação do aluguel de equipamento da BA
(referência triplica em 2030).

**Correção estrutural:** premissas com degraus datados, no padrão que o `Dashboard` já usa
para a curva de volume (linhas 79-110) — base + ajustes por data. Vale para distância,
nº de ISOs e preços de segmento.

### P12 — Sinergia de equipamentos: mecanismo pronto, desligado

A referência declara em `Premissas Gerais` (linha 108) uma redução de **35% no PR, 15% na
BA e 10% no RN** a partir de jan/2028, por compartilhamento de equipamentos entre plantas.

**Mas a linha dela resolve para zero.** A fórmula (`OPEX!1344-1346`) faz um `XLOOKUP` do
fator e o soma como se fosse reais no total de distribuição (`OPEX!701 = ...+AS1344`) —
somando R$0,35 a um total de milhões, e na prática devolvendo R$0,00 no acumulado anual.

Criamos o mecanismo correto (redução sobre o aluguel de equipamento, com data de início) e
**zeramos os percentuais em `Dashboard!202` para espelhar a referência**. Ligar a sinergia
com os percentuais declarados vale **−R$0,37 a −0,41 mi/ano** e exigiria recalibrar os ISOs
(item 15) para cima.

**Decisão pendente:** a sinergia é real na operação? Se for, o certo é ligá-la e recalibrar
— e aí divergimos da referência de propósito.

### P13 — Parâmetros de ciclo logístico calibrados, não observados

As distâncias diárias de BA (790 km/dia) e RN (805 km/dia) do item 17 vieram de calibração
contra o frete fixo da referência, não de medição. São plausíveis para carreta dedicada em
rota longa com dois motoristas, mas ficam **no limite superior** da prática brasileira
(400-600 km/dia com motorista único).

Se a operação real roda com menos, o número certo é menor e o desvio está em outro lugar —
provavelmente na tarifa de frete fixo (`Dashboard!185` = R$71.753/veículo/mês em BA e RN).
Vale confrontar com a operação antes de tratar como definitivo.

### P10 — ~~Perdas e "Others" na liquefação~~ ✅ RESOLVIDO (itens 12-13)

Mantido como registro do diagnóstico. O que se descobriu:

Único item relevante que resta da liquefação. Após os itens 5-11:

| Componente (2028) | Nosso | Referência | Δ |
|---|---|---|---|
| Energia (eletricidade + gerador) | 33,15 | 32,86 | +0,30 |
| Utilities / Insumos | 0,92 | 0,93 | −0,01 |
| O&M | 12,34 | 11,95 | +0,39 |
| **Perdas + Outros** | **9,27** | **3,64** | **+5,63** |
| Compressão | 0,00 | 0,72 | −0,72 |

Os dois estão **na mesma linha 90** do nosso modelo
(`vol × Dashboard!120 + Dashboard!178`), o que dificulta a análise. Separando:

| 2028 (R$ mi) | Nosso | Referência | Δ |
|---|---|---|---|
| Perdas | 1,81 | 3,20 | **−1,39** |
| Others | 7,46 | 0,44 | **+7,02** |

**Perdas — três diferenças:**

1. **Base de valoração.** `Dashboard!120` = `SUM(116:119) × C179`, ou seja **2% do custo de
   processamento** por m³ (R$0,021/m³). A referência usa `custo_molécula/(1−5%)×5%`, ou seja
   **o gás perdido é valorizado ao que se pagou por ele** (R$0,117/m³ no PR) — 5,5× maior.
   A referência está conceitualmente certa: o gás que evapora foi comprado.
2. **Taxa.** 5% (referência) contra 2% (`Dashboard!179`). Decisão de negócio — o nosso 2%
   pode vir de medição real da planta.
3. **Recuperação de purga.** A referência abate o gás de purga recuperado, valorizado ao
   custo da molécula: PR = 20% do volume de GNC; BA = 2.300 m³/dia; RN = nenhuma.
   Vale −R$2,72 mi/ano e **não existe no nosso modelo**.

Efeito combinado na referência (2028): perda bruta 5,91 − recuperação 2,72 = **3,20 líquido**.

**"Others" — ainda sem explicação.** `Dashboard!178`: R$108.561/mês (PR), **R$283.503/mês
(BA)** e R$170.707/mês (RN), contra R$5.000 / 15.000 / 15.000 da referência — 17× no total.
**Antes de mexer, entender o que está dentro desses valores**: pode ser diferença de
classificação (itens que a referência lança em SG&A ou insumos) e não de nível.

**Logística** — a referência modela frete por cliente, com km individual e tipo de carreta;
o nosso usa distância média por planta (`Dashboard!182/190`) e nº de veículos por `ROUNDUP`.
Gap "limpo" após o item 3: +R$7,4 mi em 2028.

**Resultado financeiro** — os saldos de dívida batem (2028: 256,4 nosso vs 259,6 da
referência), mas a despesa não. Suspeitas: indexador IPCA vindo de curvas diferentes
(ETTJ ANBIMA vs Focus) e a referência carregando IOF, comissão e seguro de dívida no
resultado financeiro.

**Impostos** — estruturas diferentes, ainda não comparadas. A referência apura o CNPJ da
SPE RN separado da matriz consolidada, tem adicional de IRPJ de 10% acima de R$20k/mês e
ICMS de 20% no RN contra 12% nas demais, trabalhando em receita bruta com deduções. O nosso
usa 34% flat sobre receita líquida com trava de 30% de prejuízo fiscal por entidade
(`Dashboard!C305/C306` estão definidos mas não são usados por nenhuma fórmula).

---

## Backups

Em **`backups-modelo/`**. Os backups intermediários foram descartados em 05/08 — restam
apenas os dois extremos:

| Arquivo | Estado |
|---|---|
| `... (backup pre-desacoplamento PR).xlsx` | **original**, antes de qualquer ajuste |
| `... (backup pre-zerar sinergia).xlsx` | estado após o item 18 |

<details>
<summary>Histórico dos backups intermediários (excluídos)</summary>

Cada arquivo preservava o estado **antes** do ajuste indicado no nome:

| # | Arquivo (`backups-modelo/`) | Estado que preserva |
|---|---|---|
| 1 | `... (backup pre-desacoplamento PR).xlsx` | original, antes de qualquer ajuste |
| 2 | `... (backup pre-recalibracao precos).xlsx` | após item 1 |
| 3 | `... (backup pre-ajuste frete servico).xlsx` | após item 2 |
| 4 | `... (backup pre-aluguel fixo).xlsx` | após item 3 |
| 5 | `... (backup pre-energia liquefacao).xlsx` | após item 4 |
| 6 | `... (backup pre-tarifa energia).xlsx` | após item 5 |
| 7 | `... (backup pre-remocao indexacao energia).xlsx` | após item 6 |
| 8 | `... (backup pre-gerador diesel).xlsx` | após item 7 |
| 9 | `... (backup pre-cenarioC energia).xlsx` | após item 8 |
| 10 | `... (backup pre-utilities).xlsx` | após item 9 |
| 11 | `... (backup pre-calibracao utilities).xlsx` | após item 10 |
| 12 | `... (backup pre-perdas).xlsx` | após item 11 |
| 13 | `... (backup pre-others).xlsx` | após item 12 |
| 14 | `... (backup pre-distancias).xlsx` | após item 13 |
| 15 | `... (backup pre-iso).xlsx` | após item 14 |
| 16 | `... (backup pre-capacidade).xlsx` | após item 15 |
| 17 | `... (backup pre-ciclo transporte).xlsx` | após item 16 |
| 18 | `... (backup pre-cavalo mecanico).xlsx` | após item 17 |
| 19 | `... (backup pre-zerar sinergia).xlsx` | após item 18 |

</details>

Para reverter tudo, restaurar o backup original. Para reverter um ajuste isolado, usar as
referências de célula documentadas em cada item da tabela de Concluídos.
