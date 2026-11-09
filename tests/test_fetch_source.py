import json

import pytest

from scripts.fetch_source import archive_url, page_text, read_source

PAGE = ('<html><head><style>p{}</style><script>var x=1</script></head>'
        '<body><h1>Decisions API</h1><p>Fast &amp; focused.</p></body></html>')


def fake(responses):
    """Devuelve una función fetch(url) que responde según el prefijo de la URL."""
    calls = []

    def fetch(url):
        calls.append(url)
        for prefix, result in responses:
            if url.startswith(prefix):
                return result
        return 404, ''
    fetch.calls = calls
    return fetch


def test_page_text_strips_tags_scripts_and_entities():
    assert page_text(PAGE) == 'Decisions API Fast & focused.'


def test_direct_read_when_official_page_works():
    fetch = fake([('https://openai.com/', (200, PAGE))])
    used, text = read_source('https://openai.com/index/x', fetch)
    assert used == 'https://openai.com/index/x' and 'Decisions API' in text
    assert len(fetch.calls) == 1


def test_falls_back_to_latest_archive_copy_with_status_200():
    cdx = json.dumps([['timestamp', 'statuscode'], ['20261020100000', '200'],
                      ['20261022194525', '200'], ['20261023084850', '403']])
    fetch = fake([('https://openai.com/', (403, 'blocked')),
                  ('https://web.archive.org/cdx/', (200, cdx)),
                  ('https://web.archive.org/web/20261022194525id_/', (200, PAGE))])
    used, text = read_source('https://openai.com/index/x', fetch)
    assert used == 'https://web.archive.org/web/20261022194525/https://openai.com/index/x'
    assert 'Fast & focused.' in text


def test_archive_url_none_without_snapshots():
    fetch = fake([('https://web.archive.org/cdx/', (200, '[]'))])
    assert archive_url('https://openai.com/index/x', fetch) is None


def test_unreadable_source_returns_none():
    fetch = fake([('https://openai.com/', (403, 'blocked')), ('https://web.archive.org/cdx/', (200, '[]'))])
    assert read_source('https://openai.com/index/x', fetch) == (None, '')


def test_bot_challenge_with_status_200_counts_as_blocked():
    challenge = '<html><body>Enable JavaScript and cookies to continue</body></html>'
    fetch = fake([('https://openai.com/', (200, challenge)), ('https://web.archive.org/cdx/', (200, '[]'))])
    assert read_source('https://openai.com/index/x', fetch) == (None, '')


URL = 'https://openai.com/index/x'
CDX = json.dumps([['timestamp', 'statuscode'], ['20261022194525', '200']])
COPY = 'https://web.archive.org/web/20261022194525id_/'


def flaky(responses):
    """Como fake(), pero cada prefijo responde con su lista de resultados en orden; el último se repite."""
    calls = []
    pending = {prefix: list(results) for prefix, results in responses}

    def fetch(url):
        calls.append(url)
        for prefix, results in pending.items():
            if url.startswith(prefix):
                return results.pop(0) if len(results) > 1 else results[0]
        return 404, ''
    fetch.calls = calls
    return fetch


def test_retries_archive_copy_when_connection_is_refused():
    fetch = flaky([('https://openai.com/', [(403, '')]),
                   ('https://web.archive.org/cdx/', [(200, CDX)]),
                   (COPY, [(0, ''), (0, ''), (200, PAGE)])])
    waits = []
    used, text = read_source(URL, fetch, sleep=waits.append)
    assert used == f'https://web.archive.org/web/20261022194525/{URL}' and 'Decisions API' in text
    assert len(waits) == 2 and waits == sorted(waits)


def test_retries_archive_lookup_when_connection_is_refused():
    fetch = flaky([('https://openai.com/', [(403, '')]),
                   ('https://web.archive.org/cdx/', [(0, ''), (200, CDX)]),
                   (COPY, [(200, PAGE)])])
    used, _ = read_source(URL, fetch, sleep=lambda seconds: None)
    assert used == f'https://web.archive.org/web/20261022194525/{URL}'


@pytest.mark.parametrize('status', [429, 500, 503])
def test_retries_archive_when_it_is_overloaded(status):
    fetch = flaky([('https://openai.com/', [(403, '')]),
                   ('https://web.archive.org/cdx/', [(status, ''), (200, CDX)]),
                   (COPY, [(200, PAGE)])])
    used, _ = read_source(URL, fetch, sleep=lambda seconds: None)
    assert used is not None


def test_gives_up_when_archive_keeps_failing():
    fetch = flaky([('https://openai.com/', [(403, '')]), ('https://web.archive.org/cdx/', [(0, '')])])
    waits = []
    assert read_source(URL, fetch, sleep=waits.append) == (None, '')
    assert len([c for c in fetch.calls if '/cdx/' in c]) == 4
    assert len(waits) == 3


def test_does_not_retry_definitive_archive_answer():
    fetch = flaky([('https://openai.com/', [(403, '')]), ('https://web.archive.org/cdx/', [(404, '')])])
    waits = []
    assert read_source(URL, fetch, sleep=waits.append) == (None, '')
    assert len(fetch.calls) == 2 and waits == []


def test_does_not_wait_when_official_page_is_blocked_and_archive_answers():
    fetch = flaky([('https://openai.com/', [(403, '')]),
                   ('https://web.archive.org/cdx/', [(200, CDX)]),
                   (COPY, [(200, PAGE)])])
    waits = []
    read_source(URL, fetch, sleep=waits.append)
    assert waits == [] and len([c for c in fetch.calls if c.startswith('https://openai.com/')]) == 1
