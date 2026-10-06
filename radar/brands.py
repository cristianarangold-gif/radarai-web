"""Marcas: color, icono de Simple Icons (static/logos) y monograma de respaldo."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Optional

from markupsafe import Markup, escape

from .models import Brand

COLOR_RE = re.compile(r'#[0-9a-fA-F]{6}')
PATH_RE = re.compile(r'<path[^>]*\sd="([^"]+)"')


def load_brands(path: Path, logos_dir: Path) -> Dict[str, Brand]:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    brands = {}
    for bid, b in data.items():
        color = b.get('color', '')
        if not COLOR_RE.fullmatch(color):
            raise ValueError(f'brands.json: «{bid}» tiene un color no válido ({color!r})')
        if not b.get('monograma'):
            raise ValueError(f'brands.json: a «{bid}» le falta el monograma')
        icon = b.get('icon') or None
        if icon and not (Path(logos_dir) / f'{icon}.svg').exists():
            icon = None
        brands[bid] = Brand(id=bid, name=b['name'], color=color.lower(), icon=icon, monograma=b['monograma'])
    return brands


def icon_path(brand: Brand, logos_dir: Path) -> Optional[str]:
    if not brand.icon:
        return None
    m = PATH_RE.search((Path(logos_dir) / f'{brand.icon}.svg').read_text(encoding='utf-8'))
    return m.group(1) if m else None


def ink_on(color: str) -> str:
    """Color del icono o la letra sobre el fondo de la marca: tinta en fondos claros."""
    r, g, b = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return '#151515' if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.6 else '#fff'


def logo_html(brand: Brand, size: int, logos_dir: Path) -> Markup:
    fg = ink_on(brand.color)
    d = icon_path(brand, logos_dir)
    inner = (f'<svg viewBox="0 0 24 24"><path fill="{fg}" d="{escape(d)}"/></svg>' if d
             else str(escape(brand.monograma)))
    return Markup(f'<span class="logo" style="--brand:{brand.color};color:{fg};'
                  f'width:{size}px;height:{size}px" aria-hidden="true">{inner}</span>')
