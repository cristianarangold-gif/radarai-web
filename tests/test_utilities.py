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


def test_video_description_has_no_fixed_hashtags_and_adapts_to_platform():
    assert '#IA #Tecnologia #Aprendizaje' not in APP
    assert 'MARCAS DE TIEMPO' in APP and 'comentarios' in APP


def test_ideas_are_real_titles_with_format_and_closing():
    assert 'Desarrolla el ángulo' not in APP
    assert 'Carrusel' in APP and 'Vídeo corto' in APP and 'Cierra' in APP


def test_prompt_improver_diagnosis_is_computed():
    assert '✓ Objetivo definido\\n✓ Contexto separado' not in APP
    assert '[completa:' in APP and ' de 6' in APP


def test_no_regex_lookbehind_for_older_safari():
    assert '(?<=' not in APP and '(?<!' not in APP


def test_hashtags_keep_enye():
    assert 'ñÑ' in APP.split('const tagWord')[1].split('};')[0]


def test_prompt_checks_accept_plurals_and_feminine():
    diag = APP.split('const diagnose')[1].split('const run')[0]
    for stem in ('m[áa]xim[oa]s?', 'l[íi]mites?', 'listas?', 'tablas?', 'ejemplos?', 'es para'):
        assert stem in diag, stem
