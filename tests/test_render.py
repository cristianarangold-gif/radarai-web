import json
import re
from datetime import date
from pathlib import Path

import pytest

from radar.models import Tool
from radar.render import make_env, render_page
from radar.tools import CATEGORIES
from tests.helpers import make_page, news

ROOT = Path(__file__).resolve().parent.parent
ADSENSE = 'adsbygoogle.js?client=ca-pub-7428485851163208'


@pytest.fixture(scope='module')
def env():
    return make_env(ROOT / 'templates')


def tool(tid, has_page):
    return Tool(id=tid, name=tid.title(), cat='escritura', desc='Desc', price='freemium',
                level='principiante', platform='web', lang='es', tags=['A'],
                url=f'https://{tid}.example/', has_page=has_page)


def ctx(**kw):
    base = dict(tools={}, categories=CATEGORIES, latest_news=[], listing=None)
    base.update(kw)
    return base


def test_adsense_in_article_not_in_legal(env):
    assert ADSENSE in render_page(env, news('n', 1), ctx())
    legal = make_page(url='/legal/aviso-legal/', slug='aviso-legal')
    assert ADSENSE not in render_page(env, legal, ctx())
    contacto = make_page(url='/contacto/', slug='contacto')
    assert ADSENSE not in render_page(env, contacto, ctx())


def test_noindex_meta_on_draft(env):
    html = render_page(env, news('n', 1, draft=True), ctx())
    assert '<meta name="robots" content="noindex,follow">' in html
    assert 'noindex' not in render_page(env, news('n', 1), ctx())


def test_basic_head(env):
    html = render_page(env, news('n', 1), ctx())
    assert html.lower().startswith('<!doctype html>')
    assert '<html lang="es">' in html
    assert '<link rel="canonical" href="https://radarai.es/noticias/n/">' in html
    assert '<meta name="radar:kind" content="noticia">' in html
    assert '<meta name="radar:words" content="1">' in html


def test_catalog_card_without_page_links_official_nofollow(env):
    html = render_page(env, make_page(url='/herramientas/'), ctx(tools={'foo': tool('foo', False)}, listing=[]))
    assert 'href="https://foo.example/" rel="noopener nofollow" target="_blank"' in html
    assert '/herramientas/foo/' not in html


def test_catalog_card_with_page_links_internal(env):
    html = render_page(env, make_page(url='/herramientas/'), ctx(tools={'bar': tool('bar', True)}, listing=[]))
    assert 'href="/herramientas/bar/"' in html


def test_catalog_groups_have_category_anchor(env):
    html = render_page(env, make_page(url='/herramientas/'), ctx(tools={'bar': tool('bar', True)}, listing=[]))
    assert 'id="cat-escritura"' in html and '/static/js/catalog.js' in html


def test_title_escaping(env):
    html = render_page(env, news('n', 1, title='A & B'), ctx())
    assert '<title>A &amp; B | Radar IA</title>' in html
    assert '&amp;amp;' not in html


def test_jsonld_embedded(env):
    html = render_page(env, news('n', 1), ctx())
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert any(json.loads(b).get('@type') == 'NewsArticle' for b in blocks)


def test_article_shows_author_dates_sources(env):
    page = news('n', 1, updated=date(2026, 10, 2), sources=['https://fuente.example/a'])
    html = render_page(env, page, ctx())
    assert 'href="/autor/"' in html and 'Cristian Arango' in html
    text = ' '.join(re.sub(r'<[^>]+>', ' ', html).split())
    assert '1 de octubre de 2026' in text
    assert 'Actualizado el 2 de octubre de 2026' in text
    assert 'href="https://fuente.example/a"' in html


def test_listing_renders_items(env):
    page = make_page(url='/noticias/', title='Noticias')
    html = render_page(env, page, ctx(listing=[news('uno', 1), news('dos', 2)]))
    assert 'href="/noticias/uno/"' in html and 'href="/noticias/dos/"' in html


def test_no_custom_cookie_banner(env):
    # El consentimiento lo gestiona el CMP certificado de Google (AdSense > Privacidad y mensajes).
    html = render_page(env, news('n', 1), ctx())
    assert 'cookie-banner' not in html


