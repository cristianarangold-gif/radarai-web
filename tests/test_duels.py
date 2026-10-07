import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import pytest

from radar.compare import compare_payload
from radar.covers import cover_for, cover_svg
from radar.duels import duel_context, duel_tools, validate_duels
from radar.models import Brand, Tool
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
BRANDS = {'alfa': Brand('alfa', 'Alfa', '#10a37f', None, 'A'), 'beta': Brand('beta', 'Beta', '#d97757', None, 'B')}


def duel(slug='alfa-vs-beta', **extra):
    base = dict(herramientas='alfa, beta', respuesta='Alfa para todo y Beta para escribir.',
                elige_1='uno | dos', elige_2='tres | cuatro | cinco')
    base.update(extra)
    sources = base.pop('fuentes', ['https://alfa.example/precios'])
    return make_page(kind='duelo', slug=slug, url=f'/{slug}/', title='Alfa vs Beta', sources=sources,
                     body_html='<p>texto</p>', extra=base)


def test_valid_duel_and_tools():
    validate_duels([duel()], FICHAS)
    assert duel_tools(duel()) == ['alfa', 'beta']


@pytest.mark.parametrize('kw, needle', [
    (dict(herramientas='alfa'), '2 herramientas'),
    (dict(herramientas='alfa, beta, gamma'), '2 herramientas'),
    (dict(herramientas='alfa, alfa'), 'distintas'),
    (dict(herramientas='alfa, zeta'), 'zeta'),
    (dict(respuesta=''), 'respuesta'),
    (dict(respuesta=' '.join(['p'] * 61)), '60 palabras'),
    (dict(elige_1='solo una'), 'elige_1'),
    (dict(elige_2='a | b | c | d | e'), 'elige_2'),
    (dict(fuentes=[]), 'fuente'),
])
def test_invalid_duels(kw, needle):
    with pytest.raises(ValueError) as e:
        validate_duels([duel(**kw)], FICHAS)
    assert needle in str(e.value) and 'cara-a-cara/alfa-vs-beta' in str(e.value)


def test_forbidden_claims_and_reversed_pair():
    bad = duel()
    bad.body_html = '<p>En nuestras pruebas fue más rápido.</p>'
    with pytest.raises(ValueError, match='nuestras pruebas'):
        validate_duels([bad], FICHAS)
    with pytest.raises(ValueError, match='repetido'):
        validate_duels([duel(), duel('beta-vs-alfa', herramientas='beta, alfa')], FICHAS)


def test_context_takes_table_from_fichas():
    payload = {t['id']: t for t in compare_payload(FICHAS, TOOLS, BRANDS, CATEGORIES)}
    others = [duel('alfa-vs-gamma', herramientas='alfa, gamma'), duel('beta-vs-gamma', herramientas='beta, gamma')]
    ctx = duel_context(duel(), payload, FICHAS, [duel()] + others)
    assert ctx['a']['n'] == 'Alfa' and ctx['b']['n'] == 'Beta'
    assert ctx['elige'][0][1] == ['uno', 'dos'] and len(ctx['elige'][1][1]) == 3
    rows = dict((label, (va, vb)) for label, va, vb in ctx['rows'])
    assert rows['Precio desde'] == ('0 €', '5 $') and rows['Comprobado'] == ('6 de octubre de 2026',) * 2
    assert [p.slug for p in ctx['related']] == ['alfa-vs-gamma', 'beta-vs-gamma']


def test_cover_has_both_brands_and_falls_back_to_monogram(tmp_path):
    spec = cover_for(duel(), BRANDS, TOOLS)
    assert spec.brand.name == 'Alfa' and spec.brand2.name == 'Beta' and spec.label == 'Cara a cara'
    svg = str(cover_svg(spec, tmp_path))
    assert '#10a37f' in svg and '#d97757' in svg and '>VS<' in svg
    spec2 = cover_for(duel(herramientas='alfa, gamma'), BRANDS, TOOLS)
    assert spec2.brand2.icon is None and spec2.brand2.monograma == 'G'
    assert '>G<' in str(cover_svg(spec2, tmp_path))


def test_real_duels(tmp_path):
    from radar.content import load_pages
    pages = load_pages(ROOT / 'content')
    duels = [p for p in pages if p.kind == 'duelo']
    fichas = {p.slug: p for p in pages if p.kind == 'ficha' and p.indexable}
    validate_duels(duels, fichas)
    assert duels and all(p.url == f'/{p.slug}/' and p.word_count >= 1000 and p.indexable for p in duels)
    assert {p.slug for p in duels} == {'chatgpt-vs-claude', 'chatgpt-vs-gemini', 'chatgpt-vs-copilot',
                                       'perplexity-vs-chatgpt', 'cursor-vs-github-copilot', 'notebooklm-vs-chatgpt'}


@pytest.fixture(scope='module')
def site():
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    return out


def test_built_duel_page(site):
    html = (site / 'chatgpt-vs-claude' / 'index.html').read_text()
    assert 'Cara a cara' in html and 'Respuesta rápida:' in html
    assert 'Elige ChatGPT si…' in html and 'Elige Claude si…' in html
    assert '<caption' in html and 'scope="row">Precio desde' in html and '23 €' not in html.split('<caption')[0]
    assert 'href="/comparador/?h=chatgpt,claude"' in html
    assert 'href="/herramientas/chatgpt/"' in html and 'href="/herramientas/claude/"' in html
    assert '"@type": "Article"' in html or '"@type":"Article"' in html
    assert re.search(r'href="/mejor-ia/">Comparativas</a>', html)
    assert (site / 'og' / 'chatgpt-vs-claude.png').exists()
