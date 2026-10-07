import json
import re
from pathlib import Path

from radar.compare import compare_payload
from radar.models import Brand, Tool
from radar.tools import CATEGORIES
from tests.helpers import make_page

ROOT = Path(__file__).resolve().parent.parent


def tool(tid, name, cat='ia-general'):
    return Tool(id=tid, name=name, cat=cat, desc='', price='', level='', platform='', lang='', tags=[],
                url=f'https://{tid}.example/', has_page=True)


def ficha(tid, **extra):
    return make_page(kind='ficha', slug=tid, url=f'/herramientas/{tid}/', title=tid, extra=extra)


def test_payload_order_fields_and_dashes():
    fichas = {'zeta': ficha('zeta', precio_desde='0 €', web='https://zeta.example/'),
              'alfa': ficha('alfa', precio_desde='5 $', plan_pago='Pro 5 $/mes', ideal_para='X',
                            plataforma='Web', veredicto='Muy bien.', web='https://alfa.example/')}
    tools = {'zeta': tool('zeta', 'Zeta'), 'alfa': tool('alfa', 'Alfa', 'video')}
    brands = {'alfa': Brand('alfa', 'Alfa Pro', '#123456', None, 'A')}
    p = compare_payload(fichas, tools, brands, CATEGORIES)
    assert [t['id'] for t in p] == ['alfa', 'zeta']
    assert p[0] == {'id': 'alfa', 'n': 'Alfa Pro', 'c': '#123456', 'm': 'A', 'u': '/herramientas/alfa/',
                    'w': 'https://alfa.example/', 'desde': '5 $', 'pago': 'Pro 5 $/mes', 'ideal': 'X',
                    'plataformas': 'Web', 'veredicto': 'Muy bien.', 'cat': 'Vídeo'}
    assert p[1]['pago'] == '—' and p[1]['plataformas'] == '—' and p[1]['c'] == '#151515' and p[1]['m'] == 'Z'


def test_real_compare_page_words():
    from radar.content import load_pages
    page = [p for p in load_pages(ROOT / 'content') if p.url == '/comparador/'][0]
    assert page.word_count >= 300 and page.indexable


def test_built_compare_page():
    import subprocess, sys, tempfile
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    html = (out / 'comparador' / 'index.html').read_text()
    fichas = sorted(p.stem for p in (ROOT / 'content' / 'herramientas').glob('*.md'))
    assert html.count('type="checkbox" name="h"') == len(fichas)
    assert 'Elige hasta 3 herramientas' in html and 'aria-live="polite"' in html
    raw = re.search(r'<script type="application/json" id="comparador-datos">(.*?)</script>', html, re.S).group(1)
    assert sorted(t['id'] for t in json.loads(raw)) == fichas
    table = html[html.index('class="compare-summary"'):]
    for f in fichas:
        assert f'href="/herramientas/{f}/"' in table
    assert 'noindex' not in html


def test_compare_js_is_dom_safe_and_small():
    import gzip
    js = (ROOT / 'static' / 'js' / 'compare.js').read_text()
    assert js.strip()
    assert 'innerHTML' not in js
    for needle in ('textContent', 'replaceState', "'scope'", 'noopener nofollow', 'Elige al menos 2', 'disabled'):
        assert needle in js, needle
    assert len(gzip.compress(js.encode('utf-8'))) <= 5000


def _env_page(**kw):
    from radar.render import make_env, render_page
    from tests.test_render import ctx, tool
    from datetime import date
    env = make_env(ROOT / 'templates')
    return env, render_page, ctx, tool, date


def test_entry_points_with_comparator():
    env, render_page, ctx, tool, date = _env_page()
    payload = [{'id': 'bar'}]
    f = make_page(kind='ficha', slug='bar', url='/herramientas/bar/', title='Bar', date=date(2026, 10, 1),
                  extra={'web': 'https://bar.example/'})
    html = render_page(env, f, ctx(tools={'bar': tool('bar', True)}, compare_payload=payload))
    assert 'href="/comparador/?h=bar">Comparar Bar con… →</a>' in html
    listing = render_page(env, make_page(url='/herramientas/', title='H'), ctx(listing=[], compare_payload=payload))
    assert 'href="/comparador/">⇄ Comparar herramientas</a>' in listing
    page = make_page(url='/que-ia-necesito/', slug='que-ia-necesito', title='Q')
    assert 'data-comparador' in render_page(env, page, ctx(assistant_payload={'tareas': {}}, compare_payload=payload))


def test_no_entry_points_without_comparator():
    env, render_page, ctx, tool, date = _env_page()
    f = make_page(kind='ficha', slug='bar', url='/herramientas/bar/', title='Bar', date=date(2026, 10, 1))
    assert '/comparador/' not in render_page(env, f, ctx(tools={'bar': tool('bar', True)}))
    assert '/comparador/' not in render_page(env, make_page(url='/herramientas/', title='H'), ctx(listing=[]))


def test_assistant_js_links_to_comparator_with_two_fichas():
    js = (ROOT / 'static' / 'js' / 'assistant.js').read_text()
    assert 'Comparar con las alternativas →' in js and 'data-comparador' in js


def test_review_fixes_compare():
    js = (ROOT / 'static' / 'js' / 'compare.js').read_text()
    assert 'if (chosen.join(\',\') !== raw) sync();' in js  # limpia ?h= al cargar
    assert "' y '" in js  # «X, Y y Z» en el caption
    text = (ROOT / 'content' / 'paginas' / 'comparador.md').read_text()
    assert 'en su apartado de precios' in text
    assistant = (ROOT / 'static' / 'js' / 'assistant.js').read_text()
    assert 'withFicha.indexOf(id) === i' in assistant  # sin duplicados