def test_nav_order_and_targets():
    from radar.render import NAV
    assert NAV == [('Comparativas', '/mejor-ia/'), ('Herramientas', '/herramientas/'), ('Guías', '/guias/'),
                   ('Noticias', '/noticias/'), ('Utilidades', '/herramientas-radar/')]


def test_no_google_fonts_and_fonts_preloaded(env):
    html = render_page(env, news('n', 1), ctx())
    assert 'fonts.googleapis' not in html and 'fonts.gstatic' not in html
    assert '<link rel="preload" href="/static/fonts/fraunces-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>' in html
    assert '/static/fonts/inter-latin-400-normal.woff2' in html


def test_footer_has_motto_and_brand(env):
    html = render_page(env, news('n', 1), ctx())
    assert 'La IA en tu día' in html and 'class="site-footer"' in html


def test_home_has_no_catalog(env):
    html = render_page(env, make_page(url='/'), ctx(tools={'bar': tool('bar', True)}))
    assert 'id="cat-' not in html and 'catalog.js' not in html


def test_home_title_emphasis_is_escaped(env):
    html = render_page(env, make_page(url='/', title='Tu <b> & la inteligencia artificial'), ctx())
    assert 'Tu &lt;b&gt; &amp; la <em>inteligencia artificial</em>' in html


FICHA_BODY = '<h2 id="planes">Planes y precios</h2><p>x</p><h2 id="faq">Preguntas frecuentes</h2><p>y</p>'


def ficha(**extra):
    return make_page(kind='ficha', slug='bar', url='/herramientas/bar/', title='Bar', body_html=FICHA_BODY,
                     word_count=1100, date=date(2026, 10, 1), extra=dict({'web': 'https://bar.example/'}, **extra))


def test_ficha_summary_verdict_toc(env):
    html = render_page(env, ficha(precio_desde='0 €', plan_pago='8 €/mes', ideal_para='Uso general',
                                  plataforma='Web', veredicto='Muy útil.'),
                       ctx(tools={'bar': tool('bar', True)}))
    assert 'class="summary"' in html and 'Precio desde' in html and 'Plan de pago' in html
    assert 'class="verdict"' in html and 'Muy útil.' in html
    toc_html = html[html.index('class="toc"'):]
    assert 'href="#planes"' in toc_html and 'href="#faq"' in toc_html
    assert '5 min de lectura' in html
    assert 'Visitar Bar' in html and 'href="https://bar.example/" rel="noopener nofollow" target="_blank"' in html
    assert 'Ficha · Escritura' in html and '/static/js/toc.js' in html


def test_ficha_hides_empty_summary_boxes(env):
    html = render_page(env, ficha(precio_desde='0 €'), ctx(tools={'bar': tool('bar', True)}))
    assert 'Precio desde' in html and 'Plan de pago' not in html and 'class="verdict"' not in html


def test_news_related_excludes_self(env):
    items = [news(f'n{i}', 10 - i) for i in range(5)]
    html = render_page(env, items[1], ctx(news=items))
    rel = html[html.index('class="related"'):]
    assert 'href="/noticias/n0/"' in rel and 'href="/noticias/n3/"' in rel
    assert 'href="/noticias/n1/"' not in rel and 'href="/noticias/n4/"' not in rel


def test_article_has_cover_and_two_columns(env):
    html = render_page(env, make_page(kind='guia', url='/guias/g/', body_html=FICHA_BODY), ctx())
    assert 'class="article-grid"' in html and '<svg class="cover"' in html and 'class="toc"' in html


def test_card_covers_are_decorative(env):
    page = make_page(url='/noticias/', title='Noticias')
    html = render_page(env, page, ctx(listing=[news('uno', 1)]))
    svg = html[html.index('<svg class="cover"'):]
    svg = svg[:svg.index('>')]
    assert 'aria-hidden="true"' in svg and 'role="img"' not in svg


def test_assets_are_versioned_by_content(env):
    import hashlib
    html = render_page(env, news('n', 1), ctx())
    css = (ROOT / 'static' / 'css' / 'radar.css').read_bytes()
    v = hashlib.sha256(css).hexdigest()[:10]
    assert f'href="/static/css/radar.css?v={v}"' in html
    assert re.search(r'src="/static/js/site\.js\?v=[0-9a-f]{10}"', html)
    assert re.search(r'src="/static/js/toc\.js\?v=[0-9a-f]{10}"', html)


