"""Imágenes de portada «radar con logotipo»: SVG en línea para la web y PNG 1200×630 para og:image."""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from markupsafe import Markup, escape

from .brands import icon_path, ink_on
from .models import Brand, Page, Tool

W, H = 1200, 630
CX, CY = W // 2, H // 2
CENTER, EDGE = (0x2a, 0x25, 0x60), (0x0d, 0x11, 0x24)
LINE = (130, 200, 210)
ACCENT, AMBER = '#e4572e', '#f3a712'
DISC = 72          # radio del círculo del logotipo
GRADIENT_STEPS = 24
RINGS = (90, 180, 270, 360, 450, 540)
# Barrido: capas superpuestas que se desvanecen desde el borde (inicio, fin en grados desde arriba, opacidad)
SWEEP = tuple((20, 20 + 8 * k, .055) for k in range(1, 9))

Point = Tuple[float, float]


@dataclass(frozen=True)
class CoverSpec:
    label: str
    brand: Optional[Brand]
    symbol: Optional[str]  # 'star' (comparativa), 'book' (guía) o None


def cover_for(page: Page, brands: Dict[str, Brand], tools: Dict[str, Tool]) -> CoverSpec:
    if page.kind == 'ficha':
        brand = brands.get(page.slug)
        tool = tools.get(page.slug)
        name = tool.name if tool else (brand.name if brand else page.title)
        return CoverSpec(name, brand, None)
    if page.kind == 'noticia':
        brand = brands.get(page.extra.get('empresa', '').strip().lower())
        return CoverSpec(brand.name, brand, None) if brand else CoverSpec('Noticia', None, None)
    if page.kind == 'comparativa':
        return CoverSpec('Comparativa', None, 'star')
    if page.kind == 'guia':
        return CoverSpec('Guía', None, 'book')
    return CoverSpec('Radar IA', None, None)


def og_rel(url: str) -> str:
    return 'og/inicio.png' if url == '/' else f'og/{url.strip("/")}.png'


# --- geometría compartida -------------------------------------------------

def _hex(color: str) -> Tuple[int, int, int]:
    return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))


def _lerp(a, b, t: float) -> Tuple[int, int, int]:
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def _gradient() -> List[Tuple[int, Tuple[int, int, int]]]:
    """Círculos concéntricos de fuera a dentro que imitan el degradado radial del radar."""
    outer = int(math.hypot(CX, CY)) + 2
    full = outer * 0.75  # el degradado llega al color del borde al 75 %
    rings = []
    for i in range(GRADIENT_STEPS + 1):
        r = outer * (1 - i / GRADIENT_STEPS)
        t = min(1.0, r / full)
        rings.append((max(1, round(r)), _lerp(CENTER, EDGE, t)))
    return rings


def _polar(deg: float, r: float) -> Point:
    a = math.radians(deg)
    return CX + r * math.sin(a), CY - r * math.cos(a)


def _symbol_polys(symbol: str, size: float) -> List[List[Point]]:
    """Polígonos del símbolo en una caja de 24×24 escalada a `size` y centrada."""
    if symbol == 'star':
        unit = [(12 + (10 if i % 2 == 0 else 4.2) * math.sin(math.radians(i * 36)),
                 12.5 - (10 if i % 2 == 0 else 4.2) * math.cos(math.radians(i * 36))) for i in range(10)]
        polys = [unit]
    else:  # libro abierto
        polys = [[(2, 5), (11, 6.5), (11, 20), (2, 18.5)], [(13, 6.5), (22, 5), (22, 18.5), (13, 20)]]
    k, ox, oy = size / 24, CX - size / 2, CY - size / 2
    return [[(ox + x * k, oy + y * k) for x, y in poly] for poly in polys]


def _disc(spec: CoverSpec) -> Tuple[str, str]:
    """Color de fondo del círculo central y color de su contenido."""
    if spec.brand:
        return spec.brand.color, ink_on(spec.brand.color)
    if spec.symbol == 'book':
        return AMBER, '#151515'
    return ACCENT, '#fff'


# --- SVG ------------------------------------------------------------------

def _f(x: float) -> str:
    return f'{x:.1f}'.rstrip('0').rstrip('.')


