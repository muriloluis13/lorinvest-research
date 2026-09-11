# GNLink BP — Mecânicas das fórmulas (registro didático p/ tooltips)

Cada item de receita/OpEx é reproduzido por fórmula em JS. Este documento registra,
em linguagem clara, **o que cada sub-linha calcula** — base para os ícones de ajuda/
tooltips do dashboard. Convenções: `op(p,k)` = flag 0/1 de planta em operação
(`Receita!767–772`); `corr(k)` = inflator IPCA de OpEx (`OPEX!556 ≡ 713`, =1 até jul/27,
depois cresce com IPCA acumulado); `dias(k)` = dias no mês; volume em m³/dia.
Regra geral: **realizado = valores reais (extraídos); projeção = fórmula (JS)**.

---

## Receita

- **Receita R$ (GNL/GNC)** = `preço_indexado × volume × dias`. Preço = `preço-base × fator de reajuste`.
  - Reajuste **IPCA 100%**: fica em 1 até o 1º aniversário da data-base; a cada aniversário multiplica por (1 + IPCA 12 meses).
  - Reajuste **Brent** (Bahia/RN/SAL): parte residual reajustada por IPCA + parte molécula reajustada por Brent×Dólar (trimestre fev/mai/ago/nov), com piso/teto.
- **Serviço sem molécula / Aluguel fixo / Outros**: linhas próprias de receita, somadas à Receita Líquida.
- **Receita Líquida** = GNL + GNC + serviço + aluguel + outros. **Bruta** = Líquida + deduções (impostos).

## Custo do gás (molécula)

- **Custo do gás** = `Σ volume(clientes com molécula) × dias × custo da molécula[planta]` + ajustes (reversão / venda no gasoduto).
- **Custo da molécula** (R$/m³): custo-base por planta reajustado (IPCA, ou Brent×Dólar) com **piso e teto**, a cada período de reajuste (anual/trimestral/mensal conforme a planta).

## Liquefação (OPEX 404–556)

Por planta = **Energia + Insumos + O&M + Perdas + Recuperação de purga + Outros**.

- **Energia = Eletricidade + Gerador.**
  - **Eletricidade** = `preço_MWh[planta] × Potência(MW) × op × fatorIPCA × 24h × dias`.
    - **Potência (MW)** = tabela por nº de Cryos ligados: 1→0,55 · 2→0,89 · 3→1,43 · 4→1,97 MW
      (base 0,35 + adicional por Cryo). Nº de Cryos = `arredonda-p/-cima(volume_planta / 19.800)`.
      → **mais volume ⇒ mais máquinas ⇒ mais potência**.
    - **preço_MWh**: 390 (PR) / 426 (BA) / 565 (RN). **Fixo até jan/2030**, depois sobe com IPCA.
  - **Gerador** = `base_R$/mês[planta] × op × IPCA` (PR = 86.000/mês; demais 0).
- **Insumos** (R$/mês por planta, × op × IPCA), cada um com sua sazonalidade:
  propano (mai+dez) · água (meses ímpares) · óleo (todo mês) · glycol · resíduos (todo mês) ·
  mercaptano (mai+dez; RN abr+nov).
- **O&M** = `base_R$/mês[planta] × op × IPCA` (PR 300k · BA 334k · RN 307k).
- **Perdas no processo** = `custo_do_gás / (1 − perda%) × perda%` (perda% = 5%). É um markup sobre o gás.
- **Recuperação de purga** = crédito (negativo) proporcional ao volume × molécula, a partir de uma data.
- **Outros** = R$/mês fixo × op × IPCA.

## Compressão (OPEX 558–565)

Por planta = `tarifa_R$/mês[planta] × op × IPCA`, liberada a partir de uma **data de início**.
Não é volume-dependente. Hoje só **RN** (20.000/mês a partir de ~ago/27).

## Terminal (OPEX 567–574)

Por planta = `tarifa[planta] × volume_GNL(planta) × dias`. **Volume-dependente, sem IPCA.**
Hoje só **Terminal PE** (0,30 por m³·dia).

## SG&A de planta (OPEX 576–709) — 11 componentes por planta

Base geral: `valor × op × IPCA`. **Atenção**: ago–dez/2026 são valores *hardcoded*; a fórmula
paramétrica vale de **jan/2027** em diante.

1. **Salários** = `R$/mês/pessoa × headcount × op × IPCA`.
2. **Seguros** (Operacional + Equipamentos) = prêmio anual `valor_segurado × taxa`, pago 1×/ano
   (a cada 12 meses a partir do início), × op × IPCA. (Equip. BA/RN: a cada 3 meses.)
