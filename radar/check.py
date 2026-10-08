"""Validación del sitio generado antes de publicar."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from .content import MIN_WORDS, text_of
from .seo import SITE

ESCAPE_RE = re.compile(r'\\u[0-9a-fA-F]{4}')
HREF_RE = re.compile(r'href="(/[^"]*)"')
DOUBLE_ESCAPE_RE = re.compile(r'&amp;(amp|quot|lt|gt|#\d+|[a-z]+);')
OG_RE = re.compile(r'<meta property="og:image" content="([^"]*)"')
REFRESH_RE = re.compile(r'http-equiv="refresh" content="0; url=([^"]+)"')


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


def _anchor_missing(site: Path, href: str) -> bool:
    """True si `href` apunta a una categoría del catálogo (#cat-…) o a un término del glosario
    (/glosario/#…), un prompt de la biblioteca (/prompts/#…) o una herramienta del historial de precios
    (/historial-de-precios/#…) que no existe en la página destino."""
    if '#cat-' not in href and not href.startswith(('/glosario/#', '/prompts/#', '/historial-de-precios/#')):
        return False
    path, frag = href.split('#', 1)
    path = path or '/'
    rel = 'index.html' if path == '/' else path.lstrip('/') + ('index.html' if path.endswith('/') else '')
    target = site / rel
    return not target.is_file() or f'id="{frag}"' not in target.read_text(encoding='utf-8')


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
        refresh = REFRESH_RE.search(html)
        if refresh:
            target = refresh.group(1)
            if target.startswith('/'):
                if not _target_exists(site, target):
                    errors.append(f'{rel}: redirección a destino inexistente {target}')
                elif _anchor_missing(site, target):
                    errors.append(f'{rel}: redirección a ancla inexistente {target}')
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
        if DOUBLE_ESCAPE_RE.search(html):
            errors.append(f'{rel}: entidad HTML con doble escape (p. ej. &amp;amp;)')
        if ESCAPE_RE.search(_visible_text(html)):
            errors.append(f'{rel}: contiene escapes \\uXXXX literales en el texto')
        for href in HREF_RE.findall(html):
            if not _target_exists(site, href):
                errors.append(f'{rel}: enlace interno roto {href}')
            elif _anchor_missing(site, href):
                errors.append(f'{rel}: enlace a ancla inexistente {href}')

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
        og = OG_RE.search(html)
        if not og:
            errors.append(f'{rel}: falta og:image')
        elif not og.group(1).startswith(SITE + '/') or not (site / og.group(1)[len(SITE) + 1:]).is_file():
            errors.append(f'{rel}: og:image inexistente {og.group(1)}')
        kind = _meta(html, 'radar:kind')
        words = _meta(html, 'radar:words')
        if kind in MIN_WORDS and words is not None and int(words) < MIN_WORDS[kind]:
            errors.append(f'{rel}: {words} palabras, mínimo {MIN_WORDS[kind]} para {kind} indexable')

    for label, seen in (('título', titles), ('description', descriptions)):
        for value, rels in seen.items():
            if len(rels) > 1:
                errors.append(f'{label} duplicado «{value}» en {", ".join(rels)}')

    index = site / 'search-index.json'
    if index.exists():
        for entry in json.loads(index.read_text(encoding='utf-8')):
            u = entry.get('u', '')
            if not _target_exists(site, u):
                errors.append(f'search-index.json: URL inexistente {u}')
            elif _anchor_missing(site, u):
                errors.append(f'search-index.json: ancla inexistente {u}')

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
