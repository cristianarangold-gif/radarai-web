from datetime import datetime, timezone
from pathlib import Path

from scripts.news_collect import Item, is_ai_related, load_sources, parse_feed, render_issue, select_candidates

FIX = Path(__file__).parent / 'fixtures'
NOW = datetime(2026, 10, 6, 5, 0, tzinfo=timezone.utc)


def rss():
    return parse_feed((FIX / 'rss.xml').read_text(), 'Medio', False)


def atom():
    return parse_feed((FIX / 'atom.xml').read_text(), 'Oficial', True)


def test_parses_rss_and_atom_dates():
    r, a = rss(), atom()
    assert r[0].published == datetime(2026, 10, 5, 10, 0, tzinfo=timezone.utc)
    assert r[1].published == datetime(2026, 9, 21, 8, 0, tzinfo=timezone.utc)
    assert a[0].published == datetime(2026, 10, 5, 18, 30, tzinfo=timezone.utc)
    assert a[1].published == datetime(2026, 10, 5, 8, 0, tzinfo=timezone.utc)
    assert a[0].url == 'https://oficial.com/x' and a[1].url == 'https://oficial.com/y'


def test_titles_unescaped():
    assert rss()[0].title == 'Nuevo modelo & API'


def test_broken_feed_does_not_abort():
    assert parse_feed('<rss><channel><item>', 'Roto', False) == []


def test_select_orders_official_first():
    sel = select_candidates(rss() + atom(), NOW)
    assert [i.url for i in sel] == ['https://oficial.com/x', 'https://oficial.com/y', 'https://ejemplo.com/a']


def test_dedupes_by_url():
    items = rss() + rss()
    assert [i.url for i in select_candidates(items, NOW)] == ['https://ejemplo.com/a']


def test_no_candidates_returns_none():
    assert render_issue([], [], '2026-10-06') is None


def test_render_issue_lists_items_and_failures():
    body = render_issue(select_candidates(atom(), NOW), ['Roto'], '2026-10-06')
    assert '[Anuncio oficial](https://oficial.com/x)' in body
    assert 'Oficial' in body and 'Roto' in body
    assert 'GUIA_EDITORIAL' in body


def _item(title, url, source='Fuente', official=True, hour=4):
    return Item(title, url, datetime(2026, 10, 6, hour, 0, tzinfo=timezone.utc), source, official)


def test_load_sources_reads_optional_filter(tmp_path):
    f = tmp_path / 'fuentes.txt'
    f.write_text('# comentario\noficial · OpenAI · https://a/rss\noficial · Meta · https://b/rss · filtrar\n', encoding='utf-8')
    assert load_sources(f) == [('OpenAI', 'https://a/rss', True, False), ('Meta', 'https://b/rss', True, True)]


def test_is_ai_related():
    for title in ('Meta presenta Llama 5', 'New Copilot features in Windows', 'La inteligencia artificial llega a…',
                  'Apple Intelligence en español', 'OpenAI y la UE', 'Nuevo agente de IA para empresas', 'Galaxy AI'):
        assert is_ai_related(title), title
    for title in ('Nuevo iPhone con mejor batería', 'Resultados trimestrales', 'Maid of honor', 'Paid plans', 'Hawaii'):
        assert not is_ai_related(title), title


def test_select_caps_items_per_source():
    items = [_item(f'N{i}', f'https://n/{i}', 'NVIDIA', hour=4 - i % 4) for i in range(5)]
    items.append(_item('Otra', 'https://o/1', 'OpenAI', hour=1))
    sel = select_candidates(items, NOW, official_per_source=2)
    assert [i.source for i in sel] == ['NVIDIA', 'NVIDIA', 'OpenAI']


def test_select_keeps_older_official_announcement_behind_customer_stories():
    stories = [_item(f'Caso de cliente {n}', f'https://o/{n}', 'OpenAI', hour=4) for n in range(5)]
    launch = _item('Introducing GPT-6 Cyber', 'https://o/gpt-6-cyber', 'OpenAI', hour=1)
    assert launch in select_candidates(stories + [launch], NOW)


def test_select_still_caps_media_per_source():
    items = [_item(f'Titular {n}', f'https://m/{n}', 'Medio', official=False) for n in range(5)]
    assert len(select_candidates(items, NOW)) == 2


def test_select_default_limit_leaves_room_for_media_behind_officials():
    official = [_item(f'O{s}{n}', f'https://o/{s}/{n}', f'Oficial {s}') for s in range(3) for n in range(6)]
    media = _item('Medio', 'https://m/1', 'Medio', official=False)
    assert media in select_candidates(official + [media], NOW)
