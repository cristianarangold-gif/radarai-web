import json
from urllib.error import URLError

import pytest

from radar.indexnow import KEY, KEY_FILE, changed_urls, parse_sitemap, payload
from scripts.indexnow import plan, send


def sitemap(*rows):
    body = ''.join(f'<url><loc>https://radarai.es{u}</loc>' + (f'<lastmod>{d}</lastmod>' if d else '') + '</url>'
                   for u, d in rows)
    return f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>'


OLD = sitemap(('/', None), ('/a/', '2026-10-01'), ('/b/', '2026-10-01'))
NEW = sitemap(('/', None), ('/a/', '2026-11-09'), ('/b/', '2026-10-01'), ('/c/', '2026-11-09'))


def test_parse_sitemap_reads_urls_and_dates():
    assert parse_sitemap(OLD) == {'https://radarai.es/': None, 'https://radarai.es/a/': '2026-10-01',
                                  'https://radarai.es/b/': '2026-10-01'}


def test_parse_sitemap_rejects_non_xml():
    with pytest.raises(ValueError):
        parse_sitemap('<html><body>Error')


def test_changed_urls_are_new_or_redated_only():
    assert changed_urls(parse_sitemap(OLD), parse_sitemap(NEW)) == ['https://radarai.es/a/', 'https://radarai.es/c/']


def test_payload_follows_the_protocol():
    assert payload(['https://radarai.es/a/']) == {
        'host': 'radarai.es', 'key': KEY, 'keyLocation': f'https://radarai.es/{KEY_FILE}',
        'urlList': ['https://radarai.es/a/']}


def test_plan_sends_only_changes():
    assert plan(NEW, lambda: OLD) == ['https://radarai.es/a/', 'https://radarai.es/c/']


def test_plan_all_ignores_the_live_sitemap():
    def fail():
        raise AssertionError('no debe leer la web')
    assert len(plan(NEW, fail, send_all=True)) == 4


@pytest.mark.parametrize('old', ['<html>Error', sitemap()])
def test_plan_sends_nothing_when_live_sitemap_is_unusable(old):
    assert plan(NEW, lambda: old) == []


def test_plan_sends_nothing_when_site_is_unreachable():
    def down():
        raise URLError('caída')
    assert plan(NEW, down) == []


@pytest.mark.parametrize('status', [200, 202])
def test_send_posts_urls_when_accepted(status, capsys):
    posted = []
    assert send(json.dumps(['https://radarai.es/a/']), lambda body: posted.append(body) or status) == 0
    assert posted[0]['urlList'] == ['https://radarai.es/a/']
    assert '::warning' not in capsys.readouterr().out


def test_send_nothing_to_do_makes_no_request():
    def fail(body):
        raise AssertionError('no debe enviar')
    assert send('[]', fail) == 0


@pytest.mark.parametrize('status', [403, 422, 429, 500])
def test_rejection_warns_but_never_fails_the_deploy(status, capsys):
    assert send(json.dumps(['https://radarai.es/a/']), lambda body: status) == 0
    assert '::warning' in capsys.readouterr().out


def test_network_error_warns_but_never_fails_the_deploy(capsys):
    def down(body):
        raise URLError('caída')
    assert send(json.dumps(['https://radarai.es/a/']), down) == 0
    assert '::warning' in capsys.readouterr().out
