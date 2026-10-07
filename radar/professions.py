"""IA por profesión: validación y contexto. El kit toma los datos de las fichas; las citas del cuerpo son prompts."""
from __future__ import annotations

import re
from typing import Dict, List, Tuple

from .content import text_of
from .duels import FORBIDDEN, ficha_text, prices_in
from .models import Page

TASKS_HEADING = 'Tareas en las que te ayuda'
PRECAUTIONS_HEADING = 'Precauciones en tu profesión'
MIN_KIT, MAX_KIT = 2, 4
MIN_TASKS, MAX_TASKS = 5, 7
MIN_PROMPTS = 5


def parse_kit(page: Page) -> List[Tuple[str, str]]:
    kit = []
    for item in page.extra.get('kit', '').split('|'):
        if not item.strip():
            continue
        tid, sep, para = item.partition('=')
        kit.append((tid.strip(), para.strip() if sep else ''))
    return kit


def label(page: Page) -> str:
    name = page.extra.get('profesion', '').strip()
    return name[:1].upper() + name[1:]


def _fail(page: Page, msg: str) -> None:
    raise ValueError(f'profesiones/{page.slug}: {msg}')


def _section(html: str, heading: str) -> str:
    """HTML entre el <h2> con `heading` y el siguiente <h2>."""
    m = re.search(r'<h2[^>]*>\s*' + re.escape(heading) + r'\s*</h2>(.*?)(?=<h2|\Z)', html, re.S)
    return m.group(1) if m else ''


def validate_professions(pages: List[Page], fichas: Dict[str, Page]) -> None:
    known = set()
    for f in fichas.values():
        known |= prices_in(ficha_text(f))
    for p in pages:
        for key in ('profesion', 'emoji'):
            if not p.extra.get(key, '').strip():
                _fail(p, f'falta «{key}»')
        kit = parse_kit(p)
        if not MIN_KIT <= len(kit) <= MAX_KIT or any(not para for _, para in kit):
            _fail(p, f'«kit» necesita {MIN_KIT}–{MAX_KIT} entradas «id = para qué» separadas por «|»')
        for tid, _ in kit:
            if tid not in fichas:
                _fail(p, f'«{tid}» del kit no tiene ficha indexable')
        if len({tid for tid, _ in kit}) != len(kit):
            _fail(p, '«kit» repite una herramienta')
        if not p.sources:
            _fail(p, 'necesita al menos una fuente en «fuentes»')
        for heading in (TASKS_HEADING, PRECAUTIONS_HEADING):
            if not re.search(r'<h2[^>]*>\s*' + re.escape(heading) + r'\s*</h2>', p.body_html):
                _fail(p, f'falta la sección «## {heading}»')
        tasks = len(re.findall(r'<h3[ >]', _section(p.body_html, TASKS_HEADING)))
        if not MIN_TASKS <= tasks <= MAX_TASKS:
            _fail(p, f'«{TASKS_HEADING}» necesita {MIN_TASKS}–{MAX_TASKS} tareas «###» (tiene {tasks})')
        prompts = p.body_html.count('<blockquote')
        if prompts < MIN_PROMPTS:
            _fail(p, f'necesita al menos {MIN_PROMPTS} prompts en cita «>» (tiene {prompts})')
        text = text_of(p.body_html).lower()
        for phrase in FORBIDDEN:
            if phrase in text:
                _fail(p, f'no se afirma «{phrase}» (no hacemos pruebas propias salvo indicación)')
        for price in sorted(prices_in(text_of(p.body_html))):
            if price not in known:
                _fail(p, f'el precio «{price}» no aparece en ninguna ficha: actualiza la página o la ficha')


def profession_context(page: Page, compare_by_id: Dict[str, dict], professions: List[Page]) -> dict:
    return {
        'kit': [(compare_by_id[tid], para) for tid, para in parse_kit(page)],
        'others': sorted((p for p in professions if p.url != page.url and p.indexable), key=label),
        'label': label(page),
    }


def recommended_for(professions: List[Page]) -> Dict[str, List[Tuple[str, str]]]:
    out: Dict[str, List[Tuple[str, str]]] = {}
    for p in sorted((p for p in professions if p.indexable), key=label):
        for tid, _ in parse_kit(p):
            out.setdefault(tid, []).append((label(p), p.url))
    return out
