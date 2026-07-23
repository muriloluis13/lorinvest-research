// ============================================================================
// Fonte única de dados das empresas do Painel de Research (Lorinvest).
// Extraído de index.html para separar DADOS de APRESENTAÇÃO.
// Consumido por: aba Empresas (renderAportes/renderGov...) e cards do Panorama.
// Carregado via <script src="data/empresas.js"> antes dos scripts de render.
// ============================================================================
    window.EMP = {
      "Bioren":{updated:"08/06/2026",pctHolder:"Hankoe",aportes:{kpis:[["Valor Hankoe","25.016,8"],["Aportes Líquidos","25.017,0"],["Correção IPCA","27.118,3"],["Correção IPCA + 15%","34.914,1"]],holdersTitle:"Acionistas",holders:[["Hankoe",77.8],["Roberto Kessel",11.1],["Carlos Carloni",11.1]]},governanca:[{title:"Conselho de Administração",eleito:"03/11/2025",mandato:"03/11/2027",membros:["Christian Lorentzen","Luciano Medeiros","Carlos Carloni","Roberto Kessel"]},{title:"Diretoria",eleito:"04/10/2023",mandato:"04/10/2026",membros:["CEO: Luiz Cidade","Diretor: José Cavalcante"]}]},
      "Eindom":{updated:"08/06/2026",pctHolder:"Hankoe",aportes:{kpis:[["Valor Hankoe","92.098,1"],["Aportes Líquidos","113.349,5"],["Correção IPCA","133.986,3"],["Correção IPCA + 15%","216.817,7"]],holdersTitle:"Acionistas",holders:[["Hankoe",100]]},governanca:[{title:"Conselho de Administração",eleito:"01/04/2026",mandato:"01/04/2028",membros:["Peter Boot","Lucas Werner"]},{title:"Diretoria",eleito:"30/04/2024",mandato:"30/08/2027",membros:["Ricardo Goldstein","Evandro Paiva"]}]},
      "Valsa":{updated:"08/06/2026",pctHolder:"Hankoe",aportes:{kpis:[["Valor Hankoe","165.000,0"],["Aportes Líquidos","165.000,0"],["Correção IPCA","181.628,7"],["Correção IPCA + 15%","221.457,1"]],holdersTitle:"Acionistas",holders:[["Hankoe",92],["Helser",8]]},governanca:[{title:"Conselho de Administração",eleito:"07/08/2025",mandato:"07/08/2027",membros:["Luciano Medeiros","Leonardo Szczerb","Alfredo Cardoso"]},{title:"Diretoria",eleito:"05/01/2026",mandato:"05/01/2028",membros:["CEO: Alfredo Cardoso","Diretor: Carlos Ceppas"]}]},
      "GBS Storage":{updated:"08/06/2026",pctHolder:"Hankoe",aportes:{kpis:[["Valor Hankoe","98.790,9"],["Aportes Líquidos","91.140,5"],["Correção IPCA","105.613,3"],["Correção IPCA + 15%","163.211,8"],["Exposição Total","298.586,0"]],holdersTitle:"Acionistas",holders:[["Hankoe",100]]},governanca:[{title:"Conselho de Administração",eleito:"05/12/2023",mandato:"05/12/2025",membros:["Marcelo Menicucci","Celso Pereira","Peter Boot","Leonardo Szczerb"]},{title:"Diretoria",eleito:"30/06/2025",mandato:"30/06/2027",membros:["CEO: Celso Pereira","Diretor: Shiniti Ohara"]}],operacional:{segurosGarantias:{groups:[{cobertura:"Intraconsórcio",rows:[{periodo:"2025",parcela:"10% GPK",tipo:"Fiança",emissor:"BTG",status:"Aguardando emissão",st:"wait"},{periodo:"2026",parcela:"10% GBS",tipo:"Seguro",emissor:"BTG",status:"Emitido a viger em 01/01/26",st:"ok"},{periodo:"2026",parcela:"10% GPK",tipo:"Fiança",emissor:"BTG",status:"Aguardando emissão",st:"wait"}]},{cobertura:"Garantia ANP",rows:[{periodo:"Set/2025 – Mar/2028",parcela:"20%",tipo:"Fiança",emissor:"BTG",status:"Vigente",st:"ok"}]}],notes:["Ações em curso a fim de mitigar os efeitos da dupla garantia.","Apesar de ter sido aprovada a garantia intraconsórcio para a baixa do fundo abandono, seguimos discutindo junto com a Brava, para que a Petrobras aceite outra alternativa.","Reunião solicitada junto à ANP a fim de propor uma mudança na resolução que trata desse assunto, propondo uma sub-rogação da garantia para o operador.","Para que a GBS pudesse dar uma garantia corporativa, o PL deveria ser de R$ 1,6 bilhões de reais, considerando a GBS com nota A-. O patrimônio líquido da GBS está por volta de R$ 60 milhões."],source:"GBS Storage — Comitê de Investimentos Lorinvest, dez/2025 (slide 3)"},usosPDI:{fontes:[{nome:"PRIO",valor:"~R$ 9,9 MM",obs:"recebido em 30/11/2025"},{nome:"Geopark (“herdado”)",valor:"R$ 1,30–2,85 MM",obs:"a investir · estimado"}],usos:[{destino:"BioRen",prio:"~R$ 4,0 MM",geopark:"~R$ 2,4 MM",mmP:4.0,mmG:2.4},{destino:"Universidades",prio:"~R$ 5,4 MM",geopark:"~R$ 300 mil",mmP:5.4,mmG:0.3},{destino:"SG&A",prio:"~R$ 500 mil",geopark:"~R$ 150 mil",mmP:0.5,mmG:0.15}],total:{prio:"~R$ 9,9 MM",geopark:"~R$ 2,85 MM"},note:"Recebido da PRIO em 30/11/2025 (~R$ 9,9 MM). Assim que o projeto da Bioren tiver aprovação da ANP, os contratos serão assinados e os recursos transferidos conforme cronograma. Valor “herdado” da Geopark a investir estimado entre R$ 1,30 MM e R$ 2,85 MM.",source:"GBS Storage — Comitê de Investimentos Lorinvest, dez/2025 (slide 4)"}},financeiro:{orcado2025:{resultado:{realizadoProj:"(8.150)",orcado:"(9.402)",saldo:"1.252"},trimestral:[{tri:"1º Tri",real:"2.844",orc:"3.674",pct:"77%"},{tri:"2º Tri",real:"4.497",orc:"5.551",pct:"81%"},{tri:"3º Tri",real:"6.224",orc:"7.407",pct:"84%"},{tri:"4º Tri",real:"8.150",orc:"9.402",pct:"87%"}],gbs:{rows:[{item:"Employee Expenses",real:"(5.595)",orc:"(6.624)",pct:"-84%"},{item:"Annual Bonus",real:"(328)",orc:"(1.080)",pct:"-30%"},{item:"G&A Expenses",real:"(1.284)",orc:"(732)",pct:"-25%"},{item:"Outsourced Services",real:"(205)",orc:"(510)",pct:"-40%"},{item:"Legal Consulting",real:"(746)",orc:"(456)",pct:"-36%"},{item:"Others",real:"8",orc:"0",pct:"0%"}],total:{real:"(8.150)",orc:"(9.402)"}},manati:{rows:[{item:"Revenue",real:"33.003",orc:"59.118",pct:"-44%"},{item:"Opex",real:"(34.001)",orc:"(36.036)",pct:"-6%"},{item:"Taxes",real:"(6.849)",orc:"(13.233)",pct:"-48%"},{item:"Royalties",real:"(1.475)",orc:"(4.920)",pct:"-70%"},{item:"Insurance & Warranty",real:"(1.866)",orc:"(2.106)",pct:"-11%"},{item:"Consulting",real:"(187)",orc:"0",pct:"0%"}],total:{real:"(11.375)",orc:"2.823"}},caixa:{data:"03/12/2025",valor:"R$ 16.774.615,54"},variacaoCaixa:[["Jan","5,37"],["Fev","1,68"],["Mar","1,70"],["Abr","1,32"],["Mai","0,38"],["Jun","3,81"],["Jul","1,58"],["Ago","0,60"],["Set","2,11"],["Out","4,53"],["Nov","16,69"],["Dez","14,28"]],note:"Valores em milhares de reais (R$ mil), salvo indicação. O G&A da GBS (realizado + projeção) fechou 2025 em (8.150) vs. (9.402) orçado — economia de 1.252. Percentuais conforme apresentados no Comitê.",source:"GBS Storage — Comitê de Investimentos Lorinvest, dez/2025 (slide 5)"},exposicao2025:{useOfProceeds:{fontes:{itens:[{valor:"R$ 91,1 mi",label:"Capital próprio"}],total:{valor:"R$ 91,1 mi",label:"Capital Investido"}},usos:{itens:[{valor:"R$ 25 mi",label:"CapEx PRIO"},{valor:"R$ 8,3 mi",label:"CapEx GeoPark"},{valor:"R$ 30,8 mi",label:"SG&A (*)"},{valor:"R$ 12,7 mi",label:"Prejuízo acumulado Manati"}],total:{valor:"R$ 76,8 mi",label:"Capital utilizado (R$ 14,4 mi em caixa)"}},footnote:"(*) inclui todos os estudos e consultorias",alloc:[{label:"CapEx PRIO",v:25,vl:"25",color:"#1F3B57"},{label:"CapEx GeoPark",v:8.3,vl:"8,3",color:"#6B8299"},{label:"SG&A",v:30.8,vl:"30,8",color:"#C55A17"},{label:"Prejuízo Manati",v:12.7,vl:"12,7",color:"#B23A2E"},{label:"Em caixa",v:14.4,vl:"14,4",color:"#9FB4C7"}],caixa:"R$ 14,4 mi"},tabela:{grupos:[{titulo:"CapEx | Stake 20% PRIO + GPRK",rows:[{item:"Signing",data:"out-22",nom:"(24,8)"},{item:"Closing",data:"nov-23",nom:"(85,7)"},{item:"1º retirada do fundo",data:"dez-23",nom:"9,8"},{item:"Closing adjustment",data:"jan-24",nom:"4,1"},{item:"2º retirada do fundo",data:"jun-24",nom:"0,3"},{item:"Cash balance",data:"set-24",nom:"5,2"},{item:"3º retirada do fundo",data:"set-24",nom:"66,2"},{item:"Total PRIO",nom:"(25,0)",tot:true},{item:"Signing GeoPark",data:"abr-25",nom:"(3,3)"},{item:"Closing GeoPark",data:"dez-25",nom:"(2,9)"},{item:"Ajustes",data:"dez-25",nom:"(2,1)"},{item:"Total GeoPark",nom:"(8,3)",tot:true},{item:"Total CapEx",nom:"(33,3)",tot:true}]},{titulo:"OpEx",rows:[{item:"SG&A",data:"jul-22 ~ dez-25",nom:"(30,8)"},{item:"Prejuízo Manati",data:"jan-24 ~ dez-25",nom:"(12,7)"},{item:"Total OpEx",nom:"(43,5)",tot:true},{item:"Caixa",nom:"(14,4)",tot:true}]}],resumo:[{item:"Exposição (contábil)",nom:"(91,1)",ipca:"(102,2)",ipca15:"(147,1)",tot:true},{item:"Despesas na GB",data:"abr-20 ~ jun-22",nom:"(13,5)",ipca:"(21,8)",ipca15:"(41,6)"},{item:"Exposição (gerencial)",nom:"(104,6)",ipca:"(124,0)",ipca15:"(188,7)",tot:true}]},source:"GBS Storage — Comitê de Investimentos Lorinvest, dez/2025 (slide 6)"}}},
      "New Wave":{updated:"08/06/2026",pctHolder:"Dyna",aportes:{kpis:[["Valor Dyna","119.331,4"],["Aportes Líquidos","144.319,9"],["Correção IPCA","168.345,8"],["Correção IPCA + 15%","266.986,4"]],holdersTitle:"Acionistas",holders:[["Dyna",78.4],["Gustavo Emina",21.6]]},governanca:[{title:"Conselho de Administração",eleito:"21/03/2023",mandato:"21/03/2025",membros:["Luciano Medeiros","Gustavo Emina","Leonardo Szczerb"]},{title:"Diretoria",eleito:"27/10/2025",mandato:"31/10/2027",membros:["CEO: Gustavo Emina","CLO: Newton Junior","CFO: Elvira Presta","Diretor: Ivan Menezes","Diretor: Bruno Ferraz","Diretor: Marcus Berto"]}]},
      "Norflor":{updated:"08/06/2026",pctHolder:"Hankoe",aportes:{kpis:[["Valor Hankoe","187.463,4"],["Aportes Líquidos","-65.566,6"],["Correção IPCA","-49.282,3"],["Correção IPCA + 15%","-101.564,7"],["Exposição Total","95.602,4"]],holdersTitle:"Acionistas",holders:[["Hankoe",100]]},governanca:[{title:"Conselho de Administração",eleito:"10/06/2024",mandato:"10/06/2026",membros:["Luciano Medeiros","Leonardo Szczerb","Maria Clara Assis"]},{title:"Diretoria",eleito:"07/06/2024",mandato:"07/06/2027",membros:["CEO: Sandro Longuinho","COO: Fabiano Lago","CSO: Adauta Braga"]}]},
      "Norsul":{updated:"08/06/2026",pctHolder:"Lorentzen",analises:{resultados:[{title:"Demonstrações financeiras auditadas — 2024",meta:"Balanço patrimonial, DRE, fluxo de caixa e notas explicativas",href:"empresas/norsul/dfsauditadas/index.html"}]},aportes:{kpis:[["Valor Hankoe","1.547.592,3"],["Valuation Múltiplo","1.320.216,9"],["Valor Hankoe - Lorentzen (%)","1.189.123,5"],["Valuation Múltiplo - Lorentzen (%)","1.014.415,1"]],holdersTitle:"Acionistas",holders:[["Lorentzen",76.8],["Hugo",19.8],["Lily",0.7],["Luke",0.7],["Outros",2]]},governanca:[{title:"Conselho de Administração",eleito:"08/07/2025",mandato:"08/07/2028",membros:["Angelo Baroncini","Luciano Medeiros","Leonardo Szczerb","Pietro Allevato","Hugo Figueiredo"]},{title:"Diretoria",eleito:"08/04/2024",mandato:"08/04/2027",membros:["CEO: Rodrigo Cuesta","CFO: André Gonçalves","Dir. Operacional: Christian Lachmann"]}]},
      "Sileto":{updated:"08/06/2026",pctHolder:"Dyna",aportes:{kpis:[["Valor Dyna","79.023,2"],["Aporte Total","74.648,6"],["Correção IPCA","82.335,3"],["Correção IPCA + 15%","111.364,0"]],holdersTitle:"Acionistas",holders:[["Crystall",51.6],["Dyna",40],["Fundo Nunki",8.4]]},governanca:[{title:"Supervisory Committee",eleito:"11/07/2025",mandato:"11/07/2027",membros:["Christian Lorentzen","Luciano Medeiros"]},{title:"Supervisory Board",eleito:"11/07/2025",mandato:"11/07/2027",membros:["Luciano Medeiros","Christian Lorentzen"]}]},
      "Target Bank":{updated:"08/06/2026",pctHolder:"Hankoe",aportes:{kpis:[["Valor Hankoe","2.377,6"],["Aportes Líquidos","96.139,8"],["Correção IPCA","110.458,1"],["Correção IPCA + 15%","229.779,2"]],holdersTitle:"Acionistas",holders:[["Hankoe",92.3],["Santos",3.4],["William",3.3],["Outros",1]]},governanca:[{title:"Conselho de Administração",eleito:"24/10/2024",mandato:"26/10/2026",membros:["Peter Boot","Leonardo Szczerb","William Rego"]},{title:"Diretoria",eleito:"16/01/2025",mandato:"16/01/2028",membros:["CEO: William Rego","Diretor Jurídico: Gustavo Abdalla"]}]},
      "Tree+":{updated:"08/06/2026",pctHolder:"Hankoe",aportes:{kpis:[["Aportes Líquidos","62.327,0"],["Correção IPCA","67.842,2"],["Correção IPCA + 15%","87.184,7"]],holdersTitle:"Quotistas",holders:[["Ti17 FIM",25],["Zest",25],["Hankoe",25.1],["Mercuria",25]]},governanca:[{title:"Comitê de Investimento",eleito:"29/09/2023",mandato:"29/09/2025",membros:["Luciano Medeiros","Eduardo Gomes de Almeida","Fábio Medeiros Martins da Silva","Marc Adam Hiller"]}],govInfo:[["Fundo","Skog FIP – Multiestratégia"],["Administrador","BTG Pactual"],["Gestor","Lorinvest"],["Data da Constituição","14/08/2023"],["Exercício Social","31/março"]]},
      // GNLink: empresa-referência. Seu workspace na aba Empresas ainda é markup
      // estático (projetos/comercial/financeiro/etc.), mas os DADOS de Aportes e
      // Governança passam a morar aqui (fonte única). A Governança usa o MESMO shape
      // das demais empresas (array de blocos title/eleito/mandato/membros) e é
      // renderizada pelo renderGov padrão — donut na paleta padrão, board igual.
      "GNLink":{updated:"08/06/2026",pctHolder:"Hankoe FIP",aportes:{kpis:[["Valor Hankoe","106.100,2"],["Aportes Líquidos","98.385,7"],["Correção IPCA","111.483,8"],["Correção IPCA + 15%","161.933,6"],["Exposição Total","98.537,1"]],holdersTitle:"Acionistas",holders:[["Hankoe FIP",64],["Copa",36]]},governanca:[{title:"Diretoria",eleito:"21/02/2025",mandato:"21/02/2027",membros:["Marcelo Rodrigues","Laila Helayel","Márcio Cardoso","Silvino Junior","Cleber Hamada"]},{title:"Conselho de Administração",eleito:"01/08/2025",mandato:"31/07/2027",membros:["Peter Boot","Celso Pereira","Marcos Mesquita"]}],orgHeadcount:{total:"62",matriz:"41",operacao:"21",exercicio:"2026",ceo:"Marcelo Rodrigues",people:{ana:{n:"Ana Jacome",r:["Analista Jr. de Comunicação"]},laila:{n:"Laila Helayel",r:["Diretora RH/JUR/REG/COMP"],c:"10"},cleber:{n:"Cleber Hamada",r:["Diretor Administrativo","Financeiro"],c:"13"},silvino:{n:"Silvino Pinto",r:["Diretor Operações","e Negócios"],c:"30"},edimar:{n:"Edimar Alves",r:["Gerente Segurança"],c:"2"},augusto:{n:"Augusto Linassi",r:["Gerente Originação","e Logística"],c:"5"}}},operacional:{full:197500,months:["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"],plantsMeta:[["PR","bb"],["BA","ita"],["RN","assu"]],views:{
        rci:{srcCap:"Comitê de Investimentos Lorinvest · 15/dez/2025 (slide 5)",
          plants:[{cls:"bb",nome:"PR — Paraná",cap:"39.580",rows:[["Início operacional","Em operação",0],["Capacidade plena","Jan/26",1],["Máquinas","2 novas + 1 usada",0]]},{cls:"ita",nome:"BA — Bahia",cap:"85.232",rows:[["Início operacional","Em operação",0],["Capacidade plena","Mai/26",1],["Máquinas","4 novas",0]]},{cls:"assu",nome:"RN — Rio Grande do Norte",cap:"72.688",rows:[["Início operacional","Fev/26",0],["Capacidade plena","Fev/26",1],["Máquinas","2 novas + 2 usadas",0]]}],
          supply:{PR:[39580,39580,39580,39580,39580,39580,39580,39580,39580,39580,39580,39580],BA:[42616,42616,42616,42616,85232,85232,85232,85232,85232,85232,85232,85232],RN:[null,72688,72688,72688,72688,72688,72688,72688,72688,72688,72688,72688]},
          rampTag:"topo: % da capacidade · segmentos: mil m³/dia",rampLegendExtra:"",tableColored:false,rfLegend:"",
          note:"<b>Máquinas por planta:</b> RN — 2 novas + 2 usadas (72.688); BA — 4 novas (85.232); PR — 2 novas + 1 usada (potencial 56.701).<br><b>Notas:</b> partida de RN em fev/26 (prazo legal da ANP); capacidade plena de BA com a 2ª fase da Energia Coelba (mai/26); 3ª máquina usada de PR não considerada (negociação Tradener e disponibilidade de energia — pode rodar com gerador) e infra pronta para +1 máquina nova (pedido não colocado na Galileo); volume adicional de GNC Purga de 14.400 m³/dia por planta.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 5)."},
        rca:{srcCap:"GNLink · RCA — mai/2026 (slides 21, 26, 31)",
          plants:[{cls:"bb",nome:"PR — Paraná",cap:"39.580",rows:[["Início operacional","Em operação",0],["Capacidade plena","Jan/26",1],["Máquinas","2 novas + 1 usada",0]]},{cls:"ita",nome:"BA — Bahia",cap:"85.232",rows:[["Parcial (até set/26)","42.616",0],["Capacidade plena","Out/26",1],["Máquinas","4 novas",0]]},{cls:"assu",nome:"RN — Rio Grande do Norte",cap:"72.688",rows:[["Parcial (fev–set/26)","32.416",0],["Capacidade plena","Out/26",1],["Máquinas","2 novas + 2 usadas",0]]}],
          supply:{PR:[39580,39580,39580,39580,39580,39580,39580,39580,39580,39580,39580,39580],BA:[42616,42616,42616,42616,42616,42616,42616,42616,42616,85232,85232,85232],RN:[null,32416,32416,32416,32416,32416,32416,32416,32416,72688,72688,72688]},
          rampTag:"topo: % da capacidade · segmentos: mil m³/dia · realizado até mai/26",rampLegendExtra:'<span style="margin-left:auto">Topo: % da capacidade plena (197.500 m³/dia)</span>',tableColored:true,
          rfLegend:'<div class="rf-legend"><span><i style="background:#C55A17"></i>Realizado (jan–mai/26)</span><span><i style="background:#4F7B8C"></i>Forecast (jun–dez/26)</span></div>',
          note:'<b>Atualização RCA vs RCI:</b> a capacidade plena (197.500 m³/dia) escorregou de mai/26 para <b>out/26</b> — BA opera a 42.616 (metade) até set/26 e sobe a 85.232 em out/26; RN parte em fev/26 a 32.416 e atinge 72.688 em out/26. PR permanece pleno (39.580) desde jan/26.<br>Fonte: GNLink — RCA, mai/2026 (linha “Capacidade Planta” · slides 21 · Barra Bonita, 26 · Itabuna, 31 · Assú).'},
        rcaJun:{srcCap:"GNLink · RCA — jun/2026 (slides 20, 25, 30)",
          plants:[{cls:"bb",nome:"PR — Paraná",cap:"39.580",rows:[["Início operacional","Em operação",0],["Capacidade plena","Jan/26",1],["GNC purga","14.400 → 19.400 (jul/26)",0],["Máquinas","2 novas + 1 usada",0]]},{cls:"ita",nome:"BA — Bahia",cap:"85.232",rows:[["Parcial (até set/26)","42.616",0],["Capacidade plena","Out/26",1],["GNC purga","14.400 (constante)",0],["Máquinas","4 novas",0]]},{cls:"assu",nome:"RN — Rio Grande do Norte",cap:"72.688",rows:[["Parcial (fev–set/26)","32.416",0],["Capacidade plena","Out/26",1],["GNC purga","14.400 → 19.400 (jul/26)",0],["Máquinas","2 novas + 2 usadas",0]]}],
          supply:{PR:[39580,39580,39580,39580,39580,39580,39580,39580,39580,39580,39580,39580],BA:[42616,42616,42616,42616,42616,42616,42616,42616,42616,85232,85232,85232],RN:[null,32416,32416,32416,32416,32416,32416,32416,32416,72688,72688,72688]},
          supplyGnc:{PR:[14400,14400,14400,14400,14400,14400,19400,19400,19400,19400,19400,19400],BA:[14400,14400,14400,14400,14400,14400,14400,14400,14400,14400,14400,14400],RN:[null,14400,14400,14400,14400,14400,19400,19400,19400,19400,19400,19400]},
          rampTag:"topo: % da capacidade · segmentos: mil m³/dia · realizado até jun/26",rampLegendExtra:'<span style="margin-left:auto">Topo: % da capacidade plena (197.500 m³/dia)</span>',tableColored:true,
          rfLegend:'<div class="rf-legend"><span><i style="background:#C55A17"></i>Realizado (jan–jun/26)</span><span><i style="background:#4F7B8C"></i>Forecast (jul–dez/26)</span></div>',
          note:'<b>Capacidade de GNL sem alteração vs. mai/26:</b> PR pleno em 39.580 desde jan/26; BA a 42.616 até set/26 e 85.232 a partir de out/26; RN parte em fev/26 a 32.416 e atinge 72.688 em out/26. A capacidade plena das três plantas (197.500 m³/dia) segue prevista para <b>out/26</b>.<br>Fonte: GNLink — RCA, jun/2026 (linha “Capacidade Planta” · slides 20 · Barra Bonita, 25 · Itabuna, 30 · Assú).',
          noteGnc:'Capacidade de <b>GNC purga</b>, apresentada em quadro próprio nos mesmos slides. PR e RN sobem de 14.400 para <b>19.400 m³/dia</b> em jul/26; BA permanece em 14.400 o ano todo. O total sai de 43.200 (jun/26) para <b>53.200 m³/dia</b> em dez/26 — capacidade adicional à do GNL.<br>Fonte: GNLink — RCA, jun/2026 (linha “Capacidade Planta” do quadro de GNC · slides 20, 25 e 30).'}
      },moleculaJun:{tag:"preço atual · jun/26",
        note:'Contratos de suprimento <b>cativos</b>, com prazo de <b>10 anos</b> cada. Preço médio ponderado de <b>R$ 1,90/m³</b> no volume atual (155.000 m³/dia) e <b>R$ 1,96/m³</b> no volume total contratado (210.000 m³/dia).<br>Fonte: GNLink — RCA, jun/2026.',groups:[
        {cls:"btg",nm:"BBOG",loc:"Barra Bonita",rows:[{v:"R$ 2,22",w:100,mm:"—",br:"—",cen:"Cativo · 10 anos"}]},
        {cls:"bah",nm:"Bahiagás",loc:"Itabuna",rows:[{v:"R$ 1,95",w:88,mm:"—",br:"—",cen:"Cativo · 10 anos"}]},
        {cls:"pet",nm:"PetroRecôncavo",loc:"Assú",rows:[{v:"R$ 1,76",w:79,mm:"—",br:"—",cen:"Cativo · 10 anos"}]}
      ]},
      molecula:{tag:"sem impostos · dez/25",note:'Premissas constantes para todas as linhas (omitidas da tabela): câmbio <b>R$ 5,45/US$</b> · Brent <b>US$ 68,97/bbl</b> · data <b>dez/25</b>. Preços <b>sem impostos</b>.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 18).',groups:[
        {cls:"tra",nm:"Tradener",loc:"Barra Bonita",rows:[{v:"R$ 2,36",w:100,mm:"11,62",br:"16,85%",cen:"Preços anteriores atualizados"},{v:"R$ 2,00",w:85,mm:"9,83",br:"14,26%",cen:""},{v:"R$ 1,70",w:72,mm:"8,37",br:"12,13%",cen:"Oferta Tradener"}]},
        {cls:"bah",nm:"Bahiagás",loc:"Itabuna",rows:[{v:"R$ 2,06",w:87,mm:"10,12",br:"14,67%",cen:"GNC Industrial"},{v:"R$ 1,91",w:81,mm:"9,42",br:"13,65%",cen:"GNC Veicular"}]},
        {cls:"btg",nm:"BTG",loc:"Itabuna",rows:[{v:"R$ 2,03",w:86,brk:"molécula R$ 1,45 · gasoduto R$ 0,58",mm:"10,00",br:"10,35%",cen:"Firme"},{v:"R$ 1,98",w:84,brk:"molécula R$ 1,40 · gasoduto R$ 0,58",mm:"9,76",br:"10,00%",cen:"PUT"}]},
        {cls:"pet",nm:"PetroRecôncavo",loc:"Itabuna",rows:[{v:"R$ 2,01",w:85,brk:"molécula R$ 1,44 · gasoduto R$ 0,57",mm:"9,90",br:"10,30%",cen:"Para Bahiagás"},{v:"R$ 1,61",w:68,loc2:"Assú",mm:"7,93",br:"11,50%",cen:"Base"},{v:"R$ 1,44",w:61,mm:"7,10",br:"10,30%",cen:"Para Cegás"},{v:"R$ 0,49",w:21,mm:"2,41",br:"3,50%",cen:"Geração de EE"}]}
      ]}},comercial:{
        funil:{
          rci:{tag:"valores em m³/dia",note:'Da demanda total mapeada até os contratos assinados. <b>Mais de R$ 1 bilhão</b> em contratos já assinados.',rows:[["Mercado mapeado","1.673.638",100],["Em prospecção","1.099.537",65.7],["Em negociação","275.000",16.4],["Negociações contratuais","96.500",5.8],["Contratos assinados","56.865 – 132.175",7.9]]},
          rca:{tag:"valores em m³/dia · ex. Norte",note:'Da demanda total mapeada (exceto Norte) até os contratos assinados. <b>Mais de R$ 1,1 bilhão</b> em contratos assinados.',rows:[["Mercado mapeado","1.847.776",100],["Em prospecção","1.118.561",60.5],["Em negociação — BID","596.050",32.3],["Em contrato","45.100",12],["Contratos assinados","90.065 – 222.675",15]]},
          rcaJun:{tag:"valores em m³/dia · ex. Norte",note:'Da demanda total mapeada (exceto Norte) até os contratos assinados. <b>R$ 1,09 bilhão</b> em contratos assinados.',rows:[["Mercado mapeado","1.847.776",100],["Em prospecção","1.118.561",60.5],["Em negociação — BID","603.350",32.7],["Em contrato","46.500",12],["Contratos assinados","90.065 – 226.175",15]]}
        },
        assinados:{
          rci:{kpiCls:"kpi-row4",tag:"preço net · reajustado desde a data-base",
            kpis:[["k-slate","Contratos assinados","6","4 GNL · 2 GNCp"],["k-teal","Prazo médio","4,4 <small>anos</small>","média simples dos 6 contratos"],["k-sage","Preço médio","R$ 3,58<small>/m³</small>","ponderado pelo volume total"],["k-stone","Volume total contratado","132.175","m³/dia · ramp-up 56.865 →"]],
            cols:["Cliente","Assinatura","Início forn.","Prazo","Término","Produto","Volume (m³/dia)","Preço net (R$/m³)","Planta"],
            rows:[
              ["CEGÁS","28/10/2025","03/11/2025","5 anos","28/10/2030","GNL","18.740 – 50.000","3,3041","RN"],
              ["BAHIAGÁS","04/11/2025","—","10 anos","31/12/2035","GNL","3.125 – 25.175","3,6359","BA"],
              ["PETROBAHIA","05/10/2023","06/06/2025","10 anos","06/06/2030","GNL","18.000 – 40.000","4,0780","BA"],
              ["PETYAN","04/07/2025","06/11/2025","10 meses","04/05/2026","GNL","12.000","3,3099","BA"],
              ["REITERLOG","12/02/2025","19/02/2025","90 dias","12/05/2025","GNCp","3.000","2,2000","PR"],
              ["RODOPRINCIPE","06/08/2025","23/07/2025","120 dias","04/12/2025","GNCp","2.000","3,2017","PR"]
            ],
            occ:[["k-teal","RN · cap. GNL","72.688","Ocupação GNL <b>69%</b>",69],["k-sage","BA · cap. GNL","85.232","Ocupação GNL <b>91%</b>",91],["k-stone","PR · cap. GNL","39.580","Ocupação GNL <b>0%</b>",0]],
            foot:'<b>(1)</b> Mais de R$ 1 bilhão em contratos assinados. &nbsp; <b>(2)</b> Preço atual considera reajustes aplicados desde a data-base do contrato. &nbsp; <b>(3)</b> 264 clientes foram passados para a COPA prospectar. &nbsp; <b>(4)</b> 46 clientes foram indicados pela COPA para a GNLink prospectar, sendo metade do volume em SP. &nbsp; <b>(5)</b> 70 clientes acima de 100 ton/mês na lista da GNLink, sendo apenas 16 na lista da COPA enviada à GNLink.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 4).'},
          rca:{kpiCls:"kpi-row5",tag:"ramp-up de volume · preço net atual",tagCol:true,total:"90.065 → 108.625 → 222.675",
            kpis:[["k-slate","Contratos assinados","15","6 definitivos · 9 em teste"],["k-teal","Prazo médio","2,7 <small>anos</small>","média simples dos 15 contratos"],["k-sage","Preço médio","R$ 3,37<small>/m³</small>","ponderado pelo volume total"],["k-stone","ToP médio","54,6%","ponderado pelo volume total"],["k-sage","Valor total dos contratos","R$ 1,10 <small>bi</small>","R$ 1.101.224.386"]],
            cols:["Contrato","Cliente","Assinatura","Início forn.","Prazo","Produto","Volume — ini → atual → total (m³/dia)","Preço net (R$/m³)","%TOP","Apuração","Início TOP","Valor do contrato","Planta"],
            rows:[
              {t:"def",c:["CEGÁS","28/10/2025","03/11/2025","5 anos","GNL","18.740 → 22.000 → 50.000","3,38","70%","Trimestral","fev/26","R$ 226.003.744","Assú"]},
              {t:"def",c:["COPERGÁS","28/01/2026","09/03/2026","3 anos","GNL","10.000 → 10.000 → 30.000","3,34","70%","Trimestral","Regás fixa","R$ 24.738.397","Assú"]},
              {t:"tst",c:["POSTO LIDER","04/03/2026","05/03/2026","330 dias","GNCp","1.000 → 1.000 → 6.000","1,90","0%","—","—","—","Assú"]},
              {t:"tst",c:["PARELHAS GÁS","16/04/2026","16/04/2026","330 dias","GNCp","1.500 → 3.000 → 3.000","1,90","0%","—","—","—","Assú"]},
              {t:"tst",c:["MERI POBO","28/01/2026","19/05/2026","6 meses","GNCp","2.000 → 2.000 → 6.000","3,17","0%","—","—","—","Assú"]},
              {t:"def",c:["COMPAGÁS","29/12/2025","12/03/2026","1 ano","GNL","7.000 → 20.000 → 20.000","3,85","70%","Anual","mar/26","R$ 71.832.000","Barra Bonita"]},
              {t:"tst",c:["SK METAIS","23/06/2026","15/07/2026","180 dias","GNL","3.000 → 3.000 → 4.000","3,80","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["FEVEREIRO LD","28/01/2026","29/01/2026","330 dias","GNCp","3.000 → 4.000 → 4.000","3,20","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["DALLON","21/01/2026","Pendente reunião","330 dias","GNCp","6.000 → 6.000 → 10.000","2,90","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["RIO BONITO","15/05/2026","01/08/2026","180 dias","GNCp","1.000 → 1.000 → 2.000","3,45","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["DALPARE","03/02/2026","20/08/2026","330 dias","GNCp","2.200 → 2.000 → 2.000","3,30","0%","—","—","—","Barra Bonita"]},
              {t:"def",c:["PETROBAHIA","05/10/2023","06/06/2025","10 anos","GNL","18.000 → 18.000 → 40.000","3,72","70%","Anual","jan/26","R$ 554.668.768","Itabuna"]},
              {t:"tst",c:["PETYAN","04/07/2025","06/11/2025","10 meses","GNL","12.000 → 12.000 → 12.000","3,02","0%","—","—","—","Itabuna"]},
              {t:"def",c:["BAHIAGÁS","04/11/2025","07/05/2026","10 anos","GNL","1.625 → 1.625 → 25.175","3,82","70%","Anual","—","R$ 205.344.029","Itabuna"]},
              {t:"def",c:["ALGÁS","13/02/2026","01/09/2026","5 anos","GNCp","3.000 → 3.000 → 8.500","1,81","70%","Anual","—","R$ 18.637.448","Itabuna"]}
            ],
            foot:'<b>(1)</b> Preço net considera o preço de face do contrato, sem efeito da receita de locação e sem os reajustes de preço ao longo do tempo. &nbsp; <b>(2)</b> %TOP = parcela take-or-pay do volume contratado.<br>Fonte: GNLink — RCA, mai/2026 (slide 6).'},
          rcaJun:{kpiCls:"kpi-row5",tag:"ramp-up de volume · preço net atual",tagCol:true,total:"90.065 → 108.625 → 226.175",totalReal:"53.248",
            kpis:[["k-slate","Contratos assinados","15","6 definitivos · 9 em teste"],["k-teal","Prazo médio","2,7 <small>anos</small>","média simples dos 15 contratos"],["k-sage","Preço médio","R$ 3,38<small>/m³</small>","ponderado pelo volume final"],["k-stone","ToP médio","53,6%","ponderado pelo volume final"],["k-sage","Valor total dos contratos","R$ 1,09 <small>bi</small>","R$ 1.091.224.386"]],
            cols:["Contrato","Cliente","Assinatura","Início forn.","Prazo","Produto","Volume — ini → atual → final (m³/dia)","Real jun/26","Preço net (R$/m³)","%TOP","Apuração","Início TOP","Valor do contrato","Planta"],
            rows:[
              {t:"def",c:["COMPAGÁS","29/12/2025","12/03/2026","1 ano","GNL","7.000 → 20.000 → 20.000","26.393","3,85","70%","Anual","mar/26","R$ 71.832.000","Barra Bonita"]},
              {t:"tst",c:["SK METAIS","23/06/2026","—","180 dias","GNL","3.000 → 3.000 → 4.000","0","3,80","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["FEVEREIRO","28/01/2026","09/02/2026","330 dias","GNCp","3.000 → 4.000 → 4.000","709","3,20","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["RB EMBALAGENS","15/05/2026","—","180 dias","GNCp","1.000 → 1.000 → 3.000","0","3,45","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["DALLON","19/01/2026","—","330 dias","GNCp","6.000 → 6.000 → 10.000","0","2,90","0%","—","—","—","Barra Bonita"]},
              {t:"tst",c:["DALPARE","03/01/2026","—","330 dias","GNCp","2.200 → 2.000 → 2.000","0","3,30","0%","—","—","—","Barra Bonita"]},
              {t:"def",c:["PETROBAHIA","05/10/2023","06/06/2025","10 anos","GNL","18.000 → 18.000 → 40.000","2.066","3,72","70%","Anual","jan/26","R$ 544.668.768","Itabuna"]},
              {t:"def",c:["BAHIAGÁS","04/11/2025","—","10 anos","GNL","1.625 → 1.625 → 25.175","429","3,82","70%","Anual","—","R$ 205.344.029","Itabuna"]},
              {t:"def",c:["ALGÁS","19/02/2026","—","5 anos","GNCp","3.000 → 3.000 → 8.000","0","1,81","70%","Anual","—","R$ 18.637.448","Itabuna"]},
              {t:"tst",c:["PETYAN","04/07/2025","06/11/2025","10 meses","GNL","12.000 → 12.000 → 12.000","2.426","3,42","0%","—","—","—","Itabuna"]},
              {t:"def",c:["CEGÁS","29/10/2025","03/11/2025","5 anos","GNL","18.740 → 22.000 → 50.000","17.645","3,38","70%","Trimestral","fev/26","R$ 226.003.744","Assú"]},
              {t:"def",c:["COPERGÁS","03/02/2026","09/03/2026","3 anos","GNL","10.000 → 10.000 → 30.000","2.452","3,34","70%","Trimestral","Regás fixa","R$ 24.738.397","Assú"]},
              {t:"tst",c:["LIDER","04/03/2026","05/03/2026","330 dias","GNCp","1.000 → 1.000 → 6.000","0","1,90","0%","—","—","—","Assú"]},
              {t:"tst",c:["MERI POBO","27/01/2026","—","180 dias","GNCp","2.000 → 2.000 → 6.000","0","3,17","0%","—","—","—","Assú"]},
              {t:"tst",c:["PARELHAS","16/04/2026","16/04/2026","330 dias","GNCp","1.500 → 3.000 → 6.000","1.128","2,05","0%","—","—","—","Assú"]}
            ],
            foot:'<b>(1)</b> Preço net considera o preço de face do contrato, sem efeito da receita de locação e sem os reajustes de preço ao longo do tempo. &nbsp; <b>(2)</b> Volume inicial, atual e final referem-se à rampa definida em contrato; o volume <b>real</b> é a média diária de jun/26. &nbsp; <b>(3)</b> %TOP = parcela take-or-pay do volume contratado.<br>Fonte: GNLink — RCA, jun/2026 (slide 6).'}
        },
        negociacao:{
          rci:{cols:[
            {cls:"neg",title:"Em negociação",total:"275.000",plants:[
              {pl:"PR",sub:"105.000",cli:[{n:"Mosaic",v:"85.000",w:66.9,reg:"sul"},{n:"SCGás / Parati",v:"20.000",w:15.7,reg:"sul"}]},
              {pl:"BA",sub:"159.000",cli:[{n:"Ibar",v:"13.000",w:10.2,reg:"ne"},{n:"PBIO",v:"10.000",w:7.9,reg:"ne"},{n:"Vanadium",v:"9.000",w:7.1,reg:"ne"},{n:"Bahiagás (BRU)",v:"127.000",w:100,reg:"ne"}]},
              {pl:"RN",sub:"11.000",cli:[{n:"Lactalis",v:"6.000",w:4.7,reg:"ne"},{n:"Master Boi",v:"5.000",w:3.9,reg:"ne"}]}
            ]},
            {cls:"ctr",title:"Negociações contratuais",total:"96.500",plants:[
              {pl:"PR",sub:"46.500",cli:[{n:"Compagás (Lapa)",v:"20.000",w:66.7,reg:"sul"},{n:"Alcast",v:"20.000",w:66.7,reg:"sul"},{n:"Dallon",sm:"GNCp",v:"6.500",w:21.7,reg:"sul"}]},
              {pl:"BA",sub:"10.000",cli:[{n:"Nexa",v:"10.000",w:33.3,reg:"ne"}]},
              {pl:"RN",sub:"40.000",cli:[{n:"Copergás (Trindade)",v:"30.000",w:100,reg:"ne"},{n:"PetroReconcavo",v:"10.000",w:33.3,reg:"ne"}]}
            ]}
          ]},
          rca:{foot:'<b>Em negociação — BID</b> e <b>Em contrato</b> somam a base ativa do funil; probabilidade indica a chance de conversão do volume em contrato.',cols:[
            {cls:"neg",title:"Em negociação — BID",total:"596.050",plants:[
              {pl:"B. Bonita",sub:"305.000",cli:[{n:"CP Compagás – Firme",v:"16.000",w:6.2},{n:"CP Compagás – Flex",v:"25.000",w:9.6},{n:"MOR",v:"4.000",w:1.5},{n:"Sulgás",v:"260.000",w:100}]},
              {pl:"Itabuna",sub:"170.050",cli:[{n:"CP Bahiagás (BRU)",v:"126.000",w:48.5},{n:"CP Bahiagás (JZ)",v:"9.400",w:3.6},{n:"Vanadio",v:"12.000",w:4.6},{n:"Goiasgás",v:"20.000",w:7.7},{n:"Eurofarma",v:"2.650",w:1}]},
              {pl:"Assú",sub:"121.000",cli:[{n:"Piaui Niquel",v:"100.000",w:38.5},{n:"Gaspisa",v:"10.000",w:3.8},{n:"Lactalis",v:"6.000",w:2.3},{n:"Master Boi",v:"5.000",w:1.9}]}
            ]},
            {cls:"ctr",title:"Em contrato",total:"45.100",plants:[
              {pl:"B. Bonita",sub:"35.100",cli:[{n:"Alcast",v:"20.000",w:100,prob:"baixa"},{n:"Grupo Stara",v:"12.000",w:60,prob:"media"},{n:"Dalba",v:"1.100",w:5.5,prob:"alta"},{n:"SAMP",v:"2.000",w:10,prob:"media"}]},
              {pl:"Assú",sub:"10.000",cli:[{n:"PetroReconcavo",v:"10.000",w:50,prob:"alta"}]}
            ]}
          ]},
          rcaJun:{foot:'<b>Em negociação — BID</b> e <b>Em contrato</b> somam a base ativa do funil. Em jun/26, Alcast, Dalba e SAMP voltaram de "Em contrato" para "Em negociação — BID", e o deck deixou de indicar probabilidade de conversão.<br>Fonte: GNLink — RCA, jun/2026 (slide 6).',cols:[
            {cls:"neg",title:"Em negociação — BID",total:"603.350",plants:[
              {pl:"B. Bonita",sub:"328.100",cli:[{n:"CP Compagás – Firme",v:"16.000",w:6.2},{n:"CP Compagás – Flex",v:"25.000",w:9.6},{n:"Alcast",v:"20.000",w:7.7},{n:"Dalba",v:"1.100",w:0.4},{n:"MOR",v:"4.000",w:1.5},{n:"SAMP",v:"2.000",w:0.8},{n:"Sulgás",v:"260.000",w:100}]},
              {pl:"Itabuna",sub:"153.250",cli:[{n:"CP Bahiagás (BRU)",v:"126.000",w:48.5},{n:"CP Bahiagás (JZ)",v:"9.400",w:3.6},{n:"CBL",v:"4.000",w:1.5},{n:"Vanadio",v:"9.000",w:3.5},{n:"Grafite do Brasil",v:"2.200",w:0.8},{n:"Eurofarma",v:"2.650",w:1}]},
              {pl:"Assú",sub:"122.000",cli:[{n:"Piaui Niquel",v:"100.000",w:38.5},{n:"Gaspisa",v:"10.000",w:3.8},{n:"Copergás Ingenor ARP",v:"3.000",w:1.2},{n:"Master Boi",v:"9.000",w:3.5}]}
            ]},
            {cls:"ctr",title:"Em contrato",total:"46.500",plants:[
              {pl:"B. Bonita",sub:"24.500",cli:[{n:"GoiasGás",v:"20.000",w:100},{n:"Lhoist",v:"4.500",w:22.5}]},
              {pl:"Assú",sub:"22.000",cli:[{n:"PetroReconcavo",v:"10.000",w:50},{n:"Grupo Stara",v:"12.000",w:60}]}
            ]}
          ]}
        },
        demanda:{
          rci:{tag:"mil m³/dia · topo = total",tableColored:false,labels:["PR","BA","RN"],scale:"Barras: m³/dia · escala 197.500 (capacidade plena)",
            supply:{PR:[null,34300,32000,32000,43000,43000,43000,43000,43000,43000,43000,43000],BA:[14625,14625,33625,33625,33625,46625,46625,56625,56625,59625,59625,62625],RN:[19740,12247,26000,31000,38000,40000,41000,68000,74000,74000,74000,74000]},
            occ:["42%","39%","59%","62%","58%","66%","66%","85%","88%","89%","89%","91%"],
            note:'% Ocupação = demanda ÷ oferta do mês. Atinge 91% da capacidade plena das 3 plantas em dez/26.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 5).'},
          rca:{tag:"mil m³/dia · topo = total · realizado até mai/26",tableColored:true,labels:["B. Bonita (PR)","Itabuna (BA)","Assú (RN)"],scale:"Barras: m³/dia · escala 197.500 (capacidade plena a partir de out/26)",
            supply:{PR:[4500,null,2700,1900,8900,29300,20200,22000,22000,22000,22000,22000],BA:[5000,6700,5000,7300,9800,3900,10200,27900,31200,30900,30800,31300],RN:[13300,6800,16400,20700,20200,20800,24300,27900,35300,35400,35300,35400]},
            occ:["28%","12%","21%","26%","34%","47%","48%","68%","77%","45%","45%","45%"],
            note:'Demanda GNL por planta usando dados <b>realizados até mai/26</b> e <b>forecast</b> a partir de jun/26. Capacidade total sobe de ~114.600 (fev–set) para 197.500 m³/dia a partir de out/26 (2ª unidade de regas em Itabuna e Assú), o que reduz a ocupação apesar da demanda crescente.<br>Fonte: GNLink — RCA, mai/2026 (slides 21 · Barra Bonita, 26 · Itabuna, 31 · Assú).'}
        },
        capacidade:{
          rca:{
            gnl:{head:"Ocupação total 76% · oferta 114.612 · demanda 86.625",tiles:[["k-teal","Assú · GNL","99%","Demanda 32.000 · Oferta 32.416",99],["k-sage","Itabuna · GNL","74%","Demanda 31.625 · Oferta 42.616",74],["k-stone","B. Bonita · GNL","58%","Demanda 23.000 · Oferta 39.580",58]]},
            gncp:{head:"Ocupação total 51% · oferta 43.200 · demanda 22.000",tiles:[["k-teal","Assú · GNCp","42%","Demanda 6.000 · Oferta 14.400",42],["k-sage","Itabuna · GNCp","21%","Demanda 3.000 · Oferta 14.400",21],["k-stone","B. Bonita · GNCp","90%","Demanda 13.000 · Oferta 14.400",90]]},
            note:'Oferta = capacidade instalada por planta e produto; demanda = volume atual dos contratos assinados. GNL agregado a 76% e GNCp a 51%.<br>Fonte: GNLink — RCA, mai/2026 (slide 6).'},
          rcaJun:{
            gnl:{head:"Ocupação total 39% · oferta 130.665 · demanda 51.411",tiles:[["k-teal","Assú · GNL","62%","Demanda 20.097 · Oferta 32.416",62],["k-sage","B. Bonita · GNL","47%","Demanda 26.393 · Oferta 55.633",47],["k-stone","Itabuna · GNL","12%","Demanda 4.921 · Oferta 42.616",12]]},
            gncp:{head:"Ocupação total 4% · oferta 43.200 · demanda 1.837",tiles:[["k-teal","Assú · GNCp","8%","Demanda 1.128 · Oferta 14.400",8],["k-sage","B. Bonita · GNCp","5%","Demanda 709 · Oferta 14.400",5],["k-stone","Itabuna · GNCp","0%","Demanda 0 · Oferta 14.400",0]]},
            note:'Oferta = capacidade instalada por planta e produto. <b>Atenção à quebra de série vs. mai/26:</b> no deck de jun/26 a demanda passou a ser o <b>volume real médio diário do mês</b>, enquanto em mai/26 era o volume <b>atual dos contratos</b>. A ocupação do GNL cai de 76% para 39% sobretudo por essa mudança de definição — e não por perda de contratos. A oferta de GNL da B. Bonita também subiu de 39.580 para 55.633 m³/dia.<br>Fonte: GNLink — RCA, jun/2026 (slide 6).'}}
      },
      financeiro:{
        dre:{tag:"R$ milhões",tblCls:"placeholder-table dre-tbl",
          cols:[["R$ milhões",""],["PR",""],["BA",""],["RN",""],["Consolidado","c-con"],["BP Copa¹","c-bp"]],
          rows:[
            {cls:"dre-r",cells:['Capacidade Real <small style="color:var(--muted)">(m³/dia)</small>',"53.980","85.427","87.088","226.495","270.708"]},
            {cls:"dre-r",cells:['Volume GNL + GNC <small style="color:var(--muted)">(m³/dia)</small>',"50.872","43.208","49.666","143.746","270.708"]},
            {cls:"dre-r",cells:["% de Utilização","94,2%","50,6%","57,0%","63,5%","100,0%"]},
            {cls:"dre-r",cells:["Receita Líquida","63,0","63,5","58,9","185,4","376,3"]},
            {cls:"dre-r",cells:["Resultado Operacional","7,6","6,8","7,0","21,4","114,8"]},
            {cls:"dre-s",noNeg:true,cells:["Margem Operacional","12,1%","10,7%","11,9%","11,5%","30,5%"]},
            {cls:"dre-r",cells:["EBITDA","—","—","—","(5,5)","89,8"]},
            {cls:"dre-s",noNeg:true,cells:["Margem EBITDA","—","—","—","(3,0%)","23,9%"]},
            {cls:"dre-r",cells:["Lucro Líquido","—","—","—","(55,3)","15,8"]},
            {cls:"dre-s",noNeg:true,cells:["Margem Líquida","—","—","—","(29,8%)","4,2%"]},
            {cls:"dre-r",cells:["Saldo Final de Caixa Livre³","—","—","—","(29,3)","—"]}
          ],
          obs:["Ramp-up: 91% da capacidade real das 3 plantas em dez/26.","Preço médio inferior, conforme plano.","Manutenção e reajuste dos contratos atuais (Tradener, Bahiagás e PetroRecôncavo).","BA: compra de volume adicional no mercado livre para reduzir o custo médio da molécula.","Energia elétrica do mercado livre no PR e BA.","RN: geradores a gás (sem disponibilidade de energia da rede local).","Diluição de custos fixos com o aumento do volume.","Realocação de custos de veículos e viagens da matriz para as plantas.","Maior depreciação pela ativação da planta do RN."],
          note:'<b>BP Copa¹:</b> Business Plan da transação de M&amp;A considerando 3 plantas (ao invés de 4). &nbsp; <b>³</b> Saldo de caixa livre considera o fundo de liquidez do BNB (retido): 3% do desembolsado na BA e 5% no RN.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 8). A coluna de BP com capacidades ajustadas ao orçamento foi omitida, conforme solicitado.'},
        fcxHist:{tag:"R$ milhões",tblCls:"placeholder-table fcx-tbl",
          cols:[["R$ mi",""],["2022",""],["2023",""],["2024",""],["FCT/25¹","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(+/–) EBITDA","(2,0)","(12,5)","(20,7)","(45,9)"]},
            {cls:"fcx-sub",cells:["Matriz","(2,0)","(12,5)","(22,2)","(26,7)"]},
            {cls:"fcx-sub",cells:["Projetos","0,0","0,0","1,5","(19,2)"]},
            {cls:"fcx-sub2",cells:["PR","0,0","0,0","1,2","(9,7)"]},
            {cls:"fcx-sub2",cells:["BA","0,0","0,0","0,3","(8,4)"]},
            {cls:"fcx-sub2",cells:["RN","0,0","0,0","0,0","(1,1)"]},
            {cls:"fcx-h",cells:["(–) IRPJ / CSLL","0,0","0,0","0,0","0,0"]},
            {cls:"fcx-h",cells:["(+/–) Δ Capital de Giro","0,0","0,4","1,3","(1,3)"]},
            {cls:"fcx-tot",cells:["(=) F.C. Operacional","(2,0)","(12,1)","(19,5)","(47,1)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) CapEx","0,0","(53,5)","(154,6)","(99,8)"]},
            {cls:"fcx-sub",cells:["Matriz","0,0","(1,1)","(1,3)","(0,3)"]},
            {cls:"fcx-sub",cells:["PR","0,0","(39,6)","(30,9)","(13,0)"]},
            {cls:"fcx-sub",cells:["BA","0,0","(12,8)","(77,9)","(29,6)"]},
            {cls:"fcx-sub",cells:["RN","0,0","0,0","(44,4)","(57,0)"]},
            {cls:"fcx-tot",cells:["(=) F.C. de Investimentos","0,0","(53,5)","(154,6)","(99,8)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(+) Aporte Hankoe","5,5","46,3","49,2","0,0"]},
            {cls:"fcx-h",cells:["(+) Aporte Copa Energia","0,0","0,0","0,0","100,0"]},
            {cls:"fcx-h",cells:["(+) Ingresso de dívida","0,0","50,0","111,0","140,5"]},
            {cls:"fcx-h",cells:["(–) Pgto Principal","0,0","0,0","0,0","(47,5)"]},
            {cls:"fcx-h",cells:["(–) Resultado Financeiro","0,0","0,0","(3,0)","(27,7)"]},
            {cls:"fcx-tot",cells:["(=) F.C. de Financiamento","5,5","96,3","157,2","193,0"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Saldo Inicial de Caixa","0,0","3,5","34,2","17,4"]},
            {cls:"fcx-key",cells:["Geração de Caixa — GNLink","3,5","30,7","(16,8)","18,8"]},
            {cls:"fcx-key",cells:["Saldo Final de Caixa","3,5","34,2","17,4","36,3"]},
            {cls:"fcx-key",cells:["Fundo de Líquidez BNB (retido)","0,0","0,0","2,1","6,4"]},
            {cls:"fcx-key fcx-strong",cells:["Saldo Final de Caixa Livre","3,5","34,2","15,3","29,8"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Dívida Bruta","0,0","50,1","94,9","260,2"]},
            {cls:"fcx-key fcx-strong",cells:["Dívida Líquida","0,0","15,8","77,5","223,9"]}
          ],
          note:'<b>¹ FCT/25:</b> forecast do ano fechado de 2025 (jan–ago realizado + set–dez projetado). &nbsp; <b>Fundo de Líquidez BNB (retido):</b> 3% do desembolsado na BA e 5% no RN — retido em caixa, não utilizável.<br>As colunas mensais (jan–ago/25, set–dez/25) e as de Orçamento/25 e variação foram omitidas, conforme solicitado. Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 19).'},
        fcxMensal:{tag:"R$ milhões",tblCls:"placeholder-table fcx-tbl mfc-tbl",
          cols:[["R$ mi",""],["jan/26",""],["fev/26",""],["mar/26",""],["abr/26",""],["mai/26",""],["jun/26",""],["jul/26",""],["ago/26",""],["set/26",""],["out/26",""],["nov/26",""],["dez/26",""],["FC 2026¹","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(+/–) EBITDA","(4,1)","(2,4)","(6,6)","(1,0)","(0,8)","(0,4)","(0,2)","2,1","1,5","2,8","2,0","1,6","(5,5)"]},
            {cls:"fcx-sub",cells:["Matriz","(1,9)","(1,7)","(6,6)","(1,9)","(1,9)","(1,7)","(1,8)","(1,8)","(1,9)","(1,8)","(2,0)","(2,1)","(26,9)"]},
            {cls:"fcx-sub",cells:["Projetos","(2,3)","(0,8)","(0,1)","0,9","1,1","1,3","1,6","3,9","3,4","4,6","4,1","3,7","21,4"]},
            {cls:"fcx-sub2",cells:["PR","(1,0)","0,5","0,5","0,5","0,4","1,0","1,0","1,0","0,9","1,0","0,8","0,9","7,6"]},
            {cls:"fcx-sub2",cells:["BA","(0,5)","(0,7)","(0,1)","0,4","0,4","0,5","0,2","1,2","1,1","1,6","1,5","1,3","6,8"]},
            {cls:"fcx-sub2",cells:["RN","(0,8)","(0,6)","(0,4)","—","0,3","(0,2)","0,4","1,7","1,5","2,0","1,8","1,5","7,0"]},
            {cls:"fcx-h",cells:["(–) IRPJ / CSLL","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+/–) Δ Capital de Giro","4,1","(0,6)","(0,9)","0,2","(0,3)","(0,2)","(0,2)","(1,0)","(0,1)","(0,3)","0,3","(0,2)","0,8"]},
            {cls:"fcx-tot",cells:["(=) F.C. Operacional","(0,1)","(3,0)","(7,6)","(0,8)","(1,1)","(0,6)","(0,4)","1,1","1,4","2,6","2,3","1,4","(4,7)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) CapEx","(12,2)","(9,5)","(8,3)","(1,7)","(0,4)","(0,4)","(1,0)","(0,6)","(0,6)","—","—","—","(34,8)"]},
            {cls:"fcx-sub",cells:["Matriz","—","—","—","—","—","—","—","—","—","—","—","—","(0,2)"]},
            {cls:"fcx-sub",cells:["PR","(3,7)","(2,3)","(1,9)","(0,7)","—","—","—","—","—","—","—","—","(8,6)"]},
            {cls:"fcx-sub",cells:["BA","(3,9)","(3,6)","(3,3)","(0,4)","(0,2)","(0,2)","(0,2)","—","—","—","—","—","(11,7)"]},
            {cls:"fcx-sub",cells:["RN","(4,7)","(3,6)","(3,2)","(0,6)","(0,2)","(0,2)","(0,8)","(0,6)","(0,6)","—","—","—","(14,3)"]},
            {cls:"fcx-tot",cells:["(=) F.C. de Investimentos","(12,2)","(9,5)","(8,3)","(1,7)","(0,4)","(0,4)","(1,0)","(0,6)","(0,6)","—","—","—","(34,8)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(+) Aporte Hankoe","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Aporte Copa Energia","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Ingresso de dívida","100,0","10,7","—","—","—","—","—","—","—","—","—","—","110,7"]},
            {cls:"fcx-h",cells:["(–) Pgto Principal","(90,0)","—","—","—","—","—","—","—","—","(0,7)","(0,7)","(0,7)","(92,1)"]},
            {cls:"fcx-h",cells:["(–) Resultado Financeiro","(6,9)","0,3","(4,1)","—","—","(10,7)","—","—","(4,4)","—","—","(12,0)","(37,7)"]},
            {cls:"fcx-tot",cells:["(=) F.C. de Financiamento","3,1","11,0","(4,1)","—","—","(10,7)","—","—","(4,4)","(0,7)","(0,7)","(12,7)","(19,0)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Saldo Inicial de Caixa","36,3","27,0","25,5","5,5","3,0","1,6","(10,0)","(11,3)","(10,9)","(14,5)","(12,7)","(11,0)","36,3"]},
            {cls:"fcx-key",cells:["Geração de Caixa — GNLink","(9,2)","(1,5)","(20,0)","(2,5)","(1,4)","(11,6)","(1,3)","0,5","(3,6)","1,8","1,6","(11,3)","(58,6)"]},
            {cls:"fcx-key",cells:["Saldo Final de Caixa","27,0","25,5","5,5","3,0","1,6","(10,0)","(11,3)","(10,9)","(14,5)","(12,7)","(11,0)","(22,4)","(22,4)"]},
            {cls:"fcx-key",cells:["Fundo de Líquidez BNB (retido)","6,4","6,4","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9"]},
            {cls:"fcx-key fcx-strong",cells:["Saldo Final de Caixa Livre","20,6","19,1","(1,4)","(3,9)","(5,3)","(16,9)","(18,3)","(17,8)","(21,4)","(19,6)","(18,0)","(29,3)","(29,3)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Dívida Bruta","265,4","278,8","277,3","280,0","282,7","274,8","277,5","280,2","278,6","280,6","282,6","272,7","272,7"]},
            {cls:"fcx-key fcx-strong",cells:["Dívida Líquida","238,4","253,3","271,8","277,0","281,1","284,8","288,8","291,1","293,1","293,2","293,7","295,1","295,1"]}
          ],
          note:'<b>¹ FC 2026:</b> forecast (total) do orçamento de 2026. &nbsp; <b>Fundo de Líquidez BNB (retido):</b> 3% do desembolsado na BA e 5% no RN — retido em caixa, não utilizável.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 20).'}
      },
      competidores:{
        intro:"Universo de competidores organizado por elo (segmento) da cadeia de energia térmica. Em destaque, o elo onde a GNLink atua.",
        legend:"Elo da GNLink",
        feature:{title:"Onde a GNLink compete — Distribuidoras de GNL/GNC",invest:"Lorinvest · White Martins · J&amp;F · Copa Energia · Ultragaz",comps:[
          {self:true,name:"GNLink",role:"Nossa investida",detail:"Small Scale LNG · liquefação e regaseificação onshore e distribuição de GNL por modal rodoviário."},
          {name:"GásLocal",role:"GNL/GNC",detail:"Informações detalhadas a incluir."},
          {name:"Logás",role:"GNL/GNC",detail:"Informações detalhadas a incluir."},
          {name:"CTG",role:"GNL/GNC",detail:"Informações detalhadas a incluir."},
          {name:"CDGN",role:"GNL/GNC",detail:"Informações detalhadas a incluir."},
          {name:"NEOgás",role:"GNL/GNC",detail:"Informações detalhadas a incluir."},
          {name:"Eneva Small Scale",role:"GNL/GNC",detail:"Informações detalhadas a incluir."},
          {name:"Edge",role:"GNL/GNC",href:"empresas/gnlink/analises-setoriais/competidores/compass/index.html",detail:"Informações detalhadas a incluir."}
        ]},
        segments:[
          {dot:"#8A6D3B",title:"Holdings diversificadas",count:"6 players",chips:[{name:"Compass",href:"empresas/gnlink/analises-setoriais/competidores/compass/index.html"},"Cosan","Energisa","J&amp;F","Mitsui","Ultrapar"]},
          {dot:"#55677C",title:"Distribuidoras de combustíveis",count:"4 players",chips:["Raízen","Ipiranga","Vibra Energia","Ultracargo"],invest:"Ultrapar · Cosan"},
          {dot:"#C55A17",title:"Distribuidoras de GLP",count:"4 players",chips:["Ultragaz","Copa Energia","Supergasbras","Nacional Gás"],invest:"Ultrapar · Itaúsa · SHV Energy · Edson Queiroz"},
          {dot:"#3D4A5C",title:"Distribuidoras de gás natural",count:"19+ players",regions:[
            {label:"Nordeste",chips:["Bahiagás","Algás","Sergás","Copergás","Cegás","Potigás (…)"]},
            {label:"Sudeste",chips:["Comgás","Gasmig","Naturgy","CEG","Necta","ESgás"]},
            {label:"Sul",chips:["Compagás","SCGás","Sulgás"]},
            {label:"Centro-Oeste",chips:["MSGás","MTGás","CEBGás","Goiasgás"]}
          ],invest:"Mitsui · Compass/Commit · Energisa"},
          {dot:"#4E8385",title:"Gas-to-Power",count:"4 players",chips:["Eneva","Âmbar Energia","KPS","Origem"],invest:"BTG · J&amp;F · Prisma"},
          {dot:"#6B8299",title:"Logística",count:"3 players",chips:["VirtuGNL","Rumo","Hidrovias do Brasil"],invest:"BTG · Perfin · Cosan · Ultrapar"}
        ]
      }}
    };

// Lista única de empresas do painel (ordem, ícone, logo, imagem de painel).
// Fonte única das pílulas (3 seletores) e do cabeçalho dos cards do Panorama.
window.COMPANIES = [
  {name:"Akron", icon:"ic-akron", logo:"logos/akron-logo.avif", panel:"logos/paineis/akron-painel.webp", pan:{rows:[{label:"% Lorinvest",value:"Pendente"},{label:"Aporte Lorinvest",value:"Pendente"},{label:"Correção IPCA",value:"Pendente"},{label:"Correção IPCA + 15%",value:"Pendente"}]}},
  {name:"Bioren", icon:"ic-bioren", logo:"logos/bioren-logo.jpg", panel:"logos/paineis/Bioren%20painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Eindom", icon:"ic-eindom", logo:"logos/eindom-logo.jpg", panel:"logos/paineis/Eindom%20painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Valsa", icon:"ic-eldry", logo:"logos/valsa-logo.svg", panel:"logos/paineis/valsa-painel.webp", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"GBS Storage", icon:"ic-gbs", logo:"logos/gbs-logo.jpg", panel:"logos/paineis/gbs-painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"GNLink", icon:"ic-gnlink", logo:"logos/gnlink-logo.jpg", panel:"logos/paineis/GNLink%20painel.jpg", active:true, pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"New Wave", icon:"ic-newwave", logo:"logos/new-wave-logo.jpg", panel:"logos/paineis/Newwave%20painel.jpg", rowBreak:true, pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Norcoast", icon:"ic-norcoast", logo:"logos/norcoast-logo.png", panel:"logos/paineis/norcoast-painel.webp", logoFill:true, pan:{rows:[{label:"% Lorinvest",value:"Pendente"},{label:"Aporte Lorinvest",value:"Pendente"},{label:"Correção IPCA",value:"Pendente"},{label:"Correção IPCA + 15%",value:"Pendente"}]}},
  {name:"Norflor", icon:"ic-norflor", logo:"logos/Norflor-logo.png", panel:"logos/paineis/Painel%20Norflor.png", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos",note:{txt:"desinvestido",title:"Negativo: os desinvestimentos já efetuados superam os aportes."}},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Norsul", icon:"ic-norsul", logo:"logos/norsul-logo.jpg", panel:"logos/paineis/Norsul2%20painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true,note:{txt:"via Lorentzen",title:"Participação indireta via Lorentzen; o painel da Norsul não tem fatia do Hankoe FIP."}},{label:"Valor Hankoe",kpi:"Valor Hankoe"},{label:"Valuation Múltiplo",kpi:"Valuation Múltiplo"},{label:"Valor Hankoe — Lorentzen (%)",kpi:"Valor Hankoe - Lorentzen (%)"}]}},
  {name:"Sileto", icon:"ic-sileto", logo:"logos/Sileto-logo.PNG", panel:"logos/paineis/Sileto%20painel.png", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true,note:{txt:"via Dyna",title:"Fatia do Dyna FIP. Demais acionistas: Crystall 51,6% e Fundo Nunki 8,4%."}},{label:"Aporte Lorinvest",kpi:"Aporte Total",note:{txt:"aporte total",title:"No painel da Sileto a métrica é rotulada &quot;Aporte Total&quot;, não &quot;Aportes Líquidos&quot;."}},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Target Bank", icon:"ic-target", logo:"logos/target-bank-logo.png", panel:"logos/paineis/Painel%20Target.png", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Tree+", icon:"ic-treeplus", logo:"logos/tree-logo.png", panel:"logos/paineis/Painel%20Norflor.png", panelAlt:"Painel Tree+ (painel da Norflor)", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true,note:{txt:"quotista",title:"Skog FIP – Multiestratégia: Hankoe 25,1%, Ti17 FIM 25,0%, Zest 25,0%, Mercuria 25,0%. Lorinvest é a gestora do fundo."}},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
];

// Analistas do To-Do Tracker (equipe). Ordem = ordem dos cards no Tracker.
// As TAREFAS ficam no banco (via /api/todos); esta lista é só quem são os
// analistas (nome, cobertura, foto, contato) para montar os cards.
window.ANALISTAS = [
  {nome:"Lucas Werner",  cfa:true,  role:"Research Lead",                                email:"lucas.werner@lorinvest.com",  phone:"+5521984401311", avatar:"logos/lucaswerner-logo.jpg"},
  {nome:"Lucas Marques", cfa:false, role:"Metals & Mining · Real Estate · Healthcare",   email:"lucas.marques@lorinvest.com", phone:"+5521995003329", avatar:"logos/lucasmarques-logo.jpg"},
  {nome:"Felipe Seixas", cfa:false, role:"Forestry · Cement",                             email:"felipe.seixas@lorinvest.com", phone:"+5521994484455", avatar:"logos/felipeseixas-logo.jpg"},
  {nome:"Murilo Nunes",  cfa:false, role:"Oil & Gas · Transportation · Industrial Tech",  email:"murilo.nunes@lorinvest.com",  phone:"+5521979028288", avatar:"logos/murilo-logo.jpg"}
];

// Organograma da estrutura societária (aba Panorama). Cada nó traz o DADO BRUTO
// (t: razão social · s: "CNPJ · país" · p: participação · k: classe visual) e a
// posição de layout (x,y,w,h) do desenho. A ORDEM do array é significativa: o
// script de render (index.html) liga os nós por índice, portanto não reordenar.
// Atualizado conforme organograma de 30/01/2026.
window.ORG = [
 {x:340,y:6,w:120,h:44,t:'Ragnhild Lorentzen',p:'24,86%',k:'per'},
 {x:470,y:6,w:120,h:44,t:'Haakon Lorentzen',p:'73,62%',k:'per'},
 {x:600,y:6,w:120,h:44,t:'Martha Freitas Lorentzen',p:'0,13%',k:'per'},
 {x:730,y:6,w:120,h:44,t:'Christian Fredrik Lorentzen',p:'1,13%',k:'per'},
 {x:860,y:6,w:120,h:44,t:'Olav Alexander Lorentzen',p:'0,13%',k:'per'},
 {x:990,y:6,w:120,h:44,t:'Sophia Anne Lorentzen',p:'0,13%',k:'per'},
 {x:360,y:96,w:170,h:46,t:'Lofoten FIP Multiestrategia IE',p:'100,00%',k:'fund'},
 {x:980,y:96,w:170,h:46,t:'Bygdoy FIP Multiestrategia IE',p:'100,00%',k:'fund'},
 {x:360,y:176,w:170,h:46,t:'Hankoe FIP Multiestrategia IE',p:'',k:'fund'},
 {x:980,y:176,w:170,h:46,t:'Dyna FIP Multiestrategia IE',p:'',k:'fund'},
 {x:20,y:280,w:152,h:64,t:'Boreal Brasil Part. S.A.',s:'62.806.695/0001-50 · Brasil',p:'14,70%',k:'brh'},
 {x:20,y:356,w:152,h:64,t:'Target Inst. de Pgto e Sec. de Creditos S.A.',s:'14.821.124/0001-42 · Brasil',p:'100,00%',k:'brh',o:1},
 {x:20,y:432,w:152,h:64,t:'TGT Securitizadora de Creditos S.A.',s:'64.122.386/0001-97 · Brasil',p:'92,31%',k:'brh',o:1},
 {x:20,y:508,w:152,h:64,t:'BioRen Tecnologia S.A.',s:'42.292.051/0001-84 · Brasil',p:'77,81%',k:'brh',o:1},
 {x:20,y:584,w:152,h:64,t:'Itaparica Beach Club Part. LTDA',s:'50.132.341/0001-99 · Brasil',p:'100,00%',k:'brh'},
 {x:20,y:660,w:152,h:64,t:'Itaparica Beach Club LTDA',s:'50.730.972/0001-00 · Brasil',p:'100,00%',k:'brh',o:1},
 {x:190,y:280,w:152,h:64,t:'GNLink Distribuidora de Gas Natural S.A.',s:'34.470.844/0001-18 · Brasil',p:'64,00%',k:'brh',o:1},
 {x:190,y:356,w:152,h:64,t:'GBS Estocagem de Gas Natural S.A.',s:'38.427.732/0001-35 · Brasil',p:'100,00%',k:'brh',o:1},
 {x:190,y:432,w:152,h:64,t:'Dharma IA S.A.',s:'57.968.071/0001-07 · Brasil',p:'21,61%',k:'brh',o:1},
 {x:190,y:508,w:152,h:64,t:'Eindom Participacoes S.A.',s:'48.803.998/0001-99 · Brasil',p:'100,00%',k:'brh'},
 {x:190,y:584,w:152,h:64,t:'Eindom Empreend. Imobiliarios S.A.',s:'36.099.356/0001-64 · Brasil',p:'100,00%',k:'brh'},
 {x:190,y:660,w:152,h:64,t:'Eindom House Adm. de Imoveis LTDA',s:'48.694.247/0001-81 · Brasil',p:'100,00%',k:'brh',o:1},
 {x:360,y:280,w:152,h:64,t:'Norflor Empreend. Florestais S.A.',s:'44.925.620/0001-07 · Brasil',p:'100,00%',k:'brh',o:1},
 {x:360,y:356,w:152,h:64,t:'Arven Ltda',s:'44.405.253/0001-10 · Brasil',p:'99,99%',k:'brh',o:1},
 {x:360,y:432,w:152,h:64,t:'Skog FIP Multiestrategia',s:'51.806.546/0001-75 · Brasil',p:'25,10%',k:'fund'},
 {x:360,y:508,w:152,h:64,t:'Tree Agroflorestal S.A.',s:'46.742.630/0001-32 · Brasil',p:'100,00%',k:'brh'},
 {x:360,y:584,w:152,h:64,t:'Tjoeme FIM CP IE',s:'32.041.793/0001-83 · Brasil',p:'100,00%',k:'fund'},
 {x:360,y:660,w:152,h:64,t:'Akron FIDC-NP',s:'43.809.937/0001-15 · Brasil',p:'100,00%',k:'fund'},
 {x:530,y:280,w:152,h:64,t:'Lorentzen Empreend. S.A.',s:'33.107.533/0001-26 · Brasil',p:'89,29% + 10,71%',k:'brh'},
 {x:530,y:356,w:152,h:64,t:'Cia de Navegacao S.A.',s:'33.127.002/0001-03 · Brasil',p:'76,84%',k:'brh',o:1},
 {x:530,y:432,w:152,h:64,t:'Norcoast Logistica S.A.',s:'48.009.424/0001-06 · Bermudas',p:'50,00%',k:'lite',o:1},
 {x:530,y:508,w:152,h:64,t:'Tyburn Ltd',s:'05.605.594/0001-88 · Bermudas',p:'100,00%',k:'lite'},
 {x:530,y:584,w:152,h:64,t:'Rio Broker (L.P.F.) Ltda.',s:'31.355.852/0001-25 · Brasil',p:'33,33%',k:'lite',o:1},
 {x:712,y:280,w:152,h:64,t:'Helser Saude S.A.',s:'33.534.973/0001-60 · Brasil',p:'70,00%',k:'brh'},
 {x:712,y:380,w:152,h:64,t:'Eldry Saude Holding S.A.',s:'32.324.414/0001-62 · Brasil',p:'92,02%',k:'brh'},
 {x:712,y:480,w:152,h:64,t:'Tann Odonto e Estetica S.A.',s:'32.112.982/0001-08 · Brasil',p:'82,67% + 17,33%',k:'brh'},
 {x:900,y:280,w:152,h:64,t:'Sileto Global Holding S.a.r.l',s:'Luxemburgo',p:'40,00%',k:'brh'},
 {x:1062,y:280,w:152,h:64,t:'Fielo Technologies Inc.',s:'39.995.546/0001-65 · Delaware - EUA',p:'26,60%',k:'brh'},
 {x:900,y:380,w:152,h:64,t:'NWF HoldCo',s:'Cayman',p:'78,44%',k:'brh'},
 {x:1062,y:380,w:152,h:64,t:'Fielo Technologies Brasil S.A.',s:'05.605.594/0001-88 · Brasil',p:'80,00%',k:'brh'},
 {x:900,y:480,w:152,h:64,t:'New Wave L.P. (Partnership)',s:'Cayman',p:'88,22%',k:'brh'},
 {x:1062,y:480,w:152,h:64,t:'New Wave G.P.',s:'',p:'100,00%',k:'brh'},
 {x:981,y:568,w:152,h:64,t:'New Wave Holding S.a.r.l',s:'48.364.956/0001-07 · Luxemburgo',p:'100,00%',k:'lite'},
 {x:796,y:656,w:152,h:64,t:'New Wave Royalties',s:'Uruguai',p:'1,00%',k:'lite'},
 {x:900,y:656,w:152,h:64,t:'New Wave Tech S.A.',s:'27.383.117/0001-58 · Brasil',p:'100,00%',k:'lite'},
 {x:1062,y:656,w:152,h:64,t:'Wave Nickel International S.a.r.L',s:'48.348.491/0001-07 · Luxemburgo',p:'100,00%',k:'lite'},
 {x:1224,y:656,w:152,h:64,t:'Wave Aluminium International S.a.r.L',s:'48.348.490/0001-62 · Luxemburgo',p:'100,00%',k:'lite'},
 {x:900,y:736,w:152,h:64,t:'New Wave Brasil S.A.',s:'51.138.361/0001-30 · Brasil',p:'100,00%',k:'lite'},
 {x:1062,y:736,w:152,h:64,t:'Wave Nickel S.A.',s:'42.099.568/0001-51 · Brasil',p:'100,00%',k:'lite'},
 {x:1224,y:736,w:152,h:64,t:'Wave Aluminium S.A.',s:'33.564.013/0001-42 · Brasil',p:'100,00%',k:'lite'}
];

// Cenário macro (aba Setores & Macro). Pares [valor, rótulo], na ordem exibida.
window.MACRO = [
  ["2,2%",    "PIB (ano corrente)"],
  ["4,0%",    "Inflação (12m)"],
  ["5,5%",    "Juros reais ex-ante"],
  ["R$ 5,20", "Câmbio (BRL/USD)"]
];