def test_search_dialog_in_every_page(env):
    html = render_page(env, news('n', 1), ctx(search_index_url='/search-index.json?v=abc'))
    assert 'id="search-dialog"' in html and 'role="dialog"' in html and 'aria-modal="true"' in html
    assert 'data-search-index="/search-index.json?v=abc"' in html
    assert re.search(r'src="/static/js/search\.js\?v=[0-9a-f]{10}"', html)


def test_search_js_is_dom_safe_and_small():
    js = (ROOT / 'static' / 'js' / 'search.js').read_text()
    assert 'innerHTML' not in js
    for needle in ('textContent', 'aria-activedescendant', 'No se ha podido cargar el buscador',
                   'ChatGPT', 'imágenes', 'Ver todos'):
        assert needle in js, needle
    import gzip
    assert len(gzip.compress(js.encode('utf-8'))) <= 8000  # tamaño de descarga, como el índice


def test_search_js_falls_back_to_partial_matches():
    js = (ROOT / 'static' / 'js' / 'search.js').read_text()
    assert 'Sin coincidencias con todas las palabras' in js


def test_search_js_review_fixes():
    js = (ROOT / 'static' / 'js' / 'search.js').read_text()
    # Enter construye la URL en el momento, no con el href de la última carga.
    assert "location.href = '/buscar/?q=' + encodeURIComponent(input.value)" in js
    # El foco que se escapa del panel vuelve dentro.
    assert '!dlg.contains(document.activeElement)' in js
    # Al pulsar un filtro, el foco vuelve al filtro activo.
    assert "filters.querySelector('[aria-pressed=\"true\"]')" in js
    # Palabras vacías fuera de la búsqueda cuando hay otras.
    assert "'para'" in js and 'STOP' in js


def test_assistant_json_escapes_script_close(env):
    page = make_page(url='/que-ia-necesito/', slug='que-ia-necesito', title='¿Qué IA necesito?')
    payload = {'tareas': {}, 'reglas': {}, 'auto': {}, 'tools': {'x': {'n': 'a</script><b>'}}}
    html = render_page(env, page, ctx(assistant_payload=payload))
    block = html[html.index('id="asistente-datos">'):]
    assert '</script><b>' not in block.split('</script>')[0] and '<\\/script>' in html


def test_real_assistant_page_has_enough_words():
    from radar.content import load_pages
    page = [p for p in load_pages(ROOT / 'content') if p.url == '/que-ia-necesito/'][0]
    assert page.word_count >= 400 and page.indexable


def test_assistant_js_is_dom_safe_and_small():
    import gzip
    js = (ROOT / 'static' / 'js' / 'assistant.js').read_text()
    assert js.strip(), 'assistant.js vacío'
    assert 'innerHTML' not in js
    for needle in ('textContent', 'replaceState', 'si_equipo', 'si_avanzado', 'Por qué encaja contigo',
                   'También encajan', 'Otras opciones del catálogo', 'noopener nofollow'):
        assert needle in js, needle
    assert len(gzip.compress(js.encode('utf-8'))) <= 6000


def test_home_primary_button_is_assistant(env):
    html = render_page(env, make_page(url='/'), ctx(assistant_payload={'tareas': {}}))
    assert '<a class="btn" href="/que-ia-necesito/">¿Qué IA necesito? →</a>' in html
    assert 'href="/mejor-ia/">Ver comparativas' in html


def test_assistant_cta_only_in_comparativas_and_guides(env):
    cta = 'Hacer el test →'
    for kind, url in (('comparativa', '/mejor-ia-x/'), ('guia', '/guias/g/')):
        html = render_page(env, make_page(kind=kind, url=url), ctx(assistant_payload={'tareas': {}}))
        assert cta in html and 'href="/que-ia-necesito/"' in html, kind
    assert cta not in render_page(env, news('n', 1), ctx())
    ficha = make_page(kind='ficha', slug='bar', url='/herramientas/bar/', date=date(2026, 10, 1))
    assert cta not in render_page(env, ficha, ctx(tools={'bar': tool('bar', True)}))


def test_no_assistant_links_without_assistant(env):
    assert '/que-ia-necesito/' not in render_page(env, make_page(url='/'), ctx())
    assert '/que-ia-necesito/' not in render_page(env, make_page(kind='guia', url='/guias/g/'), ctx())
