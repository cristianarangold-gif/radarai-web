"""Render de páginas con Jinja2."""
from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path

import jinja2
from markupsafe import Markup, escape

from .brands import logo_html
from .covers import cover_for, cover_svg, og_rel
from .editorial import reading_minutes, related_news, toc
from .models import Brand, Page
from .seo import SITE, canonical, jsonld

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
          'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

ADSENSE_CLIENT = 'ca-pub-7428485851163208'
NO_ADS_PREFIXES = ('/legal/', '/contacto/', '/404')

NAV = [
    ('Comparativas', '/mejor-ia/'),
    ('Herramientas', '/herramientas/'),
    ('Guías', '/guias/'),
    ('Noticias', '/noticias/'),
    ('Utilidades', '/herramientas-radar/'),
]

KIND_LABEL = {'noticia': 'Noticia', 'guia': 'Guía', 'comparativa': 'Comparativa', 'ficha': 'Ficha',
              'utilidad': 'Utilidad', 'pagina': 'Página'}


def _radar_slots():
    """Posición de los 5 blips (en % del disco) y retardo para que se iluminen al pasar el barrido de 6 s."""
    slots = []
    for angle in (30, 100, 170, 245, 315):
        a = math.radians(angle)
        slots.append({'left': round(50 + 33 * math.sin(a), 1), 'top': round(50 - 33 * math.cos(a), 1),
                      'delay': round(angle / 360 * 6, 2)})
    return slots


RADAR_SLOTS = _radar_slots()

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


def em_phrase(title: str, phrase: str = 'inteligencia artificial') -> Markup:
    """Escapa el título y resalta `phrase` con <em> si aparece."""
    return Markup(str(escape(title)).replace(phrase, f'<em>{phrase}</em>', 1))


@jinja2.pass_context
def cover_filter(ctx, page: Page) -> Markup:
    # Siempre acompaña a un titular visible: es decorativa para los lectores de pantalla.
    return cover_svg(cover_for(page, ctx.get('brands', {}), ctx.get('tools', {})), ctx['logos_dir'], decorative=True)


@jinja2.pass_context
def logo_filter(ctx, brand_id: str, size: int = 40, name: str = '') -> Markup:
    brand = ctx.get('brands', {}).get(brand_id)
    if brand is None:  # sin marca registrada: inicial sobre tinta
        brand = Brand(brand_id, name or brand_id, '#151515', None, (name or brand_id)[:1].upper())
    return logo_html(brand, size, ctx['logos_dir'])


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
    env.filters['em_phrase'] = em_phrase
    env.filters['cover'] = cover_filter
    env.filters['logo'] = logo_filter
    env.globals.update(SITE=SITE, NAV=NAV, ADSENSE_CLIENT=ADSENSE_CLIENT, ads_enabled=False,
                       KIND_LABEL=KIND_LABEL, RADAR_SLOTS=RADAR_SLOTS, reading_minutes=reading_minutes)
    return env


def template_for(page: Page, ctx: dict) -> str:
    if page.url == '/':
        return 'home.html'
    if page.url == '/404/':
        return '404.html'
    if ctx.get('listing') is not None:
        return 'listing.html'
    return TEMPLATE_BY_KIND[page.kind]


def render_page(env: jinja2.Environment, page: Page, ctx: dict) -> str:
    show_ads = not page.url.startswith(NO_ADS_PREFIXES)
    og_image = f'{SITE}/{og_rel(page.url)}' if page.indexable and page.url != '/404/' else None
    logos_dir = ctx.get('logos_dir', Path('static/logos'))
    return env.get_template(template_for(page, ctx)).render(
        page=page,
        canonical_url=canonical(page.url),
        jsonld=jsonld(page, og_image),
        og_image=og_image,
        cover=cover_svg(cover_for(page, ctx.get('brands', {}), ctx.get('tools', {})), logos_dir),
        show_adsense=show_ads,
        tools=ctx.get('tools', {}),
        categories=ctx.get('categories', []),
        latest_news=ctx.get('latest_news', []),
        listing=ctx.get('listing'),
        comparativas=ctx.get('comparativas', []),
        guias=ctx.get('guias', []),
        utilidades=ctx.get('utilidades', []),
        brands=ctx.get('brands', {}),
        radar=ctx.get('radar', []),
        imprescindibles=ctx.get('imprescindibles', []),
        fichas=ctx.get('fichas', {}),
        toc=toc(page.body_html),
        related=related_news(page, ctx.get('news', [])) if page.kind == 'noticia' else [],
        logos_dir=logos_dir,
    )
