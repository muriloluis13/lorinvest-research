import { next } from '@vercel/functions';

// Protege TODO o dashboard com senha, no servidor (antes de enviar qualquer
// arquivo ao navegador). Usuário/senha ficam em env vars do Vercel — nunca no
// HTML nem no Git. Necessário porque o deploy dedicado por pasta (Root Directory
// = esta pasta) NÃO inclui o middleware.js da raiz do repositório.
export const config = {
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
        return next();
      }
    }
  }

  return new Response('Acesso restrito.', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Lorinvest Research", charset="UTF-8"',
    },
  });
}
