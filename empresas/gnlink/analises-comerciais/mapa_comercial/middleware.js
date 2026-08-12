import { next } from '@vercel/functions';

// Protege TODO o site com uma senha, no servidor (antes de enviar qualquer
// arquivo ao navegador). Usuário e senha ficam em variáveis de ambiente do
// Vercel — nunca no HTML nem no Git, logo não aparecem no F12.
export const config = {
  // Roda em todas as rotas (páginas, imagens, tudo).
  matcher: '/:path*',
};

export default function middleware(request) {
  const auth = request.headers.get('authorization');

  if (auth) {
    const [scheme, encoded] = auth.split(' ');
    if (scheme === 'Basic' && encoded) {
      const decoded = atob(encoded);
      const sep = decoded.indexOf(':');
      const user = decoded.slice(0, sep);
      const pass = decoded.slice(sep + 1);

      if (user === process.env.SITE_USER && pass === process.env.SITE_PASSWORD) {
        // Credenciais corretas: deixa a requisição seguir para o arquivo.
        return next();
      }
    }
  }

  // Sem credenciais ou credenciais erradas: pede login e não entrega nada.
  return new Response('Acesso restrito.', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Lorinvest Research", charset="UTF-8"',
    },
  });
}
