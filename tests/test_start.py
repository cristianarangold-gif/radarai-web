import copy
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from radar.start import load_start, validate_start

ROOT = Path(__file__).resolve().parent.parent
URLS = {'/a/', '/b/', '/c/', '/d/'}


def link(url, texto='Enlace'):
    return {'texto': texto, 'url': url}


def sample():
    card = {'emoji': '🌱', 'titulo': 'T', 'texto': 'X', 'enlaces': [link('/a/'), link('/b/')]}
    step = {'titulo': 'P', 'texto': 'X', 'cta': {'texto': 'Ir', 'url': '/c/'}, 'extra': [link('/d/')]}
    return {'situaciones': [copy.deepcopy(card) for _ in range(4)],
            'pasos': [copy.deepcopy(step) for _ in range(5)]}


def test_sample_is_valid():
    validate_start(sample(), URLS)


@pytest.mark.parametrize('mutate, needle', [
    (lambda d: d['situaciones'].pop(), '4 situaciones'),
    (lambda d: d['pasos'].pop(), '5 pasos'),
    (lambda d: d['situaciones'][0]['enlaces'].append(link('/zzz/')), '/zzz/'),
    (lambda d: d['pasos'][2]['cta'].update(url='/nope/'), '/nope/'),
    (lambda d: d['pasos'][1].update(titulo=' '), 'titulo'),
    (lambda d: d['situaciones'][1]['enlaces'].append(link('/a/')), 'repetida'),
    (lambda d: d['situaciones'][2].update(enlaces=[link('/a/')]), '2–3 enlaces'),
    (lambda d: d['pasos'][0].update(extra=[link('/a/'), link('/b/'), link('/c/'), link('/d/')]), '0–3'),
])
def test_invalid_data_fails(mutate, needle):
    data = sample()
    mutate(data)
    with pytest.raises(ValueError) as e:
        validate_start(data, URLS)
    assert needle in str(e.value) and 'empieza.json' in str(e.value)


def test_real_file_is_valid_against_real_site():
    from radar.content import load_pages
    from scripts.build import LISTINGS
    pages = load_pages(ROOT / 'content')
    urls = {p.url for p in pages if p.indexable} | {u for u, *_ in LISTINGS}
    validate_start(load_start(ROOT / 'data' / 'empieza.json'), urls)


def test_real_page_words():
    from radar.content import load_pages
    page = [p for p in load_pages(ROOT / 'content') if p.url == '/empieza-aqui/'][0]
    assert page.word_count >= 300 and page.indexable


def test_built_start_page():
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    html = (out / 'empieza-aqui' / 'index.html').read_text()
    assert html.count('class="start-card"') == 4 and html.count('class="start-step"') == 5
    assert '¿Cuál es tu situación?' in html and 'Tu primera semana con la IA' in html
    assert 'noindex' not in html
    main = html[html.index('<main'):html.index('</main>')]
    for href in set(re.findall(r'href="(/[^"#?]*)"', main)):
        assert (out / href.strip('/') / 'index.html').exists(), href
    data = load_start(ROOT / 'data' / 'empieza.json')
    assert main.count('class="start-extra"') == sum(1 for s in data['pasos'] if s['extra'])