3. **Assistência técnica** = lump anual no mês 10 (outubro), × op × IPCA.
4. **Serviços gerais** = `R$/mês fixo × op × IPCA`.
5. **Viagens e hospedagens** = `R$/mês fixo × op × IPCA`.
6. **Projetos de engenharia** = se ocupação GNL ≥ 95% usa R$ 1.000, senão R$ 5.000; × op × IPCA.
7. **Regulatório** = R$ 5.000 a cada 3 meses (a partir de uma data-base), × op × IPCA.
8. **Segurança** (Patrimonial + Ocupacional fixos; Trabalho = R$ 5.000 a cada 6 meses), × op × IPCA.
9. **Contingência** = manual (~0).
10. **Frota** = `R$/mês/veículo × nº de veículos × op × IPCA`.
11. **Outros** = manual (~0).

## Regás (OPEX 1973–2465) — por cliente

Por planta = **Aluguel de equipamento + Montagem + Assistência técnica** (Insumos/Furui = 0 hoje).

- **Aluguel de equipamento (por cliente)** = `qtd_equipamentos × custo/dia[tipo] × IPCA`.
  - `custo/dia` = R$ 13.000 (GNL/ISO) ou R$ 22.000 (GNC/Carreta).
  - `qtd_equipamentos` = `arredonda-p/-cima( volume_cliente / capacidade × dias_de_estoque ) × op`,
    e **zero se o cliente é FOB** (faz a própria logística). Capacidade 24.000 (GNL) / 6.500 (GNC);
    dias de estoque 2,5 (GNL) / 1 (GNC). → **mais volume ⇒ mais equipamentos**.
- **Montagem de regás (por cliente)** = custo único (de `Clientes!T`), lançado **só no mês de início**, × IPCA.
- **Assistência técnica (por planta)** = `arredonda-p/-cima(volume_planta / 5.000) × R$ 1.500 × op × IPCA`.

## Logística / Distribuição (OPEX 716–1370) — por cliente

Por planta = **Frete fixo + Frete variável + Aluguel de equipamento + Cavalo mecânico +
Ociosos/preparação + Sinergia**. Base de tudo: o **nº de carretas** que o cliente exige,
função de volume, distância e tipo.

- **Nº de carretas (cliente)** = `(volume/dia ÷ capacidade) × (distância_ida×2/450 + descarga/24) × op`.
  Capacidade 24.000 (ISO GNL) / 6.500 (GNC) / 34.000 (Carreta GNL); 450 km/dia; descarga 9h (GNL)/3h (GNC).
  Duas versões: **RAW** (fracionário) e **arredondada** (frota da planta/tipo arredondada p/ cima e re-rateada).
- **Frete fixo (cliente)** = `custo_fixo_por_viagem × nº carretas ARREDONDADO × IPCA`
  (42.582 ISO GNL / 60.839 GNC / 71.572 Carreta GNL).
- **Frete variável (cliente)** = `R$/km × km_rodados_no_mês × IPCA`; `km_mês = (volume/capacidade) × dist×2 × 30`
  (**30 dias fixos**, não os dias do mês). R$/km = 4,90 / 5,78 / 4,55.
- **Aluguel de equipamento (cliente)** = `aluguel_ISO(13.000/mês) × nº carretas RAW × IPCA` (GNL; GNC = 0).
- **Cavalo mecânico (planta)** = `(fixo + variável)[planta] × op × IPCA` (ambos R$/mês fixos; PR 39.000+11.600).
- **Ociosos/preparação** (global, rateado por planta pela frota): custo fixo de ISOs ociosos (22.000/ISO)
  + preparação de ISOs novos (30.000/ISO), até 2028.
- **Sinergia** (planta) = **crédito** = `−redução%[planta] × frete_fixo_da_planta`, **ativo só até dez/2027**
  (PR −35% / BA −15% / RN −10%).

## Custo da molécula — motor recursivo (Variável 184–268)

`custo_molécula[planta][k] = custo-base × fator_de_reajuste[k] × (1 + desconto)`, onde o **fator é recursivo**
(carrega o mês anterior) e só muda no **mês de reajuste** (`MOD(mês − mês-base, ocorrência)=0`; ocorrência =
12 anual / 3 trimestral / 1 mensal):
- **IPCA**: no reajuste, `fator = fator_anterior × (1 + IPCA 12m)` (PR).
- **Brent** (BA/RN/PE): no reajuste, `fator = fator_anterior × (Brent_atual/Brent_da-data-base) × (Dólar_atual/Dólar_base)`,
  com **piso/teto** sobre o Brent (RN: piso 70 / teto 120 US$/bbl).
- **Dólar** (Argentina): motor próprio (dólar corrente/base × CPI de agosto).
- **IPCA+Brent composto** (Projeto Sal): parcela fixa reajustada por IPCA + parcela Brent×Dólar.
Divisor de conversão Brent→R$/m³ = 26,8081. O preço de venda **Brent** dos clientes acopla este motor
(Bahia usa a molécula da planta; PR/RN/SAL recomputam o termo Brent do trimestre).

## DRE / EBITDA

Receita Líquida → (− Custos) → Resultado Operacional → **EBITDA** → (− Depreciação) → EBIT →
(− Resultado Financeiro/Impostos) → Lucro Líquido. Margem EBITDA = EBITDA / Receita Líquida.
