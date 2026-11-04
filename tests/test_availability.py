from datetime import date, timedelta
from pathlib import Path

import pytest

from radar.availability import availability_context, parse_availability, validate_availability
from tests.helpers import make_page

ROOT = Path(__file__).resolve().parent.parent
TODAY = date(2026, 11, 4)
FICHAS = {'chatgpt': make_page(kind='ficha', slug='chatgpt', url='/herramientas/chatgpt/')}
URLS = {'/noticias/siri/'}
FIELDS = {'id': 'siri-ia', 'empresa': 'apple', 'ficha': '', 'eeuu': 'si', 'ue': 'no', 'es': 'no',
          'nota': 'Sin fecha para la UE.', 'comprobado': '2026-11-04',
          'fuentes': 'https://www.apple.com/es/ios/', 'noticia': '/noticias/siri/'}


def block(title='Siri con IA', **changes):
    fields = {**FIELDS, **changes}
    lines = [f'{k}: {v}' for k, v in fields.items() if v is not None]
    return '\n'.join([f'## {title}'] + lines) + '\n\n'


def check(text):
    validate_availability(parse_availability(text), FICHAS, URLS, TODAY)


def test_parse_block():
    f = parse_availability('Comentario inicial.\n\n' + block())[0]
    assert (f.title, f.id, f.empresa, f.ficha) == ('Siri con IA', 'siri-ia', 'apple', '')
    assert (f.eeuu, f.ue, f.es) == ('si', 'no', 'no')
    assert f.nota == 'Sin fecha para la UE.' and f.comprobado == '2026-11-04'
    assert f.fuentes == ['https://www.apple.com/es/ios/'] and f.noticia == '/noticias/siri/'


def test_valid_block_passes():
    check(block())


@pytest.mark.parametrize('field', ['id', 'empresa', 'eeuu', 'ue', 'es', 'comprobado', 'fuentes'])
def test_rejects_missing_field(field):
    with pytest.raises(ValueError, match=f'«Siri con IA».*{field}'):
        check(block(**{field: None}))


def test_rejects_unknown_status():
    with pytest.raises(ValueError, match='estado'):
        check(block(es='quizas', ue='si'))


def test_rejects_repeated_id():
    with pytest.raises(ValueError, match='id'):
        check(block('Uno') + block('Dos'))


def test_rejects_repeated_title():
    with pytest.raises(ValueError, match='repetido'):
        check(block('Uno', id='a') + block('Uno', id='b'))


def test_rejects_id_with_uppercase():
    with pytest.raises(ValueError, match='id'):
        check(block(id='Siri-IA'))


def test_rejects_unknown_company():
    with pytest.raises(ValueError, match='empresa'):
        check(block(empresa='acme'))


def test_rejects_unknown_ficha():
    with pytest.raises(ValueError, match='ficha'):
        check(block(ficha='no-existe'))


def test_rejects_future_date():
    with pytest.raises(ValueError, match='fecha'):
        check(block(comprobado=(TODAY + timedelta(days=1)).isoformat()))


def test_rejects_invalid_date():
    with pytest.raises(ValueError, match='fecha'):
        check(block(comprobado='2026-13-40'))


def test_rejects_unofficial_domain():
    with pytest.raises(ValueError, match='fuente'):
        check(block(fuentes='https://example.com/siri'))


def test_rejects_press_source():
    with pytest.raises(ValueError, match='fuente'):
        check(block(fuentes='https://techcrunch.com/siri'))


def test_rejects_more_than_three_sources():
    with pytest.raises(ValueError, match='fuente'):
        check(block(fuentes=', '.join(f'https://www.apple.com/{i}' for i in range(4))))


def test_rejects_http_source():
    with pytest.raises(ValueError, match='https'):
        check(block(fuentes='http://www.apple.com/'))


def test_rejects_lookalike_and_foreign_archive():
    for url in ('https://apple.com.evil.es/siri', 'https://web.archive.org/web/20261020/https://example.com/'):
        with pytest.raises(ValueError, match='fuente'):
            check(block(fuentes=url))


def test_accepts_subdomain_and_official_archive():
    check(block(fuentes='https://support.apple.com/es-es/1, '
                        'https://web.archive.org/web/20261020120000/https://www.apple.com/es/ios/'))


def test_rejects_partial_without_note():
    with pytest.raises(ValueError, match='nota'):
        check(block(ue='parcial', es='parcial', nota=''))


def test_rejects_note_over_30_words():
    with pytest.raises(ValueError, match='nota'):
        check(block(nota=' '.join(['palabra'] * 31)))


def test_accepts_note_of_30_words():
    check(block(nota=' '.join(['palabra'] * 30)))


def test_rejects_missing_news():
    with pytest.raises(ValueError, match='noticia'):
        check(block(noticia='/noticias/no-existe/'))


def test_rejects_eu_no_with_spain_otherwise():
    with pytest.raises(ValueError, match='España'):
        check(block(ue='no', es='parcial'))


def test_accepts_eu_yes_with_spain_unconfirmed():
    check(block(ue='si', es='sin_confirmar'))


def test_sort_order():
    text = (block('Zeta', id='z', ue='si', es='si') + block('Ángel', id='a', ue='si', es='si')
            + block('Duda', id='d', ue='si', es='sin_confirmar') + block('Parcial', id='p', ue='si', es='parcial')
            + block('Nada', id='n'))
    rows = availability_context(parse_availability(text), TODAY)['rows']
    assert [r.title for r in rows] == ['Nada', 'Parcial', 'Duda', 'Ángel', 'Zeta']


def test_stale_boundary():
    at_60 = (TODAY - timedelta(days=60)).isoformat()
    at_61 = (TODAY - timedelta(days=61)).isoformat()
    ctx = availability_context(parse_availability(block('Sesenta', id='a', comprobado=at_60)
                                                  + block('Sesenta y uno', id='b', comprobado=at_61)), TODAY)
    assert {r.title: r.stale for r in ctx['rows']} == {'Sesenta': False, 'Sesenta y uno': True}
    assert [r.title for r in ctx['stale']] == ['Sesenta y uno']


def test_context_counts_latest_and_groups_by_ficha():
    text = block('A', id='a', ficha='chatgpt', comprobado='2026-10-01') + block('B', id='b')
    ctx = availability_context(parse_availability(text), TODAY)
    assert ctx['count'] == 2 and ctx['latest'] == '4 de noviembre de 2026'
    assert [r.title for r in ctx['by_ficha']['chatgpt']] == ['A']


def test_real_data_has_minimum():
    features = parse_availability((ROOT / 'data' / 'disponibilidad.md').read_text(encoding='utf-8'))
    assert len(features) >= 12
    assert all(f.fuentes and f.comprobado for f in features)
