# -*- coding: utf-8 -*-
"""
Proxy local para planilha de precos ANP e scraping Investing.com
Roda em http://localhost:3001
Uso: python proxy_anp.py   (ou duplo-clique em Iniciar Proxy ANP.bat)
"""

import http.server
import urllib.request
import urllib.parse
import http.cookiejar
import json
import re
import time
import sys
import os
import gzip
import zlib

# Garante que o stdout suporte UTF-8 no Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ANP_URL = (
    'https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia'
    '/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/mensal'
    '/mensal-estados-desde-jan2013.xlsx'
)
BARCHART_BRENT_PAGE_URL = 'https://www.barchart.com/futures/quotes/CB*0/futures-prices?page=all'
BARCHART_JKM_PAGE_URL = 'https://www.barchart.com/futures/quotes/JKM*1/futures-prices'
BARCHART_JKM_HIST_PAGE_URL = 'https://www.barchart.com/futures/quotes/JKM*1/price-history/historical'
BARCHART_API_BASE = 'https://www.barchart.com/proxies/core-api/v1/quotes/get'
BARCHART_TIMESERIES_URL = 'https://www.barchart.com/proxies/timeseries/queryeod.ashx'
YAHOO_CHART_API = 'https://query1.finance.yahoo.com/v8/finance/chart/'
PORT = 3001
_cache = {}            # path -> bytes
_cache_timestamps = {} # path -> epoch seconds (para invalidar caches voláteis)
BARCHART_TTL_SECONDS = 300  # 5 minutos

_BARCHART_UA = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/120.0.0.0 Safari/537.36'
)

_BARCHART_FIELDS = (
    'symbol,contractSymbol,contractName,contractNameHistorical,'
    'lastPrice,priceChange,percentChange,bidPrice,askPrice,'
    'volume,openInterest,previous,open,high,low,'
    'tradeTime,contractExpirationDate,symbolCode,symbolType'
)


def _decompress_if_needed(raw, content_encoding):
    """Descomprime resposta HTTP se Content-Encoding for gzip/deflate ou magic number bater."""
    ce = (content_encoding or '').lower()
    is_gzip = len(raw) >= 2 and raw[:2] == b'\x1f\x8b'
    is_deflate = len(raw) >= 2 and raw[:2] in (b'\x78\x9c', b'\x78\x01', b'\x78\xda')
    if 'gzip' in ce or is_gzip:
        try:
            return gzip.decompress(raw)
        except Exception:
            pass
    if 'deflate' in ce or is_deflate:
        try:
            return zlib.decompress(raw)
        except Exception:
            pass
    return raw


def _fetch_barchart_futures(root, page_url):
    """
    Fluxo de 2 etapas para contornar a tabela renderizada via JS:
      1) GET na página de quotes do contrato para obter cookie XSRF-TOKEN
      2) Chamada à core-api enviando o token decodificado no header X-XSRF-TOKEN

    Parâmetros:
      root      Código raiz do contrato (ex.: 'CB' para Brent, 'JKM' para LNG asiático)
      page_url  URL da página de quotes usada para popular cookies + Referer

    Retorna dict no formato { 'data': [ ... ], 'total': N, 'fetched_at': ISO } onde cada item
    contém pelo menos { symbol, contractName, lastPrice, raw: { lastPrice, ... } }.
    """
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # Etapa 1: carrega a página para obter cookies de sessão (XSRF-TOKEN, laravel_session, etc.)
    page_req = urllib.request.Request(
        page_url,
        headers={
            'User-Agent': _BARCHART_UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.barchart.com/',
            'Upgrade-Insecure-Requests': '1',
        },
    )
    with opener.open(page_req, timeout=30) as r:
        _decompress_if_needed(r.read(), r.headers.get('Content-Encoding'))

    xsrf_token = None
    for c in cj:
        if c.name == 'XSRF-TOKEN' and c.value:
            xsrf_token = urllib.parse.unquote(c.value)
            break
    if not xsrf_token:
        raise RuntimeError('Cookie XSRF-TOKEN não recebido do Barchart.')

    # Etapa 2: chama a API JSON. Limite alto para minimizar paginação.
    all_items = []
    total = None
    page = 1
    limit = 200
    while True:
        params = {
            'lists': 'futures.contractInRoot',
            'root': root,
            'fields': _BARCHART_FIELDS,
            'orderBy': 'contractExpirationDate',
            'orderDir': 'asc',
            'meta': 'field.shortName,field.type,field.description',
            'hasOptions': 'true',
            'page': str(page),
            'limit': str(limit),
            'raw': '1',
        }
        api_url = BARCHART_API_BASE + '?' + urllib.parse.urlencode(params)
        api_req = urllib.request.Request(
            api_url,
            headers={
                'User-Agent': _BARCHART_UA,
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': page_url,
                'X-XSRF-TOKEN': xsrf_token,
                'X-Requested-With': 'XMLHttpRequest',
            },
        )
        with opener.open(api_req, timeout=30) as r:
            raw = _decompress_if_needed(r.read(), r.headers.get('Content-Encoding'))
        body = raw.decode('utf-8', errors='replace')
        try:
            j = json.loads(body)
        except json.JSONDecodeError as e:
            raise RuntimeError(f'Resposta da core-api não é JSON válido: {e}; preview: {body[:200]!r}')

        page_items = j.get('data') or []
        all_items.extend(page_items)
        total = j.get('total', len(all_items))

        if len(all_items) >= total or not page_items:
            break
        page += 1
        if page > 20:  # salvaguarda contra loop infinito
            break

    return {
        'total': total if total is not None else len(all_items),
        'count': len(all_items),
        'data': all_items,
        'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S%z') or time.strftime('%Y-%m-%dT%H:%M:%S'),
    }


