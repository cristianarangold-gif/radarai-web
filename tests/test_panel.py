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
