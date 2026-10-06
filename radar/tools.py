"""Catálogo de herramientas (data/tools.json)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from .models import Tool

CATEGORIES = [
    ('ia-general', 'IA general'),
    ('escritura', 'Escritura'),
    ('imagenes', 'Imágenes'),
    ('video', 'Vídeo'),
    ('audio', 'Audio y música'),
    ('programacion', 'Programación'),
    ('educacion', 'Educación'),
    ('marketing', 'Marketing'),
    ('productividad', 'Productividad'),
]


def load_tools(path: Path, content_dir: Path) -> Dict[str, Tool]:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    pages_dir = Path(content_dir) / 'herramientas'
    tools = {}
    for tid, t in data.items():
        tools[tid] = Tool(
            id=tid, name=t['name'], cat=t['cat'], desc=t.get('desc', ''),
            price=t.get('price', ''), level=t.get('level', ''),
            platform=t.get('platform', ''), lang=t.get('lang', ''),
            tags=list(t.get('tags', [])), url=t['url'],
            has_page=(pages_dir / f'{tid}.md').exists(),
        )
    return tools
