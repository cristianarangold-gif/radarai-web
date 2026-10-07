import copy
import json
from pathlib import Path

import pytest

from radar.assistant import (BUDGETS, TASKS, auto_alternatives, load_assistant, pick_rule, resolve_payload,
                             validate_assistant)
from radar.models import Brand, Tool
from tests.helpers import make_page

ROOT = Path(__file__).resolve().parent.parent


def tool(tid, cat='ia-general', price='freemium', level='principiante', has_page=False, name=None):
    return Tool(id=tid, name=name or tid.title(), cat=cat, desc=f'Desc {tid}', price=price, level=level,
                platform='', lang='', tags=[], url=f'https://{tid}.example/', has_page=has_page)


def ficha(tid, desde='0 €'):
    return make_page(kind='ficha', slug=tid, url=f'/herramientas/{tid}/', title=tid,
                     extra={'precio_desde': desde, 'ideal_para': 'Uso general', 'web': f'https://{tid}.example/'})


def base_data():
    tareas = {t: {'etiqueta': t, 'emoji': '•', 'comparativa': '/c/', 'guia': '/g/', 'categorias': ['ia-general']}
              for t in TASKS}
    rule = {'principal': 'chatgpt', 'porque': ['Uno.', 'Dos.'], 'alternativas': [{'id': 'claude', 'motivo': 'M'}]}
    return {'tareas': tareas, 'reglas': {f'{t}/{b}': copy.deepcopy(rule) for t in TASKS for b in BUDGETS}}


TOOLS = {'chatgpt': tool('chatgpt', has_page=True, name='ChatGPT'), 'claude': tool('claude', has_page=True),
         'midjourney': tool('midjourney', cat='imagenes', price='pago', has_page=True),
         'zeta': tool('zeta'), 'alfa': tool('alfa', price='pago'), 'beta': tool('beta', level='avanzado'),
         'gamma': tool('gamma')}
FICHAS = {'chatgpt': ficha('chatgpt'), 'claude': ficha('claude', '0 $'), 'midjourney': ficha('midjourney', '10 $/mes')}
URLS = {'/c/', '/g/'}


def test_base_data_is_valid():
    validate_assistant(base_data(), TOOLS, FICHAS, URLS)


@pytest.mark.parametrize('mutate, message', [
    (lambda d: d['reglas'].pop('video/poco'), 'falta la regla video/poco'),
    (lambda d: d['reglas']['video/poco'].update(principal='nadie'), 'herramienta desconocida «nadie»'),
    (lambda d: d['reglas']['video/poco'].update(principal='zeta'), '«zeta» no tiene ficha'),
    (lambda d: d['reglas']['video/poco']['alternativas'].append({'id': 'nadie', 'motivo': 'x'}), 'herramienta desconocida «nadie»'),
    (lambda d: d['tareas']['video'].update(comparativa='/no/'), 'URL inexistente /no/'),
    (lambda d: d['reglas']['video/poco'].update(porque=['Solo una.']), 'entre 2 y 3 frases'),
    (lambda d: d['reglas']['video/poco'].update(porque=['a', 'b', 'c', 'd']), 'entre 2 y 3 frases'),
    (lambda d: d['reglas']['video/poco'].update(porque=['Lo hemos probado.', 'b']), 'hemos probado'),
    (lambda d: d['reglas']['video/gratis'].update(principal='midjourney'), 'no es gratis'),
    (lambda d: d['reglas']['video/gratis'].update(si_equipo={'principal': 'midjourney', 'porque': ['a', 'b']}), 'no es gratis'),
])
def test_validation_errors(mutate, message):
    data = base_data()
    mutate(data)
    with pytest.raises(ValueError, match=message):
        validate_assistant(data, TOOLS, FICHAS, URLS)


def test_pick_rule_team_wins_over_advanced():
    data = base_data()
    data['reglas']['programar/poco']['si_avanzado'] = {'principal': 'claude', 'porque': ['a', 'b']}
    data['reglas']['programar/poco']['si_equipo'] = {'principal': 'midjourney', 'porque': ['a', 'b']}
    assert pick_rule(data, 'programar', 'poco', 'avanzado', 'equipo')['principal'] == 'midjourney'
    assert pick_rule(data, 'programar', 'poco', 'avanzado', 'mi')['principal'] == 'claude'
    assert pick_rule(data, 'programar', 'poco', 'empiezo', 'mi')['principal'] == 'chatgpt'