def cover_svg(spec: CoverSpec, logos_dir: Path) -> Markup:
    bg, fg = _disc(spec)
    parts = [f'<svg class="cover" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
             f'role="img" aria-label="{escape(spec.label)}">',
             f'<rect width="{W}" height="{H}" fill="rgb{EDGE}"/>']
    parts += [f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="rgb{c}"/>' for r, c in _gradient()]
    parts += [f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="rgba{LINE + (.22,)}" stroke-width="2"/>'
              for r in RINGS]
    for start, end, alpha in SWEEP:
        (x1, y1), (x2, y2) = _polar(start, 700), _polar(end, 700)
        parts.append(f'<path d="M{CX} {CY}L{_f(x1)} {_f(y1)}A700 700 0 0 1 {_f(x2)} {_f(y2)}Z" '
                     f'fill="rgba{LINE + (alpha,)}"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{DISC + 12}" fill="rgba(255,255,255,.08)"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{DISC}" fill="{bg}"/>')
    d = icon_path(spec.brand, logos_dir) if spec.brand else None
    if d:
        size = DISC * 2 * .58
        parts.append(f'<g transform="translate({_f(CX - size / 2)} {_f(CY - size / 2)}) scale({_f(size / 24)})">'
                     f'<path fill="{fg}" d="{escape(d)}"/></g>')
    elif spec.symbol:
        for poly in _symbol_polys(spec.symbol, DISC * 2 * .6):
            pts = ' '.join(f'{_f(x)},{_f(y)}' for x, y in poly)
            parts.append(f'<polygon points="{pts}" fill="{fg}"/>')
    else:
        letter = spec.brand.monograma if spec.brand else 'R'
        parts.append(f'<text x="{CX}" y="{CY}" dy=".35em" text-anchor="middle" fill="{fg}" '
                     f'font-family="Inter,system-ui,sans-serif" font-weight="700" font-size="64">'
                     f'{escape(letter)}</text>')
    parts.append(f'<text x="48" y="582" fill="#cfd6f5" font-family="Inter,system-ui,sans-serif" '
                 f'font-weight="700" font-size="26" letter-spacing="3">{escape(spec.label.upper())}</text>')
    parts.append(f'<text x="1152" y="584" text-anchor="end" fill="#fff" font-family="Fraunces,Georgia,serif" '
                 f'font-weight="800" font-size="34">Radar<tspan fill="#ff8a5c">IA</tspan></text>')
    parts.append('</svg>')
    return Markup(''.join(parts))


# --- PNG ------------------------------------------------------------------

def write_cover_png(spec: CoverSpec, dest: Path, fonts_dir: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    fonts_dir = Path(fonts_dir)
    img = Image.new('RGB', (W, H), EDGE)
    draw = ImageDraw.Draw(img)
    for r, c in _gradient():
        draw.ellipse((CX - r, CY - r, CX + r, CY + r), fill=c)

    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r in RINGS:
        od.ellipse((CX - r, CY - r, CX + r, CY + r), outline=LINE + (56,), width=2)
    for start, end, alpha in SWEEP:
        od.pieslice((CX - 700, CY - 700, CX + 700, CY + 700), start - 90, end - 90, fill=LINE + (round(alpha * 255),))
    glow = DISC + 12
    od.ellipse((CX - glow, CY - glow, CX + glow, CY + glow), fill=(255, 255, 255, 20))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    bg, fg = _disc(spec)
    draw.ellipse((CX - DISC, CY - DISC, CX + DISC, CY + DISC), fill=bg)
    if spec.symbol and not spec.brand:
        for poly in _symbol_polys(spec.symbol, DISC * 2 * .6):
            draw.polygon(poly, fill=fg)
    else:
        letter = spec.brand.monograma if spec.brand else 'R'
        font = ImageFont.truetype(str(fonts_dir / 'inter-latin-700-normal.woff2'), 72)
        draw.text((CX, CY), letter, fill=fg, font=font, anchor='mm')

    label_font = ImageFont.truetype(str(fonts_dir / 'inter-latin-700-normal.woff2'), 26)
    x = 48
    for ch in spec.label.upper():  # espaciado entre letras como en el SVG
        draw.text((x, 582), ch, fill='#cfd6f5', font=label_font, anchor='ls')
        x += draw.textlength(ch, font=label_font) + 3

    mark = ImageFont.truetype(str(fonts_dir / 'fraunces-latin-800-normal.woff2'), 34)
    ia_w = draw.textlength('IA', font=mark)
    draw.text((1152 - ia_w, 584), 'IA', fill='#ff8a5c', font=mark, anchor='ls')
    draw.text((1152 - ia_w, 584), 'Radar', fill='#fff', font=mark, anchor='rs')

    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, 'PNG', optimize=True)
