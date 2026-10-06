"""Validación del sitio generado antes de publicar."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from .content import MIN_WORDS, text_of
from .seo import SITE

ESCAPE_RE = re.compile(r'\\u[0-9a-fA-F]{4}')
HREF_RE = re.compile(r'href="(/[^"]*)"')


def _meta(html: str, name: str) -> Optional[str]:
    m = re.search(rf'<meta name="{re.escape(name)}" content="([^"]*)"', html)
    return m.group(1) if m else None


def _url_of(rel: str) -> str:
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def _target_exists(site: Path, href: str) -> bool:
    path = href.split('#', 1)[0].split('?', 1)[0]
    if path in ('', '/'):
        return (site / 'index.html').exists()
    rel = path.lstrip('/')
    if path.endswith('/'):
        return (site / rel / 'index.html').exists()
    return (site / rel).exists()


def _visible_text(html: str) -> str:
    body = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', html)
    return text_of(body)


def check_site(site_dir: Path) -> List[str]:
    site = Path(site_dir)
    errors: List[str] = []
    titles: Dict[str, List[str]] = defaultdict(list)
    descriptions: Dict[str, List[str]] = defaultdict(list)
    noindex_urls = set()

    for path in sorted(site.rglob('*.html')):
        rel = path.relative_to(site).as_posix()
        html = path.read_text(encoding='utf-8')
        if 'http-equiv="refresh"' in html:
            continue
        url = _url_of(rel)
        noindex = 'name="robots" content="noindex' in html

        if not html.lstrip().lower().startswith('<!doctype html>'):
            errors.append(f'{rel}: falta DOCTYPE')
        if '<html lang="es">' not in html:
            errors.append(f'{rel}: falta lang="es"')
        found_titles = re.findall(r'<title>(.*?)</title>', html, re.S)
        if len(found_titles) != 1 or not found_titles[0].strip():
            errors.append(f'{rel}: debe tener exactamente un <title> no vacío')
        if ESCAPE_RE.search(_visible_text(html)):
            errors.append(f'{rel}: contiene escapes \\uXXXX literales en el texto')
        for href in HREF_RE.findall(html):
            if not _target_exists(site, href):
                errors.append(f'{rel}: enlace interno roto {href}')

        if noindex or rel == '404.html':
            noindex_urls.add(url)
            continue

        desc = _meta(html, 'description')
        if not desc:
            errors.append(f'{rel}: falta meta description')
        else:
            descriptions[desc].append(rel)
        if found_titles:
            titles[found_titles[0].strip()].append(rel)
        if f'<link rel="canonical" href="{SITE}{url}">' not in html:
            errors.append(f'{rel}: canonical ausente o distinto de {SITE}{url}')
        kind = _meta(html, 'radar:kind')
        words = _meta(html, 'radar:words')
        if kind in MIN_WORDS and words is not None and int(words) < MIN_WORDS[kind]:
            errors.append(f'{rel}: {words} palabras, mínimo {MIN_WORDS[kind]} para {kind} indexable')

    for label, seen in (('título', titles), ('description', descriptions)):
        for value, rels in seen.items():
            if len(rels) > 1:
                errors.append(f'{label} duplicado «{value}» en {", ".join(rels)}')

    sitemap = site / 'sitemap.xml'
    if not sitemap.exists():
        errors.append('falta sitemap.xml')
    else:
        for loc in re.findall(r'<loc>(.*?)</loc>', sitemap.read_text(encoding='utf-8')):
            url = loc[len(SITE):] if loc.startswith(SITE) else loc
            if not _target_exists(site, url):
                errors.append(f'sitemap.xml: {url} no existe')
            elif url in noindex_urls:
                errors.append(f'sitemap.xml: {url} es noindex')
    return errors
