"""Página «Empieza aquí»: carga y valida data/empieza.json (tarjetas de situación y ruta de 5 pasos)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Set

N_SITUACIONES = 4
N_PASOS = 5


def load_start(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _fail(msg: str) -> None:
    raise ValueError(f'empieza.json: {msg}')


def _check_text(item: dict, fields, where: str) -> None:
    for f in fields:
        if not str(item.get(f) or '').strip():
            _fail(f'{where}: falta «{f}»')


def _check_links(links: List[dict], urls: Set[str], where: str) -> None:
    seen = set()
    for ln in links:
        if not isinstance(ln, dict):
            _fail(f'{where}: cada enlace debe ser un objeto con «texto» y «url»')
        _check_text(ln, ('texto', 'url'), where)
        if ln['url'] not in urls:
            _fail(f'{where}: la URL {ln["url"]} no existe en el sitio')
        if ln['url'] in seen:
            _fail(f'{where}: URL repetida {ln["url"]}')
        seen.add(ln['url'])


def validate_start(data: dict, urls: Set[str]) -> None:
    if not isinstance(data, dict):
        _fail('debe ser un objeto con «situaciones» y «pasos»')
    situaciones, pasos = data.get('situaciones') or [], data.get('pasos') or []
    if not isinstance(situaciones, list) or not all(isinstance(x, dict) for x in situaciones):
        situaciones = []
    if not isinstance(pasos, list) or not all(isinstance(x, dict) for x in pasos):
        pasos = []
    if len(situaciones) != N_SITUACIONES:
        _fail(f'hacen falta {N_SITUACIONES} situaciones (hay {len(situaciones)})')
    if len(pasos) != N_PASOS:
        _fail(f'hacen falta {N_PASOS} pasos (hay {len(pasos)})')
    for i, s in enumerate(situaciones, 1):
        where = f'situación {i}'
        _check_text(s, ('emoji', 'titulo', 'texto'), where)
        if not isinstance(s.get('enlaces'), list) or not 2 <= len(s['enlaces']) <= 3:
            _fail(f'{where}: cada situación lleva 2–3 enlaces')
        _check_links(s['enlaces'], urls, where)
    for i, p in enumerate(pasos, 1):
        where = f'paso {i}'
        _check_text(p, ('titulo', 'texto'), where)
        extra = p.get('extra') or []
        if not isinstance(p.get('cta'), dict):
            _fail(f'{where}: falta «cta» (objeto con «texto» y «url»)')
        if not isinstance(extra, list) or len(extra) > 3:
            _fail(f'{where}: admite 0–3 enlaces extra')
        _check_links([p['cta']] + extra, urls, where)
