"""Comparador: datos de las herramientas con ficha para comparar lado a lado."""
from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from .models import Brand, Page, Tool

EMPTY = '—'


def compare_payload(fichas: Dict[str, Page], tools: Dict[str, Tool], brands: Dict[str, Brand],
                    categories: Sequence[Tuple[str, str]]) -> List[dict]:
    cats = dict(categories)
    items = []
    for slug, page in fichas.items():
        tool, brand = tools.get(slug), brands.get(slug)
        name = brand.name if brand else (tool.name if tool else page.title)
        extra = page.extra
        items.append({
            'id': slug, 'n': name,
            'c': brand.color if brand else '#151515',
            'm': brand.monograma if brand else name[:1].upper(),
            'u': page.url,
            'w': extra.get('web') or (tool.url if tool else ''),
            'desde': extra.get('precio_desde') or EMPTY,
            'pago': extra.get('plan_pago') or EMPTY,
            'ideal': extra.get('ideal_para') or EMPTY,
            'plataformas': extra.get('plataforma') or EMPTY,
            'veredicto': extra.get('veredicto') or EMPTY,
            'cat': cats.get(tool.cat, EMPTY) if tool else EMPTY,
        })
    return sorted(items, key=lambda t: t['n'].lower())
