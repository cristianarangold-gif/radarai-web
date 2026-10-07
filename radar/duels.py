"""Páginas «Cara a cara» (X vs Y): validación y contexto. Los datos de la tabla salen siempre de las fichas."""
from __future__ import annotations

from typing import Dict, List, Tuple

import re

from .content import count_words, text_of
from .models import Page

FORBIDDEN = ('hemos probado', 'en nuestras pruebas')
MAX_RESPUESTA = 60
MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
          'noviembre', 'diciembre']
ROWS = (('Precio desde', 'desde'), ('Plan de pago', 'pago'), ('Ideal para', 'ideal'), ('Plataformas', 'plataformas'))
MAX_RELATED = 3
# Precios citados («23 €», «17 $», «0,01 $», «17 US$»): cada uno debe figurar en una de las dos fichas.
PRICE = re.compile(r'(\d+(?:[.,]\d+)?)\s?(€|US\$|\$)')


def prices_in(text: str) -> set:
    return {f'{n} {"$" if c != "€" else "€"}' for n, c in PRICE.findall(text)}


def ficha_text(page: Page) -> str:
    return ' '.join([text_of(page.body_html)] + [str(v) for v in page.extra.values()])


def duel_tools(page: Page) -> List[str]:
    return [t.strip() for t in page.extra.get('herramientas', '').split(',') if t.strip()]


def _phrases(value: str) -> List[str]:
    return [p.strip() for p in (value or '').split('|') if p.strip()]


def _fail(page: Page, msg: str) -> None:
    raise ValueError(f'cara-a-cara/{page.slug}: {msg}')


def validate_duels(duels: List[Page], fichas: Dict[str, Page]) -> None:
    pairs: Dict[frozenset, str] = {}
    for p in duels:
        ids = duel_tools(p)
        if len(ids) != 2:
            _fail(p, f'«herramientas» debe tener 2 herramientas (tiene {len(ids)})')
        if ids[0] == ids[1]:
            _fail(p, 'las 2 herramientas deben ser distintas')
        for t in ids:
            if t not in fichas:
                _fail(p, f'«{t}» no tiene ficha indexable')
        if p.slug != f'{ids[0]}-vs-{ids[1]}':
            _fail(p, f'el archivo debe llamarse {ids[0]}-vs-{ids[1]}.md (mismo orden que «herramientas»)')
        respuesta = p.extra.get('respuesta', '').strip()
        if not respuesta:
            _fail(p, 'falta «respuesta»')
        if count_words(respuesta) > MAX_RESPUESTA:
            _fail(p, f'«respuesta» supera las {MAX_RESPUESTA} palabras')
        for key in ('elige_1', 'elige_2'):
            if not 2 <= len(_phrases(p.extra.get(key, ''))) <= 4:
                _fail(p, f'«{key}» necesita 2–4 frases separadas por «|»')
        if not p.sources:
            _fail(p, 'necesita al menos una fuente en «fuentes»')
        text = ' '.join([text_of(p.body_html), respuesta, p.extra.get('elige_1', ''),
                         p.extra.get('elige_2', '')]).lower()
        for phrase in FORBIDDEN:
            if phrase in text:
                _fail(p, f'no se afirma «{phrase}» (no hacemos pruebas propias salvo indicación)')
        known = prices_in(ficha_text(fichas[ids[0]]) + ' ' + ficha_text(fichas[ids[1]]))
        for price in sorted(prices_in(text_of(p.body_html) + ' ' + respuesta + ' ' + p.extra.get('elige_1', '')
                                    + ' ' + p.extra.get('elige_2', ''))):
            if price not in known:
                _fail(p, f'el precio «{price}» no aparece en las fichas de {ids[0]} ni {ids[1]}: '
                         'actualiza el duelo o la ficha')
        pair = frozenset(ids)
        if pair in pairs:
            _fail(p, f'par repetido: ya existe cara-a-cara/{pairs[pair]}')
        pairs[pair] = p.slug


def _fecha(page: Page) -> str:
    d = page.lastmod
    return f'{d.day} de {MONTHS[d.month - 1]} de {d.year}' if d else '—'


def duel_context(page: Page, compare_by_id: Dict[str, dict], fichas: Dict[str, Page], duels: List[Page]) -> dict:
    a_id, b_id = duel_tools(page)
    a, b = compare_by_id[a_id], compare_by_id[b_id]
    rows = [(label, a[key], b[key]) for label, key in ROWS]
    rows.append(('Comprobado', _fecha(fichas[a_id]), _fecha(fichas[b_id])))
    mine = set((a_id, b_id))
    others = [d for d in duels if d.url != page.url and d.indexable]
    related = sorted(others, key=lambda d: not (mine & set(duel_tools(d))))[:MAX_RELATED]
    return {
        'a': a, 'b': b, 'respuesta': page.extra.get('respuesta', ''),
        'elige': [(a, _phrases(page.extra.get('elige_1', ''))), (b, _phrases(page.extra.get('elige_2', '')))],
        'rows': rows, 'related': related,
    }


def duel_links(duels: List[Page], compare_by_id: Dict[str, dict]) -> Tuple[Dict[str, List[dict]], Dict[str, dict]]:
    """Enlaces a los duelos publicados: por herramienta (fichas) y por par ordenado «a,b» (comparador)."""
    by_tool: Dict[str, List[dict]] = {}
    pairs: Dict[str, dict] = {}
    for d in sorted((d for d in duels if d.indexable), key=lambda d: d.title):
        a, b = duel_tools(d)
        label = f'{compare_by_id[a]["n"]} vs {compare_by_id[b]["n"]}'
        for t in (a, b):
            by_tool.setdefault(t, []).append({'u': d.url, 'label': label, 'a': a, 'b': b})
        pairs[','.join(sorted((a, b)))] = {'u': d.url, 'label': label}
    return by_tool, pairs
