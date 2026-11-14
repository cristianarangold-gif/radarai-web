from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from scripts.tweet import intent_link, parse_tweet, pr_body, problems, weighted_length

GOOD = """fecha: 2026-11-13
tipo: noticia
url: https://radarai.es/noticias/x/

Gemini ya funciona en Apple CarPlay 🚗

Te contamos qué cambia en España 👇

#Gemini #CarPlay
"""


def test_parse_reads_metadata_and_text():
    t = parse_tweet(GOOD)
    assert t['fecha'] == '2026-11-13' and t['tipo'] == 'noticia' and t['url'] == 'https://radarai.es/noticias/x/'
    assert t['texto'].startswith('Gemini ya funciona') and t['texto'].endswith('#Gemini #CarPlay')


def test_weighted_length_counts_emoji_double_and_accents_single():
    assert weighted_length('España') == 6
    assert weighted_length('🚗') == 2
    assert weighted_length('👇️') == 2


def test_good_tweet_has_no_problems():
    assert problems(parse_tweet(GOOD), live=lambda url: True) == []


def test_too_long_counts_the_link_as_23():
    t = parse_tweet(GOOD)
    t['texto'] = 'a' * 253 + ' #IA'  # 257 + espacio + enlace (23) = 281
    assert any('280' in p for p in problems(t, live=lambda url: True))
    t['texto'] = 'a' * 252 + ' #IA'  # justo 280
    assert problems(t, live=lambda url: True) == []


def test_link_must_be_radar_ia():
    t = parse_tweet(GOOD.replace('https://radarai.es/noticias/x/', 'https://otra.web/x/'))
    assert any('radarai.es' in p for p in problems(t, live=lambda url: True))


def test_link_must_be_published():
    assert any('publicada' in p for p in problems(parse_tweet(GOOD), live=lambda url: False))


def test_text_must_not_repeat_the_link():
    t = parse_tweet(GOOD)
    t['texto'] += ' https://radarai.es/noticias/x/'
    assert any('enlace' in p for p in problems(t, live=lambda url: True))


@pytest.mark.parametrize('tags', ['', '#IA #Gemini #Google'])
def test_needs_one_or_two_hashtags(tags):
    t = parse_tweet(GOOD)
    t['texto'] = 'Texto del tuit 👇 ' + tags
    assert any('hashtag' in p for p in problems(t, live=lambda url: True))


@pytest.mark.parametrize('field', ['fecha', 'tipo', 'url'])
def test_missing_metadata_is_reported(field):
    t = parse_tweet(GOOD)
    del t[field]
    assert any(field in p for p in problems(t, live=lambda url: True))


def test_unknown_type_is_reported():
    t = parse_tweet(GOOD.replace('tipo: noticia', 'tipo: meme'))
    assert any('tipo' in p for p in problems(t, live=lambda url: True))


def test_intent_link_opens_x_with_text_and_url():
    link = intent_link(parse_tweet(GOOD))
    parsed = urlparse(link)
    assert parsed.netloc == 'x.com' and parsed.path == '/intent/post'
    query = parse_qs(parsed.query)
    assert query['text'][0].startswith('Gemini ya funciona en Apple CarPlay 🚗\n\n')
    assert query['url'] == ['https://radarai.es/noticias/x/']


def test_pr_body_has_a_clickable_publish_link():
    tweet = parse_tweet(GOOD.replace('url:', 'fuente: data/noticias.md\nurl:'))
    body = pr_body(tweet)
    # Un enlace Markdown normal: GitHub lo muestra pulsable. Entre comillas invertidas sería código.
    assert f'👉 **[Publicar en X]({intent_link(tweet)})**' in body
    assert '`' not in body
    assert '> Gemini ya funciona en Apple CarPlay 🚗\n>\n> Te contamos qué cambia en España 👇' in body
    assert 'https://radarai.es/noticias/x/' in body and 'data/noticias.md' in body
    assert 'Pulsa el enlace' in body


def test_tweet_prs_get_their_body_rewritten_by_github():
    # La rutina en la nube puede estropear el enlace al copiar el cuerpo; GitHub lo regenera con el script.
    workflow = (Path(__file__).parent.parent / '.github/workflows/tuit-enlace.yml').read_text(encoding='utf-8')
    assert "startsWith(github.head_ref, 'tuit/')" in workflow
    assert 'pull-requests: write' in workflow
    assert 'scripts/tweet.py' in workflow and '--pr' in workflow
    assert 'gh pr edit' in workflow and '--body-file' in workflow
