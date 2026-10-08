"""Historial de precios: cambios pasados (data/historial-precios.md) y tomas propias fechadas (data/tomas-precios/)."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from .content import count_words
from .duels import FORBIDDEN, MONTHS, ficha_text, prices_in
from .models import Page

KINDS = {'sube': '↑ Subida', 'baja': '↓ Bajada', 'nuevo': '＋ Plan nuevo', 'retirado': '− Plan retirado',
         'condiciones': '≈ Condiciones'}
ARROW = '→'
PRICE_VALUE = re.compile(r'^(desde )?(\d+(?:,\d+)?) (€|\$)(/mes|/año)?( \(anual\))?$')
DATE_VALUE = re.compile(r'^(\d{4})-(\d{2})(?:-(\d{2}))?$')
SNAPSHOT_NAME = re.compile(r'^\d{4}-\d{2}-\d{2}\.json$')
ENTERPRISE_WORDS = ('business', 'team', 'enterprise', 'empresa')
MAX_TEXT = 30
START = (2023, 1)
# Dominios oficiales además de los de la ficha (web y fuentes): blogs y webs corporativas de la misma empresa.
OFFICIAL_EXTRA = {
    'chatgpt': ['openai.com'],
    'claude': ['anthropic.com', 'claude.com'],
    'gemini': ['blog.google', 'google.com'],
    'notebooklm': ['blog.google', 'google.com', 'gemini.google'],
    'copilot': ['microsoft.com'],
    'github-copilot': ['github.blog'],
    'runway': ['runwayml.com'],
    'notion-ai': ['notion.so'],
    'canva-ai': ['canva.com'],
    'deepl-write': ['deepl.com'],
}
# Prensa reconocida aceptada como fuente. Nunca webs comerciales de seguimiento de precios.
PRESS = ['xataka.com', 'xatakandroid.com', 'xatakamovil.com', 'genbeta.com', 'techcrunch.com', 'theverge.com',
         'ocu.org', 'elpais.com', 'eldiario.es', 'reuters.com', 'arstechnica.com', 'engadget.com']
ARCHIVE_HOST = 'web.archive.org'
ARCHIVE_PATH = re.compile(r'^/web/[0-9a-z_*]+/(.+)$')


@dataclass
class Price:
    amount: Decimal
    currency: str
    period: str
    desde: bool
    text: str

    def same_unit(self, other: 'Price') -> bool:
        return (self.currency, self.period) == (other.currency, other.period)


@dataclass
class Change:
    date: str
    tool: str
    kind: str
    plan: str
    raw_price: str
    text: str
    source: str
    line: int = 0
    auto: bool = False
    before: Optional[Price] = None
    price: Optional[Price] = None

    @property
    def label(self) -> str:
        return KINDS.get(self.kind, self.kind)


@dataclass
class Snapshot:
    date: str
    file: str
    tools: Dict[str, dict] = field(default_factory=dict)


def parse_price(s: str) -> Optional[Price]:
    m = PRICE_VALUE.match((s or '').strip())
    if not m:
        return None
    return Price(Decimal(m.group(2).replace(',', '.')), m.group(3), (m.group(4) or '') + (m.group(5) or ''),
                 bool(m.group(1)), s.strip())


def _prices(raw: str) -> Tuple[Optional[Price], Optional[Price]]:
    if ARROW in raw:
        a, _, b = raw.partition(ARROW)
        return parse_price(a), parse_price(b)
    return None, parse_price(raw)


def parse_history(text: str) -> List[Change]:
    changes = []
    for n, line in enumerate(text.split('\n'), 1):
        if '|' not in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) != 7:
            raise ValueError(f'historial-precios.md: línea {n}: hacen falta 7 campos separados por «|» '
                             f'(fecha | herramienta | tipo | plan | precio | frase | fuente), hay {len(parts)}')
        c = Change(*parts, line=n)
        c.before, c.price = _prices(c.raw_price)
        changes.append(c)
    return changes


def load_snapshots(directory: Path) -> List[Snapshot]:
    snapshots = []
    for f in sorted(Path(directory).glob('*.json')):
        if not SNAPSHOT_NAME.match(f.name):
            raise ValueError(f'tomas-precios/{f.name}: el nombre debe ser la fecha de la revisión, AAAA-MM-DD.json')
        data = json.loads(f.read_text(encoding='utf-8'))
        snapshots.append(Snapshot(f.stem, f.name, data.get('herramientas') or {}))
    return snapshots


def _host(url: str) -> str:
    host = (urlparse(url).hostname or '').lower()
    return host[4:] if host.startswith('www.') else host


def _matches(host: str, domains: List[str]) -> bool:
    return any(host == d or host.endswith('.' + d) for d in domains)


def official_domains(tool: str, ficha: Optional[Page]) -> List[str]:
    urls = ([ficha.extra.get('web', '')] + list(ficha.sources)) if ficha else []
    return [h for h in (_host(u) for u in urls) if h] + OFFICIAL_EXTRA.get(tool, [])


def source_problem(url: str, tool: str, ficha: Optional[Page], official_only: bool = False) -> Optional[str]:
    if not url.startswith('https://'):
        return f'la fuente debe empezar por https:// («{url}»)'
    host, official = _host(url), official_domains(tool, ficha)
    if host == ARCHIVE_HOST:
        m = ARCHIVE_PATH.match(urlparse(url).path)
        inner = m.group(1) if m else ''
        inner = inner if '://' in inner else 'https://' + inner
        if not (m and _matches(_host(inner), official)):
            return 'la copia archivada debe ser de una web oficial de la herramienta'
        return None
    if _matches(host, official) or (not official_only and _matches(host, PRESS)):
        return None
    kind = 'oficial' if official_only else 'oficial, copia archivada o prensa reconocida'
    return f'«{host}» no es una fuente permitida ({kind})'


def _date_problem(value: str, today: date) -> Optional[str]:
    m = DATE_VALUE.match(value)
    if not m:
        return f'fecha «{value}» no válida (AAAA-MM o AAAA-MM-DD)'
    y, mo, d = int(m.group(1)), int(m.group(2)), m.group(3)
    try:
        full = date(y, mo, int(d) if d else 1)
    except ValueError:
        return f'fecha «{value}» no válida (AAAA-MM o AAAA-MM-DD)'
    if (y, mo) < START:
        return f'fecha «{value}» anterior a enero de 2023'
    if (full if d else (y, mo)) > (today if d else (today.year, today.month)):
        return f'fecha «{value}» futura'
    return None


def _is_enterprise(plan: str) -> bool:
    return any(w in plan.lower() for w in ENTERPRISE_WORDS)


def _change_problem(c: Change, fichas: Dict[str, Page], today: date) -> Optional[str]:
    problem = _date_problem(c.date, today)
    if problem:
        return problem
    if c.tool not in fichas:
        return f'«{c.tool}» no tiene ficha indexable'
    if c.kind not in KINDS:
        return f'tipo «{c.kind}» no válido (válidos: {", ".join(KINDS)})'
    if not c.plan:
        return 'falta el plan'
    if _is_enterprise(c.plan):
        return f'«{c.plan}» es un plan de empresa: el historial solo sigue planes individuales'
    has_arrow = ARROW in c.raw_price
    if c.kind in ('sube', 'baja'):
        if not has_arrow:
            return f'«{c.kind}» necesita el precio como «antes {ARROW} después»'
        if not (c.before and c.price):
            return f'precio «{c.raw_price}» no válido (ejemplo: 9,99 €/mes {ARROW} 8 €/mes)'
        if c.before.same_unit(c.price):
            if c.before.amount == c.price.amount:
                return f'«{c.kind}» con el mismo precio antes y después'
            if (c.price.amount > c.before.amount) != (c.kind == 'sube'):
                return f'«{c.kind}» no cuadra con el precio ({c.raw_price})'
    else:
        if has_arrow:
            return f'solo «sube» y «baja» llevan «{ARROW}» en el precio'
        if c.raw_price and not c.price:
            return f'precio «{c.raw_price}» no válido (ejemplo: 8 €/mes, desde 103 €/mes, 110 €/año)'
        if c.kind == 'nuevo' and not c.price:
            return '«nuevo» necesita el precio del plan'
    if not c.text or count_words(c.text) > MAX_TEXT:
        return f'la frase es obligatoria y admite {MAX_TEXT} palabras como máximo'
    for phrase in FORBIDDEN:
        if phrase in c.text.lower():
            return f'no se afirma «{phrase}»'
    return source_problem(c.source, c.tool, fichas.get(c.tool))


def _snapshot_problem(s: Snapshot, fichas: Dict[str, Page], latest: bool) -> Optional[str]:
    if latest:
        for tool in sorted(fichas):
            if tool not in s.tools:
                return f'falta la herramienta «{tool}» (la última toma debe cubrir todas las fichas)'
    for tool, data in s.tools.items():
        if tool not in fichas:
            return f'«{tool}» no tiene ficha indexable'
        problem = source_problem(data.get('fuente', ''), tool, fichas[tool], official_only=True)
        if problem:
            return f'«{tool}»: {problem}'
        planes = data.get('planes') or {}
        if not planes:
            return f'«{tool}» no tiene planes'
        for plan, value in planes.items():
            if _is_enterprise(plan):
                return f'«{tool}»: «{plan}» es un plan de empresa: solo planes individuales'
            if not parse_price(value):
                return f'«{tool}» {plan}: precio «{value}» no válido (ejemplo: 8 €/mes, desde 103 €/mes)'
            if latest:
                missing = prices_in(value) - prices_in(ficha_text(fichas[tool]))
                if missing:
                    return (f'«{tool}» {plan}: el precio «{sorted(missing)[0]}» no aparece en la ficha: '
                            'actualiza la ficha o la toma')
    return None


def validate_history(changes: List[Change], snapshots: List[Snapshot], fichas: Dict[str, Page], today: date) -> None:
    if not snapshots:
        raise ValueError('tomas-precios: no hay ninguna toma de precios (AAAA-MM-DD.json)')
    for i, s in enumerate(snapshots):
        problem = _snapshot_problem(s, fichas, latest=i == len(snapshots) - 1)
        if problem:
            raise ValueError(f'tomas-precios/{s.file}: {problem}')
    seen: Dict[tuple, int] = {}
    for c in changes:
        problem = _change_problem(c, fichas, today)
        key = (c.date, c.tool, c.plan, c.kind)
        if not problem and key in seen:
            problem = f'cambio repetido (igual que la línea {seen[key]})'
        if problem:
            raise ValueError(f'historial-precios.md: línea {c.line}: {problem}')
        seen[key] = c.line


def long_date(value: str) -> str:
    """«2026-10-06» → «6 de octubre de 2026»; «2025-11» → «noviembre de 2025»."""
    parts = value.split('-')
    month = f'{MONTHS[int(parts[1]) - 1]} de {parts[0]}'
    return f'{int(parts[2])} de {month}' if len(parts) == 3 else month


def auto_changes(snapshots: List[Snapshot], changes: List[Change]) -> List[Change]:
    known = {(c.tool, c.plan, c.kind, c.date[:7]) for c in changes}
    out = []
    for old, new in zip(snapshots, snapshots[1:]):
        text = f'Detectado en nuestra revisión del {long_date(new.date)}.'
        for tool, data in new.tools.items():
            before_plans = (old.tools.get(tool) or {}).get('planes') or {}
            plans = data.get('planes') or {}
            found = []
            for plan, value in plans.items():
                if plan not in before_plans:
                    found.append(('nuevo', plan, value, text))
                    continue
                a, b = parse_price(before_plans[plan]), parse_price(value)
                if not (a and b) or (a.same_unit(b) and a.amount == b.amount):
                    continue
                if a.same_unit(b):
                    found.append(('sube' if b.amount > a.amount else 'baja', plan, f'{a.text} {ARROW} {b.text}', text))
                else:
                    found.append(('condiciones', plan, b.text, f'{text[:-1]}: pasa de {a.text} a {b.text}.'))
            if tool in old.tools:
                found += [('retirado', plan, value, text) for plan, value in before_plans.items() if plan not in plans]
            for kind, plan, raw, phrase in found:
                if (tool, plan, kind, new.date[:7]) in known:
                    continue
                c = Change(new.date, tool, kind, plan, raw, phrase, data.get('fuente', ''), auto=True)
                c.before, c.price = _prices(raw)
                out.append(c)
    return out


def _sort_key(value: str) -> str:
    return value if len(value) == 10 else value + '-01'


def chart_points(changes: List[Change], snapshots: List[Snapshot], tool: str) -> Optional[dict]:
    """Puntos (fecha, precio) del plan de pago con más precios distintos; solo la moneda y periodo de su último punto."""
    latest_order = list(((snapshots[-1].tools.get(tool) or {}).get('planes') or {}) if snapshots else [])
    series: Dict[str, List[Tuple[str, Price]]] = {}
    for c in changes:
        if c.tool == tool and c.kind in ('nuevo', 'sube', 'baja') and c.price:
            series.setdefault(c.plan, []).append((c.date, c.price))
    for s in snapshots:
        for plan, value in ((s.tools.get(tool) or {}).get('planes') or {}).items():
            p = parse_price(value)
            if p:
                series.setdefault(plan, []).append((s.date, p))
    best, best_key = None, None
    for plan, pts in series.items():
        pts = sorted(pts, key=lambda x: _sort_key(x[0]))
        last = pts[-1][1]
        pts = [(d, p) for d, p in pts if p.same_unit(last)]
        if len({_sort_key(d) for d, _ in pts}) < 2 or not any(p.amount for _, p in pts):
            continue
        order = latest_order.index(plan) if plan in latest_order else len(latest_order)
        key = (len({p.amount for _, p in pts}), len(pts), -order)
        if best_key is None or key > best_key:
            best, best_key = {'plan': plan, 'currency': last.currency, 'period': last.period, 'points': pts}, key
    return best