def _fetch_barchart_eod(symbol, page_url):
    """
    Histórico end-of-day (EOD) via /proxies/timeseries/queryeod.ashx do Barchart.
    Mesmo fluxo de 2 etapas usado em _fetch_barchart_futures.
    Retorna lista ordenada asc de { 'date': 'YYYY-MM-DD', 'value': close }.
    """
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    page_req = urllib.request.Request(
        page_url,
        headers={
            'User-Agent': _BARCHART_UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.barchart.com/',
            'Upgrade-Insecure-Requests': '1',
        },
    )
    with opener.open(page_req, timeout=30) as r:
        _decompress_if_needed(r.read(), r.headers.get('Content-Encoding'))

    xsrf_token = None
    for c in cj:
        if c.name == 'XSRF-TOKEN' and c.value:
            xsrf_token = urllib.parse.unquote(c.value)
            break
    if not xsrf_token:
        raise RuntimeError('Cookie XSRF-TOKEN não recebido do Barchart.')

    params = {
        'symbol': symbol,
        'data': 'daily',
        'maxrecords': '20000',
        'volume': 'contract',
        'order': 'asc',
        'dividends': 'false',
        'backadjust': 'false',
        'daystoexpiration': '1',
        'contractroll': 'expiration',
    }
    api_url = BARCHART_TIMESERIES_URL + '?' + urllib.parse.urlencode(params)
    api_req = urllib.request.Request(
        api_url,
        headers={
            'User-Agent': _BARCHART_UA,
            'Accept': 'text/plain,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': page_url,
            'X-XSRF-TOKEN': xsrf_token,
            'X-Requested-With': 'XMLHttpRequest',
        },
    )
    with opener.open(api_req, timeout=30) as r:
        raw = _decompress_if_needed(r.read(), r.headers.get('Content-Encoding'))
    body = raw.decode('utf-8', errors='replace')

    # Formato CSV: symbol,date,open,high,low,close,volume,openinterest
    points = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) < 6:
            continue
        date_str = parts[1].strip()
        try:
            close = float(parts[5])
        except ValueError:
            continue
        if close <= 0:
            continue
        points.append({'date': date_str, 'value': close})

    if not points:
        raise RuntimeError(f'Nenhum ponto retornado pelo timeseries para {symbol}.')
    points.sort(key=lambda p: p['date'])
    return points


