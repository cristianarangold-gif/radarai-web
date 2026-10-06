"""Redirecciones de URLs retiradas (GitHub Pages no admite 301)."""
from __future__ import annotations

from pathlib import Path
from typing import List

import jinja2

from .models import Redirect
from .seo import canonical


def normalize_source(src: str) -> str:
    src = '/' + src.strip().strip('/')
    if src.endswith('/index.html'):
        src = src[:-len('index.html')]
    elif not src.endswith('.html') and not src.endswith('/'):
        src += '/'
    return src


def load_redirects(path: Path) -> List[Redirect]:
    """Lee líneas «origen: destino». Ignora vacías y comentarios (#)."""
    redirects = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        src, _, target = line.partition(': ')
        redirects.append(Redirect(normalize_source(src), target.strip()))
    return redirects


def output_paths(r: Redirect) -> List[str]:
    rel = r.source.lstrip('/')
    if rel.endswith('.html'):
        return [rel]
    return [rel + 'index.html']


def render_redirect(env: jinja2.Environment, r: Redirect) -> str:
    target_abs = r.target if r.target.startswith('http') else canonical(r.target)
    return env.get_template('redirect.html').render(target=r.target, target_abs=target_abs)
