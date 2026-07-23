// Health check leve — substitui o /ping do proxy local. O index.html faz um ping
// rápido antes de baixar a planilha ANP.
export default function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  return res.status(200).send('ok');
}
