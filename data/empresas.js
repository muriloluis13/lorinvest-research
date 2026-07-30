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
      "Norsul":{updated:"08/06/2026",pctHolder:"Lorentzen",analises:{resultados:[{title:"Demonstrações financeiras auditadas",meta:"Balanço patrimonial, DRE, fluxo de caixa e notas explicativas",href:"empresas/norsul/dfsauditadas/index.html"}]},aportes:{kpis:[["Valor Hankoe","1.547.592,3"],["Valuation Múltiplo","1.320.216,9"],["Valor Hankoe - Lorentzen (%)","1.189.123,5"],["Valuation Múltiplo - Lorentzen (%)","1.014.415,1"]],holdersTitle:"Acionistas",holders:[["Lorentzen",76.8],["Hugo",19.8],["Lily",0.7],["Luke",0.7],["Outros",2]]},governanca:[{title:"Conselho de Administração",eleito:"08/07/2025",mandato:"08/07/2028",membros:["Angelo Baroncini","Luciano Medeiros","Leonardo Szczerb","Pietro Allevato","Hugo Figueiredo"]},{title:"Diretoria",eleito:"08/04/2024",mandato:"08/04/2027",membros:["CEO: Rodrigo Cuesta","CFO: André Gonçalves","Dir. Operacional: Christian Lachmann"]}]},
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
        {cls:"btg",nm:"BBOG",loc:"PR",rows:[{v:"R$ 2,22",w:100,mm:"—",br:"—",cen:"Cativo · 10 anos"}]},
        {cls:"bah",nm:"Bahiagás",loc:"BA",rows:[{v:"R$ 1,95",w:88,mm:"—",br:"—",cen:"Cativo · 10 anos"}]},
        {cls:"pet",nm:"PetroRecôncavo",loc:"RN",rows:[{v:"R$ 1,76",w:79,mm:"—",br:"—",cen:"Cativo · 10 anos"}]}
      ]},
      molecula:{tag:"sem impostos · dez/25",note:'Premissas constantes para todas as linhas (omitidas da tabela): câmbio <b>R$ 5,45/US$</b> · Brent <b>US$ 68,97/bbl</b> · data <b>dez/25</b>. Preços <b>sem impostos</b>.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 18).',groups:[
        {cls:"tra",nm:"Tradener",loc:"PR",rows:[{v:"R$ 2,36",w:100,mm:"11,62",br:"16,85%",cen:"Preços anteriores atualizados"},{v:"R$ 2,00",w:85,mm:"9,83",br:"14,26%",cen:""},{v:"R$ 1,70",w:72,mm:"8,37",br:"12,13%",cen:"Oferta Tradener"}]},
        {cls:"bah",nm:"Bahiagás",loc:"BA",rows:[{v:"R$ 2,06",w:87,mm:"10,12",br:"14,67%",cen:"GNC Industrial"},{v:"R$ 1,91",w:81,mm:"9,42",br:"13,65%",cen:"GNC Veicular"}]},
        {cls:"btg",nm:"BTG",loc:"BA",rows:[{v:"R$ 2,03",w:86,brk:"molécula R$ 1,45 · gasoduto R$ 0,58",mm:"10,00",br:"10,35%",cen:"Firme"},{v:"R$ 1,98",w:84,brk:"molécula R$ 1,40 · gasoduto R$ 0,58",mm:"9,76",br:"10,00%",cen:"PUT"}]},
        {cls:"pet",nm:"PetroRecôncavo",loc:"BA",rows:[{v:"R$ 2,01",w:85,brk:"molécula R$ 1,44 · gasoduto R$ 0,57",mm:"9,90",br:"10,30%",cen:"Para Bahiagás"},{v:"R$ 1,61",w:68,loc2:"RN",mm:"7,93",br:"11,50%",cen:"Base"},{v:"R$ 1,44",w:61,mm:"7,10",br:"10,30%",cen:"Para Cegás"},{v:"R$ 0,49",w:21,mm:"2,41",br:"3,50%",cen:"Geração de EE"}]}
      ]}},comercial:{
        funil:{
          rci:{tag:"valores em m³/dia",note:'Da demanda total mapeada até os contratos assinados. <b>Mais de R$ 1 bilhão</b> em contratos já assinados.',rows:[["Mercado mapeado","1.673.638",100],["Em prospecção","1.099.537",65.7],["Em negociação","275.000",16.4],["Negociações contratuais","96.500",5.8],["Contratos assinados","56.865 – 132.175",7.9]]},
          rca:{tag:"valores em m³/dia · ex. Norte",note:'Da demanda total mapeada (exceto Norte) até os contratos assinados. <b>Mais de R$ 1,1 bilhão</b> em contratos assinados.',rows:[["Mercado mapeado","1.847.776",100],["Em prospecção","1.118.561",60.5],["Em negociação — BID","596.050",32.3],["Em contrato","45.100",12],["Contratos assinados","90.065 – 222.675",15]]},
          rcaJun:{tag:"valores em m³/dia · ex. Norte",note:'Da demanda total mapeada (exceto Norte) até os contratos assinados. <b>R$ 1,09 bilhão</b> em contratos assinados.',rows:[["Mercado mapeado","1.847.776",100],["Em prospecção","1.118.561",60.5],["Em negociação — BID","603.350",32.7],["Em contrato","46.500",12],["Contratos assinados","90.065 – 226.175",15]]}
        },
        assinados:{
          rci:{kpiCls:"kpi-row4",tag:"preço net · reajustado desde a data-base",
            kpis:[["k-slate","Contratos assinados","6","4 GNL · 2 GNCp"],["k-teal","Prazo médio","4,4 <small>anos</small>","média simples dos 6 contratos"],["k-sage","Preço médio","R$ 3,58<small>/m³</small>","GNL 3,61 · GNCp 2,60 · pond. pelo volume total"],["k-stone","Volume total contratado","132.175","m³/dia · ramp-up 56.865 →"]],
            cols:["Cliente","Assinatura","Início forn.","Prazo","Término","Produto","Inicial","Final","Preço net (R$/m³)","Planta"],
            rows:[
              ["CEGÁS","28/10/2025","03/11/2025","5 anos","28/10/2030","GNL","18.740","50.000","3,3041","RN"],
              ["BAHIAGÁS","04/11/2025","—","10 anos","31/12/2035","GNL","3.125","25.175","3,6359","BA"],
              ["PETROBAHIA","05/10/2023","06/06/2025","10 anos","06/06/2030","GNL","18.000","40.000","4,0780","BA"],
              ["PETYAN","04/07/2025","06/11/2025","10 meses","04/05/2026","GNL","12.000","12.000","3,3099","BA"],
              ["REITERLOG","12/02/2025","19/02/2025","90 dias","12/05/2025","GNCp","3.000","3.000","2,2000","PR"],
              ["RODOPRINCIPE","06/08/2025","23/07/2025","120 dias","04/12/2025","GNCp","2.000","2.000","3,2017","PR"]
            ],
            occ:[["k-teal","RN · cap. GNL","72.688","Ocupação GNL <b>69%</b>",69],["k-sage","BA · cap. GNL","85.232","Ocupação GNL <b>91%</b>",91],["k-stone","PR · cap. GNL","39.580","Ocupação GNL <b>0%</b>",0]],
            foot:'<b>(1)</b> Mais de R$ 1 bilhão em contratos assinados. &nbsp; <b>(2)</b> Preço atual considera reajustes aplicados desde a data-base do contrato. &nbsp; <b>(3)</b> 264 clientes foram passados para a COPA prospectar. &nbsp; <b>(4)</b> 46 clientes foram indicados pela COPA para a GNLink prospectar, sendo metade do volume em SP. &nbsp; <b>(5)</b> 70 clientes acima de 100 ton/mês na lista da GNLink, sendo apenas 16 na lista da COPA enviada à GNLink.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 4).'},
          rca:{kpiCls:"kpi-row4",tag:"ramp-up de volume (m³/dia) · preço net atual",tagCol:true,totalSpan:6,totalVols:["90.065","108.625","222.675"],
            kpis:[["k-slate","Contratos assinados","15","6 definitivos · 9 em teste"],["k-teal","Prazo médio","2,7 <small>anos</small>","média simples dos 15 contratos"],["k-sage","Preço médio","R$ 3,37<small>/m³</small>","GNL 3,55 · GNCp 2,57 · pond. pelo volume total"],["k-sage","Valor total dos contratos","R$ 1,10 <small>bi</small>","R$ 1.101.224.386"]],
            cols:["Contrato","Cliente","Assinatura","Início forn.","Prazo","Produto","Inicial","Atual","Final","Preço net (R$/m³)","%TOP","Apuração","Início TOP","Valor do contrato","Planta"],
            rows:[
              {t:"def",c:["CEGÁS","28/10/2025","03/11/2025","5 anos","GNL","18.740","22.000","50.000","3,38","70%","Trimestral","fev/26","R$ 226.003.744","RN"]},
              {t:"def",c:["COPERGÁS","28/01/2026","09/03/2026","3 anos","GNL","10.000","10.000","30.000","3,34","70%","Trimestral","Regás fixa","R$ 24.738.397","RN"]},
              {t:"tst",c:["POSTO LIDER","04/03/2026","05/03/2026","330 dias","GNCp","1.000","1.000","6.000","1,90","—","—","—","—","RN"]},
              {t:"tst",c:["PARELHAS GÁS","16/04/2026","16/04/2026","330 dias","GNCp","1.500","3.000","3.000","1,90","—","—","—","—","RN"]},
              {t:"tst",c:["MERI POBO","28/01/2026","19/05/2026","6 meses","GNCp","2.000","2.000","6.000","3,17","—","—","—","—","RN"]},
              {t:"def",c:["COMPAGÁS","29/12/2025","12/03/2026","1 ano","GNL","7.000","20.000","20.000","3,85","70%","Anual","mar/26","R$ 71.832.000","PR"]},
              {t:"tst",c:["SK METAIS","23/06/2026","15/07/2026","180 dias","GNL","3.000","3.000","4.000","3,80","—","—","—","—","PR"]},
              {t:"tst",c:["FEVEREIRO LD","28/01/2026","29/01/2026","330 dias","GNCp","3.000","4.000","4.000","3,20","—","—","—","—","PR"]},
              {t:"tst",c:["DALLON","21/01/2026","Pendente reunião","330 dias","GNCp","6.000","6.000","10.000","2,90","—","—","—","—","PR"]},
              {t:"tst",c:["RIO BONITO","15/05/2026","01/08/2026","180 dias","GNCp","1.000","1.000","2.000","3,45","—","—","—","—","PR"]},
              {t:"tst",c:["DALPARE","03/02/2026","20/08/2026","330 dias","GNCp","2.200","2.000","2.000","3,30","—","—","—","—","PR"]},
              {t:"def",c:["PETROBAHIA","05/10/2023","06/06/2025","10 anos","GNL","18.000","18.000","40.000","3,72","70%","Anual","jan/26","R$ 554.668.768","BA"]},
              {t:"tst",c:["PETYAN","04/07/2025","06/11/2025","10 meses","GNL","12.000","12.000","12.000","3,02","—","—","—","—","BA"]},
              {t:"def",c:["BAHIAGÁS","04/11/2025","07/05/2026","10 anos","GNL","1.625","1.625","25.175","3,82","70%","Anual","—","R$ 205.344.029","BA"]},
              {t:"def",c:["ALGÁS","13/02/2026","01/09/2026","5 anos","GNCp","3.000","3.000","8.500","1,81","70%","Anual","—","R$ 18.637.448","BA"]}
            ],
            foot:'<b>(1)</b> Preço net considera o preço de face do contrato, sem efeito da receita de locação e sem os reajustes de preço ao longo do tempo. &nbsp; <b>(2)</b> %TOP = parcela take-or-pay do volume contratado.<br>Fonte: GNLink — RCA, mai/2026 (slide 6).'},
          rcaJun:{kpiCls:"kpi-row4",tag:"ramp-up de volume (m³/dia) · preço net atual",tagCol:true,totalSpan:6,totalVols:["90.065","108.625","53.248","226.175"],
            kpis:[["k-slate","Contratos assinados","15","6 definitivos · 9 em teste"],["k-teal","Prazo médio","2,7 <small>anos</small>","média simples dos 15 contratos"],["k-sage","Preço médio","R$ 3,38<small>/m³</small>","GNL 3,57 · GNCp 2,58 · pond. pelo volume final"],["k-sage","Valor total dos contratos","R$ 1,09 <small>bi</small>","R$ 1.091.224.386"]],
            cols:["Contrato","Cliente","Assinatura","Início forn.","Prazo","Produto","Inicial","Atual","Real","Final","Preço net (R$/m³)","%TOP","Apuração","Início TOP","Valor do contrato","Planta"],
            rows:[
              {t:"def",c:["COMPAGÁS","29/12/2025","12/03/2026","1 ano","GNL","7.000","20.000","26.393","20.000","3,85","70%","Anual","mar/26","R$ 71.832.000","PR"]},
              {t:"tst",c:["SK METAIS","23/06/2026","—","180 dias","GNL","3.000","3.000","0","4.000","3,80","—","—","—","—","PR"]},
              {t:"tst",c:["FEVEREIRO","28/01/2026","09/02/2026","330 dias","GNCp","3.000","4.000","709","4.000","3,20","—","—","—","—","PR"]},
              {t:"tst",c:["RB EMBALAGENS","15/05/2026","—","180 dias","GNCp","1.000","1.000","0","3.000","3,45","—","—","—","—","PR"]},
              {t:"tst",c:["DALLON","19/01/2026","—","330 dias","GNCp","6.000","6.000","0","10.000","2,90","—","—","—","—","PR"]},
              {t:"tst",c:["DALPARE","03/01/2026","—","330 dias","GNCp","2.200","2.000","0","2.000","3,30","—","—","—","—","PR"]},
              {t:"def",c:["PETROBAHIA","05/10/2023","06/06/2025","10 anos","GNL","18.000","18.000","2.066","40.000","3,72","70%","Anual","jan/26","R$ 544.668.768","BA"]},
              {t:"def",c:["BAHIAGÁS","04/11/2025","—","10 anos","GNL","1.625","1.625","429","25.175","3,82","70%","Anual","—","R$ 205.344.029","BA"]},
              {t:"def",c:["ALGÁS","19/02/2026","—","5 anos","GNCp","3.000","3.000","0","8.000","1,81","70%","Anual","—","R$ 18.637.448","BA"]},
              {t:"tst",c:["PETYAN","04/07/2025","06/11/2025","10 meses","GNL","12.000","12.000","2.426","12.000","3,42","—","—","—","—","BA"]},
              {t:"def",c:["CEGÁS","29/10/2025","03/11/2025","5 anos","GNL","18.740","22.000","17.645","50.000","3,38","70%","Trimestral","fev/26","R$ 226.003.744","RN"]},
              {t:"def",c:["COPERGÁS","03/02/2026","09/03/2026","3 anos","GNL","10.000","10.000","2.452","30.000","3,34","70%","Trimestral","Regás fixa","R$ 24.738.397","RN"]},
              {t:"tst",c:["LIDER","04/03/2026","05/03/2026","330 dias","GNCp","1.000","1.000","0","6.000","1,90","—","—","—","—","RN"]},
              {t:"tst",c:["MERI POBO","27/01/2026","—","180 dias","GNCp","2.000","2.000","0","6.000","3,17","—","—","—","—","RN"]},
              {t:"tst",c:["PARELHAS","16/04/2026","16/04/2026","330 dias","GNCp","1.500","3.000","1.128","6.000","2,05","—","—","—","—","RN"]}
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
              {pl:"PR",sub:"305.000",cli:[{n:"CP Compagás – Firme",v:"16.000",w:6.2},{n:"CP Compagás – Flex",v:"25.000",w:9.6},{n:"MOR",v:"4.000",w:1.5},{n:"Sulgás",v:"260.000",w:100}]},
              {pl:"BA",sub:"170.050",cli:[{n:"CP Bahiagás (BRU)",v:"126.000",w:48.5},{n:"CP Bahiagás (JZ)",v:"9.400",w:3.6},{n:"Vanadio",v:"12.000",w:4.6},{n:"Goiasgás",v:"20.000",w:7.7},{n:"Eurofarma",v:"2.650",w:1}]},
              {pl:"RN",sub:"121.000",cli:[{n:"Piaui Niquel",v:"100.000",w:38.5},{n:"Gaspisa",v:"10.000",w:3.8},{n:"Lactalis",v:"6.000",w:2.3},{n:"Master Boi",v:"5.000",w:1.9}]}
            ]},
            {cls:"ctr",title:"Em contrato",total:"45.100",plants:[
              {pl:"PR",sub:"35.100",cli:[{n:"Alcast",v:"20.000",w:100,prob:"baixa"},{n:"Grupo Stara",v:"12.000",w:60,prob:"media"},{n:"Dalba",v:"1.100",w:5.5,prob:"alta"},{n:"SAMP",v:"2.000",w:10,prob:"media"}]},
              {pl:"RN",sub:"10.000",cli:[{n:"PetroReconcavo",v:"10.000",w:50,prob:"alta"}]}
            ]}
          ]},
          rcaJun:{foot:'<b>Em negociação — BID</b> e <b>Em contrato</b> somam a base ativa do funil. Em jun/26, Alcast, Dalba e SAMP voltaram de "Em contrato" para "Em negociação — BID", e o deck deixou de indicar probabilidade de conversão.<br>Fonte: GNLink — RCA, jun/2026 (slide 6).',cols:[
            {cls:"neg",title:"Em negociação — BID",total:"603.350",plants:[
              {pl:"PR",sub:"328.100",cli:[{n:"CP Compagás – Firme",v:"16.000",w:6.2},{n:"CP Compagás – Flex",v:"25.000",w:9.6},{n:"Alcast",v:"20.000",w:7.7},{n:"Dalba",v:"1.100",w:0.4},{n:"MOR",v:"4.000",w:1.5},{n:"SAMP",v:"2.000",w:0.8},{n:"Sulgás",v:"260.000",w:100}]},
              {pl:"BA",sub:"153.250",cli:[{n:"CP Bahiagás (BRU)",v:"126.000",w:48.5},{n:"CP Bahiagás (JZ)",v:"9.400",w:3.6},{n:"CBL",v:"4.000",w:1.5},{n:"Vanadio",v:"9.000",w:3.5},{n:"Grafite do Brasil",v:"2.200",w:0.8},{n:"Eurofarma",v:"2.650",w:1}]},
              {pl:"RN",sub:"122.000",cli:[{n:"Piaui Niquel",v:"100.000",w:38.5},{n:"Gaspisa",v:"10.000",w:3.8},{n:"Copergás Ingenor ARP",v:"3.000",w:1.2},{n:"Master Boi",v:"9.000",w:3.5}]}
            ]},
            {cls:"ctr",title:"Em contrato",total:"46.500",plants:[
              {pl:"PR",sub:"24.500",cli:[{n:"GoiasGás",v:"20.000",w:100},{n:"Lhoist",v:"4.500",w:22.5}]},
              {pl:"RN",sub:"22.000",cli:[{n:"PetroReconcavo",v:"10.000",w:50},{n:"Grupo Stara",v:"12.000",w:60}]}
            ]}
          ]}
        },
        demanda:{
          rci:{tag:"mil m³/dia · topo = total",tableColored:false,labels:["PR","BA","RN"],scale:"Barras: m³/dia · escala 197.500 (capacidade plena)",
            supply:{PR:[null,34300,32000,32000,43000,43000,43000,43000,43000,43000,43000,43000],BA:[14625,14625,33625,33625,33625,46625,46625,56625,56625,59625,59625,62625],RN:[19740,12247,26000,31000,38000,40000,41000,68000,74000,74000,74000,74000]},
            occ:["42%","39%","59%","62%","58%","66%","66%","85%","88%","89%","89%","91%"],
            note:'% Ocupação = demanda ÷ oferta do mês. Atinge 91% da capacidade plena das 3 plantas em dez/26.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 5).'},
          rca:{tag:"mil m³/dia · topo = total · realizado até mai/26",tableColored:true,labels:["PR","BA","RN"],scale:"Barras: m³/dia · escala 197.500 (capacidade plena a partir de out/26)",
            supply:{PR:[4500,null,2700,1900,8900,29300,20200,22000,22000,22000,22000,22000],BA:[5000,6700,5000,7300,9800,3900,10200,27900,31200,30900,30800,31300],RN:[13300,6800,16400,20700,20200,20800,24300,27900,35300,35400,35300,35400]},
            occ:["28%","12%","21%","26%","34%","47%","48%","68%","77%","45%","45%","45%"],
            note:'Demanda GNL por planta usando dados <b>realizados até mai/26</b> e <b>forecast</b> a partir de jun/26. Capacidade total sobe de ~114.600 (fev–set) para 197.500 m³/dia a partir de out/26 (2ª unidade de regas em BA e RN), o que reduz a ocupação apesar da demanda crescente.<br>Fonte: GNLink — RCA, mai/2026 (slides 21 · PR, 26 · BA, 31 · RN).'}
        },
        capacidade:{
          rca:{
            gnl:{head:"Ocupação total 76% · oferta 114.612 · demanda 86.625",tiles:[["k-teal","PR · GNL","58%","Demanda 23.000 · Oferta 39.580",58],["k-sage","BA · GNL","74%","Demanda 31.625 · Oferta 42.616",74],["k-stone","RN · GNL","99%","Demanda 32.000 · Oferta 32.416",99]]},
            gncp:{head:"Ocupação total 51% · oferta 43.200 · demanda 22.000",tiles:[["k-teal","PR · GNCp","90%","Demanda 13.000 · Oferta 14.400",90],["k-sage","BA · GNCp","21%","Demanda 3.000 · Oferta 14.400",21],["k-stone","RN · GNCp","42%","Demanda 6.000 · Oferta 14.400",42]]},
            note:'Oferta = capacidade instalada por planta e produto; demanda = volume atual dos contratos assinados. GNL agregado a 76% e GNCp a 51%.<br>Fonte: GNLink — RCA, mai/2026 (slide 6).'},
          rcaJun:{
            gnl:{head:"Ocupação total 39% · oferta 130.665 · demanda 51.411",tiles:[["k-teal","PR · GNL","47%","Demanda 26.393 · Oferta 55.633",47],["k-sage","BA · GNL","12%","Demanda 4.921 · Oferta 42.616",12],["k-stone","RN · GNL","62%","Demanda 20.097 · Oferta 32.416",62]]},
            gncp:{head:"Ocupação total 4% · oferta 43.200 · demanda 1.837",tiles:[["k-teal","PR · GNCp","5%","Demanda 709 · Oferta 14.400",5],["k-sage","BA · GNCp","0%","Demanda 0 · Oferta 14.400",0],["k-stone","RN · GNCp","8%","Demanda 1.128 · Oferta 14.400",8]]},
            note:'Oferta = capacidade instalada por planta e produto. <b>Atenção à quebra de série vs. mai/26:</b> no deck de jun/26 a demanda passou a ser o <b>volume real médio diário do mês</b>, enquanto em mai/26 era o volume <b>atual dos contratos</b>. A ocupação do GNL cai de 76% para 39% sobretudo por essa mudança de definição — e não por perda de contratos. A oferta de GNL da planta PR também subiu de 39.580 para 55.633 m³/dia.<br>Fonte: GNLink — RCA, jun/2026 (slide 6).'}}
      },
      financeiro:{
        // Fluxo de caixa histórico (visão "Resultados históricos") — base única.
        fcxHist:{tag:"R$ milhões",tblCls:"placeholder-table fcx-tbl",
          cols:[["R$ mi",""],["2022",""],["2023",""],["2024",""],["FCT/25¹","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(+/–) EBITDA","(2,0)","(12,5)","(20,7)","(45,9)"]},
            {cls:"fcx-sub",cells:["Matriz","(2,0)","(12,5)","(22,2)","(26,7)"]},
            {cls:"fcx-sub",cells:["Projetos","0,0","0,0","1,5","(19,2)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["PR","0,0","0,0","1,2","(9,7)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["BA","0,0","0,0","0,3","(8,4)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["RN","0,0","0,0","0,0","(1,1)"]},
            {cls:"fcx-h",cells:["(–) IRPJ / CSLL","0,0","0,0","0,0","0,0"]},
            {cls:"fcx-h",cells:["(+/–) Δ Capital de Giro","0,0","0,4","1,3","(1,3)"]},
            {cls:"fcx-tot",cells:["(=) CFO","(2,0)","(12,1)","(19,5)","(47,1)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) CapEx","0,0","(53,5)","(154,6)","(99,8)"]},
            {cls:"fcx-sub",cells:["Matriz","0,0","(1,1)","(1,3)","(0,3)"]},
            {cls:"fcx-sub fcx-plt",cells:["PR","0,0","(39,6)","(30,9)","(13,0)"]},
            {cls:"fcx-sub fcx-plt",cells:["BA","0,0","(12,8)","(77,9)","(29,6)"]},
            {cls:"fcx-sub fcx-plt",cells:["RN","0,0","0,0","(44,4)","(57,0)"]},
            {cls:"fcx-tot",cells:["(=) CFI","0,0","(53,5)","(154,6)","(99,8)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(+) Aporte Hankoe","5,5","46,3","49,2","0,0"]},
            {cls:"fcx-h",cells:["(+) Aporte Copa Energia","0,0","0,0","0,0","100,0"]},
            {cls:"fcx-h",cells:["(+) Ingresso de dívida","0,0","50,0","111,0","140,5"]},
            {cls:"fcx-h",cells:["(–) Pgto Principal","0,0","0,0","0,0","(47,5)"]},
            {cls:"fcx-h",cells:["(–) Resultado Financeiro","0,0","0,0","(3,0)","(27,7)"]},
            {cls:"fcx-tot",cells:["(=) CFF","5,5","96,3","157,2","193,0"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key fcx-blk fcx-blk-top",cells:["Caixa BoP","0,0","3,5","34,2","17,4"]},
            {cls:"fcx-key fcx-blk",cells:["(+/–) Δ Caixa","3,5","30,7","(16,8)","18,8"]},
            {cls:"fcx-key fcx-blk",cells:["Caixa EoP","3,5","34,2","17,4","36,3"]},
            {cls:"fcx-key fcx-blk",cells:["Fundo de Líquidez BNB (retido)","0,0","0,0","2,1","6,4"]},
            {cls:"fcx-key fcx-strong fcx-blk",cells:["Caixa EoP livre","3,5","34,2","15,3","29,8"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Dívida Bruta","0,0","50,1","94,9","260,2"]},
            {cls:"fcx-key fcx-strong",cells:["Dívida Líquida","0,0","15,8","77,5","223,9"]}
          ],
          note:'<b>¹ FCT/25:</b> forecast do ano fechado de 2025 (jan–ago realizado + set–dez projetado). &nbsp; <b>Fundo de Líquidez BNB (retido):</b> 3% do desembolsado na BA e 5% no RN — retido em caixa, não utilizável.<br>As colunas mensais (jan–ago/25, set–dez/25) e as de Orçamento/25 e variação foram omitidas, conforme solicitado. Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 19).'},
        // Orçamento 2026 por base de dados (seletor RCI Dez/25 / RCA Mai/26 / RCA Jun/26).
        // Cada base é { dre:{...}, fcxMensal:{...} } — ambos opcionais. "rci" tem DRE +
        // fluxo mensal (CI Dez/25); "rcaJun" tem só o fluxo mensal (RCA Jun/26, slide 16).
        // Bases anteriores nunca são sobrescritas: base nova entra como item adicional.
        orc2026:{
        rci:{
        // Faixa de KPIs do orçamento 2026. O CI Dez/25 não abre custos por etapa em
        // nenhum slide, então esta base não tem os cards de molécula e de custos GNLink;
        // o volume do ano vem de 143.746 m³/dia × 365 (o deck só publica a média diária).
        kpis:{groups:[
          {cls:"kpi-grid",tiles:[
            {c:"k-slate",k:"Receita líquida 2026",v:"185,4",u:"R$ mi",
             s:"PR 63,0 · BA 63,5 · RN 58,9",
             sub:'Volume do ano <b>52,5 mi de m³</b> · utilização <b>63,5%</b>'},
            {c:"k-slate",k:"Preço médio",v:"3,53",u:"R$/m³",
             s:"Orçamento, sem abertura por produto",
             sub:'Implícito: receita ÷ <b>143.746 m³/dia</b> × 365'},
            {c:"k-stone",k:"Despesas matriz",v:"(26,9)",u:"R$ mi",neg:true,
             s:"Contra 21,4 de resultado dos projetos",
             sub:'<b>(0,51) R$/m³</b>'}
          ]},
          {cls:"kpi-grid",tiles:[
            {c:"k-red",k:"EBITDA 2026",v:"(5,5)",u:"R$ mi",neg:true,
             s:"Consolidado · projetos 21,4",
             sub:'<b>(0,10) R$/m³</b> · projetos <b>0,41</b>'},
            {c:"k-red",k:"Resultado financeiro 2026",v:"(37,7)",u:"R$ mi",neg:true,
             s:"20% da receita líquida",
             sub:'<b>(0,72) R$/m³</b>'},
            {c:"k-red",k:"Lucro líquido 2026",v:"(55,3)",u:"R$ mi",neg:true,
             s:"Depreciação (12,1) · financeiro (37,7)",
             sub:'<b>(1,05) R$/m³</b>'}
          ]}
        ],
        note:'Base de orçamento (sem realizado). O CI Dez/25 não traz a abertura de custos por etapa — molécula, liquefação, distribuição, regás e SG&amp;A —, por isso esta faixa tem seis cards e não oito. Os R$/m³ usam o <b>volume de 52,5 milhões de m³</b>, anualizado a partir dos 143.746 m³/dia médios do slide 8 (× 365); o deck não publica o volume do ano nem o preço médio, então o preço de 3,53 é implícito. A depreciação de (12,1) é a diferença entre o EBITDA de (5,5), o resultado financeiro de (37,7) e o lucro líquido de (55,3).'},
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
        fcxMensal:{tag:"R$ milhões",tblCls:"placeholder-table fcx-tbl mfc-tbl",
          cols:[["R$ mi",""],["jan/26<small>orçado</small>","mth-orc"],["fev/26<small>orçado</small>","mth-orc"],["mar/26<small>orçado</small>","mth-orc"],["abr/26<small>orçado</small>","mth-orc"],["mai/26<small>orçado</small>","mth-orc"],["jun/26<small>orçado</small>","mth-orc"],["jul/26<small>orçado</small>","mth-orc"],["ago/26<small>orçado</small>","mth-orc"],["set/26<small>orçado</small>","mth-orc"],["out/26<small>orçado</small>","mth-orc"],["nov/26<small>orçado</small>","mth-orc"],["dez/26<small>orçado</small>","mth-orc"],["FC 2026¹<small>total</small>","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(+/–) EBITDA","(4,1)","(2,4)","(6,6)","(1,0)","(0,8)","(0,4)","(0,2)","2,1","1,5","2,8","2,0","1,6","(5,5)"]},
            {cls:"fcx-sub",cells:["Matriz","(1,9)","(1,7)","(6,6)","(1,9)","(1,9)","(1,7)","(1,8)","(1,8)","(1,9)","(1,8)","(2,0)","(2,1)","(26,9)"]},
            {cls:"fcx-sub",cells:["Projetos","(2,3)","(0,8)","(0,1)","0,9","1,1","1,3","1,6","3,9","3,4","4,6","4,1","3,7","21,4"]},
            {cls:"fcx-sub2 fcx-plt",cells:["PR","(1,0)","0,5","0,5","0,5","0,4","1,0","1,0","1,0","0,9","1,0","0,8","0,9","7,6"]},
            {cls:"fcx-sub2 fcx-plt",cells:["BA","(0,5)","(0,7)","(0,1)","0,4","0,4","0,5","0,2","1,2","1,1","1,6","1,5","1,3","6,8"]},
            {cls:"fcx-sub2 fcx-plt",cells:["RN","(0,8)","(0,6)","(0,4)","—","0,3","(0,2)","0,4","1,7","1,5","2,0","1,8","1,5","7,0"]},
            {cls:"fcx-h",cells:["(–) IRPJ / CSLL","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+/–) Δ Capital de Giro","4,1","(0,6)","(0,9)","0,2","(0,3)","(0,2)","(0,2)","(1,0)","(0,1)","(0,3)","0,3","(0,2)","0,8"]},
            {cls:"fcx-tot",cells:["(=) CFO","(0,1)","(3,0)","(7,6)","(0,8)","(1,1)","(0,6)","(0,4)","1,1","1,4","2,6","2,3","1,4","(4,7)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) CapEx","(12,2)","(9,5)","(8,3)","(1,7)","(0,4)","(0,4)","(1,0)","(0,6)","(0,6)","—","—","—","(34,8)"]},
            {cls:"fcx-sub",cells:["Matriz","—","—","—","—","—","—","—","—","—","—","—","—","(0,2)"]},
            {cls:"fcx-sub fcx-plt",cells:["PR","(3,7)","(2,3)","(1,9)","(0,7)","—","—","—","—","—","—","—","—","(8,6)"]},
            {cls:"fcx-sub fcx-plt",cells:["BA","(3,9)","(3,6)","(3,3)","(0,4)","(0,2)","(0,2)","(0,2)","—","—","—","—","—","(11,7)"]},
            {cls:"fcx-sub fcx-plt",cells:["RN","(4,7)","(3,6)","(3,2)","(0,6)","(0,2)","(0,2)","(0,8)","(0,6)","(0,6)","—","—","—","(14,3)"]},
            {cls:"fcx-tot",cells:["(=) CFI","(12,2)","(9,5)","(8,3)","(1,7)","(0,4)","(0,4)","(1,0)","(0,6)","(0,6)","—","—","—","(34,8)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(+) Aporte Hankoe","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Aporte Copa Energia","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Ingresso de dívida","100,0","10,7","—","—","—","—","—","—","—","—","—","—","110,7"]},
            {cls:"fcx-h",cells:["(–) Pgto Principal","(90,0)","—","—","—","—","—","—","—","—","(0,7)","(0,7)","(0,7)","(92,1)"]},
            {cls:"fcx-h",cells:["(–) Resultado Financeiro","(6,9)","0,3","(4,1)","—","—","(10,7)","—","—","(4,4)","—","—","(12,0)","(37,7)"]},
            {cls:"fcx-tot",cells:["(=) CFF","3,1","11,0","(4,1)","—","—","(10,7)","—","—","(4,4)","(0,7)","(0,7)","(12,7)","(19,0)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key fcx-blk fcx-blk-top",cells:["Caixa BoP","36,3","27,0","25,5","5,5","3,0","1,6","(10,0)","(11,3)","(10,9)","(14,5)","(12,7)","(11,0)","36,3"]},
            {cls:"fcx-key fcx-blk",cells:["(+/–) Δ Caixa","(9,2)","(1,5)","(20,0)","(2,5)","(1,4)","(11,6)","(1,3)","0,5","(3,6)","1,8","1,6","(11,3)","(58,6)"]},
            {cls:"fcx-key fcx-blk",cells:["Caixa EoP","27,0","25,5","5,5","3,0","1,6","(10,0)","(11,3)","(10,9)","(14,5)","(12,7)","(11,0)","(22,4)","(22,4)"]},
            {cls:"fcx-key fcx-blk",cells:["Fundo de Líquidez BNB (retido)","6,4","6,4","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9","6,9"]},
            {cls:"fcx-key fcx-strong fcx-blk",cells:["Caixa EoP livre","20,6","19,1","(1,4)","(3,9)","(5,3)","(16,9)","(18,3)","(17,8)","(21,4)","(19,6)","(18,0)","(29,3)","(29,3)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Dívida Bruta","265,4","278,8","277,3","280,0","282,7","274,8","277,5","280,2","278,6","280,6","282,6","272,7","272,7"]},
            {cls:"fcx-key fcx-strong",cells:["Dívida Líquida","238,4","253,3","271,8","277,0","281,1","284,8","288,8","291,1","293,1","293,2","293,7","295,1","295,1"]}
          ],
          note:'<b>¹ FC 2026:</b> forecast (total) do orçamento de 2026. &nbsp; <b>Fundo de Líquidez BNB (retido):</b> 3% do desembolsado na BA e 5% no RN — retido em caixa, não utilizável.<br>Fonte: GNLink — Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 20).'}
        },
        // RCA Mai/26: por ora só a faixa de KPIs, extraída do slide 19 do deck de maio
        // (jan–mai realizado, jun–dez forecast). As tabelas mensais seguem pendentes.
        // Este é o único deck que publica o volume do ano (25,9 mi de m³), então aqui
        // os R$/m³ não dependem de nenhuma estimativa de volume.
        rcaMai:{
        kpis:{groups:[
          {cls:"kpi-row4",tiles:[
            {c:"k-slate",k:"Receita líquida 2026",v:"89,8",u:"R$ mi",
             s:"GNL 77,0 · GNC 11,7 · outros 1,0",
             sub:'Volume do ano <b>25,9 mi de m³</b>'},
            {c:"k-slate",k:"Preço médio",v:"3,47",u:"R$/m³",
             s:"GNL 3,71 · GNC 2,66",
             sub:'Último mês realizado, mai/26: <b>3,26</b>'},
            {c:"k-stone",k:"Custo da molécula",v:"1,76",u:"R$/m³",
             s:"R$ 45,5 mi · 51% da receita",
             sub:'51% do preço médio'},
            {c:"k-stone",k:"Custos GNLink",v:"2,13",u:"R$/m³",
             s:"R$ 55,1 mi no ano",
             sub:'Liquefação <b>0,99</b> · distribuição <b>0,71</b> · regás <b>0,11</b> · SG&amp;A <b>0,32</b>'}
          ]},
          {cls:"kpi-row4",tiles:[
            {c:"k-stone",k:"Despesas matriz",v:"(26,7)",u:"R$ mi",neg:true,
             s:"71% do EBITDA negativo do ano",
             sub:'<b>(1,03) R$/m³</b>'},
            {c:"k-red",k:"EBITDA 2026",v:"(37,6)",u:"R$ mi",neg:true,
             s:"Consolidado · projetos (10,9)",
             sub:'<b>(1,45) R$/m³</b> · projetos <b>(0,42)</b>'},
            {c:"k-red",k:"Resultado financeiro 2026",v:"(38,3)",u:"R$ mi",neg:true,
             s:"43% da receita líquida",
             sub:'<b>(1,48) R$/m³</b>'},
            {c:"k-red",k:"Lucro líquido 2026",v:"(88,2)",u:"R$ mi",neg:true,
             s:"Depreciação (12,2) · financeiro (38,3)",
             sub:'<b>(3,41) R$/m³</b>'}
          ]}
        ],
        note:'Único deck que publica o volume do ano (<b>25,9 milhões de m³</b>), então os R$/m³ aqui não dependem de estimativa — e reproduzem a margem unitária de (0,42) do próprio slide 19. A conta fecha: preço 3,47 − molécula 1,76 − custos GNLink 2,13 = (0,42). <b>Atenção:</b> a coluna TOTAL do custo unitário de liquefação no slide traz 2,86, valor inconsistente com os próprios meses (nenhum passa de 2,12) e com R$ 25,5 mi ÷ 25,9 mi de m³ = 0,99; o card usa 0,99.'},
        dreMensal:{tag:"R$ milhões · R$/m³ · %",tblCls:"placeholder-table fcx-tbl mfc-tbl mfc-rf",
          cols:[["R$ mi",""],["jan/26<small>real</small>","mth-rz"],["fev/26<small>real</small>","mth-rz"],["mar/26<small>real</small>","mth-rz"],["abr/26<small>real</small>","mth-rz"],["mai/26<small>real</small>","mth-rz"],["jun/26<small>fcst</small>","mth-fc"],["jul/26<small>fcst</small>","mth-fc"],["ago/26<small>fcst</small>","mth-fc"],["set/26<small>fcst</small>","mth-fc"],["out/26<small>fcst</small>","mth-fc"],["nov/26<small>fcst</small>","mth-fc"],["dez/26<small>fcst</small>","mth-fc"],["2026<small>real+fcst</small>","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(=) Receita Líquida","2,5","1,1","2,6","3,3","4,2","6,6","7,7","11,1","12,3","12,8","12,6","12,9","89,8"]},
            {cls:"fcx-sub",cells:["GNL","2,4","1,0","2,5","3,0","3,7","6,1","6,2","9,4","10,3","10,9","10,6","11,0","77,0"]},
            {cls:"fcx-sub",cells:["Serviço sem molécula GNL","—","—","—","—","—","—","—","—","0,1","0,2","0,2","0,2","0,6"]},
            {cls:"fcx-sub",cells:["Gás excedente (mercado livre)","—","0,1","—","—","0,3","—","—","—","—","—","—","—","0,4"]},
            {cls:"fcx-sub",cells:["GNC","0,1","0,1","0,1","0,3","0,2","0,5","1,5","1,7","1,8","1,8","1,9","1,8","11,7"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Preço médio (R$/m³)","3,42","2,79","3,32","3,27","3,26","3,53","3,25","3,52","3,49","3,57","3,56","3,60","3,47"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Preço médio GNL (R$/m³)","3,43","3,47","3,35","3,36","3,51","3,60","3,50","3,74","3,77","3,85","3,87","3,88","3,71"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Serviço sem molécula GNL (R$/m³)","—","—","—","—","1,34","1,34","—","—","1,54","1,54","1,68","1,68","1,54"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Gás excedente (R$/m³)","—","0,83","—","—","1,87","—","—","—","—","—","—","—","1,45"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Preço médio GNC (R$/m³)","3,20","3,20","2,84","2,60","2,73","2,90","2,52","2,68","2,65","2,70","2,61","2,67","2,66"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) Custo da molécula","(1,6)","(0,8)","(1,5)","(2,1)","(2,5)","(3,5)","(4,2)","(6,2)","(7,0)","(3,5)","(6,4)","(6,3)","(45,5)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário molécula (R$/m³)","2,12","2,10","1,88","2,08","1,94","1,90","1,78","1,98","2,03","1,00","1,85","1,79","1,76"]},
            {cls:"fcx-h",cells:["(–) Custo de liquefação","(1,3)","(0,8)","(1,1)","(1,6)","(1,8)","(2,3)","(2,4)","(2,7)","(2,8)","(2,6)","(2,9)","(3,2)","(25,5)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário liquefação (R$/m³)¹","1,68","2,12","1,40","1,56","1,39","1,23","1,00","0,85","0,81","0,74","0,82","0,89","2,86"]},
            {cls:"fcx-h",cells:["(–) Distribuição","(1,9)","(0,9)","(1,5)","(1,6)","(1,3)","(1,3)","(1,4)","(1,6)","(1,7)","(1,7)","(1,7)","(1,7)","(18,3)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário distribuição (R$/m³)","2,62","2,26","1,94","1,61","0,97","0,67","0,61","0,52","0,48","0,47","0,48","0,47","0,71"]},
            {cls:"fcx-h",cells:["(–) Regás / descompressão","(0,1)","(0,1)","(0,2)","(0,2)","(0,2)","(0,3)","(0,3)","(0,3)","(0,4)","(0,3)","(0,3)","(0,3)","(2,9)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário regás (R$/m³)","0,13","0,24","0,20","0,16","0,15","0,18","0,12","0,10","0,10","0,08","0,08","0,08","0,11"]},
            {cls:"fcx-h",cells:["(–) Plant-level SG&amp;A","(0,9)","(0,6)","(0,7)","(0,8)","(0,4)","(0,7)","(0,9)","(0,5)","(0,7)","(0,8)","(0,6)","(0,8)","(8,4)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário SG&amp;A (R$/m³)","1,16","1,54","0,93","0,82","0,30","0,38","0,37","0,16","0,20","0,22","0,16","0,23","0,32"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-tot",cells:["(=) Resultado Operacional","(3,2)","(2,2)","(2,4)","(3,0)","(1,9)","(1,5)","(1,5)","(0,2)","(0,3)","3,9","0,7","0,7","(10,9)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Margem unitária (R$/m³)","(4,29)","(5,47)","(3,03)","(2,95)","(1,47)","(0,82)","(0,62)","(0,08)","(0,07)","1,09","0,21","0,18","(0,42)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Margem operacional","(125,3%)","(195,7%)","(91,3%)","(90,4%)","(45,1%)","(23,4%)","(19,2%)","(2,2%)","(2,1%)","30,6%","5,9%","5,1%","(12,1%)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) Despesas matriz","(1,7)","(2,2)","(1,7)","(5,8)","(1,9)","(1,7)","(1,7)","(1,8)","(2,0)","(1,8)","(2,1)","(2,2)","(26,7)"]},
            {cls:"fcx-tot",cells:["(=) EBITDA","(4,9)","(4,4)","(4,2)","(8,8)","(3,8)","(3,3)","(3,2)","(2,1)","(2,2)","2,1","(1,4)","(1,5)","(37,6)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Margem EBITDA","(193,1%)","(396,3%)","(157,7%)","(267,5%)","(91,0%)","(49,8%)","(40,8%)","(18,7%)","(18,1%)","16,3%","(10,9%)","(11,7%)","(41,9%)"]},
            {cls:"fcx-h",cells:["EBITDA normalizado²","(4,6)","(3,7)","(4,1)","(8,8)","(3,8)","(3,3)","(3,2)","(2,1)","(2,2)","2,1","(1,4)","(1,5)","(37,6)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) Depreciação","(0,5)","(0,1)","(0,9)","(0,6)","(0,5)","(1,3)","(1,4)","(1,4)","(1,4)","(1,4)","(1,4)","(1,4)","(12,2)"]},
            {cls:"fcx-h",cells:["(–) Despesas financeiras","(2,8)","(2,2)","(3,2)","(2,4)","(2,6)","(3,1)","(4,6)","(3,1)","(3,8)","(3,2)","(3,4)","(3,8)","(38,3)"]},
            {cls:"fcx-h",cells:["(–) CSLL / IRPJ","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key fcx-strong fcx-blk fcx-blk-top",cells:["(=) Resultado Líquido","(8,2)","(6,8)","(8,2)","(11,7)","(6,9)","(7,8)","(9,2)","(6,5)","(7,4)","(2,6)","(6,1)","(6,7)","(88,2)"]},
            {cls:"fcx-sub2 fcx-blk",noNeg:true,cells:["Margem líquida","(324,1%)","(609,6%)","(313,1%)","(357,6%)","(163,4%)","(117,8%)","(118,5%)","(59,1%)","(59,9%)","(20,0%)","(48,9%)","(52,1%)","(98,2%)"]}
          ],
          rfLegend:'<div class="rf-legend"><span><i style="background:#C55A17"></i>Realizado (jan–mai/26)</span><span><i style="background:#4F7B8C"></i>Forecast (jun–dez/26)</span></div>',
          note:'<b>¹</b> A coluna 2026 do custo unitário de liquefação vem do slide como <b>2,86</b>, valor inconsistente com os próprios meses (nenhum passa de 2,12) e com R$ 25,5 mi ÷ 25,9 mi de m³ = 0,99; mantido como no original, mas os KPIs acima usam 0,99. &nbsp; <b>²</b> EBITDA normalizado exclui do SG&amp;A os gastos com a arbitragem da BBOG e, no custo de molécula do PR, a diferença entre a NF e o valor pago — ajustes só em jan–mar/26; aqui também a coluna 2026 do slide repete o EBITDA sem ajuste.<br>Fonte: GNLink — Apresentação de Resultados Mai/26 (slide 19). Os dois blocos de volume (m³/dia e mil m³) do slide foram omitidos, conforme solicitado; o volume do ano (25,9 mi de m³) segue nos KPIs acima. Linhas em R$ milhões, exceto preços e custos unitários (R$/m³) e margens (%).'},
        fcxMensal:{tag:"R$ milhões",tblCls:"placeholder-table fcx-tbl mfc-tbl mfc-rf",
          cols:[["R$ mi",""],["jan/26<small>real</small>","mth-rz"],["fev/26<small>real</small>","mth-rz"],["mar/26<small>real</small>","mth-rz"],["abr/26<small>real</small>","mth-rz"],["mai/26<small>real</small>","mth-rz"],["jun/26<small>fcst</small>","mth-fc"],["jul/26<small>fcst</small>","mth-fc"],["ago/26<small>fcst</small>","mth-fc"],["set/26<small>fcst</small>","mth-fc"],["out/26<small>fcst</small>","mth-fc"],["nov/26<small>fcst</small>","mth-fc"],["dez/26<small>fcst</small>","mth-fc"],["2026<small>real+fcst</small>","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(+/–) EBITDA","(4,9)","(4,4)","(4,2)","(8,8)","(3,8)","(3,3)","(3,2)","(2,1)","(2,2)","2,1","(1,4)","(1,5)","(37,6)"]},
            {cls:"fcx-sub",cells:["Matriz","(1,7)","(2,2)","(1,7)","(5,8)","(1,9)","(1,7)","(1,7)","(1,8)","(2,0)","(1,8)","(2,1)","(2,2)","(26,7)"]},
            {cls:"fcx-sub",cells:["Projetos","(3,2)","(2,2)","(2,4)","(3,0)","(1,9)","(1,5)","(1,5)","(0,2)","(0,3)","3,9","0,7","0,7","(10,9)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["PR","(1,9)","(0,9)","(0,8)","(1,2)","(0,7)","(0,1)","(0,2)","—","(0,2)","3,6","0,5","0,5","(1,6)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["BA","(1,2)","(1,1)","(1,2)","(1,1)","(0,9)","(1,2)","(0,9)","(0,1)","(0,2)","0,1","—","(0,1)","(7,9)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["RN","(0,1)","(0,2)","(0,4)","(0,6)","(0,3)","(0,2)","(0,3)","(0,1)","0,1","0,2","0,3","0,3","(1,3)"]},
            {cls:"fcx-h",cells:["(–) IRPJ / CSLL","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+/–) Δ Capital de Giro","0,9","(2,2)","(1,5)","(1,0)","0,7","(2,4)","1,4","1,1","1,4","(10,0)","7,3","0,4","(3,9)"]},
            {cls:"fcx-tot",cells:["(=) CFO","(4,0)","(6,6)","(5,7)","(9,8)","(3,2)","(5,6)","(1,8)","(1,0)","(0,8)","(7,9)","5,9","(1,1)","(41,5)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) CapEx","(7,2)","(3,7)","(6,0)","(1,7)","(2,0)","(4,2)","(4,2)","(3,0)","(2,0)","(1,9)","(1,7)","(2,3)","(39,9)"]},
            {cls:"fcx-sub",cells:["Matriz","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-sub fcx-plt",cells:["PR","(1,2)","(1,2)","(1,3)","(0,5)","(0,1)","(1,2)","(1,2)","(1,4)","(0,7)","(0,6)","(0,4)","(0,5)","(10,3)"]},
            {cls:"fcx-sub fcx-plt",cells:["BA","(1,1)","(0,8)","(0,5)","(0,2)","(0,9)","(1,4)","(1,5)","(0,7)","(0,6)","(0,6)","(0,6)","(0,8)","(9,9)"]},
            {cls:"fcx-sub fcx-plt",cells:["RN","(4,8)","(1,6)","(4,1)","(1,0)","(0,9)","(1,6)","(1,5)","(1,0)","(0,7)","(0,7)","(0,7)","(1,0)","(19,6)"]},
            {cls:"fcx-tot",cells:["(=) CFI","(7,2)","(3,7)","(6,0)","(1,7)","(2,0)","(4,2)","(4,2)","(3,0)","(2,0)","(1,9)","(1,7)","(2,3)","(39,9)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(+) Aporte Hankoe","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Aporte Copa Energia","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Ingresso de dívida","145,3","75,3","—","—","—","—","176,7","—","—","—","—","—","397,3"]},
            {cls:"fcx-h",cells:["(–) Pgto Principal","(135,0)","—","—","—","—","—","(145,3)","—","—","(0,7)","(0,7)","(0,7)","(282,4)"]},
            {cls:"fcx-h",cells:["(–) Resultado Financeiro","(10,3)","0,6","(1,5)","0,8","(1,5)","(1,7)","(14,4)","(2,1)","(2,7)","0,3","(3,8)","(0,9)","(37,3)"]},
            {cls:"fcx-tot",cells:["(=) CFF","(0,1)","75,9","(1,5)","0,8","(1,5)","(1,7)","17,1","(2,1)","(2,7)","(0,4)","(4,5)","(1,6)","77,7"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key fcx-blk fcx-blk-top",cells:["Caixa BoP","18,9","7,7","73,3","60,2","49,4","42,8","31,3","42,4","36,3","30,8","20,5","20,2","18,9"]},
            {cls:"fcx-key fcx-blk",cells:["(+/–) Δ Caixa","(11,2)","65,6","(13,2)","(10,8)","(6,6)","(11,5)","11,2","(6,1)","(5,5)","(10,3)","(0,3)","(5,1)","(3,7)"]},
            {cls:"fcx-key fcx-blk",cells:["Caixa EoP","7,7","73,3","60,2","49,4","42,8","31,3","42,4","36,3","30,8","20,5","20,2","15,2","15,2"]},
            {cls:"fcx-key fcx-blk",cells:["Fundo de Líquidez BNB (retido)","(6,5)","(6,6)","(6,6)","(6,8)","(6,8)","(6,8)","(7,7)","(7,7)","(7,7)","(7,7)","(7,7)","(7,7)","(7,7)"]},
            {cls:"fcx-key fcx-strong fcx-blk",cells:["Caixa EoP livre","1,2","66,7","53,6","42,7","36,0","24,5","34,8","28,7","23,1","12,9","12,6","7,5","7,5"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Dívida Bruta","236,5","314,6","316,3","319,4","320,5","322,0","343,7","344,8","345,8","348,6","347,5","349,7","349,7"]},
            {cls:"fcx-key fcx-strong",cells:["Dívida Líquida","228,8","241,3","256,1","270,0","277,8","290,7","301,3","308,4","315,0","328,1","327,3","334,5","334,5"]}
          ],
          rfLegend:'<div class="rf-legend"><span><i style="background:#C55A17"></i>Realizado (jan–mai/26)</span><span><i style="background:#4F7B8C"></i>Forecast (jun–dez/26)</span></div>',
          note:'<b>Fundo de Líquidez BNB (retido):</b> 3% do desembolsado na BA e 5% no RN — retido em caixa, não utilizável; nesta base, como no RCA Jun/26, aparece com sinal negativo (dedução do saldo final).<br>Fonte: GNLink — Apresentação de Resultados Mai/26 (slide 17). As colunas de orçado e de variação (mai/26 e 2026) do slide foram omitidas, como nas demais bases.'}},
        rcaJun:{ // DRE mensal (slide 18) + fluxo de caixa indireto mensal (slide 16) do RCA Jun/26:
                 // jan–jun realizado e jul–dez forecast, fechando na coluna do ano. O cabeçalho usa
                 // mth-rz/mth-fc; no fluxo, as colunas de orçado/variação do slide foram omitidas.
        // KPIs do ano 2026 (real jan–jun + fcst jul–dez). Todo R$/m³ da faixa usa o MESMO
        // denominador — o volume do ano —, para os cards fecharem entre si; os unitários
        // publicados no slide 18 usam bases distintas por linha e ficam na tabela.
        // Duas faixas de 4 para não sobrar coluna vazia na grade.
        kpis:{groups:[
          {cls:"kpi-row4",tiles:[
            {c:"k-slate",k:"Receita líquida 2026",v:"83,0",u:"R$ mi",
             s:"GNL 72,8 · GNC 8,8 · outros 1,4",
             sub:'Volume implícito no ano <b>23,6 mi de m³</b>'},
            {c:"k-slate",k:"Preço médio",v:"3,51",u:"R$/m³",
             s:"GNL 3,69 · GNC 2,94",
             sub:'Último mês realizado, jun/26: <b>3,52</b>'},
            {c:"k-stone",k:"Custo da molécula",v:"1,62",u:"R$/m³",
             s:"R$ 38,2 mi · 46% da receita",
             sub:'46% do preço médio'},
            {c:"k-stone",k:"Custos GNLink",v:"2,24",u:"R$/m³",
             s:"R$ 53,0 mi no ano",
             sub:'Liquefação <b>0,99</b> · distribuição <b>0,76</b> · regás <b>0,14</b> · SG&amp;A <b>0,35</b>'}
          ]},
          {cls:"kpi-row4",tiles:[
            {c:"k-stone",k:"Despesas matriz",v:"(26,9)",u:"R$ mi",neg:true,
             s:"77% do EBITDA negativo do ano",
             sub:'<b>(1,14) R$/m³</b>'},
            {c:"k-red",k:"EBITDA 2026",v:"(35,0)",u:"R$ mi",neg:true,
             s:"Consolidado · projetos (8,1)",
             sub:'<b>(1,48) R$/m³</b> · projetos <b>(0,34)</b>'},
            {c:"k-red",k:"Resultado financeiro 2026",v:"(37,5)",u:"R$ mi",neg:true,
             s:"45% da receita · no caixa (37,8)",
             sub:'<b>(1,59) R$/m³</b>'},
            {c:"k-red",k:"Lucro líquido 2026",v:"(84,5)",u:"R$ mi",neg:true,
             s:"Depreciação (11,9) · financeiro (37,5)",
             sub:'<b>(3,57) R$/m³</b>'}
          ]}
        ],
        note:'O deck de jun/26 não publica o volume do ano: os R$/m³ acima usam o <b>volume implícito de 23,6 milhões de m³</b> (receita ÷ preço médio), que reproduz a margem unitária de (0,34) do próprio slide 18. Como todos os cards dividem pelo mesmo volume, a conta fecha: preço 3,51 − molécula 1,62 − custos GNLink 2,24 = (0,35) de margem operacional unitária. Na tabela abaixo, os unitários publicados no deck são um pouco diferentes porque cada linha usa uma base de volume própria (molécula, distribuição e regás desconsideram o “Serviço sem molécula”; liquefação desconsidera o gás excedente).'},
        dreMensal:{tag:"R$ milhões · R$/m³ · %",tblCls:"placeholder-table fcx-tbl mfc-tbl mfc-rf",
          cols:[["R$ mi",""],["jan/26<small>real</small>","mth-rz"],["fev/26<small>real</small>","mth-rz"],["mar/26<small>real</small>","mth-rz"],["abr/26<small>real</small>","mth-rz"],["mai/26<small>real</small>","mth-rz"],["jun/26<small>real</small>","mth-rz"],["jul/26<small>fcst</small>","mth-fc"],["ago/26<small>fcst</small>","mth-fc"],["set/26<small>fcst</small>","mth-fc"],["out/26<small>fcst</small>","mth-fc"],["nov/26<small>fcst</small>","mth-fc"],["dez/26<small>fcst</small>","mth-fc"],["2026<small>real+fcst</small>","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(=) Receita Líquida","2,5","1,1","2,7","3,3","4,2","6,4","6,4","7,3","8,7","12,5","13,5","14,4","83,0"]},
            {cls:"fcx-sub",cells:["GNL","2,4","1,0","2,6","3,0","3,7","5,7","6,0","6,0","7,1","10,8","11,9","12,6","72,8"]},
            {cls:"fcx-sub",cells:["Serviço sem molécula GNL","—","—","—","—","—","—","—","—","0,1","0,1","0,1","0,2","0,6"]},
            {cls:"fcx-sub",cells:["Gás excedente (mercado livre)","—","0,1","—","—","0,3","0,4","—","—","—","—","—","—","0,8"]},
            {cls:"fcx-sub",cells:["GNC","0,1","0,1","0,1","0,3","0,2","0,2","0,5","1,3","1,4","1,5","1,5","1,6","8,8"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Preço médio (R$/m³)","3,42","2,79","3,41","3,30","3,24","3,52","3,53","3,47","3,61","3,60","3,62","3,55","3,51"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Preço médio GNL (R$/m³)","3,43","3,47","3,44","3,39","3,51","3,74","3,61","3,63","3,89","3,78","3,79","3,70","3,69"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Serviço sem molécula GNL (R$/m³)","—","—","—","1,32","0,67","1,34","—","—","1,46","1,46","1,53","1,53","1,42"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Gás excedente (R$/m³)","—","0,83","—","—","1,84","2,19","—","—","—","—","—","—","1,77"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Preço médio GNC (R$/m³)","3,20","3,20","2,84","2,60","2,73","2,75","2,81","2,95","2,96","2,99","2,94","2,98","2,94"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) Custo da molécula","(1,6)","(0,8)","(1,5)","(2,1)","(2,5)","(3,6)","(3,4)","(3,9)","(4,3)","(3,3)","(5,4)","(5,7)","(38,2)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário molécula (R$/m³)","2,12","2,10","1,88","2,08","1,94","2,03","1,87","1,87","1,87","0,98","1,48","1,46","1,65"]},
            {cls:"fcx-h",cells:["(–) Custo de liquefação","(1,3)","(0,9)","(1,1)","(1,3)","(1,5)","(1,2)","(2,3)","(2,4)","(2,4)","(2,7)","(3,1)","(3,3)","(23,4)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário liquefação (R$/m³)","1,71","2,87","1,44","1,32","1,31","0,75","1,26","1,12","1,01","0,77","0,82","0,82","1,01"]},
            {cls:"fcx-h",cells:["(–) Distribuição","(1,8)","(0,8)","(1,6)","(1,6)","(1,3)","(1,3)","(1,2)","(1,4)","(1,5)","(1,7)","(1,9)","(2,0)","(18,0)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário distribuição (R$/m³)","2,43","2,75","2,00","1,56","1,12","0,78","0,68","0,68","0,63","0,50","0,51","0,50","0,79"]},
            {cls:"fcx-h",cells:["(–) Regás / descompressão","(0,2)","(0,2)","(0,3)","(0,3)","(0,2)","(0,2)","(0,2)","(0,3)","(0,2)","(0,4)","(0,4)","(0,4)","(3,3)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário regás (R$/m³)","0,25","0,61","0,41","0,27","0,19","0,12","0,11","0,15","0,11","0,13","0,10","0,09","0,15"]},
            {cls:"fcx-h",cells:["(–) Plant-level SG&amp;A","(0,8)","(0,5)","(0,8)","(0,5)","(0,7)","(0,8)","(0,9)","(0,5)","(0,7)","(0,8)","(0,6)","(0,8)","(8,3)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Custo unitário SG&amp;A (R$/m³)","1,01","1,23","0,97","0,51","0,54","0,45","0,48","0,23","0,29","0,23","0,15","0,20","0,35"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-tot",cells:["(=) Resultado Operacional","(3,1)","(2,1)","(2,6)","(2,4)","(2,0)","(0,7)","(1,6)","(1,2)","(0,5)","3,6","2,3","2,2","(8,1)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Margem unitária (R$/m³)","(4,11)","(5,22)","(3,28)","(2,43)","(1,54)","(0,41)","(0,86)","(0,58)","(0,21)","1,03","0,61","0,54","(0,34)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Margem operacional","(119,9%)","(186,6%)","(96,2%)","(73,8%)","(47,4%)","(11,6%)","(24,3%)","(16,6%)","(5,7%)","28,8%","16,9%","15,1%","(9,8%)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) Despesas matriz","(1,6)","(1,6)","(1,5)","(5,7)","(1,8)","(2,1)","(1,8)","(2,0)","(2,2)","(2,0)","(2,3)","(2,3)","(26,9)"]},
            {cls:"fcx-tot",cells:["(=) EBITDA","(4,6)","(3,7)","(4,1)","(8,1)","(3,8)","(2,8)","(3,3)","(3,2)","(2,7)","1,6","—","(0,2)","(35,0)"]},
            {cls:"fcx-sub2",noNeg:true,cells:["Margem EBITDA","(182,6%)","(331,0%)","(151,1%)","(245,4%)","(90,8%)","(44,8%)","(51,7%)","(43,9%)","(30,7%)","12,8%","0,0%","(1,2%)","(42,2%)"]},
            {cls:"fcx-h",cells:["EBITDA normalizado¹","(4,3)","(3,0)","(4,0)","(8,1)","(3,8)","(2,8)","(3,3)","(3,2)","(2,7)","1,6","—","(0,2)","(35,0)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) Depreciação","(0,4)","(0,4)","(0,7)","(0,7)","(0,7)","(0,7)","(1,4)","(1,4)","(1,4)","(1,4)","(1,4)","(1,4)","(11,9)"]},
            {cls:"fcx-h",cells:["(–) Despesas financeiras","(3,0)","(2,4)","(3,4)","(2,6)","(3,0)","(3,4)","(3,1)","(2,6)","(4,1)","(2,8)","(3,1)","(4,0)","(37,5)"]},
            {cls:"fcx-h",cells:["(–) CSLL / IRPJ","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key fcx-strong fcx-blk fcx-blk-top",cells:["(=) Resultado Líquido","(8,1)","(6,5)","(8,1)","(11,4)","(7,5)","(6,9)","(7,8)","(7,2)","(8,2)","(2,6)","(4,5)","(5,5)","(84,5)"]},
            {cls:"fcx-sub2 fcx-blk",noNeg:true,cells:["Margem líquida","(319,8%)","(589,0%)","(299,8%)","(344,7%)","(176,8%)","(109,0%)","(121,6%)","(98,2%)","(94,1%)","(21,0%)","(33,5%)","(38,6%)","(101,8%)"]}
          ],
          rfLegend:'<div class="rf-legend"><span><i style="background:#C55A17"></i>Realizado (jan–jun/26)</span><span><i style="background:#4F7B8C"></i>Forecast (jul–dez/26)</span></div>',
          note:'<b>¹ EBITDA normalizado:</b> segundo o deck, exclui do SG&amp;A os gastos com a arbitragem da BBOG e, no custo de molécula do PR, a diferença entre o valor da NF e o efetivamente pago — ajustes que aparecem só em jan–mar/26. <b>A coluna 2026 do slide traz (35,0)</b>, igual ao EBITDA sem ajuste; a soma dos 12 meses normalizados dá (33,8). Valor mantido como no original.<br>Fonte: GNLink — Apresentação de Resultados Jun/26, 24/jun/2026 (slide 18). Linhas em R$ milhões, exceto preços e custos unitários (R$/m³) e margens (%).'},
        fcxMensal:{tag:"R$ milhões",tblCls:"placeholder-table fcx-tbl mfc-tbl mfc-rf",
          cols:[["R$ mi",""],["jan/26<small>real</small>","mth-rz"],["fev/26<small>real</small>","mth-rz"],["mar/26<small>real</small>","mth-rz"],["abr/26<small>real</small>","mth-rz"],["mai/26<small>real</small>","mth-rz"],["jun/26<small>real</small>","mth-rz"],["jul/26<small>fcst</small>","mth-fc"],["ago/26<small>fcst</small>","mth-fc"],["set/26<small>fcst</small>","mth-fc"],["out/26<small>fcst</small>","mth-fc"],["nov/26<small>fcst</small>","mth-fc"],["dez/26<small>fcst</small>","mth-fc"],["FY 2026<small>real+fcst</small>","c-fct"]],
          rows:[
            {cls:"fcx-h",cells:["(+/–) EBITDA","(4,6)","(3,7)","(4,1)","(8,1)","(3,8)","(2,8)","(3,3)","(3,2)","(2,7)","1,6","—","(0,2)","(35,0)"]},
            {cls:"fcx-sub",cells:["Matriz","(1,6)","(1,6)","(1,5)","(5,7)","(1,8)","(2,1)","(1,8)","(2,0)","(2,2)","(2,0)","(2,3)","(2,3)","(26,9)"]},
            {cls:"fcx-sub",cells:["Projetos","(3,1)","(2,1)","(2,6)","(2,4)","(2,0)","(0,7)","(1,6)","(1,2)","(0,5)","3,6","2,3","2,2","(8,1)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["PR","(1,9)","(1,0)","(0,9)","(1,1)","(0,8)","(0,2)","(0,2)","(0,3)","(0,2)","3,1","1,4","1,4","(0,7)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["BA","(1,0)","(0,9)","(1,2)","(1,0)","(0,6)","(0,2)","(1,2)","(0,9)","(0,9)","(0,1)","(0,1)","(0,5)","(8,6)"]},
            {cls:"fcx-sub2 fcx-plt",cells:["RN","(0,1)","(0,1)","(0,5)","(0,4)","(0,6)","(0,3)","(0,2)","—","0,6","0,6","1,0","1,2","1,2"]},
            {cls:"fcx-h",cells:["(–) IRPJ / CSLL","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+/–) Δ Capital de Giro","1,3","(2,7)","(1,3)","(1,5)","1,0","(3,6)","1,9","0,3","(0,2)","(4,6)","4,3","0,9","(4,2)"]},
            {cls:"fcx-tot",cells:["(=) CFO","(3,4)","(6,4)","(5,4)","(9,6)","(2,8)","(6,4)","(1,4)","(2,9)","(2,8)","(3,0)","4,3","0,7","(39,2)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(–) CapEx","(7,2)","(3,7)","(6,0)","(1,7)","(2,0)","(4,5)","(6,2)","(3,1)","(1,6)","(2,1)","(2,1)","(2,5)","(42,6)"]},
            {cls:"fcx-sub",cells:["Matriz","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-sub fcx-plt",cells:["PR","(1,2)","(1,2)","(1,3)","(0,5)","(0,1)","(1,4)","(1,6)","(1,0)","(0,6)","(0,5)","(0,7)","(0,7)","(10,8)"]},
            {cls:"fcx-sub fcx-plt",cells:["BA","(1,1)","(0,8)","(0,5)","(0,2)","(0,9)","(1,2)","(0,9)","(0,6)","(0,2)","(0,9)","(0,9)","(0,9)","(9,1)"]},
            {cls:"fcx-sub fcx-plt",cells:["RN","(4,8)","(1,6)","(4,1)","(1,0)","(0,9)","(1,9)","(3,7)","(1,5)","(0,8)","(0,7)","(0,5)","(0,9)","(22,6)"]},
            {cls:"fcx-tot",cells:["(=) CFI","(7,2)","(3,7)","(6,0)","(1,7)","(2,0)","(4,5)","(6,2)","(3,1)","(1,6)","(2,1)","(2,1)","(2,5)","(42,6)"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-h",cells:["(+) Aporte Hankoe","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Aporte Copa Energia","—","—","—","—","—","—","—","—","—","—","—","—","—"]},
            {cls:"fcx-h",cells:["(+) Ingresso de dívida","145,3","75,3","—","—","—","—","160,0","16,7","—","—","—","—","397,3"]},
            {cls:"fcx-h",cells:["(–) Pgto Principal","(135,0)","—","—","—","—","—","(145,3)","—","—","(0,7)","(0,7)","(0,7)","(282,4)"]},
            {cls:"fcx-h",cells:["(–) Resultado Financeiro","(10,5)","0,4","(1,7)","0,5","(1,9)","(2,0)","(14,5)","(1,9)","(2,5)","(0,2)","(2,5)","(1,0)","(37,8)"]},
            {cls:"fcx-tot",cells:["(=) CFF","(0,3)","75,7","(1,7)","0,5","(1,9)","(2,0)","0,2","14,9","(2,5)","(0,9)","(3,2)","(1,7)","77,2"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key fcx-blk fcx-blk-top",cells:["Caixa BoP","18,6","7,8","73,4","60,4","49,6","42,9","30,0","22,5","31,3","24,4","18,4","17,4","18,6"]},
            {cls:"fcx-key fcx-blk",cells:["(+/–) Δ Caixa","(10,8)","65,6","(13,0)","(10,8)","(6,7)","(12,9)","(7,5)","8,9","(7,0)","(6,0)","(1,0)","(3,4)","(4,6)"]},
            {cls:"fcx-key fcx-blk",cells:["Caixa EoP","7,8","73,4","60,4","49,6","42,9","30,0","22,5","31,3","24,4","18,4","17,4","14,0","14,0"]},
            {cls:"fcx-key fcx-blk",cells:["Fundo de Líquidez BNB (retido)","(6,5)","(6,6)","(6,6)","(6,8)","(6,8)","(6,8)","(6,8)","(7,6)","(7,6)","(7,6)","(7,6)","(7,6)","(7,6)"]},
            {cls:"fcx-key fcx-strong fcx-blk",cells:["Caixa EoP livre","1,2","66,8","53,8","42,8","36,1","23,2","15,7","23,7","16,8","10,8","9,8","6,4","6,4"]},
            {cls:"fcx-sp",sp:1},
            {cls:"fcx-key",cells:["Dívida Bruta","236,5","314,6","316,3","319,4","320,5","322,0","326,9","344,3","345,9","347,8","347,8","350,1","350,1"]},
            {cls:"fcx-key fcx-strong",cells:["Dívida Líquida","228,7","241,3","255,9","269,9","277,7","292,0","304,4","313,0","321,5","329,5","330,4","336,1","336,1"]}
          ],
          rfLegend:'<div class="rf-legend"><span><i style="background:#C55A17"></i>Realizado (jan–jun/26)</span><span><i style="background:#4F7B8C"></i>Forecast (jul–dez/26)</span></div>',
          note:'<b>Fundo de Líquidez BNB (retido):</b> 3% do desembolsado na BA e 5% no RN — retido em caixa, não utilizável; nesta base o fundo aparece com sinal negativo (dedução do saldo final), diferente da apresentação do RCI Dez/25.<br>Fonte: GNLink — Apresentação de Resultados Jun/26, 24/jun/2026 (slide 16).'}
        }
        }
      },
      // Alavancagem — mapeamento da dívida, uma entrada por base de dados (a mais
      // recente é o default do seletor; ver o script no fim do index.html).
      //   rci    → RCI Dez/25 (slide 13): NÃO é série mensal. O deck compara o perfil
      //            da dívida de então ("cenário atual") com o alongamento pretendido
      //            ("cenário futuro"), por isso a base tem tipo:"cenarios".
      //   rcaMai → RCA Mai/26 (slide 15) e rcaJun → RCA Jun/26 (slide 14): saldo
      //            devedor mensal por emissão em 2026 (tipo:"mensal"). realN = nº de
      //            meses realizados; os demais são forecast.
      // Nas duas bases mensais o financiamento BNB da Bahia entra como UMA emissão
      // (1ª + 2ª fase), como no slide, que só publica o total das fases. A debênture
      // de infraestrutura do PR fica de fora: no RCA ela só existe na coluna orçado.
      alavancagem:{
        meses:["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"],
        views:{
          rci:{tipo:"cenarios",
            srcCap:"RCI · Comitê de Investimentos Lorinvest, 15/dez/2025 (slide 13)",
            titulo:"Evolução do perfil da dívida — posição dez/2025",
            tag:"R$ milhões",
            intro:'Nesta base a dívida ainda não era acompanhada mês a mês. O RCI compara o <b>perfil de então</b> com o <b>cenário pretendido</b>: substituir as bridges de 6 meses da ABC pelos financiamentos BNB de 12 anos e pela debênture de infraestrutura, alongando o prazo e reduzindo o custo médio.',
            cenarios:[{key:"atual",nome:"Cenário atual",total:206.0,taxa:14.4},
                      {key:"futuro",nome:"Cenário futuro",total:275.0,taxa:11.1}],
            plantas:[
              {key:"BA",nome:"Bahia",
                atual:[{nome:"Financiamento BNB — 1ª fase",valor:71.0,idx:"IPCA + 4,4% a.a.",taxa:"9,1%",prazo:"12 anos",longo:1,gar:"75% contrato Petrobahia + 25% fiança corporativa"}],
                futuro:[{nome:"Financiamento BNB — 1ª fase",valor:71.0,idx:"IPCA + 4,4% a.a.",taxa:"9,1%",prazo:"12 anos",longo:1,gar:"75% contrato Petrobahia + 25% fiança corporativa"},
                        {nome:"Financiamento BNB — 2ª fase",valor:17.8,idx:"IPCA + 4,4% a.a.",taxa:"9,1%",prazo:"12 anos",longo:1,gar:"75% contrato Petrobahia + 25% fiança corporativa"}]},
              {key:"RN",nome:"Assú",
                atual:[{nome:"Bridge (ABC) — 5ª emissão",valor:45.0,idx:"CDI + 2,4% a.a.",taxa:"17,3%",prazo:"6 meses",longo:0,gar:"100% fiança corporativa"}],
                futuro:[{nome:"Financiamento BNB — 1ª fase",valor:75.3,idx:"IPCA + 5,7% a.a.",taxa:"10,4%",prazo:"12 anos",longo:1,gar:"Inicialmente 100% fiança corporativa e, após a liberação da 2ª fase, 50% fiança corporativa e 50% contrato Cegás"},
                        {nome:"Financiamento BNB — 2ª fase",valor:10.9,idx:"IPCA + 5,7% a.a.",taxa:"10,4%",prazo:"12 anos",longo:1,gar:"Inicialmente 100% fiança corporativa e, após a liberação da 2ª fase, 50% fiança corporativa e 50% contrato Cegás"}],
                futFn:1},
              {key:"PR",nome:"Paraná",
                atual:[{nome:"Bridge (ABC) — 6ª emissão",valor:50.0,idx:"CDI + 2,4% a.a.",taxa:"17,3%",prazo:"6 meses",longo:0,gar:"100% fiança corporativa"},
                       {nome:"Bridge (ABC) — 7ª emissão",valor:40.0,idx:"CDI + 1,9% a.a.",taxa:"16,8%",prazo:"6 meses",longo:0,gar:"100% fiança corporativa"}],
                futuro:[{nome:"Debênture de infraestrutura",valor:100.0,idx:"IPCA + 8,95% a.a.",taxa:"13,6%",prazo:"10 anos",longo:1,gar:"100% contrato Bahiagás"}]}
            ],
            foot:'Valores em R$ milhões · <b>Taxa</b> = custo nominal (% a.a.) informado no deck; o custo médio de cada cenário é a média ponderada pelo saldo. &nbsp; <sup>1</sup> Apesar do valor pré-aprovado do BNB ser de até R$ 94,1 mi, a GNLink ainda estava em fase de comprovação do orçamento do projeto e o banco indicou a liberação de R$ 86,2 mi. &nbsp; Fonte: GNLink — RCI dez/2025 (slide 13).'},

          rcaMai:{tipo:"mensal",realN:5,pos:"mai/26",posTitulo:"posição mai/2026",
            srcCap:"RCA · Mai/26 — Apresentação de Resultados GNLink (slide 15)",
            intro:'Saldo devedor por emissão, planta e banco — <b>realizado até mai/26</b>, demais meses em <b>forecast</b>. Em maio já havia sido orçado o desembolso final do BNB Assú (R$ 10,9 mi), mas seguia em discussão com o banco a crítica de R$ 8 mi; a documentação adicional foi enviada e aguardava-se retorno da área técnica. <span style="color:var(--muted)">Colunas de orçado (mai/26 e dez/26) e variação foram omitidas.</span>',
            total:[236.5,314.6,316.3,319.4,320.5,322.0,343.7,344.8,345.8,348.6,347.5,349.7],
            plantas:[
              {key:"BA",nome:"Bahia",emissoes:[
                {nome:"Financiamento BNB",banco:"BNB",emissao:"13/12/24",venc:"15/09/36",taxa:"8,5%",idx:"IPCA + 4,4% a.a.",pnom:"12 anos",gar:"75% contrato Copergás<sup>1</sup> + 25% fiança corporativa",saldo:[89.8,90.5,89.4,89.8,90.5,89.3,90.0,90.7,88.9,88.9,87.4,86.7]}
              ],sub:[89.8,90.5,89.4,89.8,90.5,89.3,90.0,90.7,88.9,88.9,87.4,86.7]},
              {key:"RN",nome:"Assú",emissoes:[
                {nome:"Financiamento BNB Carnaúba — 1ª fase",banco:"BNB",emissao:"05/02/26",venc:"15/11/37",taxa:"9,8%",idx:"IPCA + 5,7% a.a.",pnom:"12 anos",gar:"Fiança corporativa + contrato Cegás",saldo:[null,75.7,76.4,77.1,75.6,76.3,76.6,75.3,75.9,76.6,75.3,75.9]},
                {nome:"Financiamento BNB Carnaúba — 2ª fase",banco:"BNB",emissao:"TBD",venc:"TBD",taxa:"9,8%",idx:"IPCA + 5,7% a.a.",pnom:"12 anos",gar:"Fiança corporativa + contrato Cegás",saldo:[null,null,null,null,null,null,17.1,16.7,16.9,17.1,16.7,16.9]}
              ],sub:[null,75.7,76.4,77.1,75.6,76.3,93.7,92.0,92.9,93.7,92.0,92.9]},
              {key:"PR",nome:"Paraná",emissoes:[
                {nome:"Bridge (ABC) — 9ª emissão",banco:"ABC",emissao:"12/01/26",venc:"07/07/26",taxa:"17,1%",idx:"CDI + 2,4% a.a.",pnom:"6 meses",gar:"100% fiança corporativa",saldo:[42.6,43.1,43.8,44.3,44.9,45.5,null,null,null,null,null,null]},
                {nome:"Bridge (ABC) — 10ª emissão",banco:"ABC",emissao:"12/01/26",venc:"07/07/26",taxa:"17,1%",idx:"CDI + 2,4% a.a.",pnom:"6 meses",gar:"100% fiança corporativa",saldo:[54.5,55.1,55.9,56.6,57.4,58.1,null,null,null,null,null,null]},
                {nome:"NC privada — 12ª emissão",banco:"TBD",emissao:"TBD",venc:"TBD",taxa:"16,7%",idx:"CDI + 2,4% a.a.",pnom:"1 ano",gar:"100% fiança corporativa",saldo:[null,null,null,null,null,null,100.0,101.2,102.5,103.7,105.0,106.3]}
              ],sub:[97.1,98.2,99.7,100.9,102.3,103.6,100.0,101.2,102.5,103.7,105.0,106.3]},
              {key:"GIRO",nome:"Giro",emissoes:[
                {nome:"Bridge (ABC) — 8ª emissão",banco:"ABC",emissao:"06/01/26",venc:"07/07/26",taxa:"17,1%",idx:"CDI + 2,4% a.a.",pnom:"6 meses",gar:"100% fiança corporativa",saldo:[49.6,50.2,50.9,51.5,52.2,52.8,null,null,null,null,null,null]},
                {nome:"NC privada — 11ª emissão",banco:"TBD",emissao:"TBD",venc:"TBD",taxa:"16,7%",idx:"CDI + 2,4% a.a.",pnom:"1 ano",gar:"100% fiança corporativa",saldo:[null,null,null,null,null,null,60.0,60.8,61.5,62.3,63.1,63.9]}
              ],sub:[49.6,50.2,50.9,51.5,52.2,52.8,60.0,60.8,61.5,62.3,63.1,63.9]}
            ],
            foot:'Valores em R$ milhões · <b>Prazo</b> = vencimento − emissão. &nbsp; <sup>1</sup> BNB Bahia: tentaremos substituir o contrato Petrobahia por contrato da Copergás. &nbsp; Fonte: GNLink — RCA mai/2026 (slide 15).'},

          rcaJun:{tipo:"mensal",realN:6,pos:"jun/26",posTitulo:"posição jun/2026",
            srcCap:"RCA · Jun/26 — Apresentação de Resultados GNLink, 24/jun/2026 (slide 14)",
            intro:'Saldo devedor por emissão, planta e banco — <b>realizado até jun/26</b>, demais meses em <b>forecast</b>. Em junho já havia sido orçado o desembolso final do BNB Assú (R$ 10,9 mi), mas segue em discussão com o banco a crítica de R$ 8 mi; a documentação adicional foi enviada e aguarda-se retorno da área técnica. <span style="color:var(--muted)">Colunas de orçado (jun/26 e dez/26) e variação foram omitidas.</span>',
            total:[236.5,314.6,316.3,319.4,320.5,322.0,326.9,344.3,345.9,347.8,347.8,350.1],
            plantas:[
              {key:"BA",nome:"Bahia",emissoes:[
                {nome:"Financiamento BNB",banco:"BNB",emissao:"13/12/24",venc:"15/09/36",taxa:"8,5%",idx:"IPCA + 4,4% a.a.",pnom:"12 anos",gar:"75% contrato Copergás<sup>1</sup> + 25% fiança corporativa",saldo:[89.8,90.5,89.4,89.8,90.5,89.2,89.9,90.3,88.8,88.1,87.4,86.7]}
              ],sub:[89.8,90.5,89.4,89.8,90.5,89.2,89.9,90.3,88.8,88.1,87.4,86.7]},
              {key:"RN",nome:"Assú",emissoes:[
                {nome:"Financiamento BNB Carnaúba — 1ª fase",banco:"BNB",emissao:"05/02/26",venc:"15/11/37",taxa:"9,8%",idx:"IPCA + 5,7% a.a.",pnom:"12 anos",gar:"Fiança corporativa + contrato Cegás",saldo:[null,75.7,76.4,77.1,75.6,76.3,76.7,75.4,75.7,76.1,75.4,75.7]},
                {nome:"Financiamento BNB Carnaúba — 2ª fase",banco:"BNB",emissao:"TBD",venc:"TBD",taxa:"9,8%",idx:"IPCA + 5,7% a.a.",pnom:"12 anos",gar:"Fiança corporativa + contrato Cegás",saldo:[null,null,null,null,null,null,0.3,16.7,17.2,17.4,16.7,17.1]}
              ],sub:[null,75.7,76.4,77.1,75.6,76.3,77.0,92.0,93.0,93.5,92.0,92.9]},
              {key:"PR",nome:"Paraná",emissoes:[
                {nome:"Bridge (ABC) — 9ª emissão",banco:"ABC",emissao:"12/01/26",venc:"07/07/26",taxa:"17,1%",idx:"CDI + 2,4% a.a.",pnom:"6 meses",gar:"100% fiança corporativa",saldo:[42.6,43.1,43.8,44.3,44.9,45.5,null,null,null,null,null,null]},
                {nome:"Bridge (ABC) — 10ª emissão",banco:"ABC",emissao:"12/01/26",venc:"07/07/26",taxa:"17,1%",idx:"CDI + 2,4% a.a.",pnom:"6 meses",gar:"100% fiança corporativa",saldo:[54.5,55.1,55.9,56.6,57.4,58.1,null,null,null,null,null,null]},
                {nome:"NC privada — 12ª emissão",banco:"TBD",emissao:"TBD",venc:"TBD",taxa:"16,7%",idx:"CDI + 2,4% a.a.",pnom:"1 ano",gar:"100% fiança corporativa",saldo:[null,null,null,null,null,null,100.0,101.3,102.5,103.8,105.1,106.5]}
              ],sub:[97.1,98.2,99.7,100.9,102.3,103.6,100.0,101.3,102.5,103.8,105.1,106.5]},
              {key:"GIRO",nome:"Giro",emissoes:[
                {nome:"Bridge (ABC) — 8ª emissão",banco:"ABC",emissao:"06/01/26",venc:"07/07/26",taxa:"17,1%",idx:"CDI + 2,4% a.a.",pnom:"6 meses",gar:"100% fiança corporativa",saldo:[49.6,50.2,50.9,51.5,52.2,52.9,null,null,null,null,null,null]},
                {nome:"NC privada — 11ª emissão",banco:"TBD",emissao:"TBD",venc:"TBD",taxa:"16,7%",idx:"CDI + 2,4% a.a.",pnom:"1 ano",gar:"100% fiança corporativa",saldo:[null,null,null,null,null,null,60.0,60.8,61.6,62.4,63.2,64.0]}
              ],sub:[49.6,50.2,50.9,51.5,52.2,52.9,60.0,60.8,61.6,62.4,63.2,64.0]}
            ],
            foot:'Valores em R$ milhões · <b>Prazo</b> = vencimento − emissão. &nbsp; <sup>1</sup> BNB Bahia: tentaremos substituir o contrato Petrobahia por contrato da Copergás. &nbsp; Fonte: GNLink — RCA jun/2026 (slide 14).'}
        }
      },
      // Projetos operacionais — "Evolutivo de Volume" de cada planta nos RCAs.
      // Uma entrada por planta; dentro, uma base por deck (a mais recente é o default).
      // Só entram as colunas Real (meses fechados) e Fcst (demais) — as de Orçado do
      // slide ficam de fora. Clientes que só aparecem no orçado (sem volume em real nem
      // em forecast, caso dos riscados em vermelho no deck) são contados em semVol.
      // realN = nº de meses realizados na base; status = legenda de contrato do slide.
      projetos:{
        meses:["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"],
        plantas:[
          {key:"PR",nome:"Barra Bonita",uf:"Paraná",bases:{
            rcaMai:{realN:5,srcCap:"RCA · Mai/26 — Apresentação de Resultados GNLink (slide 21)",
              gnl:{cli:[["LD CELULOSE","spot",[4.5,null,null,null,null,null,null,null,null,null,null,null]],["COMPAGÁS","ativo",[null,null,2.7,1.9,8.9,29.3,20,20,20,20,20,20]],["STARA","previsto",[null,null,null,null,null,null,0.2,2,2,2,2,2]]],
              total:[4.5,null,2.7,1.9,8.9,29.3,20.2,22,22,22,22,22],
              cap:[39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6],semVol:4},
              gnc:{cli:[["FEVEREIRO","ativo",[1.2,0.6,1,1.1,0.8,0.8,2,2,2,2,2,2]],["DALLON","ativo",[null,null,null,0.5,null,1.8,6.7,6.7,6.7,6.7,6.7,6.7]],["RIO BONITO EMBALAG","previsto",[null,null,null,null,null,null,2,2,2,2,2,2]],["DALPARE","ativo",[null,null,null,null,null,null,0.4,2,2,2.5,2.5,2.5]]],
              total:[1.2,0.6,1,1.6,0.8,2.6,11.1,12.7,12.7,13.2,13.2,13.2],
              cap:[14.4,14.4,14.4,14.4,14.4,14.4,19.4,19.4,19.4,19.4,19.4,19.4],semVol:3}},
            rcaJun:{realN:6,srcCap:"RCA · Jun/26 — Apresentação de Resultados GNLink, 24/jun/2026 (slide 20)",
              gnl:{cli:[["LD CELULOSE","spot",[4.5,null,null,null,null,null,null,null,null,null,null,null]],["COMPAGÁS","ativo",[null,null,2.7,1.9,8.9,26.4,25.5,23,23,23,23,23]],["STARA","previsto",[null,null,null,null,null,null,null,null,null,0.2,2,2]],["LHOIST","previsto",[null,null,null,null,null,null,null,null,null,null,4.5,4.5]],["GOIASGÁS","previsto",[null,null,null,null,null,null,null,null,null,5,5,5]],["SK METAIS","previsto",[null,null,null,null,null,null,null,0.2,3,3,3,3]]],
              total:[4.5,null,2.7,1.9,8.9,26.4,25.5,23.2,26,31.2,37.5,37.5],
              cap:[39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6,39.6],semVol:0},
              gnc:{cli:[["FEVEREIRO","ativo",[1.2,0.6,1,1.1,0.8,0.7,0.8,2,2,2,2,2]],["DALLON","ativo",[null,null,null,0.5,null,null,1.5,6.7,6.7,6.7,6.7,6.7]],["RIO BONITO EMBALAG","previsto",[null,null,null,null,null,null,null,0.7,2,2,2,2]],["DALPARE","ativo",[null,null,null,null,null,null,null,null,1.1,2,2,2]],["DALBA","previsto",[null,null,null,null,null,null,null,null,1.1,1.1,1.1,1.1]],["SAMP","previsto",[null,null,null,null,null,null,null,null,null,null,null,0.5]]],
              total:[1.2,0.6,1,1.6,0.8,0.7,2.4,9.4,12.9,13.8,13.8,14.3],
              cap:[14.4,14.4,14.4,14.4,14.4,14.4,19.4,19.4,19.4,19.4,19.4,19.4],semVol:0}}
          }},
          {key:"BA",nome:"Itabuna",uf:"Bahia",bases:{
            rcaMai:{realN:5,srcCap:"RCA · Mai/26 — Apresentação de Resultados GNLink (slide 26)",
              gnl:{cli:[["PETROBAHIA","ativo",[2.1,1.5,1.5,2.5,1,1.7,1.5,1.5,1.5,1.5,1.5,1.5]],["PETYAN","ativo",[2.9,1.6,3.5,4.9,4.1,2.2,5.6,8.1,8.8,8.5,8.4,8.9]],["BAHIAGÁS VDC","ativo",[null,null,null,null,null,null,3.1,3.1,3.1,3.1,3.1,3.1]],["BAHIAGÁS BRU","previsto",[null,null,null,null,null,null,null,15.1,15.1,15.1,15.1,15.1]],["GASODUTO","ativo",[null,3.5,null,null,4.7,null,null,null,null,null,null,null]],["EUROFARMA","previsto",[null,null,null,null,null,null,null,null,2.7,2.7,2.7,2.7]]],
              total:[5,6.7,5,7.3,9.8,3.9,10.2,27.9,31.2,30.9,30.8,31.3],
              cap:[42.6,42.6,42.6,42.6,42.6,42.6,42.6,42.6,42.6,85.2,85.2,85.2],semVol:6},
              gnc:{cli:[["ALGÁS (SERVIÇO)","ativo",[null,null,null,null,null,null,null,null,3,3,3,3]],["BAHIAGÁS","previsto",[null,null,null,null,0.3,0.5,0.5,0.5,0.5,0.5,0.5,0.5]]],
              total:[null,null,null,null,0.3,0.5,0.5,0.5,3.5,3.5,3.5,3.5],
              cap:[14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4],semVol:1}},
            rcaJun:{realN:6,srcCap:"RCA · Jun/26 — Apresentação de Resultados GNLink, 24/jun/2026 (slide 25)",
              gnl:{cli:[["PETROBAHIA","ativo",[2.1,1.5,1.5,2.5,1,2.1,1.9,2,2,2,2,2]],["PETYAN","ativo",[2.9,1.6,3.5,4.9,4.1,2.4,4.8,4.4,4.8,5.3,5.3,5.6]],["BAHIAGÁS VDC","ativo",[null,null,null,null,null,null,null,null,1.5,1.5,1.5,1.5]],["VANADIUM","previsto",[null,null,null,null,null,null,null,null,null,9,9,9]],["CBL","previsto",[null,null,null,null,null,null,null,null,null,4,4,null]],["GRAFITE DO BRASIL","previsto",[null,null,null,null,null,null,null,null,null,2.2,2.2,2.2]]],
              total:[5,3.1,5,7.3,5.1,4.5,6.7,6.4,8.3,24,24,20.3],
              cap:[42.6,42.6,42.6,42.6,42.6,42.6,42.6,42.6,42.6,85.2,85.2,85.2],semVol:2},
              gnc:{cli:[["ALGÁS (SERVIÇO)","ativo",[null,null,null,null,null,null,null,null,3,3,3,3]],["BAHIAGÁS","ativo",[null,null,null,null,0.3,0.4,0.5,1,null,null,null,null]]],
              total:[null,null,null,null,0.3,0.4,0.5,1,3,3,3,3],
              cap:[14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4,14.4],semVol:0}}
          }},
          {key:"RN",nome:"Assú",uf:"Rio Grande do Norte",bases:{
            rcaMai:{realN:5,srcCap:"RCA · Mai/26 — Apresentação de Resultados GNLink (slide 31)",
              gnl:{cli:[["CEGÁS","ativo",[13.3,6.8,14.7,18.2,17.5,18,20.2,20.2,20.1,20.2,20.1,20.2]],["COPERGÁS","ativo",[null,null,1.7,2.4,2.5,2.6,3.9,7.5,15,15,15,15]],["PETRORECONCAVO","ativo",[null,null,null,0.1,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]]],
              total:[13.3,6.8,16.4,20.7,20.2,20.8,24.3,27.9,35.3,35.4,35.3,35.4],
              cap:[null,32.4,32.4,32.4,32.4,32.4,32.4,32.4,32.4,72.7,72.7,72.7],semVol:3},
              gnc:{cli:[["MERI POBO","ativo",[null,null,null,0.5,0.7,1.2,3,3,3,3,3,3]],["PARELHAS","novo",[null,null,null,0.8,1.1,1,3,3,3,3,3,3]],["LIDER","novo",[null,null,0.4,0.8,0.1,null,0.5,0.5,3,0.5,3,0.5]],["NATURAL GAS","novo",[null,null,null,null,null,null,1,1,1,1,1,1]]],
              total:[null,null,0.4,2,1.9,2.2,7.5,7.5,10,7.5,10,7.5],
              cap:[null,14.4,14.4,14.4,14.4,14.4,19.4,19.4,19.4,19.4,19.4,19.4],semVol:0}},
            rcaJun:{realN:6,srcCap:"RCA · Jun/26 — Apresentação de Resultados GNLink, 24/jun/2026 (slide 30)",
              gnl:{cli:[["CEGÁS","ativo",[13.3,6.8,14.7,18.2,17.5,17.6,18.7,20.2,20.1,20.2,20.1,20.2]],["COPERGÁS","ativo",[null,null,1.7,2.4,2.5,2.5,2.5,3.5,6.7,7.5,14,23]],["MASTERBOI","ativo",[null,null,null,null,null,null,null,null,null,9,9,9]]],
              total:[13.3,6.8,16.4,20.6,20,20.1,21.2,23.7,26.8,36.7,43.1,52.2],
              cap:[null,32.4,32.4,32.4,32.4,32.4,32.4,32.4,32.4,72.7,72.7,72.7],semVol:0},
              gnc:{cli:[["MERI POBO","ativo",[null,null,null,0.5,0.7,null,0.7,2,2,2,2,2]],["PARELHAS","novo",[null,null,null,0.8,1.1,1.1,1.3,2,2,2,2,2]],["LIDER","novo",[null,null,0.4,0.8,0.1,null,0.3,null,null,null,null,null]]],
              total:[null,null,0.4,2,1.9,1.1,2.3,4,4,4,4,4],
              cap:[null,14.4,14.4,14.4,14.4,14.4,19.4,19.4,19.4,19.4,19.4,19.4],semVol:1}}
          }}
        ]
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
          {dot:"#7C6BA0",title:"Distribuidoras de combustíveis",count:"4 players",chips:["Raízen","Ipiranga","Vibra Energia","Ultracargo"],invest:"Ultrapar · Cosan"},
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
  {name:"Akron", icon:"ic-akron", cor:"#C06010", logo:"logos/akron-logo.avif", panel:"logos/paineis/akron-painel.webp", pan:{rows:[{label:"% Lorinvest",value:"Pendente"},{label:"Aporte Lorinvest",value:"Pendente"},{label:"Correção IPCA",value:"Pendente"},{label:"Correção IPCA + 15%",value:"Pendente"}]}},
  {name:"Bioren", icon:"ic-bioren", cor:"#003648", logo:"logos/bioren-logo.jpg", panel:"logos/paineis/Bioren%20painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Eindom", icon:"ic-eindom", cor:"#EAA800", logo:"logos/eindom-logo.jpg", panel:"logos/paineis/Eindom%20painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Valsa", icon:"ic-eldry", cor:"#002682", logo:"logos/valsa-logo.svg", panel:"logos/paineis/valsa-painel.webp", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"GBS Storage", icon:"ic-gbs", cor:"#10A088", logo:"logos/gbs-logo.jpg", panel:"logos/paineis/gbs-painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"GNLink", icon:"ic-gnlink", cor:"#104050", logo:"logos/gnlink-logo.jpg", panel:"logos/paineis/GNLink%20painel.jpg", active:true, pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"New Wave", icon:"ic-newwave", cor:"#55677C", logo:"logos/new-wave-logo.jpg", panel:"logos/paineis/Newwave%20painel.jpg", rowBreak:true, pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Norcoast", icon:"ic-norcoast", cor:"#309C90", logo:"logos/norcoast-logo.png", panel:"logos/paineis/norcoast-painel.webp", logoFill:true, pan:{rows:[{label:"% Lorinvest",value:"Pendente"},{label:"Aporte Lorinvest",value:"Pendente"},{label:"Correção IPCA",value:"Pendente"},{label:"Correção IPCA + 15%",value:"Pendente"}]}},
  {name:"Norflor", icon:"ic-norflor", cor:"#587028", logo:"logos/Norflor-logo.png", panel:"logos/paineis/Painel%20Norflor.png", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos",note:{txt:"desinvestido",title:"Negativo: os desinvestimentos já efetuados superam os aportes."}},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Norsul", icon:"ic-norsul", cor:"#4E008A", logo:"logos/norsul-logo.jpg", panel:"logos/paineis/Norsul2%20painel.jpg", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true,note:{txt:"via Lorentzen",title:"Participação indireta via Lorentzen; o painel da Norsul não tem fatia do Hankoe FIP."}},{label:"Valor Hankoe",kpi:"Valor Hankoe"},{label:"Valuation Múltiplo",kpi:"Valuation Múltiplo"},{label:"Valor Hankoe — Lorentzen (%)",kpi:"Valor Hankoe - Lorentzen (%)"}]}},
  {name:"Sileto", icon:"ic-sileto", cor:"#54788A", logo:"logos/Sileto-logo.PNG", panel:"logos/paineis/Sileto%20painel.png", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true,note:{txt:"via Dyna",title:"Fatia do Dyna FIP. Demais acionistas: Crystall 51,6% e Fundo Nunki 8,4%."}},{label:"Aporte Lorinvest",kpi:"Aporte Total",note:{txt:"aporte total",title:"No painel da Sileto a métrica é rotulada &quot;Aporte Total&quot;, não &quot;Aportes Líquidos&quot;."}},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Target Bank", icon:"ic-target", cor:"#F6DE00", logo:"logos/target-bank-logo.png", panel:"logos/paineis/Painel%20Target.png", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
  {name:"Tree+", icon:"ic-treeplus", cor:"#206860", logo:"logos/tree-logo.png", panel:"logos/paineis/Painel%20Norflor.png", panelAlt:"Painel Tree+ (painel da Norflor)", pan:{rows:[{label:"% Lorinvest",hl:true,pct:true,note:{txt:"quotista",title:"Skog FIP – Multiestratégia: Hankoe 25,1%, Ti17 FIM 25,0%, Zest 25,0%, Mercuria 25,0%. Lorinvest é a gestora do fundo."}},{label:"Aporte Lorinvest",kpi:"Aportes Líquidos"},{label:"Correção IPCA",kpi:"Correção IPCA"},{label:"Correção IPCA + 15%",kpi:"Correção IPCA + 15%"}]}},
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
