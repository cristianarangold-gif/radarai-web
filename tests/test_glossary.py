import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from radar.glossary import (defined_term_set, glossary_context, letter_of, parse_glossary, slugify, sort_key,
                            validate_glossary)

ROOT = Path(__file__).resolve().parent.parent
DEF = ' '.join(['palabra'] * 30)
URLS = {'/guias/x/', '/mejor-ia/'}


def block(term, meta='tema: basicos', body=DEF):
    return f'## {term}\n{meta}\n\n{body}\n'


def test_parse_meta_body_and_slug():
    text = ('Comentario inicial que se ignora.\n\n'
            + block('Modelo de lenguaje', 'tema: modelos\nalias: LLM, modelo grande\nrelacionados: token\n'
                    'ver: /guias/x/, /mejor-ia/\nejemplo: Un ejemplo.')
            + block('Token', 'tema: modelos'))
    terms = parse_glossary(text)
    m = terms[0]
    assert (m.term, m.slug, m.tema) == ('Modelo de lenguaje', 'modelo-de-lenguaje', 'modelos')
    assert m.alias == ['LLM', 'modelo grande'] and m.relacionados == ['token']
    assert m.ver == ['/guias/x/', '/mejor-ia/'] and m.ejemplo == 'Un ejemplo.'
    assert m.html.startswith('<p>palabra') and 'Comentario' not in m.html
    validate_glossary(terms, URLS)


def test_slug_and_spanish_order():
    assert slugify('Alucinación') == 'alucinacion'
    assert slugify('IA generativa (GenAI)') == 'ia-generativa-genai'
    words = ['Ñandú', 'Ética', 'Nube', 'Árbol', 'Embedding', 'Ozono', 'agente']
    assert sorted(words, key=sort_key) == ['agente', 'Árbol', 'Embedding', 'Ética', 'Nube', 'Ñandú', 'Ozono']
    assert [letter_of(w) for w in ('Árbol', 'Ñandú', 'ética', 'token')] == ['A', 'Ñ', 'E', 'T']


@pytest.mark.parametrize('text, needle', [
    (block('A', 'tema: otro'), 'tema'),
    (block('A', 'tema: basicos\nrelacionados: nada'), 'nada'),
    (block('Token', 'tema: basicos\nrelacionados: token'), 'sí mismo'),
    (block('A', 'tema: basicos\nver: /no-existe/'), '/no-existe/'),
    (block('A', 'tema: basicos\nver: /guias/x/, /mejor-ia/, /guias/x/'), 'ver'),
    (block('A', body='corta'), 'palabras'),
    (block('A', body=' '.join(['p'] * 170)), 'palabras'),
    (block('A', body=DEF + ' hemos probado'), 'hemos probado'),
    (block('A') + block('A'), 'duplicado'),
    (block('A', 'tema: basicos\ncolor: rojo'), 'color'),
    (block('A', 'relacionados: b'), 'tema'),
])
def test_validation_errors(text, needle):
    with pytest.raises(ValueError) as e:
        validate_glossary(parse_glossary(text), URLS)
    assert needle in str(e.value) and 'glosario.md' in str(e.value)


def test_context_letters_and_related():
    terms = parse_glossary(block('Token', 'tema: modelos\nrelacionados: agente\nver: /guias/x/')
                           + block('Agente', 'tema: uso'))
    ctx = glossary_context(terms, {'/guias/x/': 'Guía X'})
    letters = {l['letter']: l for l in ctx['letters']}
    assert list(letters)[:3] == ['A', 'B', 'C'] and 'Ñ' in letters and len(letters) == 27
    assert [t.slug for t in letters['A']['terms']] == ['agente'] and letters['B']['terms'] == []
    tok = letters['T']['terms'][0]
    assert tok.related == [('agente', 'Agente')] and tok.see == [('/guias/x/', 'Guía X')]


def test_defined_term_set():
    terms = parse_glossary(block('Token', 'tema: modelos', 'Un <b>trozo</b> de texto ' + DEF))
    data = defined_term_set(terms)
    assert data['@type'] == 'DefinedTermSet' and data['url'] == 'https://radarai.es/glosario/'
    t = data['hasDefinedTerm'][0]
    assert t == {'@type': 'DefinedTerm', 'name': 'Token', 'url': 'https://radarai.es/glosario/#token',
                 'description': t['description']}
    assert t['description'].startswith('Un trozo de texto') and '<' not in t['description']


@pytest.fixture(scope='module')
def site():
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    return out


def test_built_glossary_page(site):
    html = (site / 'glosario' / 'index.html').read_text()
    terms = parse_glossary((ROOT / 'data' / 'glosario.md').read_text(encoding='utf-8'))
    for t in terms:
        assert f'id="{t.slug}"' in html
    assert html.count('<div class="term"') == len(terms)
    assert 'class="glossary-controls" hidden' in html
    assert re.search(r'<span class="glossary-letter"[^>]*>Ñ</span>|<a class="glossary-letter" href="#letra-ñ">', html)
    blocks = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
    sets = [b for b in blocks if b.get('@type') == 'DefinedTermSet']
    assert len(sets) == 1 and len(sets[0]['hasDefinedTerm']) == len(terms)
    assert 'noindex' not in html


def test_glossary_page_requires_data(tmp_path):
    from scripts.build import build
    from tests.test_build import make_root
    root = make_root(tmp_path)
    (root / 'content' / 'paginas' / 'glosario.md').write_text('titulo: G\ndescripcion: d\n\nTexto', encoding='utf-8')
    with pytest.raises(ValueError, match='glosario.md'):
        build(root, tmp_path / '_site')


def test_real_glossary_is_valid_and_complete():
    from radar.content import load_pages
    from scripts.build import LISTINGS
    pages = load_pages(ROOT / 'content')
    urls = {p.url for p in pages if p.indexable} | {u for u, *_ in LISTINGS}
    terms = parse_glossary((ROOT / 'data' / 'glosario.md').read_text(encoding='utf-8'))
    validate_glossary(terms, urls)
    assert len(terms) >= 45
    assert {t.tema for t in terms} == {'basicos', 'modelos', 'uso', 'precios', 'etica'}
    page = [p for p in pages if p.url == '/glosario/'][0]
    assert page.indexable and page.word_count >= 300
