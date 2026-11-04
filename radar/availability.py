"""¿Funciona en España?: lee data/disponibilidad.md (bloques «## Función» + metadatos), lo valida y lo prepara."""
from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from datetime import date
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse

from .glossary import sort_key
from .models import Page
from .price_history import ARCHIVE_HOST, ARCHIVE_PATH, _host, _matches, long_date

# Empresa → dominios oficiales. Una empresa nueva se añade aquí expresamente.
OFICIALES: Dict[str, List[str]] = {
    'anthropic': ['anthropic.com', 'claude.com', 'claude.ai'],
    'apple': ['apple.com'],
    'canva': ['canva.com'],
    'cursor': ['cursor.com'],
    'deepl': ['deepl.com'],
    'elevenlabs': ['elevenlabs.io'],
    'github': ['github.com', 'github.blog'],
    'google': ['google.com', 'blog.google', 'gemini.google', 'antigravity.google'],
    'meta': ['meta.com', 'meta.ai', 'about.fb.com', 'facebook.com'],
    'microsoft': ['microsoft.com'],
    'notion': ['notion.com'],
    'openai': ['openai.com', 'chatgpt.com'],
    'perplexity': ['perplexity.ai'],
    'runway': ['runwayml.com', 'runway.com'],
    'suno': ['suno.com'],
}
# Estado → (etiqueta, clase CSS). El orden es el de la tabla.
ESTADOS: Dict[str, Tuple[str, str]] = {
    'no': ('✕ No disponible', 'avail-no'),
    'parcial': ('◐ Parcial', 'avail-parcial'),
    'sin_confirmar': ('? Sin confirmar', 'avail-duda'),
    'si': ('✓ Disponible', 'avail-si'),
}
NOMBRES = {'anthropic': 'Anthropic', 'apple': 'Apple', 'canva': 'Canva', 'cursor': 'Cursor', 'deepl': 'DeepL',
           'elevenlabs': 'ElevenLabs', 'github': 'GitHub', 'google': 'Google', 'meta': 'Meta',
           'microsoft': 'Microsoft', 'notion': 'Notion', 'openai': 'OpenAI', 'perplexity': 'Perplexity',
           'runway': 'Runway', 'suno': 'Suno'}
REQUIRED = ('id', 'empresa', 'eeuu', 'ue', 'es', 'comprobado', 'fuentes')
ID_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
MAX_NOTE_WORDS, MAX_SOURCES, STALE_DAYS = 30, 3, 60


@dataclass
class Feature:
    title: str
    id: str = ''
    empresa: str = ''
    ficha: str = ''
    eeuu: str = ''
    ue: str = ''
    es: str = ''
    nota: str = ''
    comprobado: str = ''  # AAAA-MM-DD; validate_availability comprueba que sea una fecha real
    fuentes: List[str] = field(default_factory=list)
    noticia: str = ''
    stale: bool = False

    @property
    def fecha(self) -> str:
        return long_date(self.comprobado)

    @property
    def empresa_nombre(self) -> str:
        return NOMBRES.get(self.empresa, self.empresa)

    @property
    def links(self) -> List[Tuple[str, str]]:
        return [('copia archivada' if _host(u) == ARCHIVE_HOST else _host(u), u) for u in self.fuentes]


def parse_availability(text: str) -> List[Feature]:
    features = []
    for chunk in re.split(r'(?m)^## ', text)[1:]:
        lines = chunk.split('\n')
        meta: Dict[str, str] = {}
        for line in lines[1:]:
            if not line.strip():
                break
            key, _, value = line.partition(':')
            meta[key.strip().lower()] = value.strip()
        features.append(Feature(title=lines[0].strip(), id=meta.get('id', ''), empresa=meta.get('empresa', ''),
                                ficha=meta.get('ficha', ''), eeuu=meta.get('eeuu', ''), ue=meta.get('ue', ''),
                                es=meta.get('es', ''), nota=meta.get('nota', ''),
                                comprobado=meta.get('comprobado', ''),
                                fuentes=[u.strip() for u in meta.get('fuentes', '').split(',') if u.strip()],
                                noticia=meta.get('noticia', '')))
    return features


