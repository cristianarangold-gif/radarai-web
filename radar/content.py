"""Carga de contenido Markdown con metadatos (extensión `meta`)."""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path
from typing import List, Optional

import markdown

from .models import Page

KIND_BY_DIR = {
    'mejor-ia': 'comparativa',
    'guias': 'guia',
    'noticias': 'noticia',
    'herramientas': 'ficha',
    'paginas': 'pagina',
}

MIN_WORDS = {
    'ficha': 1000,
    'comparativa': 1200,
    'guia': 1200,
    'noticia': 500,
    'utilidad': 300,
    'pagina': 0,
}

DATED_KINDS = {'noticia', 'ficha'}
DEFAULT_AUTHOR = 'Cristian Arango'
EXTENSIONS = ['meta', 'tables', 'toc', 'attr_list', 'md_in_html']


def text_of(fragment: str) -> str:
    """Texto plano visible de un fragmento HTML."""
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragment))


def count_words(fragment: str) -> int:
    return len(re.findall(r'\w+', text_of(fragment)))


def _url_for(kind_dir: str, rel: Path) -> str:
    stem = rel.with_suffix('').as_posix()
    if kind_dir == 'paginas':
        return '/' if stem == 'inicio' else f'/{stem}/'
    if kind_dir == 'mejor-ia':
        return f'/{stem}/'
    return f'/{kind_dir}/{stem}/'


def _parse_date(value: Optional[str], path: Path, key: str) -> Optional[date]:
    if not value:
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        raise ValueError(f'{path}: «{key}» debe tener formato AAAA-MM-DD (valor: {value!r})')


def load_page(path: Path, kind_dir: str, rel: Path) -> Page:
    md = markdown.Markdown(extensions=EXTENSIONS)
    body = md.convert(path.read_text(encoding='utf-8'))
    meta = {k: [v.strip() for v in vals if v.strip()] for k, vals in md.Meta.items()}

    def one(key: str) -> str:
        return ' '.join(meta.get(key, [])).strip()

    kind = KIND_BY_DIR[kind_dir]
    for required in ('titulo', 'descripcion'):
        if not one(required):
            raise ValueError(f'{path}: falta «{required}» en los metadatos')
    published = _parse_date(one('fecha'), path, 'fecha')
    if kind in DATED_KINDS and published is None:
        raise ValueError(f'{path}: falta «fecha» (obligatoria en {kind})')

    reserved = {'titulo', 'descripcion', 'fecha', 'actualizado', 'autor', 'fuentes', 'borrador'}
    return Page(
        kind=kind,
        slug=rel.with_suffix('').name,
        url=_url_for(kind_dir, rel),
        title=one('titulo'),
        description=one('descripcion'),
        body_html=body,
        date=published,
        updated=_parse_date(one('actualizado'), path, 'actualizado'),
        author=one('autor') or DEFAULT_AUTHOR,
        sources=meta.get('fuentes', []),
        draft=one('borrador').lower() in ('si', 'sí', 'true'),
        word_count=count_words(body),
        extra={k: one(k) for k in meta if k not in reserved},
    )


def load_pages(content_dir: Path) -> List[Page]:
    content_dir = Path(content_dir)
    pages = []
    for kind_dir in KIND_BY_DIR:
        base = content_dir / kind_dir
        if not base.is_dir():
            continue
        for path in sorted(base.rglob('*.md')):
            if path.name[0] == '_' or path.name[0].isupper():
                continue
            pages.append(load_page(path, kind_dir, path.relative_to(base)))
    return pages
