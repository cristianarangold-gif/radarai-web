"""Asistente «¿Qué IA necesito?»: reglas editoriales (data/asistente.json) y alternativas del catálogo."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Set

from .models import Brand, Page, Tool

TASKS = ('escribir', 'estudiar', 'imagenes', 'video', 'musica', 'programar', 'marketing', 'productividad', 'general')
BUDGETS = ('gratis', 'poco', 'sin-limite')
LEVELS = ('empiezo', 'me-manejo', 'avanzado')
AUDIENCES = ('mi', 'equipo')
OVERRIDES = ('si_avanzado', 'si_equipo')
FREE_PRICES = ('gratis', 'freemium')


def load_assistant(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _check_rule(key: str, rule: dict, tools: Dict[str, Tool], fichas: Dict[str, Page], budget: str) -> None:
    where = f'asistente.json: {key}'
    principal = rule.get('principal', '')
    if principal not in tools:
        raise ValueError(f'{where}: herramienta desconocida «{principal}»')
    if principal not in fichas:
        raise ValueError(f'{where}: «{principal}» no tiene ficha')
    if budget == 'gratis' and not fichas[principal].extra.get('precio_desde', '').startswith('0'):
        raise ValueError(f'{where}: «{principal}» no es gratis (precio_desde)')
    porque = rule.get('porque', [])
    if not 2 <= len(porque) <= 3:
        raise ValueError(f'{where}: «porque» debe tener entre 2 y 3 frases')
    texts = list(porque) + [a.get('motivo', '') for a in rule.get('alternativas', [])]
    if any('hemos probado' in t.lower() for t in texts):
        raise ValueError(f'{where}: no se puede decir «hemos probado»')
    for alt in rule.get('alternativas', []):
        if alt.get('id') not in tools:
            raise ValueError(f'{where}: herramienta desconocida «{alt.get("id")}»')


def validate_assistant(data: dict, tools: Dict[str, Tool], fichas: Dict[str, Page], urls: Set[str]) -> None:
    for task in TASKS:
        info = data['tareas'].get(task)
        if not info:
            raise ValueError(f'asistente.json: falta la tarea {task}')
        for field in ('comparativa', 'guia'):
            if info.get(field) not in urls:
                raise ValueError(f'asistente.json: {task}: URL inexistente {info.get(field)}')
    for task in TASKS:
        for budget in BUDGETS:
            key = f'{task}/{budget}'
            rule = data['reglas'].get(key)
            if rule is None:
                raise ValueError(f'asistente.json: falta la regla {key}')
            _check_rule(key, rule, tools, fichas, budget)
            for name in OVERRIDES:
                if name in rule:
                    _check_rule(f'{key} ({name})', rule[name], tools, fichas, budget)


def pick_rule(data: dict, tarea: str, presupuesto: str, nivel: str, para: str) -> dict:
    rule = data['reglas'][f'{tarea}/{presupuesto}']
    if para == 'equipo' and 'si_equipo' in rule:
        return rule['si_equipo']
    if nivel == 'avanzado' and 'si_avanzado' in rule:
        return rule['si_avanzado']
    return rule


def auto_alternatives(data: dict, tools: Dict[str, Tool], tarea: str, presupuesto: str, nivel: str,
                      exclude: Set[str], n: int = 2) -> List[str]:
    cats = set(data['tareas'][tarea]['categorias'])
    found = [t for t in tools.values()
             if t.cat in cats and t.id not in exclude
             and (presupuesto != 'gratis' or t.price in FREE_PRICES)
             and (nivel != 'empiezo' or t.level != 'avanzado')]
    found.sort(key=lambda t: (not t.has_page, t.name.lower()))
    return [t.id for t in found[:n]]


def _tool_info(t: Tool, brands: Dict[str, Brand], fichas: Dict[str, Page]) -> dict:
    ficha = fichas.get(t.id)
    brand = brands.get(t.id)
    return {
        'n': brand.name if brand else t.name,
        'u': ficha.url if ficha else f'/herramientas/#cat-{t.cat}',
        'c': brand.color if brand else '#151515',
        'm': brand.monograma if brand else t.name[:1].upper(),
        'p': ficha.extra.get('precio_desde', '') if ficha else '',
        'i': (ficha.extra.get('ideal_para') if ficha else '') or t.desc,
        'w': (ficha.extra.get('web') if ficha else '') or t.url,
        'nivel': t.level,
    }


def resolve_payload(data: dict, tools: Dict[str, Tool], brands: Dict[str, Brand], fichas: Dict[str, Page]) -> dict:
    """Datos que necesita assistant.js: reglas, alternativas automáticas y ficha corta de cada herramienta usada."""
    used: Set[str] = set()
    auto: Dict[str, List[str]] = {}
    for key, rule in data['reglas'].items():
        for r in [rule] + [rule[o] for o in OVERRIDES if o in rule]:
            used.add(r['principal'])
            used.update(a['id'] for a in r.get('alternativas', []))
    for task in TASKS:
        for budget in BUDGETS:
            rule = data['reglas'][f'{task}/{budget}']
            for level in LEVELS:
                exclude = set()
                for r in [rule] + [rule[o] for o in OVERRIDES if o in rule]:
                    exclude.add(r['principal'])
                    exclude.update(a['id'] for a in r.get('alternativas', []))
                ids = auto_alternatives(data, tools, task, budget, level, exclude)
                auto[f'{task}/{budget}/{level}'] = ids
                used.update(ids)
    return {
        'tareas': data['tareas'],
        'reglas': data['reglas'],
        'auto': auto,
        'tools': {tid: _tool_info(tools[tid], brands, fichas) for tid in sorted(used)},
    }
