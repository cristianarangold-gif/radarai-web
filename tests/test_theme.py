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
    ('on-ink', 'ink', 4.5), ('on-ink', 'accent-ink', 4.5), ('accent-ink', 'paper-2', 4.5), ('on-accent', 'accent-ink', 4.5), ('ink', 'paper-2', 4.5), ('code-fg', 'code-bg', 4.5),
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
    assert head.count('<meta name="theme-color"') == 2


def test_theme_button(home):
    header = home.split('<header')[1].split('</header>')[0]
    assert re.search(r'<button class="theme-toggle" type="button" hidden aria-label="Activar modo oscuro"', header)
    js = (ROOT / 'static' / 'js' / 'site.js').read_text(encoding='utf-8')
    assert 'radar-tema' in js and 'prefers-color-scheme: dark' in js and 'Activar modo claro' in js
    assert 'innerHTML' not in js


# Selectores con colores fijos a propósito: el pie y el radar son oscuros en ambos modos; el velo del buscador también.
LITERAL_OK = ('.site-footer', '.footer-in', '.footer-base', '.mini-radar', '.radar-', '.blip-in', '@keyframes', '35%',
              '.search-dialog', '0%', '6%', '100%')


def test_no_literal_colors_outside_tokens():
    body = CSS[CSS.index('/* 3. Base */'):]
    for selector, decl in re.findall(r'([^{}]+)\{([^}]*)\}', body):
        sel = ' '.join(selector.split())
        if re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(', decl):
            assert sel.startswith(LITERAL_OK), sel


@pytest.mark.parametrize('theme', ['light', 'dark'])
@pytest.mark.parametrize('fg, bg', [
    ('price-sube-fg', 'price-sube-bg'), ('price-baja-fg', 'price-baja-bg'), ('price-nuevo-fg', 'price-nuevo-bg'),
    ('price-retirado-fg', 'price-retirado-bg'), ('price-condiciones-fg', 'price-condiciones-bg'),
    ('on-amber', 'amber'), ('on-amber', 'slot-filled'), ('ink', 'mark-bg'), ('on-ink-accent', 'ink'),
])
def test_component_contrast(theme, fg, bg):
    tokens = LIGHT if theme == 'light' else {**LIGHT, **DARK_MEDIA}
    ratio = contrast(tokens[fg], tokens[bg])
    assert ratio >= 4.5, f'{theme}: {fg}/{bg} = {ratio:.2f}'


def test_small_orange_text_and_buttons_use_accent_ink():
    assert re.search(r'\.eyebrow, \.kicker \{ color: var\(--accent-ink\)', CSS)
    assert re.search(r'\.must a:hover strong \{ color: var\(--accent-ink\)', CSS)
    for selector, decl in re.findall(r'([^{}]+)\{([^}]*)\}', CSS):
        sel = ' '.join(selector.split())
        # El naranja claro (--accent) solo como fondo decorativo, nunca detrás de texto.
        if re.search(r'background:\s*var\(--accent\)', decl):
            assert 'color:' not in decl, sel
        # Texto sobre fondo naranja: --on-accent; sobre fondo --ink: --on-ink.
        if re.search(r'background:\s*var\(--accent-ink\)', decl) and 'color:' in decl:
            assert 'var(--on-accent)' in decl, sel
        if re.search(r'background:\s*var\(--ink\)', decl) and 'color:' in decl:
            assert 'var(--on-ink)' in decl, sel


def test_hover_on_ink_sets_on_ink_text():
    for sel in (r'\.utility-app \.btn\.primary:hover', r'\.assistant-try:hover'):
        m = re.search(sel + r' \{([^}]*)\}', CSS)
        assert m and 'color: var(--on-ink)' in m.group(1), sel


def test_light_root_declares_color_scheme():
    root = CSS[CSS.index('/* 2. Tokens */'):].split('}')[0]
    assert 'color-scheme: light' in root


def test_sticky_header_color_mix_has_supports_fallback():
    main_rule = re.search(r'\n\.site-header \{([^}]*)\}', CSS).group(1)
    assert 'color-mix' not in main_rule and 'background: var(--paper)' in main_rule
    assert re.search(r'@supports \(background: color-mix\(in srgb, red 50%, transparent\)\) \{\s*\.site-header', CSS)


@pytest.mark.parametrize('theme', ['light', 'dark'])
@pytest.mark.parametrize('bg', ['paper', 'surface'])
def test_control_borders_are_visible(theme, bg):
    tokens = LIGHT if theme == 'light' else {**LIGHT, **DARK_MEDIA}
    assert contrast(tokens['control-border'], tokens[bg]) >= 3


def test_dark_logo_ring_is_visible():
    tokens = {**LIGHT, **DARK_MEDIA}
    assert contrast(tokens['logo-ring'], '#151515') >= 3 and 'box-shadow: 0 0 0 1px var(--logo-ring)' in CSS


def test_head_script_is_scoped_and_updates_theme_color(home):
    head = home.split('</head>')[0]
    script = head[head.index("localStorage.getItem('radar-tema')") - 120:head.index('radar.css')]
    assert '(function(){' in script and 'theme-color' in script
    js = (ROOT / 'static' / 'js' / 'site.js').read_text(encoding='utf-8')
    assert 'theme-color' in js
