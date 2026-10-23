"""Lee el texto de una fuente primaria; si la web oficial bloquea la descarga, usa su copia en archive.org.

Uso: python scripts/fetch_source.py URL
Escribe en la primera línea «Leído en: <url>» (la oficial o la copia archivada) y después el texto de la página.
Si no hay forma de leerla, lo dice y sale con código 1: la rutina debe descartar la candidata.
"""
from __future__ import annotations

import gzip
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable, Optional, Tuple

USER_AGENT = 'Mozilla/5.0 (compatible; RadarIA-news/1.0; +https://radarai.es)'
# Páginas de comprobación antibots que algunas webs devuelven con código 200.
BLOCKED = re.compile(r'Enable JavaScript and cookies to continue|Just a moment\.\.\.|Access denied', re.I)

Fetch = Callable[[str], Tuple[int, str]]


def fetch(url: str, timeout: int = 40) -> Tuple[int, str]:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept-Encoding': 'gzip'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            if resp.headers.get('Content-Encoding') == 'gzip':
                body = gzip.decompress(body)
            return resp.status, body.decode('utf-8', errors='replace')
    except urllib.error.HTTPError as exc:
        return exc.code, ''
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, ''


def page_text(raw: str) -> str:
    raw = re.sub(r'<(script|style|noscript)\b.*?</\1>', ' ', raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    return re.sub(r'\s+', ' ', text).strip()


def _readable(status: int, raw: str) -> bool:
    return status == 200 and not BLOCKED.search(raw)


def archive_url(url: str, fetch: Fetch = fetch) -> Optional[str]:
    """Copia más reciente de la URL con código 200 en archive.org, o None."""
    query = urllib.parse.urlencode({'url': url, 'output': 'json', 'fl': 'timestamp,statuscode'})
    status, body = fetch(f'https://web.archive.org/cdx/search/cdx?{query}')
    if status != 200:
        return None
    try:
        rows = json.loads(body or '[]')[1:]
    except ValueError:
        return None
    stamps = sorted(ts for ts, code in rows if code == '200')
    return f'https://web.archive.org/web/{stamps[-1]}/{url}' if stamps else None


def read_source(url: str, fetch: Fetch = fetch) -> Tuple[Optional[str], str]:
    """(URL leída, texto). Primero la web oficial; si bloquea, su última copia buena en archive.org."""
    status, raw = fetch(url)
    if _readable(status, raw):
        return url, page_text(raw)
    copy = archive_url(url, fetch)
    if copy:
        # «id_» pide a archive.org la página original, sin su barra de navegación.
        status, raw = fetch(copy.replace(f'/{url}', f'id_/{url}', 1))
        if _readable(status, raw):
            return copy, page_text(raw)
    return None, ''


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    used, text = read_source(sys.argv[1])
    if not used:
        print(f'No se ha podido leer {sys.argv[1]} ni una copia en archive.org: descarta la candidata.')
        return 1
    print(f'Leído en: {used}\n')
    print(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
