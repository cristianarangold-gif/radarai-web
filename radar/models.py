"""Modelos de datos del generador de Radar IA."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Page:
    kind: str
    slug: str
    url: str
    title: str
    description: str
    body_html: str
    date: Optional[date]
    updated: Optional[date]
    author: str
    sources: List[str]
    draft: bool
    word_count: int
    extra: dict = field(default_factory=dict)

    @property
    def indexable(self) -> bool:
        return not self.draft and self.extra.get('noindex', '').lower() not in ('si', 'sí', 'true')

    @property
    def lastmod(self) -> Optional[date]:
        return self.updated or self.date


@dataclass
class Tool:
    id: str
    name: str
    cat: str
    desc: str
    price: str
    level: str
    platform: str
    lang: str
    tags: List[str]
    url: str
    has_page: bool = False


@dataclass
class Redirect:
    source: str
    target: str
