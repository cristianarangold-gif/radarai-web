from datetime import date

from radar.seo import canonical, jsonld, rss_xml, sitemap_xml
from tests.helpers import make_page, news


def test_canonical_absolute():
    assert canonical('/noticias/x/') == 'https://radarai.es/noticias/x/'
    assert canonical('/') == 'https://radarai.es/'


def test_sitemap_excludes_drafts_and_noindex():
    xml = sitemap_xml([make_page(url='/a/'), make_page(url='/b/', draft=True),
                       make_page(url='/c/', extra={'noindex': 'si'})])
    assert '<loc>https://radarai.es/a/</loc>' in xml
    assert '/b/' not in xml and '/c/' not in xml


def test_sitemap_lastmod():
    xml = sitemap_xml([news('n', 1, updated=date(2026, 10, 3))])
    assert '<lastmod>2026-10-03</lastmod>' in xml


def test_jsonld_news_has_dates_and_author():
    data = jsonld(news('n', 1))
    article = next(d for d in data if d['@type'] == 'NewsArticle')
    assert article['datePublished'] == '2026-10-01'
    assert article['author'] == {'@type': 'Person', 'name': 'Cristian Arango',
                                 'url': 'https://radarai.es/autor/',
                                 'sameAs': ['https://www.instagram.com/cristian__fit/']}
    assert any(d['@type'] == 'BreadcrumbList' for d in data)


def test_jsonld_home_is_website_without_breadcrumb():
    types = [d['@type'] for d in jsonld(make_page(url='/'))]
    assert types == ['WebSite']


def test_jsonld_tool_is_software_application():
    page = make_page(kind='ficha', url='/herramientas/claude/', title='Claude', date=date(2026, 10, 1))
    assert 'SoftwareApplication' in [d['@type'] for d in jsonld(page)]


def test_rss_orders_by_date_desc_and_skips_drafts():
    xml = rss_xml([news('vieja', 1), news('nueva', 5), news('borrador', 9, draft=True)])
    assert xml.index('nueva') < xml.index('vieja')
    assert 'borrador' not in xml
    assert '<pubDate>' in xml


def test_jsonld_author_page_is_profile_page():
    data = jsonld(make_page(url='/autor/', title='Cristian Arango', description='Autor'))
    profile = next(d for d in data if d['@type'] == 'ProfilePage')
    person = profile['mainEntity']
    assert person['name'] == 'Cristian Arango' and person['image'] == 'https://radarai.es/static/img/cristian-arango.jpg'
    assert person['sameAs'] == ['https://www.instagram.com/cristian__fit/']
