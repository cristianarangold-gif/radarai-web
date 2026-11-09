"""Avisa a IndexNow de lo publicado. Un fallo aquí nunca debe tumbar el despliegue.

python scripts/indexnow.py plan   Antes de desplegar: JSON con las URL nuevas o con fecha cambiada frente a la web.
                                  Con INDEXNOW_ALL=true devuelve todas las del sitemap.
python scripts/indexnow.py send   Después de desplegar: envía la lista JSON de INDEXNOW_URLS.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from radar.indexnow import ENDPOINT, SITE, changed_urls, parse_sitemap, payload  # noqa: E402

TIMEOUT = 30


def _live_sitemap() -> str:
    req = urllib.request.Request(f'{SITE}/sitemap.xml', headers={'User-Agent': 'RadarIA-indexnow/1.0'})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode('utf-8')


def _post(body: dict) -> int:
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode('utf-8'), method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code


def plan(new_xml: str, live_sitemap: Callable[[], str] = _live_sitemap, send_all: bool = False) -> List[str]:
    new = parse_sitemap(new_xml)
    if send_all:
        return sorted(new)
    try:
        old = parse_sitemap(live_sitemap())
    except (OSError, ValueError) as exc:
        print(f'IndexNow: no se ha podido leer el sitemap publicado: {exc}', file=sys.stderr)
        return []
    # Sin una versión anterior válida no se sabe qué ha cambiado: mejor no avisar que reenviarlo todo.
    return changed_urls(old, new) if old else []


def send(urls_json: str, post: Callable[[dict], int] = _post) -> int:
    urls = json.loads(urls_json or '[]')
    if not urls:
        print('IndexNow: nada que enviar.')
        return 0
    try:
        status = post(payload(urls))
    except OSError as exc:
        print(f'::warning::IndexNow no ha respondido: {exc}')
        return 0
    if status in (200, 202):
        print(f'IndexNow: {len(urls)} URL enviadas (HTTP {status}).')
    else:
        print(f'::warning::IndexNow ha rechazado el envío de {len(urls)} URL (HTTP {status}).')
    return 0


def main() -> int:
    command = sys.argv[1] if len(sys.argv) == 2 else ''
    if command == 'plan':
        new_xml = (Path(__file__).resolve().parent.parent / '_site' / 'sitemap.xml').read_text(encoding='utf-8')
        print(json.dumps(plan(new_xml, send_all=os.environ.get('INDEXNOW_ALL') == 'true')))
        return 0
    if command == 'send':
        return send(os.environ.get('INDEXNOW_URLS', '[]'))
    print(__doc__.strip())
    return 2


if __name__ == '__main__':
    sys.exit(main())
