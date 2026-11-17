import json
from pathlib import Path

import pytest

from radar.panel import panel_prices
from radar.price_history import Snapshot

ROOT = Path(__file__).resolve().parent.parent


def test_panel_prices_keeps_only_euro_plans():
    snap = Snapshot('2026-11-16', '2026-11-16.json', {'chatgpt': {'fuente': 'x', 'planes': {
        'Gratis': '0 €', 'Plus': '23 €/mes', 'Pro': 'desde 103 €/mes', 'Max': '200 $/mes', 'Anual': '180 €/año'}}})
    data = panel_prices(snap, {'chatgpt': 'ChatGPT'})
    planes = data['herramientas']['chatgpt']['planes']
    assert data['fecha'] == '2026-11-16' and data['herramientas']['chatgpt']['nombre'] == 'ChatGPT'
    assert 'Max' not in planes
    assert planes['Plus'] == {'texto': '23 €/mes', 'euros': 23.0, 'ciclo': 'mensual', 'desde': False}
    assert planes['Pro']['desde'] is True and planes['Pro']['euros'] == 103.0
    assert planes['Anual']['ciclo'] == 'anual' and planes['Gratis']['euros'] == 0.0


def test_panel_prices_skips_tools_without_euro_plans():
    snap = Snapshot('2026-11-16', 'x.json', {'cursor': {'planes': {'Pro': '20 $/mes'}}})
    assert panel_prices(snap, {'cursor': 'Cursor'})['herramientas'] == {}


@pytest.fixture(scope='module')
def site():
    import subprocess
    import sys
    import tempfile
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    return out


def test_site_has_panel_page_and_prices(site):
    html = (site / 'mi-panel' / 'index.html').read_text(encoding='utf-8')
    assert 'id="panel"' in html and 'js/panel.js' in html and 'noindex' not in html
    assert '/que-ia-necesito/' in html
    data = json.loads((site / 'mi-panel' / 'precios.json').read_text(encoding='utf-8'))
    latest = sorted((ROOT / 'data' / 'tomas-precios').glob('*.json'))[-1].stem
    assert data['fecha'] == latest and 'chatgpt' in data['herramientas']


def test_save_prompt_button_is_loaded(site):
    util = (site / 'herramientas-radar' / 'generador-de-prompts' / 'index.html').read_text(encoding='utf-8')
    lib = (site / 'prompts' / 'index.html').read_text(encoding='utf-8')
    assert 'js/guardar-prompt.js' in util and 'js/guardar-prompt.js' in lib


def test_word_counter_has_no_save_button(site):
    html = (site / 'herramientas-radar' / 'contador-de-palabras' / 'index.html').read_text(encoding='utf-8')
    assert 'js/guardar-prompt.js' not in html


def test_panel_has_prompts_and_notes_sections(site):
    html = (site / 'mi-panel' / 'index.html').read_text(encoding='utf-8')
    for id_ in ('lista-prompts', 'form-nota', 'nota-proyecto', 'lista-notas', 'filtro-proyecto', 'form-proyecto'):
        assert f'id="{id_}"' in html
    assert 'Muy pronto' not in html


def _main(html):
    return html.split('<footer', 1)[0]


def test_panel_is_linked_from_related_pages(site):
    for rel in ('herramientas-radar/generador-de-prompts', 'herramientas-radar/mejorador-de-prompts', 'prompts',
                'historial-de-precios'):
        assert 'href="/mi-panel/"' in _main((site / rel / 'index.html').read_text(encoding='utf-8')), rel


def test_footer_links_to_panel(site):
    html = (site / 'index.html').read_text(encoding='utf-8')
    assert 'href="/mi-panel/"' in html.split('<footer', 1)[1]


def test_privacy_and_cookies_explain_panel(site):
    privacy = _main((site / 'legal' / 'politica-privacidad' / 'index.html').read_text(encoding='utf-8'))
    assert 'Mi panel' in privacy and 'navegador' in privacy and 'href="/mi-panel/"' in privacy
    cookies = _main((site / 'legal' / 'politica-cookies' / 'index.html').read_text(encoding='utf-8'))
    assert 'Mi panel' in cookies


def test_header_menu_links_to_panel(site):
    import re
    for rel in ('index.html', 'mi-panel/index.html'):
        nav = re.search(r'<nav id="menu-principal".*?</nav>', (site / rel).read_text(encoding='utf-8'), re.S).group(0)
        assert 'href="/mi-panel/"' in nav, rel
    nav = re.search(r'<nav id="menu-principal".*?</nav>', (site / 'mi-panel' / 'index.html').read_text(encoding='utf-8'), re.S).group(0)
    assert 'href="/mi-panel/" aria-current="page"' in nav



def test_every_news_has_two_internal_links_besides_the_listing(site):
    import re
    news_dir = site / 'noticias'
    slugs = [d.name for d in news_dir.iterdir() if (d / 'index.html').exists()
             and 'noindex' not in (d / 'index.html').read_text(encoding='utf-8')]
    incoming = {s: 0 for s in slugs}
    sources = [news_dir / s / 'index.html' for s in slugs] + list((site / 'herramientas').glob('*/index.html'))
    for f in sources:
        html = f.read_text(encoding='utf-8')
        for t in set(re.findall(r'href="/noticias/([^/"]+)/"', html)):
            if t in incoming and f.parent.name != t:
                incoming[t] += 1
    # La noticia más antigua solo tiene «siguiente»; el resto, anterior y siguiente como mínimo.
    sin_anterior = [s for s in slugs if 'rel="prev"' not in (news_dir / s / 'index.html').read_text(encoding='utf-8')]
    assert len(sin_anterior) == 1
    oldest = sin_anterior[0]
    low = {k: v for k, v in incoming.items() if v < (1 if k == oldest else 2)}
    assert slugs and not low, low


def test_ficha_lists_its_news(site):
    html = (site / 'herramientas' / 'chatgpt' / 'index.html').read_text(encoding='utf-8')
    assert 'Últimas noticias de ChatGPT' in html


def test_indexable_pages_allow_large_image_previews(site):
    html = (site / 'noticias' / 'genie-4-deepmind' / 'index.html').read_text(encoding='utf-8')
    assert '<meta name="robots" content="max-image-preview:large">' in html
    assert 'max-image-preview' not in (site / 'buscar' / 'index.html').read_text(encoding='utf-8')