def test_auto_alternatives_filters_and_order():
    data = base_data()
    # gratis excluye «alfa» (pago); empiezo excluye «beta» (avanzado); excluye las ya recomendadas
    assert auto_alternatives(data, TOOLS, 'escribir', 'gratis', 'empiezo', {'chatgpt', 'claude'}) == ['gamma', 'zeta']
    assert 'alfa' in auto_alternatives(data, TOOLS, 'escribir', 'sin-limite', 'avanzado', {'chatgpt', 'claude'}, n=5)
    assert 'beta' in auto_alternatives(data, TOOLS, 'escribir', 'sin-limite', 'avanzado', {'chatgpt', 'claude'}, n=5)
    # primero las que tienen ficha
    assert auto_alternatives(data, TOOLS, 'escribir', 'gratis', 'empiezo', {'chatgpt'})[0] == 'claude'


def test_resolve_payload_links_catalog_tools_to_category():
    data = base_data()
    data['reglas']['video/poco']['alternativas'] = [{'id': 'zeta', 'motivo': 'x'}]
    brands = {'chatgpt': Brand('chatgpt', 'ChatGPT', '#10a37f', None, 'C')}
    p = resolve_payload(data, TOOLS, brands, FICHAS)
    assert p['tools']['zeta']['u'] == '/herramientas/#cat-ia-general'
    assert p['tools']['chatgpt'] == {'n': 'ChatGPT', 'u': '/herramientas/chatgpt/', 'c': '#10a37f', 'm': 'C',
                                     'p': '0 €', 'i': 'Uso general', 'w': 'https://chatgpt.example/',
                                     'nivel': 'principiante'}
    assert len(p['reglas']) == 27 and 'escribir/gratis/empiezo' in p['auto']
    json.dumps(p)


def test_real_assistant_file_is_valid():
    from radar.content import load_pages
    from radar.tools import load_tools
    pages = load_pages(ROOT / 'content')
    tools = load_tools(ROOT / 'data' / 'tools.json', ROOT / 'content')
    fichas = {p.slug: p for p in pages if p.kind == 'ficha'}
    data = load_assistant(ROOT / 'data' / 'asistente.json')
    validate_assistant(data, tools, fichas, {p.url for p in pages})
    assert len(data['reglas']) == 27


def test_payload_uses_brand_name_when_available():
    data = base_data()
    brands = {'chatgpt': Brand('chatgpt', 'ChatGPT Plus', '#10a37f', None, 'C')}
    assert resolve_payload(data, TOOLS, brands, FICHAS)['tools']['chatgpt']['n'] == 'ChatGPT Plus'
    assert resolve_payload(data, TOOLS, brands, FICHAS)['tools']['claude']['n'] == 'Claude'


def test_team_override_not_allowed_on_small_budget():
    data = base_data()
    data['reglas']['video/poco']['si_equipo'] = {'principal': 'claude', 'porque': ['a', 'b']}
    with pytest.raises(ValueError, match='video/poco: los planes de equipo superan'):
        validate_assistant(data, TOOLS, FICHAS, URLS)


def test_small_budget_skips_paid_catalog_tools_without_page():
    data = base_data()
    ids = auto_alternatives(data, TOOLS, 'escribir', 'poco', 'avanzado', {'chatgpt', 'claude'}, n=5)
    assert 'alfa' not in ids  # «alfa» es de pago y no tiene ficha


def test_real_rules_texts_are_accurate():
    text = (ROOT / 'data' / 'asistente.json').read_text()
    assert 'Para corregir y traducir con privacidad (gratis' not in text
    assert 'segura para uso comercial, según Adobe' not in text


def test_assistant_page_says_no_own_tests():
    text = (ROOT / 'content' / 'paginas' / 'que-ia-necesito.md').read_text()
    assert 'pruebas propias' in text
