import json
from datetime import date

from radar.models import Brand, Tool
from radar.search import build_index, index_json
from tests.helpers import make_page, news


def tool(tid, name, cat, has_page, desc='Descripción', tags=()):
    return Tool(id=tid, name=name, cat=cat, desc=desc, price='', level='', platform='', lang='',
                tags=list(tags), url='https://x/', has_page=has_page)


TOOLS = {'chatgpt': tool('chatgpt', 'ChatGPT', 'ia-general', True),
         'claude': tool('claude', 'Claude', 'ia-general', True),
         'runway': tool('runway', 'Runway', 'video', False, 'Vídeo con IA', ['Edición'])}
BRANDS = {'chatgpt': Brand('chatgpt', 'ChatGPT', '#10a37f', None, 'C'),
          'openai': Brand('openai', 'OpenAI', '#10a37f', None, 'O')}


def pages():
    return [
        make_page(url='/', title='Inicio'),
        make_page(url='/sobre/', slug='sobre', title='Sobre Radar IA'),
        make_page(kind='ficha', slug='chatgpt', url='/herramientas/chatgpt/', title='ChatGPT en España',
                  body_html='<h2 id="a">Planes y precios</h2>', date=date(2026, 10, 6),
                  extra={'ideal_para': 'Uso general', 'precio_desde': '0 €'}),
        make_page(kind='ficha', slug='claude', url='/herramientas/claude/', title='Claude de Anthropic',
                  date=date(2026, 10, 6)),
        news('n1', 6, title='OpenAI lanza algo', extra={'empresa': 'openai', 'herramientas': 'chatgpt'}),
        news('borr', 5, title='Borrador', draft=True),
        make_page(kind='comparativa', url='/mejor-ia-x/', title='La mejor IA para x', description='d' * 300),
    ]


def index():
    idx = build_index(pages(), TOOLS, BRANDS)
    return idx, {e['u']: e for e in idx}


def test_index_excludes_home_and_drafts():
    _, by_url = index()
    assert '/' not in by_url and '/noticias/borr/' not in by_url
    assert by_url['/sobre/']['k'] == 'Página'


def test_ficha_entry_has_price_keywords_and_brand_icon():
    _, by_url = index()
    e = by_url['/herramientas/chatgpt/']
    assert e['k'] == 'Ficha' and e['p'] == '0 €'
    assert 'Planes y precios' in e['x'] and 'Uso general' in e['x'] and 'IA general' in e['x']
    assert e['c'] == '#10a37f' and e['m'] == 'C'


def test_news_entry_has_short_date_company_and_tools():
    _, by_url = index()
    e = by_url['/noticias/n1/']
    assert e['f'] == '6 oct 2026' and 'OpenAI' in e['x'] and 'ChatGPT' in e['x'] and e['m'] == 'O'


def test_catalog_tool_without_page_links_to_category_and_no_duplicates():
    idx, by_url = index()
    e = by_url['/herramientas/#cat-video']
    assert e['t'] == 'Runway' and e['k'] == 'Catálogo' and e['d'] == 'Vídeo con IA'
    assert 'Edición' in e['x'] and 'Vídeo' in e['x'] and e['m'] == 'R'
    assert sum(x['t'] == 'Claude' for x in idx) == 0  # su ficha entra con su propio título
    assert sum(x['k'] == 'Catálogo' for x in idx) == 1


def test_symbol_icons_by_kind():
    _, by_url = index()
    assert (by_url['/mejor-ia-x/']['c'], by_url['/mejor-ia-x/']['m']) == ('#e4572e', '★')
    assert by_url['/sobre/']['m'] == 'P'


def test_description_truncated_to_160_with_ellipsis():
    _, by_url = index()
    d = by_url['/mejor-ia-x/']['d']
    assert len(d) <= 160 and d.endswith('…')


def test_index_json_is_compact_and_unicode():
    idx, _ = index()
    s = index_json(idx)
    assert '": ' not in s and 'Página' in s and json.loads(s) == idx


def test_glossary_terms_in_index():
    from radar.glossary import parse_glossary
    terms = parse_glossary('## Modelo de lenguaje\ntema: modelos\nalias: LLM\n\n' + 'Programa que predice. ' * 10)
    idx = build_index(pages(), TOOLS, BRANDS, terms)
    e = [x for x in idx if x['k'] == 'Glosario'][0]
    assert e['t'] == 'Modelo de lenguaje' and e['u'] == '/glosario/#modelo-de-lenguaje'
    assert 'LLM' in e['x'] and 'Modelos y tecnología' in e['x'] and e['d'].startswith('Programa que predice.')
    assert e['m'] == 'G' and len(e['d']) <= 160
