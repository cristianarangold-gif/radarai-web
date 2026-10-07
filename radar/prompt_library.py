"""Biblioteca de prompts: lee data/prompts.md (bloques «## Título» + metadatos + prompt con [huecos]) y lo valida."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .content import count_words
from .duels import FORBIDDEN
from .glossary import slugify

CATEGORIES = [
    ('escribir', 'Escribir', '✍️'),
    ('estudiar', 'Estudiar', '📚'),
    ('trabajo', 'Trabajo', '💼'),
    ('marketing', 'Marketing', '📣'),
    ('imagenes', 'Imágenes', '🎨'),
    ('programar', 'Programar', '💻'),
    ('dia-a-dia', 'Día a día', '🏠'),
    ('pensar', 'Pensar mejor', '🧠'),
]
KEYS = ('categoria', 'herramientas', 'para', 'consejo')
MIN_WORDS, MAX_WORDS = 15, 150
MAX_SLOTS, MAX_TOOLS = 4, 2
MAX_PARA, MAX_CONSEJO = 25, 40
SLOT = re.compile(r'\[([^\[\]]+)\]')


@dataclass
class Prompt:
    title: str
    slug: str
    meta: Dict[str, str]
    text: str
    cat: str = ''
    tools: List[str] = field(default_factory=list)
    para: str = ''
    consejo: str = ''
    dup_keys: List[str] = field(default_factory=list)
    tool_links: List[Tuple[str, str, str]] = field(default_factory=list)  # (id, nombre, url), lo rellena el contexto

    @property
    def segments(self) -> List[Tuple[str, str]]:
        out, pos = [], 0
        for m in SLOT.finditer(self.text):
            if m.start() > pos:
                out.append(('text', self.text[pos:m.start()]))
            out.append(('slot', m.group(1).strip()))
            pos = m.end()
        if pos < len(self.text):
            out.append(('text', self.text[pos:]))
        return out

    @property
    def slots(self) -> List[str]:
        seen: List[str] = []
        for kind, value in self.segments:
            if kind == 'slot' and value not in seen:
                seen.append(value)
        return seen


def parse_prompts(text: str) -> List[Prompt]:
    prompts = []
    for chunk in re.split(r'(?m)^## ', text)[1:]:
        lines = chunk.split('\n')
        title, rest = lines[0].strip(), lines[1:]
        meta: Dict[str, str] = {}
        dups = []
        while rest and rest[0].strip():
            key, _, value = rest.pop(0).partition(':')
            key = key.strip().lower()
            if key in meta:
                dups.append(key)
            meta[key] = value.strip()
        body = ' '.join(' '.join(rest).split())
        prompts.append(Prompt(title=title, slug=slugify(title), meta=meta, text=body, cat=meta.get('categoria', ''),
                              tools=[t.strip() for t in meta.get('herramientas', '').split(',') if t.strip()],
                              para=meta.get('para', ''), consejo=meta.get('consejo', ''), dup_keys=dups))
    return prompts


def _fail(p: Prompt, msg: str) -> None:
    raise ValueError(f'prompts.md: «{p.title}»: {msg}')


def validate_prompts(prompts: List[Prompt], fichas: Dict[str, object]) -> None:
    if not prompts:
        raise ValueError('prompts.md: no hay ningún prompt (cada uno empieza con «## Título»)')
    cats = {c for c, _, _ in CATEGORIES}
    seen: Dict[str, str] = {}
    for p in prompts:
        if not p.title or not p.slug:
            _fail(p, 'título vacío')
        if p.slug in seen:
            _fail(p, f'título duplicado (mismo ancla que «{seen[p.slug]}»)')
        seen[p.slug] = p.title
        if p.dup_keys:
            _fail(p, f'clave repetida «{p.dup_keys[0]}»')
        unknown = sorted(set(p.meta) - set(KEYS))
        if unknown:
            _fail(p, f'clave desconocida «{unknown[0]}» (válidas: {", ".join(KEYS)}); '
                     '¿falta la línea en blanco antes del prompt?')
        if p.cat not in cats:
            _fail(p, f'categoría «{p.cat}» no válida (válidas: {", ".join(sorted(cats))})')
        if not 1 <= len(p.tools) <= MAX_TOOLS or len(set(p.tools)) != len(p.tools):
            _fail(p, f'«herramientas» necesita 1–{MAX_TOOLS} ids distintos')
        for t in p.tools:
            if t not in fichas:
                _fail(p, f'«{t}» no tiene ficha indexable')
        if not p.para or count_words(p.para) > MAX_PARA:
            _fail(p, f'«para» es obligatorio y admite {MAX_PARA} palabras como máximo')
        if count_words(p.consejo) > MAX_CONSEJO:
            _fail(p, f'«consejo» admite {MAX_CONSEJO} palabras como máximo')
        if '[' in SLOT.sub('', p.text) or ']' in SLOT.sub('', p.text):
            _fail(p, 'corchetes sin cerrar o anidados: escribe los huecos como [nombre]')
        words = count_words(p.text)
        if not MIN_WORDS <= words <= MAX_WORDS:
            _fail(p, f'el prompt tiene {words} palabras (entre {MIN_WORDS} y {MAX_WORDS})')
        if len(p.slots) > MAX_SLOTS:
            _fail(p, f'tiene {len(p.slots)} huecos distintos (máximo {MAX_SLOTS})')
        text = ' '.join([p.text, p.para, p.consejo]).lower()
        for phrase in FORBIDDEN:
            if phrase in text:
                _fail(p, f'no se afirma «{phrase}»')


def library_context(prompts: List[Prompt], compare_by_id: Dict[str, dict]) -> dict:
    for p in prompts:
        p.tool_links = [(t, compare_by_id[t]['n'], compare_by_id[t]['u']) for t in p.tools if t in compare_by_id]
    groups = [{'id': c, 'label': label, 'emoji': emoji, 'prompts': [p for p in prompts if p.cat == c]}
              for c, label, emoji in CATEGORIES]
    return {'groups': [g for g in groups if g['prompts']], 'count': len(prompts), 'categories': CATEGORIES}
