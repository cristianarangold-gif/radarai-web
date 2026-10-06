"""Canonical, datos estructurados (JSON-LD), sitemap y RSS."""
from __future__ import annotations

from datetime import datetime, time, timezone
from email.utils import format_datetime
from typing import List
from xml.sax.saxutils import escape

from .models import Page

SITE = 'https://radarai.es'
SITE_NAME = 'Radar IA'
AUTHOR_URL = SITE + '/autor/'

SECTION_BY_KIND = {
    'noticia': ('Noticias', '/noticias/'),
    'guia': ('Guías', '/guias/'),
    'comparativa': ('Comparativas', '/mejor-ia/'),
    'ficha': ('Herramientas', '/herramientas/'),
}


def canonical(url: str) -> str:
    return SITE + url


def _person(name: str) -> dict:
    return {'@type': 'Person', 'name': name, 'url': AUTHOR_URL}


def _breadcrumb(page: Page) -> dict:
    items = [('Inicio', '/')]
    if page.kind in SECTION_BY_KIND and page.url != SECTION_BY_KIND[page.kind][1]:
        items.append(SECTION_BY_KIND[page.kind])
    items.append((page.title, page.url))
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'name': name, 'item': canonical(url)}
            for i, (name, url) in enumerate(items, 1)
        ],
    }


def jsonld(page: Page) -> List[dict]:
    if page.url == '/':
        return [{
            '@context': 'https://schema.org', '@type': 'WebSite',
            'name': SITE_NAME, 'url': SITE + '/', 'inLanguage': 'es',
            'description': page.description,
        }]
    data = []
    article_type = {'noticia': 'NewsArticle', 'guia': 'Article', 'comparativa': 'Article'}.get(page.kind)
    if article_type or page.kind == 'ficha':
        article = {
            '@context': 'https://schema.org', '@type': article_type or 'Article',
            'headline': page.title, 'description': page.description,
            'inLanguage': 'es', 'mainEntityOfPage': canonical(page.url),
            'author': _person(page.author),
            'publisher': {'@type': 'Organization', 'name': SITE_NAME, 'url': SITE + '/'},
        }
        if page.date:
            article['datePublished'] = page.date.isoformat()
        if page.lastmod:
            article['dateModified'] = page.lastmod.isoformat()
        data.append(article)
    if page.kind == 'ficha':
        data.append({
            '@context': 'https://schema.org', '@type': 'SoftwareApplication',
            'name': page.title, 'applicationCategory': 'BusinessApplication',
            'operatingSystem': page.extra.get('plataforma', 'Web'),
        })
    data.append(_breadcrumb(page))
    return data


def sitemap_xml(pages: List[Page]) -> str:
    rows = []
    for p in sorted((p for p in pages if p.indexable), key=lambda p: p.url):
        lastmod = f'<lastmod>{p.lastmod.isoformat()}</lastmod>' if p.lastmod else ''
        rows.append(f'  <url><loc>{escape(canonical(p.url))}</loc>{lastmod}</url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + '\n'.join(rows) + '\n</urlset>\n')


def rss_xml(news: List[Page]) -> str:
    items = sorted((p for p in news if p.indexable and p.date), key=lambda p: p.date, reverse=True)[:20]
    rows = []
    for p in items:
        pub = format_datetime(datetime.combine(p.date, time(8, 0), tzinfo=timezone.utc))
        rows.append(
            f'<item><title>{escape(p.title)}</title><link>{canonical(p.url)}</link>'
            f'<guid>{canonical(p.url)}</guid><pubDate>{pub}</pubDate>'
            f'<description>{escape(p.description)}</description></item>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f'<title>{SITE_NAME} · Noticias de IA</title><link>{SITE}/noticias/</link>'
            '<description>Noticias de inteligencia artificial con análisis en español.</description>'
            '<language>es-es</language>' + ''.join(rows) + '</channel></rss>\n')
