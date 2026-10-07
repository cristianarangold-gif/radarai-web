import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import pytest

from radar.prompt_library import library_context, parse_prompts, validate_prompts
from tests.helpers import make_page

ROOT = Path(__file__).resolve().parent.parent
PROMPT = 'Redacta una respuesta breve y cordial a este correo de [quién escribe]. Explica [qué ha pasado] y ofrece una solución clara a [quién escribe].'
FICHAS = {t: make_page(kind='ficha', slug=t, url=f'/herramientas/{t}/', date=date(2026, 10, 6))
          for t in ('chatgpt', 'claude')}


def block(title='Responder un correo difícil', meta='categoria: escribir\nherramientas: chatgpt, claude\npara: Contestar una queja.',
          body=PROMPT):
    return f'## {title}\n{meta}\n\n{body}\n'


def test_parse_segments_and_slots():
    p = parse_prompts('Comentario.\n\n' + block(meta='categoria: escribir\nherramientas: chatgpt\npara: Contestar.\n'
                                                     'consejo: Pega el correo debajo.'))[0]
    assert (p.title, p.slug, p.cat, p.tools, p.para, p.consejo) == (
        'Responder un correo difícil', 'responder-un-correo-dificil', 'escribir', ['chatgpt'], 'Contestar.',
        'Pega el correo debajo.')
    assert p.slots == ['quién escribe', 'qué ha pasado']
    assert p.segments[0] == ('text', 'Redacta una respuesta breve y cordial a este correo de ')
    assert p.segments[1] == ('slot', 'quién escribe') and [k for k, _ in p.segments].count('slot') == 3
    validate_prompts([p], FICHAS)


@pytest.mark.parametrize('text, needle', [
    (block(meta='categoria: otra\nherramientas: chatgpt\npara: x'), 'categoría'),
    (block(meta='categoria: escribir\nherramientas: zeta\npara: x'), 'zeta'),
    (block(meta='categoria: escribir\nherramientas: chatgpt, claude, chatgpt\npara: x'), 'herramientas'),
    (block(meta='categoria: escribir\nherramientas:\npara: x'), 'herramientas'),
    (block(meta='categoria: escribir\nherramientas: chatgpt'), 'para'),
    (block(meta='categoria: escribir\nherramientas: chatgpt\npara: ' + 'p ' * 26), 'para'),
    (block(meta='categoria: escribir\nherramientas: chatgpt\npara: x\nconsejo: ' + 'p ' * 41), 'consejo'),
    (block(body='Muy corto [a].'), 'palabras'),
    (block(body=' '.join(['palabra'] * 151)), 'palabras'),
    (block(body=PROMPT + ' [b] [c] [d] [e]'), 'huecos'),
    (block(body=PROMPT + ' [sin cerrar'), 'corchetes'),
    (block(body=PROMPT + ' Lo hemos probado.'), 'hemos probado'),
    (block() + block(), 'duplicado'),
    (block(meta='categoria: escribir\nherramientas: chatgpt\npara: x\nnivel: alto'), 'nivel'),
])
def test_validation_errors(text, needle):
    with pytest.raises(ValueError) as e:
        validate_prompts(parse_prompts(text), FICHAS)
    assert needle in str(e.value) and 'prompts.md' in str(e.value)


def test_empty_file_fails():
    with pytest.raises(ValueError, match='prompts.md'):
        validate_prompts(parse_prompts('Nada'), FICHAS)


def test_context_groups_by_category_order():
    prompts = parse_prompts(block('Uno', 'categoria: estudiar\nherramientas: chatgpt\npara: x') + block()
                            + block('Dos', 'categoria: escribir\nherramientas: claude\npara: y'))
    payload = {'chatgpt': {'id': 'chatgpt', 'n': 'ChatGPT', 'u': '/herramientas/chatgpt/'},
               'claude': {'id': 'claude', 'n': 'Claude', 'u': '/herramientas/claude/'}}
    ctx = library_context(prompts, payload)
    assert [g['id'] for g in ctx['groups']] == ['escribir', 'estudiar'] and ctx['count'] == 3
    assert [p.title for p in ctx['groups'][0]['prompts']] == ['Responder un correo difícil', 'Dos']
    assert ctx['groups'][0]['label'] == 'Escribir' and ctx['groups'][0]['emoji'] == '✍️'
    assert ctx['groups'][0]['prompts'][1].tool_links == [('claude', 'Claude', '/herramientas/claude/')]


def test_library_js_is_dom_safe_and_small():
    import gzip
    js = (ROOT / 'static' / 'js' / 'library.js').read_bytes()
    assert b'innerHTML' not in js and len(gzip.compress(js)) <= 2560
    assert b'clipboard' in js and b'aria-live' in js and b'hashchange' in js


@pytest.fixture(scope='module')
def site():
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    return out


def test_built_library_page(site):
    html = (site / 'prompts' / 'index.html').read_text()
    prompts = parse_prompts((ROOT / 'data' / 'prompts.md').read_text(encoding='utf-8'))
    assert html.count('<article class="prompt-card"') == len(prompts)
    for p in prompts:
        assert f'id="{p.slug}"' in html
    slots = sum(k == 'slot' for p in prompts for k, _ in p.segments)
    assert html.count('<mark class="slot"') == slots
    assert html.count('<div class="prompt-fill" hidden>') == sum(1 for p in prompts if p.slots)
    assert 'class="library-controls" hidden' in html and 'Prompts para copiar y' in html
    assert re.search(r'<script src="/static/js/library\.js\?v=[0-9a-f]{10}" defer>', html)
    assert 'noindex' not in html


def test_real_page_words():
    from radar.content import load_pages
    page = [p for p in load_pages(ROOT / 'content') if p.url == '/prompts/'][0]
    assert page.indexable and page.word_count >= 250


def test_library_page_requires_data(tmp_path):
    from scripts.build import build
    from tests.test_build import make_root
    root = make_root(tmp_path)
    (root / 'content' / 'paginas' / 'prompts.md').write_text('titulo: P\ndescripcion: d\n\nTexto', encoding='utf-8')
    with pytest.raises(ValueError, match='prompts.md'):
        build(root, tmp_path / '_site')
