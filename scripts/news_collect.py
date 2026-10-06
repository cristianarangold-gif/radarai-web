"""Recoge noticias candidatas de IA de las fuentes RSS/Atom y genera el cuerpo de una issue.

Uso: python scripts/news_collect.py [--hours 26] [--limit 10]
Escribe el cuerpo en stdout; si no hay candidatas no escribe nada (código de salida 0).
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import namedtuple
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'data' / 'news_sources.txt'
ATOM = '{http://www.w3.org/2005/Atom}'
USER_AGENT = 'Mozilla/5.0 (compatible; RadarIA-news/1.0; +https://radarai.es)'

Item = namedtuple('Item', 'title url published source official')


def _text(el) -> str:
    return html.unescape((el.text or '').strip()) if el is not None else ''


def _parse_date(value: str) -> Optional[datetime]:
    value = (value or '').strip()
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse(xml_text: str, source: str, official: bool) -> List[Item]:
    root = ET.fromstring(xml_text)
    items = []
    for it in root.iter('item'):
        items.append(Item(_text(it.find('title')), _text(it.find('link')),
                          _parse_date(_text(it.find('pubDate'))), source, official))
    for entry in root.iter(f'{ATOM}entry'):
        link = entry.find(f'{ATOM}link[@rel="alternate"]')
        if link is None:
            link = entry.find(f'{ATOM}link')
        date = _text(entry.find(f'{ATOM}published')) or _text(entry.find(f'{ATOM}updated'))
        items.append(Item(_text(entry.find(f'{ATOM}title')),
                          link.get('href', '').strip() if link is not None else '',
                          _parse_date(date), source, official))
    return [i for i in items if i.title and i.url and i.published]


def parse_feed(xml_text: str, source: str, official: bool) -> List[Item]:
    """Devuelve las entradas del feed; un XML inválido devuelve una lista vacía."""
    try:
        return _parse(xml_text, source, official)
    except ET.ParseError:
        return []


def load_sources(path: Path = SOURCES) -> List[Tuple[str, str, bool]]:
    sources = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        kind, name, url = [p.strip() for p in line.split('·')]
        sources.append((name, url, kind == 'oficial'))
    return sources


def select_candidates(items: List[Item], now: datetime, hours: int = 26, limit: int = 10) -> List[Item]:
    since = now - timedelta(hours=hours)
    seen, fresh = set(), []
    for it in sorted(items, key=lambda i: (not i.official, -i.published.timestamp())):
        if it.published < since or it.published > now + timedelta(hours=1) or it.url in seen:
            continue
        seen.add(it.url)
        fresh.append(it)
    return fresh[:limit]


def render_issue(items: List[Item], failures: List[str], today: str, hours: int = 26) -> Optional[str]:
    if not items:
        return None
    lines = [f'Candidatas recogidas el {today} (últimas {hours} horas). Las fuentes oficiales aparecen primero.', '']
    for it in items:
        tag = 'oficial' if it.official else 'medio'
        hora = it.published.strftime('%d/%m %H:%M UTC')
        lines.append(f'- [ ] [{it.title}]({it.url}) — {it.source} ({tag}, {hora})')
    lines += ['', 'La rutina de redacción elegirá 1–2 candidatas y abrirá un PR en borrador siguiendo '
              '`content/GUIA_EDITORIAL.md`. Nada se publica sin revisión.']
    if failures:
        lines += ['', 'Fuentes que no se pudieron leer hoy: ' + ', '.join(failures) + '.']
    return '\n'.join(lines) + '\n'


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', errors='replace')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--hours', type=int, default=26)
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()
    items, failures = [], []
    for name, url, official in load_sources():
        try:
            items += _parse(fetch(url), name, official)
        except Exception as exc:  # noqa: BLE001 — una fuente caída no debe parar la recogida
            failures.append(name)
            print(f'Aviso: {name}: {exc}', file=sys.stderr)
    now = datetime.now(timezone.utc)
    body = render_issue(select_candidates(items, now, args.hours, args.limit), failures,
                        now.strftime('%Y-%m-%d'), args.hours)
    if body:
        sys.stdout.write(body)


if __name__ == '__main__':
    main()
