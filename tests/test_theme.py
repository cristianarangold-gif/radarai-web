"""Modo oscuro: tokens, contraste, script sin destello y botón de la cabecera."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / 'static' / 'css' / 'radar.css').read_text(encoding='utf-8')
TOKEN = re.compile(r'--([\w-]+):\s*(#[0-9a-fA-F]{3,6})\b')


def _block(pattern):
    m = re.search(pattern, CSS, re.S)
    assert m, pattern
    return dict(TOKEN.findall(m.group(1)))


LIGHT = _block(r'/\* 2\. Tokens \*/\s*:root \{(.*?)\n\}')
DARK_MEDIA = _block(r'@media \(prefers-color-scheme: dark\) \{\s*:root:not\(\[data-theme="light"\]\) \{(.*?)\}')
DARK_ATTR = _block(r':root\[data-theme="dark"\] \{(.*?)\}')


def _lum(hex_color):
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    def chan(i):
        c = int(h[i:i + 2], 16) / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * chan(0) + 0.7152 * chan(2) + 0.0722 * chan(4)


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def test_dark_blocks_are_identical_and_complete():
    assert DARK_MEDIA == DARK_ATTR
    colors = {k for k in LIGHT if k not in ('white',)}
    assert colors <= set(DARK_MEDIA), colors - set(DARK_MEDIA)
    assert 'color-scheme: dark' in CSS.split(':root[data-theme="dark"]')[1].split('}')[0]


@pytest.mark.parametrize('theme', ['light', 'dark'])
@pytest.mark.parametrize('fg, bg, minimum', [
    ('ink', 'paper', 4.5), ('body', 'paper', 4.5), ('body', 'surface', 4.5), ('ink-2', 'paper', 4.5), ('ink-3', 'paper', 4.5), ('ink', 'surface', 4.5),
    ('ink-2', 'surface', 4.5), ('ink-3', 'surface', 4.5), ('accent-ink', 'paper', 4.5), ('accent-ink', 'surface', 4.5),
    ('on-ink', 'ink', 4.5), ('on-ink', 'accent-ink', 4.5), ('ink', 'paper-2', 4.5), ('code-fg', 'code-bg', 4.5),
    ('rule', 'paper', 1.2), ('ink', 'rule', 3),
])
def test_token_contrast(theme, fg, bg, minimum):
    tokens = LIGHT if theme == 'light' else {**LIGHT, **DARK_MEDIA}
    ratio = contrast(tokens[fg], tokens[bg])
    assert ratio >= minimum, f'{theme}: {fg}/{bg} = {ratio:.2f}'


def test_on_accent_is_readable_in_dark():
    tokens = {**LIGHT, **DARK_MEDIA}
    assert contrast(tokens['on-accent'], tokens['accent']) >= 4.5


# Selectores donde el texto blanco va sobre un fondo propio que no cambia con el modo (logos, radar, pie).
WHITE_TEXT_OK = ('.blip-in', '.search-ic', '.assistant-logo', '.compare-option .logo', '.compare-table thead th .logo',
                 '.site-footer', '.tagline', '.footer-in')


def test_no_white_text_on_ink():
    for selector, body in re.findall(r'([^{}]+)\{([^}]*)\}', CSS):
        if re.search(r'(^|[;\s])color:\s*var\(--white\)', body):
            sel = ' '.join(selector.split())
            assert sel.startswith(WHITE_TEXT_OK), sel
        assert not re.search(r'background:\s*var\(--white\)', body), ' '.join(selector.split())


@pytest.fixture(scope='module')
def home():
    import subprocess
    import sys
    import tempfile
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True, capture_output=True)
    return (out / 'index.html').read_text(encoding='utf-8')


def test_head_script_before_stylesheet(home):
    head = home.split('</head>')[0]
    script = head.index("localStorage.getItem('radar-tema')")
    assert script < head.index('radar.css') and 'try' in head[max(0, script - 200):script]
    assert '<meta name="color-scheme" content="light dark">' in head
    assert head.count('name="theme-color"') == 2


def test_theme_button(home):
    header = home.split('<header')[1].split('</header>')[0]
    assert re.search(r'<button class="theme-toggle" type="button" hidden aria-label="Activar modo oscuro"', header)
    js = (ROOT / 'static' / 'js' / 'site.js').read_text(encoding='utf-8')
    assert 'radar-tema' in js and 'prefers-color-scheme: dark' in js and 'Activar modo claro' in js
    assert 'innerHTML' not in js
