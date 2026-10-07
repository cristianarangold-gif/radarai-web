"""Índice del buscador (search-index.json): artículos y herramientas del catálogo sin ficha."""
from __future__ import annotations

import json
from typing import Dict, List, Optional

from .content import text_of
from .editorial import split_ids, toc
from .models import Brand, Page, Tool
from .tools import CATEGORIES

INDEX_KINDS = ('ficha', 'comparativa', 'guia', 'noticia', 'utilidad', 'pagina')
EXCLUDED_URLS = ('/', '/404/', '/buscar/')
KIND_LABEL = {'ficha': 'Ficha', 'comparativa': 'Comparativa', 'guia': 'Guía', 'noticia': 'Noticia',
              'utilidad': 'Utilidad', 'pagina': 'Página'}
SYMBOL = {'comparativa': ('#e4572e', '★'), 'guia': ('#f3a712', 'G'), 'utilidad': ('#151515', 'U'),
          'pagina': ('#151515', 'P'), 'noticia': ('#151515', 'N'), 'ficha': ('#151515', '')}
MONTHS = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
MAX_DESC = 160


def _short(text: str) -> str:
    text = ' '.join(text.split())
    return text if len(text) <= MAX_DESC else text[:MAX_DESC - 1].rstrip() + '…'


def _keywords(parts: List[str]) -> str:
    seen, out = set(), []
    for p in parts:
        p = ' '.join(text_of(p or '').split())
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return ' · '.join(out)


def _page_entry(p: Page, tools: Dict[str, Tool], brands: Dict[str, Brand], cats: Dict[str, str]) -> dict:
    keywords = [text for _, text in toc(p.body_html)]
    color, mark = SYMBOL[p.kind]
    brand = None
    entry = {'t': p.title, 'u': p.url, 'k': KIND_LABEL[p.kind], 'd': _short(p.description)}
    if p.kind == 'ficha':
        tool = tools.get(p.slug)
        brand = brands.get(p.slug)
        keywords += [tool.name if tool else '', cats.get(tool.cat, '') if tool else '', p.extra.get('ideal_para', '')]
        mark = mark or (tool.name if tool else p.title)[:1].upper()
        if p.extra.get('precio_desde'):
            entry['p'] = p.extra['precio_desde']
    elif p.kind == 'noticia':
        brand = brands.get(p.extra.get('empresa', '').strip().lower())
        keywords += [brand.name if brand else '']
        keywords += [tools[t].name for t in split_ids(p.extra.get('herramientas', '')) if t in tools]
        if p.date:
            entry['f'] = f'{p.date.day} {MONTHS[p.date.month - 1]} {p.date.year}'
    if brand:
        color, mark = brand.color, brand.monograma
    entry.update(x=_keywords(keywords), c=color, m=mark)
    return entry


def build_index(pages: List[Page], tools: Dict[str, Tool], brands: Dict[str, Brand],
                glossary: Optional[list] = None) -> List[dict]:
    cats = dict(CATEGORIES)
    entries = [_page_entry(p, tools, brands, cats) for p in pages
               if p.kind in INDEX_KINDS and p.indexable and p.url not in EXCLUDED_URLS]
    for t in sorted(tools.values(), key=lambda t: t.name.lower()):
        if t.has_page:
            continue
        entries.append({'t': t.name, 'u': f'/herramientas/#cat-{t.cat}', 'k': 'Catálogo', 'd': _short(t.desc),
                        'x': _keywords([cats.get(t.cat, '')] + list(t.tags)), 'c': '#151515',
                        'm': t.name[:1].upper()})
    for term in glossary or []:
        entries.append({'t': term.term, 'u': f'/glosario/#{term.slug}', 'k': 'Glosario', 'd': _short(term.text),
                        'x': _keywords(list(term.alias) + [term.tema_label]), 'c': '#151515', 'm': 'G'})
    return entries


def index_json(entries: List[dict]) -> str:
    return json.dumps(entries, ensure_ascii=False, separators=(',', ':'))
