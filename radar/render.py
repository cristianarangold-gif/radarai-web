"""Render de páginas con Jinja2."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import jinja2
from markupsafe import Markup

from .models import Page
from .seo import SITE, canonical, jsonld

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
          'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

ADSENSE_CLIENT = 'ca-pub-7428485851163208'
NO_ADS_PREFIXES = ('/legal/', '/contacto/', '/404')

NAV = [
    ('Inicio', '/'),
    ('Herramientas', '/#herramientas'),
    ('Comparativas', '/mejor-ia/'),
    ('Guías', '/guias/'),
    ('Noticias', '/noticias/'),
    ('Utilidades', '/herramientas-radar/'),
]

TEMPLATE_BY_KIND = {
    'ficha': 'tool.html',
    'noticia': 'article.html',
    'guia': 'article.html',
    'comparativa': 'article.html',
    'pagina': 'page.html',
    'utilidad': 'utility.html',
}


def fecha_es(value: date) -> str:
    return f'{value.day} de {MONTHS[value.month - 1]} de {value.year}'


def to_json(value) -> Markup:
    text = json.dumps(value, ensure_ascii=False).replace('</', '<\\/')
    return Markup(text)


def make_env(templates_dir: Path) -> jinja2.Environment:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=jinja2.StrictUndefined,
    )
    env.filters['fecha_es'] = fecha_es
    env.filters['to_json'] = to_json
    env.globals.update(SITE=SITE, NAV=NAV, ADSENSE_CLIENT=ADSENSE_CLIENT, ads_enabled=False)
    return env


def template_for(page: Page, ctx: dict) -> str:
    if page.url == '/':
        return 'home.html'
    if ctx.get('listing') is not None:
        return 'listing.html'
    return TEMPLATE_BY_KIND[page.kind]


def render_page(env: jinja2.Environment, page: Page, ctx: dict) -> str:
    show_ads = not page.url.startswith(NO_ADS_PREFIXES)
    return env.get_template(template_for(page, ctx)).render(
        page=page,
        canonical_url=canonical(page.url),
        jsonld=jsonld(page),
        show_adsense=show_ads,
        tools=ctx.get('tools', {}),
        categories=ctx.get('categories', []),
        latest_news=ctx.get('latest_news', []),
        listing=ctx.get('listing'),
    )