def _fail(f: Feature, msg: str) -> None:
    raise ValueError(f'disponibilidad.md: «{f.title}»: {msg}')


def _official(url: str, domains: List[str]) -> bool:
    host = _host(url)
    if host == ARCHIVE_HOST:
        m = ARCHIVE_PATH.match(urlparse(url).path)
        inner = m.group(1) if m else ''
        return bool(m) and _matches(_host(inner if '://' in inner else 'https://' + inner), domains)
    return _matches(host, domains)


def _check(f: Feature, fichas: Dict[str, Page], site_urls: Set[str], today: date) -> None:
    for key in REQUIRED:
        if not getattr(f, key):
            _fail(f, f'falta el campo «{key}»')
    if not ID_RE.match(f.id):
        _fail(f, f'id «{f.id}» no válido (minúsculas y guiones)')
    if f.empresa not in OFICIALES:
        _fail(f, f'empresa «{f.empresa}» desconocida (añádela a OFICIALES)')
    if f.ficha and f.ficha not in fichas:
        _fail(f, f'ficha «{f.ficha}» desconocida')
    for region in (f.eeuu, f.ue, f.es):
        if region not in ESTADOS:
            _fail(f, f'estado «{region}» no válido (válidos: {", ".join(ESTADOS)})')
    if f.ue == 'no' and f.es != 'no':
        _fail(f, 'si la UE es «no», España debe ser «no»')
    if 'parcial' in (f.eeuu, f.ue, f.es) and not f.nota:
        _fail(f, 'un estado «parcial» necesita nota')
    if len(f.nota.split()) > MAX_NOTE_WORDS:
        _fail(f, f'la nota supera las {MAX_NOTE_WORDS} palabras')
    try:
        checked = date.fromisoformat(f.comprobado)
    except ValueError:
        _fail(f, f'fecha «{f.comprobado}» no válida (AAAA-MM-DD)')
    if checked > today:
        _fail(f, f'la fecha «{f.comprobado}» es futura')
    if len(f.fuentes) > MAX_SOURCES:
        _fail(f, f'máximo {MAX_SOURCES} fuentes')
    for url in f.fuentes:
        if not url.startswith('https://'):
            _fail(f, f'la fuente debe empezar por https:// («{url}»)')
        if not _official(url, OFICIALES[f.empresa]):
            _fail(f, f'la fuente «{url}» no es oficial de «{f.empresa}» ni una copia archivada suya')
    if f.noticia and f.noticia not in site_urls:
        _fail(f, f'noticia «{f.noticia}» inexistente')


def validate_availability(features: List[Feature], fichas: Dict[str, Page], site_urls: Set[str], today: date) -> None:
    ids, titles = set(), set()
    for f in features:
        _check(f, fichas, site_urls, today)
        if f.id in ids:
            _fail(f, f'id «{f.id}» repetido')
        if f.title in titles:
            _fail(f, 'título repetido')
        ids.add(f.id)
        titles.add(f.title)


def availability_context(features: List[Feature], today: date) -> dict:
    order = {state: i for i, state in enumerate(ESTADOS)}
    rows = sorted((replace(f, stale=(today - date.fromisoformat(f.comprobado)).days > STALE_DAYS) for f in features),
                  key=lambda f: (order[f.es], sort_key(f.title)))
    by_ficha: Dict[str, List[Feature]] = {}
    for r in rows:
        if r.ficha:
            by_ficha.setdefault(r.ficha, []).append(r)
    latest = max((r.comprobado for r in rows), default='')
    return {'rows': rows, 'count': len(rows), 'latest': long_date(latest) if latest else '',
            'stale': [r for r in rows if r.stale], 'by_ficha': by_ficha, 'estados': ESTADOS}
