// Curva de contratos futuros do JKM (GNL asiático) — SEM FONTE ATIVA.
//
// A curva vinha do Barchart (root 'JKM'), que desde set/2026 serve todo o site
// atrás do AWS WAF Bot Control e não é mais acessível por requisição automatizada
// — ver o cabeçalho de lib/yahoo.js.
//
// Diferente de Brent e do histórico do JKM, não há substituto público gratuito
// para a CURVA do JKM: o Yahoo só publica o contínuo de 1º mês (JKM=F, usado em
// /api/jkm-historical) e não os contratos mensais; CME e ICE respondem 403 a
// requisições automatizadas. Recuperar este card exige uma fonte paga com chave
// (Barchart OnDemand ou equivalente), que ainda não foi contratada.
//
// Até lá o endpoint responde 503 com uma mensagem explícita, para o card dizer o
// que houve em vez de simular uma falha temporária de rede.
export const maxDuration = 10;

export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  return res.status(503).json({
    error: 'fonte_indisponivel',
    message:
      'A curva de futuros do JKM não tem fonte ativa. O Barchart, que alimentava ' +
      'este card, passou a bloquear acesso automatizado (AWS WAF), e não há ' +
      'substituto público gratuito para a curva do JKM — o Yahoo publica apenas o ' +
      'contínuo de 1º mês, usado no card de JKM Histórico. Reativar depende de ' +
      'contratar uma fonte paga com chave de API.',
    fetched_at: new Date().toISOString(),
  });
}
