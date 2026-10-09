"""Las utilidades deben hacer lo que dicen sus páginas (comprobaciones estáticas de static/utilidades/app.js)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = (ROOT / 'static' / 'utilidades' / 'app.js').read_text(encoding='utf-8')


def test_no_literal_combining_marks_and_no_inner_html():
    assert not any(0x300 <= ord(c) <= 0x36f for c in APP)
    assert '\\u0300-\\u036f' in APP and 'innerHTML' not in APP


def test_word_counter_reports_repeated_words_and_long_sentences():
    assert 'PALABRAS MÁS REPETIDAS' in APP and 'FRASES DE MÁS DE 30 PALABRAS' in APP and 'MEDIA POR FRASE' in APP


def test_hashtags_have_no_fixed_tags_and_no_platform_field():
    assert "['ia','tecnologia','aprendizaje']" not in APP
    hashtags = APP.split("'generador-de-hashtags':")[1].split('\n')[0]
    assert 'plataforma' not in hashtags and 'nicho' in hashtags and 'audiencia' in hashtags


def test_titles_do_not_claim_own_tests():
    assert 'Probé' not in APP and 'probé' not in APP