class ProxyHandler(http.server.BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == '/anp.xlsx':
            self._serve_anp()
        elif self.path == '/barchart-brent-futuro':
            self._serve_barchart_futures(
                cache_key='barchart_brent_futuro',
                root='CB',
                page_url=BARCHART_BRENT_PAGE_URL,
                label='Brent',
            )
        elif self.path == '/barchart-jkm-futuro':
            self._serve_barchart_futures(
                cache_key='barchart_jkm_futuro',
                root='JKM',
                page_url=BARCHART_JKM_PAGE_URL,
                label='JKM',
            )
        elif self.path.startswith('/barchart-jkm-historical'):
            self._serve_barchart_jkm_historical()
        elif self.path.startswith('/yahoo-brent-historical'):
            self._serve_yahoo_brent_historical()
        elif self.path == '/ping':
            body = b'ok'
            self.send_response(200)
            self._cors()
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, 'Not found')

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')

    def _serve_anp(self):
        global _cache
        if 'anp' not in _cache:
            print('[proxy] Baixando planilha da ANP...', flush=True)
            try:
                req = urllib.request.Request(
                    ANP_URL,
                    headers={
                        'User-Agent': (
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 Chrome/120 Safari/537.36'
                        ),
                        'Accept': '*/*',
                    }
                )
                with urllib.request.urlopen(req, timeout=120) as r:
                    _cache['anp'] = r.read()
                mb = len(_cache['anp']) / 1_048_576
                print(f'[proxy] Planilha baixada ({mb:.1f} MB). Cache ativo.', flush=True)
            except Exception as e:
                print(f'[proxy] ERRO ao baixar: {e}', flush=True)
                msg = str(e).encode()
                self.send_response(502)
                self._cors()
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Content-Length', str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
                return

        data = _cache['anp']
        self.send_response(200)
        self._cors()
        self.send_header(
            'Content-Type',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'max-age=3600')
        self.end_headers()
        self.wfile.write(data)

    def _serve_barchart_futures(self, cache_key, root, page_url, label):
        global _cache, _cache_timestamps

        # Invalida cache após TTL (preços de contratos mudam ao longo do dia)
        cached_at = _cache_timestamps.get(cache_key, 0)
        if cache_key in _cache and (time.time() - cached_at) > BARCHART_TTL_SECONDS:
            del _cache[cache_key]

        if cache_key not in _cache:
            print(f'[proxy] Buscando contratos futuros de {label} na API do Barchart (root={root})...', flush=True)
            try:
                payload = _fetch_barchart_futures(root, page_url)
                _cache[cache_key] = json.dumps(payload).encode('utf-8')
                _cache_timestamps[cache_key] = time.time()
                kb = len(_cache[cache_key]) / 1024
                n = len(payload.get('data', [])) if isinstance(payload, dict) else 0
                print(f'[proxy] {n} contratos de {label} baixados ({kb:.1f} KB). Cache ativo.', flush=True)
            except Exception as e:
                print(f'[proxy] ERRO ao buscar {label} no Barchart: {e}', flush=True)
                import traceback
                traceback.print_exc()
                if cache_key in _cache:
                    del _cache[cache_key]
                msg = str(e).encode('utf-8')
                self.send_response(502)
                self._cors()
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Content-Length', str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
                return

        data = _cache[cache_key]
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'max-age=300')
        self.end_headers()
        self.wfile.write(data)

    def _serve_yahoo_brent_historical(self):
        """
        Histórico diário do Brent (BZ=F) via Yahoo Finance v8 chart API.
        Aceita ?start=YYYY-MM-DD&end=YYYY-MM-DD. Defaults: 2007-07-30 a hoje.
        Retorna JSON normalizado: { 'symbol': 'BZ=F', 'data': [ { 'date': 'YYYY-MM-DD', 'value': 75.74 } ... ] }.
        """
        global _cache, _cache_timestamps
        from urllib.parse import urlparse, parse_qs
        import datetime as dt

        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        start_str = params.get('start', [None])[0]
        end_str = params.get('end', [None])[0]

        def to_ts(s, default_ts):
            if not s:
                return default_ts
            try:
                return int(dt.datetime.strptime(s, '%Y-%m-%d').replace(tzinfo=dt.timezone.utc).timestamp())
            except ValueError:
                return default_ts

        # Default range: 2007-07-30 (mesmo do exemplo) até agora.
        default_start = 1185768000  # 2007-07-30 UTC
        default_end = int(time.time())
        period1 = to_ts(start_str, default_start)
        period2 = to_ts(end_str, default_end)

        cache_key = f'yahoo_brent_historical_{period1}_{period2}'
        cached_at = _cache_timestamps.get(cache_key, 0)
        if cache_key in _cache and (time.time() - cached_at) > BARCHART_TTL_SECONDS:
            del _cache[cache_key]

        if cache_key not in _cache:
            print(f'[proxy] Buscando Brent histórico no Yahoo (period {period1} -> {period2})...', flush=True)
            try:
                url = (
                    f'{YAHOO_CHART_API}BZ=F'
                    f'?period1={period1}&period2={period2}&interval=1d'
                )
                req = urllib.request.Request(
                    url,
                    headers={
                        'User-Agent': _BARCHART_UA,
                        'Accept': 'application/json,*/*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate',
                    },
                )
                with urllib.request.urlopen(req, timeout=30) as r:
                    raw = _decompress_if_needed(r.read(), r.headers.get('Content-Encoding'))
                body = raw.decode('utf-8', errors='replace')
                j = json.loads(body)
                chart = j.get('chart') or {}
                err = chart.get('error')
                if err:
                    raise RuntimeError(f'Yahoo retornou erro: {err}')
                results = chart.get('result') or []
                if not results:
                    raise RuntimeError('Yahoo retornou resultado vazio.')
                r0 = results[0]
                timestamps = r0.get('timestamp') or []
                quote = (r0.get('indicators') or {}).get('quote') or [{}]
                closes = quote[0].get('close') or []

                points = []
                for ts, close in zip(timestamps, closes):
                    if close is None:
                        continue
                    d = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).strftime('%Y-%m-%d')
                    points.append({'date': d, 'value': close})

                payload = {
                    'symbol': r0.get('meta', {}).get('symbol', 'BZ=F'),
                    'currency': r0.get('meta', {}).get('currency'),
                    'period1': period1,
                    'period2': period2,
                    'count': len(points),
                    'data': points,
                    'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
                }
                _cache[cache_key] = json.dumps(payload).encode('utf-8')
                _cache_timestamps[cache_key] = time.time()
                kb = len(_cache[cache_key]) / 1024
                print(f'[proxy] {len(points)} pontos diários do Brent (Yahoo) baixados ({kb:.1f} KB). Cache ativo.', flush=True)
            except Exception as e:
                print(f'[proxy] ERRO ao buscar Brent histórico no Yahoo: {e}', flush=True)
                import traceback
                traceback.print_exc()
                if cache_key in _cache:
                    del _cache[cache_key]
                msg = str(e).encode('utf-8')
                self.send_response(502)
                self._cors()
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Content-Length', str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
                return

        data = _cache[cache_key]
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'max-age=300')
        self.end_headers()
        self.wfile.write(data)

    def _serve_barchart_jkm_historical(self):
        """
        Histórico diário do JKM (LNG asiático, contrato perpetual M2 'JKM*1') via Barchart timeseries.
        Fluxo de 2 etapas: HTML → cookie XSRF-TOKEN → /proxies/timeseries/queryeod.ashx.
        Aceita ?start=YYYY-MM-DD&end=YYYY-MM-DD para filtrar.
        Retorna JSON: { symbol: '...', count: N, data: [{date, value}, ...] }.
        """
        global _cache, _cache_timestamps
        from urllib.parse import urlparse, parse_qs

        parsed_url = urlparse(self.path)
        qs = parse_qs(parsed_url.query)
        start_str = qs.get('start', [None])[0]
        end_str = qs.get('end', [None])[0]

        cache_key = f'barchart_jkm_historical_{start_str}_{end_str}'
        cached_at = _cache_timestamps.get(cache_key, 0)
        if cache_key in _cache and (time.time() - cached_at) > BARCHART_TTL_SECONDS:
            del _cache[cache_key]

        if cache_key not in _cache:
            print(f'[proxy] Buscando JKM histórico no Barchart (start={start_str} end={end_str})...', flush=True)
            try:
                points = _fetch_barchart_eod('JKM*1', BARCHART_JKM_HIST_PAGE_URL)

                # Filtragem opcional por intervalo de datas
                if start_str:
                    points = [p for p in points if p['date'] >= start_str]
                if end_str:
                    points = [p for p in points if p['date'] <= end_str]

                payload = {
                    'symbol': 'JKM*1',
                    'count': len(points),
                    'data': points,
                    'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
                }
                _cache[cache_key] = json.dumps(payload).encode('utf-8')
                _cache_timestamps[cache_key] = time.time()
                kb = len(_cache[cache_key]) / 1024
                print(f'[proxy] {len(points)} pontos diários do JKM baixados ({kb:.1f} KB). Cache ativo.', flush=True)
            except Exception as e:
                print(f'[proxy] ERRO ao buscar JKM histórico no Barchart: {e}', flush=True)
                import traceback
                traceback.print_exc()
                if cache_key in _cache:
                    del _cache[cache_key]
                msg = str(e).encode('utf-8')
                self.send_response(502)
                self._cors()
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Content-Length', str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
                return

        data = _cache[cache_key]
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'max-age=300')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # filtra logs repetitivos; mostra apenas erros
        if args and (str(args[1]) != '200'):
            print(f'[proxy] {self.address_string()} {fmt % args}', flush=True)


if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', PORT), ProxyHandler)
    print(f'================================================', flush=True)
    print(f'  Proxy local rodando em http://localhost:{PORT}', flush=True)
    print(f'  Endpoints disponíveis:', flush=True)
    print(f'    - /anp.xlsx (planilha ANP)', flush=True)
    print(f'    - /barchart-brent-futuro (Barchart - Contratos Brent)', flush=True)
    print(f'    - /barchart-jkm-futuro (Barchart - Contratos JKM/LNG)', flush=True)
    print(f'    - /barchart-jkm-historical (Barchart - JKM*1 histórico diário)', flush=True)
    print(f'    - /yahoo-brent-historical (Yahoo Finance - BZ=F histórico diário)', flush=True)
    print(f'    - /ping (health check)', flush=True)
    print(f'  Deixe esta janela aberta enquanto usa o HTML', flush=True)
    print(f'  Pressione Ctrl+C para encerrar', flush=True)
    print(f'================================================', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n[proxy] Encerrado.', flush=True)
        server.server_close()
