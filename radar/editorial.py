"""Lógica editorial: radar de la portada, tiempo de lectura, índice, relacionadas e imprescindibles."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from .content import text_of
from .models import Brand, Page, Tool

DEFAULT_RADAR = ['chatgpt', 'claude', 'gemini', 'midjourney', 'perplexity']
H2_RE = re.compile(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', re.S)


def split_ids(value: str) -> List[str]:
    return [v.strip().lower() for v in (value or '').split(',') if v.strip()]


def validate_news_meta(pages: List[Page], tools: Dict[str, Tool], brands: Dict[str, Brand]) -> None:
    for p in pages:
        if p.kind != 'noticia':
            continue
        for tid in split_ids(p.extra.get('herramientas', '')):
            if tid not in tools:
                raise ValueError(f'noticias/{p.slug}: herramienta desconocida «{tid}»')
        empresa = p.extra.get('empresa', '').strip().lower()
        if empresa and empresa not in brands:
            raise ValueError(f'noticias/{p.slug}: empresa desconocida «{empresa}»')


def radar_tools(news: List[Page], tools: Dict[str, Tool], n: int = 5, recent: int = 6) -> List[Tool]:
    ids: List[str] = []
    for p in news[:recent]:
        ids += split_ids(p.extra.get('herramientas', ''))
    chosen: List[Tool] = []
    for tid in ids + DEFAULT_RADAR:
        t = tools.get(tid)
        if t and t.has_page and t not in chosen:
            chosen.append(t)
        if len(chosen) == n:
            break
    return chosen


def reading_minutes(page: Page) -> int:
    return max(1, round(page.word_count / 220))


def toc(body_html: str) -> List[Tuple[str, str]]:
    return [(hid, ' '.join(text_of(inner).split())) for hid, inner in H2_RE.findall(body_html)]


def related_news(page: Page, news: List[Page], n: int = 3) -> List[Page]:
    return [p for p in news if p.url != page.url][:n]


def load_imprescindibles(path: Path, by_url: Dict[str, Page]) -> List[Page]:
    result = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        url = line.strip()
        if not url or url.startswith('#'):
            continue
        page = by_url.get(url)
        if page is None or not page.indexable:
            raise ValueError(f'imprescindibles.txt: {url} no existe o no es indexable')
        result.append(page)
    return result[:4]
