from datetime import date

import pytest

from radar.editorial import (DEFAULT_RADAR, load_imprescindibles, radar_tools, reading_minutes,
                             related_news, split_ids, toc, validate_news_meta)
from radar.models import Brand, Tool
from tests.helpers import make_page, news


def tool(tid, has_page=True):
    return Tool(id=tid, name=tid.title(), cat='ia-general', desc='', price='', level='', platform='',
                lang='', tags=[], url='https://x/', has_page=has_page)


TOOLS = {t.id: t for t in [tool('chatgpt'), tool('claude'), tool('gemini'), tool('midjourney'),
                           tool('perplexity'), tool('cursor'), tool('runway', has_page=False)]}
BRANDS = {'openai': Brand('openai', 'OpenAI', '#10a37f', None, 'O')}


def test_default_radar():
    assert DEFAULT_RADAR == ['chatgpt', 'claude', 'gemini', 'midjourney', 'perplexity']


def test_split_ids():
    assert split_ids(' Claude, cursor ,,') == ['claude', 'cursor']
    assert split_ids('') == []


def test_radar_tools_takes_recent_news_order_then_defaults():
    items = [news('a', 6, extra={'herramientas': 'claude, cursor'}),
             news('b', 5, extra={'herramientas': 'claude,runway'})]
    assert [t.id for t in radar_tools(items, TOOLS)] == ['claude', 'cursor', 'chatgpt', 'gemini', 'midjourney']


def test_radar_tools_ignores_news_older_than_six():
    items = [news(f'n{i}', 20 - i) for i in range(6)] + [news('vieja', 1, extra={'herramientas': 'cursor'})]
    assert 'cursor' not in [t.id for t in radar_tools(items, TOOLS)]


def test_radar_tools_never_returns_tools_without_page():
    items = [news('a', 6, extra={'herramientas': 'runway'})]
    ids = [t.id for t in radar_tools(items, TOOLS)]
    assert 'runway' not in ids and len(ids) == 5


def test_validate_news_meta_unknown_tool_names_file_and_id():
    with pytest.raises(ValueError, match=r'noticias/x: herramienta desconocida «chatgtp»'):
        validate_news_meta([news('x', 6, extra={'herramientas': 'chatgtp'})], TOOLS, BRANDS)


def test_validate_news_meta_unknown_company():
    with pytest.raises(ValueError, match=r'noticias/x: empresa desconocida «openia»'):
        validate_news_meta([news('x', 6, extra={'empresa': 'openia'})], TOOLS, BRANDS)


def test_news_without_empresa_or_herramientas_is_fine():
    validate_news_meta([news('x', 6), news('y', 5, extra={'empresa': 'OpenAI', 'herramientas': 'runway'})],
                       TOOLS, BRANDS)


def test_reading_minutes():
    assert reading_minutes(make_page(word_count=0)) == 1
    assert reading_minutes(make_page(word_count=100)) == 1
    assert reading_minutes(make_page(word_count=1100)) == 5


def test_toc_reads_h2_ids_and_plain_text():
    assert toc('<h2 id="a">Planes &amp; <em>precios</em></h2><h3 id="b">x</h3><h2>sin id</h2>') == \
        [('a', 'Planes & precios')]


def test_related_news_excludes_self_and_limits_to_three():
    items = [news(f'n{i}', 10 - i) for i in range(5)]
    rel = related_news(items[1], items)
    assert [p.slug for p in rel] == ['n0', 'n2', 'n3']


def test_imprescindibles_reads_urls_in_order(tmp_path):
    pages = {u: make_page(url=u, title=u) for u in ('/a/', '/b/', '/c/', '/d/', '/e/')}
    f = tmp_path / 'i.txt'
    f.write_text('# comentario\n/b/\n\n/a/\n/c/\n/d/\n/e/\n', encoding='utf-8')
    assert [p.url for p in load_imprescindibles(f, pages)] == ['/b/', '/a/', '/c/', '/d/']


def test_imprescindibles_unknown_url_raises(tmp_path):
    f = tmp_path / 'i.txt'
    f.write_text('/no-existe/\n', encoding='utf-8')
    with pytest.raises(ValueError, match='/no-existe/'):
        load_imprescindibles(f, {})


def test_imprescindibles_noindex_url_raises(tmp_path):
    f = tmp_path / 'i.txt'
    f.write_text('/a/\n', encoding='utf-8')
    with pytest.raises(ValueError, match='/a/'):
        load_imprescindibles(f, {'/a/': make_page(url='/a/', draft=True)})


def test_validate_fichas_requires_at_least_one_field():
    from radar.editorial import FICHA_FIELDS, validate_fichas
    assert FICHA_FIELDS == ('precio_desde', 'plan_pago', 'ideal_para', 'veredicto')
    validate_fichas([make_page(kind='ficha', slug='a', extra={'veredicto': 'x'}), make_page(kind='guia')])
    with pytest.raises(ValueError, match='herramientas/b: faltan precio_desde, plan_pago, ideal_para y veredicto'):
        validate_fichas([make_page(kind='ficha', slug='b')])


def test_real_fichas_have_all_summary_fields():
    from pathlib import Path
    from radar.content import load_pages
    from radar.editorial import FICHA_FIELDS
    root = Path(__file__).resolve().parent.parent
    for p in load_pages(root / 'content'):
        if p.kind == 'ficha':
            for f in FICHA_FIELDS:
                assert p.extra.get(f), f'{p.slug}: falta {f}'
            assert len(p.extra['veredicto'].split()) <= 30, p.slug
            assert 'hemos probado' not in p.extra['veredicto'].lower()


def test_no_promise_of_own_test_blocks():
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    for path in list((root / 'content').rglob('*.md')) + [root / 'static' / 'css' / 'radar.css']:
        text = path.read_text(encoding='utf-8')
        assert 'NUESTRA PRUEBA' not in text and 'nuestra-prueba' not in text, path
        assert '«Nuestra prueba»' not in text, path


def test_author_page_has_photo_and_profile():
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    text = (root / 'content' / 'paginas' / 'autor.md').read_text(encoding='utf-8')
    assert '/static/img/cristian-arango.jpg' in text and 'instagram.com/cristian__fit' in text
    assert (root / 'static' / 'img' / 'cristian-arango.jpg').stat().st_size < 60_000


def test_author_title_is_not_a_regulated_profession_claim():
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    text = (root / 'content' / 'paginas' / 'autor.md').read_text(encoding='utf-8')
    assert 'dietista' not in text.lower() and 'entrenador personal especializado en nutrición deportiva' in text
