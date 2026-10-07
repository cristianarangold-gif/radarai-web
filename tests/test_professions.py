import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import pytest

from radar.compare import compare_payload
from radar.models import Brand, Tool
from radar.professions import parse_kit, profession_context, recommended_for, validate_professions
from radar.tools import CATEGORIES
from tests.helpers import make_page

ROOT = Path(__file__).resolve().parent.parent


def ficha(tid, **extra):
    base = dict(precio_desde='0 €', plan_pago='Pro 10 €/mes', ideal_para='Todo', plataforma='Web')
    base.update(extra)
    return make_page(kind='ficha', slug=tid, url=f'/herramientas/{tid}/', title=tid, date=date(2026, 10, 6),
                     extra=base)


FICHAS = {'alfa': ficha('alfa'), 'beta': ficha('beta', precio_desde='5 $'), 'gamma': ficha('gamma')}
TOOLS = {t: Tool(id=t, name=t.title(), cat='ia-general', desc='', price='', level='', platform='', lang='',
                 tags=[], url=f'https://{t}.example/', has_page=True) for t in FICHAS}
BRANDS = {'alfa': Brand('alfa', 'Alfa', '#10a37f', None, 'A')}


def body(tasks=5, quotes=5, precautions=True, extra=''):
    parts = ['<p>Entradilla.</p>', '<h2 id="tareas">Tareas en las que te ayuda</h2>']
    for i in range(tasks):
        parts.append(f'<h3>Tarea {i}</h3><p>Texto.</p>')
        if i < quotes:
            parts.append('<blockquote><p>«Prompt»</p></blockquote>')
    for i in range(tasks, quotes):
        parts.append('<blockquote><p>«Prompt extra»</p></blockquote>')
    if precautions:
        parts.append('<h2 id="precauciones">Precauciones en tu profesión</h2><p>Cuidado.</p>')
    parts.append(extra)
    return ''.join(parts)


def prof(slug='docentes', html=None, **extra):
    base = dict(profesion='docentes', emoji='🍎', kit='alfa = Preparar clases | beta = Ejercicios')
    base.update(extra)
    sources = base.pop('fuentes', ['https://www.aepd.es/'])
    return make_page(kind='profesion', slug=slug, url=f'/ia-para-{slug}/', title=f'IA para {slug}',
                     sources=sources, body_html=body() if html is None else html, extra=base)


def test_valid_profession_and_kit():
    validate_professions([prof()], FICHAS)
    assert parse_kit(prof()) == [('alfa', 'Preparar clases'), ('beta', 'Ejercicios')]


@pytest.mark.parametrize('kw, needle', [
    (dict(profesion=''), 'profesion'),
    (dict(emoji=''), 'emoji'),
    (dict(kit='alfa = Uno'), 'kit'),
    (dict(kit='alfa = a | beta = b | gamma = c | alfa = d | beta = e'), 'kit'),
    (dict(kit='alfa = Uno | zeta = Dos'), 'zeta'),
    (dict(kit='alfa = Uno | beta'), 'kit'),
    (dict(fuentes=[]), 'fuente'),
    (dict(html=body(precautions=False)), 'Precauciones en tu profesión'),
    (dict(html=body(tasks=4, quotes=5)), 'tareas'),
    (dict(html=body(tasks=8, quotes=8)), 'tareas'),
    (dict(html=body(tasks=5, quotes=4)), 'prompts'),
    (dict(html=body(extra='<p>Lo hemos probado en clase.</p>')), 'hemos probado'),
    (dict(html=body(extra='<p>Cuesta 99 €/mes.</p>')), '99 €'),
])
def test_invalid_professions(kw, needle):
    html = kw.pop('html', None)
    with pytest.raises(ValueError) as e:
        validate_professions([prof(html=html, **kw)], FICHAS)
    assert needle in str(e.value) and 'profesiones/docentes' in str(e.value)


def test_context_and_recommended_for():
    payload = {t['id']: t for t in compare_payload(FICHAS, TOOLS, BRANDS, CATEGORIES)}
    other = prof('disenadores', profesion='diseñadores', kit='gamma = Ideas | alfa = Imágenes')
    draft = prof('periodistas', profesion='periodistas', kit='beta = Fuentes | gamma = Transcribir')
    draft.draft = True
    ctx = profession_context(prof(), payload, [prof(), other, draft])
    assert [(t['n'], para) for t, para in ctx['kit']] == [('Alfa', 'Preparar clases'), ('Beta', 'Ejercicios')]
    assert ctx['kit'][1][0]['desde'] == '5 $' and [p.slug for p in ctx['others']] == ['disenadores']
    rec = recommended_for([prof(), other, draft])
    assert rec['alfa'] == [('Diseñadores', '/ia-para-disenadores/'), ('Docentes', '/ia-para-docentes/')]
    assert rec['gamma'] == [('Diseñadores', '/ia-para-disenadores/')]


def test_prompts_js_is_dom_safe_and_small():
    import gzip
    js = (ROOT / 'static' / 'js' / 'prompts.js').read_bytes()
    assert b'innerHTML' not in js and len(gzip.compress(js)) <= 1024
    assert b'clipboard' in js and b'aria-live' in js


def test_real_professions():
    from radar.content import load_pages
    pages = load_pages(ROOT / 'content')
    profs = [p for p in pages if p.kind == 'profesion']
    validate_professions(profs, {p.slug: p for p in pages if p.kind == 'ficha' and p.indexable})
    assert profs and all(p.url == f'/ia-para-{p.slug}/' and p.word_count >= 1000 and p.indexable for p in profs)
    hub = [p for p in pages if p.url == '/ia-por-profesion/'][0]
    assert hub.word_count >= 250


@pytest.fixture(scope='module')
def site():
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    return out


def test_built_profession_and_hub(site):
    html = (site / 'ia-para-docentes' / 'index.html').read_text()
    assert 'IA por profesión' in html and 'Tu kit en 30 segundos' in html
    assert html.count('class="kit-card"') == 3 and 'Desde 0 €' in html
    assert 'class="prose prompt-page"' in html or 'prompt-page' in html
    assert re.search(r'<script src="/static/js/prompts\.js\?v=[0-9a-f]{10}" defer>', html)
    assert re.search(r'href="/ia-por-profesion/">IA por profesión</a>', html)
    hub = (site / 'ia-por-profesion' / 'index.html').read_text()
    assert 'href="/ia-para-docentes/"' in hub and 'class="prof-card"' in hub and 'noindex' not in hub
    assert (site / 'og' / 'ia-para-docentes.png').exists()


def test_fixture_build_has_no_profession_hub(tmp_path):
    from scripts.build import build
    from tests.test_build import make_root
    build(make_root(tmp_path), tmp_path / '_site')
    assert not (tmp_path / '_site' / 'ia-por-profesion').exists()
