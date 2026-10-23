import json

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
