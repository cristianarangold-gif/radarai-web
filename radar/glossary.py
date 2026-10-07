"""Glosario de IA: lee data/glosario.md (bloques «## Término» + metadatos + Markdown), lo valida y lo prepara."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

import markdown

from .content import count_words, text_of
from .seo import SITE

TEMAS = {
    'basicos': 'Conceptos básicos',
    'modelos': 'Modelos y tecnología',
    'uso': 'Usar la IA',
    'precios': 'Precios y planes',
    'etica': 'Privacidad y ética',
}
KEYS = ('tema', 'relacionados', 'ver', 'alias', 'ejemplo')
LETTERS = list('ABCDEFGHIJKLMN') + ['Ñ'] + list('OPQRSTUVWXYZ')
MIN_WORDS, MAX_WORDS, MAX_VER = 25, 160, 2
URL = '/glosario/'


@dataclass
class Term:
    term: str
    slug: str
    meta: Dict[str, str]
    html: str
    tema: str = ''
    relacionados: List[str] = field(default_factory=list)
    ver: List[str] = field(default_factory=list)
    alias: List[str] = field(default_factory=list)
    ejemplo: str = ''
    related: List[Tuple[str, str]] = field(default_factory=list)  # (slug, término), lo rellena glossary_context
    see: List[Tuple[str, str]] = field(default_factory=list)  # (url, título)

    @property
    def text(self) -> str:
        return ' '.join(text_of(self.html).split())

    @property
    def tema_label(self) -> str:
        return TEMAS.get(self.tema, '')


def _fold(s: str) -> str:
    """Minúsculas sin tildes, conservando la ñ."""
    s = s.lower().replace('ñ', '\0')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.replace('\0', 'ñ')


def slugify(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', _fold(s).replace('ñ', 'n')).strip('-')


def sort_key(s: str) -> str:
    # «n~» ordena después de cualquier «n»+letra: la Ñ queda entre la N y la O.
    return _fold(s).replace('ñ', 'n~')


def letter_of(s: str) -> str:
    first = _fold(s)[:1]
    return 'Ñ' if first == 'ñ' else first.upper()


def _split(value: str) -> List[str]:
    return [v.strip() for v in value.split(',') if v.strip()]


def parse_glossary(text: str) -> List[Term]:
    terms = []
    for chunk in re.split(r'(?m)^## ', text)[1:]:
        lines = chunk.split('\n')
        name, rest = lines[0].strip(), lines[1:]
        meta: Dict[str, str] = {}
        while rest and rest[0].strip():
            key, _, value = rest.pop(0).partition(':')
            meta[key.strip().lower()] = value.strip()
        html = markdown.markdown('\n'.join(rest).strip())
        terms.append(Term(term=name, slug=slugify(name), meta=meta, html=html, tema=meta.get('tema', ''),
                          relacionados=_split(meta.get('relacionados', '')), ver=_split(meta.get('ver', '')),
                          alias=_split(meta.get('alias', '')), ejemplo=meta.get('ejemplo', '')))
    return sorted(terms, key=lambda t: sort_key(t.term))


def _fail(t: Term, msg: str) -> None:
    raise ValueError(f'glosario.md: «{t.term}»: {msg}')


def validate_glossary(terms: List[Term], urls: Set[str]) -> None:
    slugs: Dict[str, Term] = {}
    for t in terms:
        if not t.term or not t.slug:
            _fail(t, 'término vacío')
        if t.slug in slugs:
            _fail(t, f'término duplicado (mismo slug que «{slugs[t.slug].term}»)')
        slugs[t.slug] = t
    for t in terms:
        unknown = sorted(set(t.meta) - set(KEYS))
        if unknown:
            _fail(t, f'clave desconocida «{unknown[0]}» (válidas: {", ".join(KEYS)})')
        if t.tema not in TEMAS:
            _fail(t, f'tema «{t.tema}» no válido (válidos: {", ".join(TEMAS)})')
        for r in t.relacionados:
            if r == t.slug:
                _fail(t, 'se cita a sí mismo en «relacionados»')
            if r not in slugs:
                _fail(t, f'relacionado inexistente «{r}»')
        if len(t.ver) > MAX_VER:
            _fail(t, f'como máximo {MAX_VER} URLs en «ver»')
        for u in t.ver:
            if u not in urls:
                _fail(t, f'la URL {u} de «ver» no existe en el sitio')
        words = count_words(t.html)
        if not MIN_WORDS <= words <= MAX_WORDS:
            _fail(t, f'la definición tiene {words} palabras (entre {MIN_WORDS} y {MAX_WORDS})')
        if 'hemos probado' in (t.text + ' ' + t.ejemplo).lower():
            _fail(t, 'no se afirma «hemos probado»')


def glossary_context(terms: List[Term], titles: Dict[str, str]) -> dict:
    by_slug = {t.slug: t for t in terms}
    for t in terms:
        t.related = [(r, by_slug[r].term) for r in t.relacionados if r in by_slug]
        t.see = [(u, titles.get(u, u)) for u in t.ver]
    letters = [{'letter': L, 'id': 'letra-' + L.lower(), 'terms': [t for t in terms if letter_of(t.term) == L]}
               for L in LETTERS]
    return {'terms': terms, 'letters': letters, 'temas': TEMAS}


def defined_term_set(terms: List[Term]) -> dict:
    return {
        '@context': 'https://schema.org', '@type': 'DefinedTermSet',
        'name': 'Glosario de inteligencia artificial de Radar IA', 'inLanguage': 'es', 'url': SITE + URL,
        'hasDefinedTerm': [{'@type': 'DefinedTerm', 'name': t.term, 'url': f'{SITE}{URL}#{t.slug}',
                            'description': t.text} for t in terms],
    }
