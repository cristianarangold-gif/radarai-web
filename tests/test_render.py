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
    html = render_page(env, make_page(url='/'), ctx(tools={'foo': tool('foo', False)}))
    assert 'href="https://foo.example/" rel="noopener nofollow" target="_blank"' in html
    assert '/herramientas/foo/' not in html


def test_catalog_card_with_page_links_internal(env):
    html = render_page(env, make_page(url='/'), ctx(tools={'bar': tool('bar', True)}))
    assert 'href="/herramientas/bar/"' in html


def test_catalog_groups_have_category_anchor(env):
    html = render_page(env, make_page(url='/'), ctx(tools={'bar': tool('bar', True)}))
    assert 'id="cat-escritura"' in html


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
