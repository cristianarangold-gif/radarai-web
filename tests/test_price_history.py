import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from radar.price_history import (auto_changes, chart_points, load_snapshots, parse_history, parse_price,
                                 validate_history)
from tests.helpers import make_page

ROOT = Path(__file__).resolve().parent.parent
TODAY = date(2026, 10, 8)
BODY = '<p>Gratis 0 €, Go 8 €/mes, Plus 23 €/mes y Pro desde 103 €/mes. Claude Free 0 $ y Pro 20 $/mes.</p>'
FICHAS = {
    'chatgpt': make_page(kind='ficha', slug='chatgpt', url='/herramientas/chatgpt/', body_html=BODY,
                         sources=['https://chatgpt.com/es-ES/pricing/'], extra={'web': 'https://chatgpt.com/'}),
    'claude': make_page(kind='ficha', slug='claude', url='/herramientas/claude/', body_html=BODY,
                        sources=['https://claude.com/pricing'], extra={'web': 'https://claude.ai/'}),
}
SNAP = {'herramientas': {
    'chatgpt': {'fuente': 'https://chatgpt.com/es-ES/pricing/',
                'planes': {'Gratis': '0 €', 'Go': '8 €/mes', 'Plus': '23 €/mes', 'Pro': 'desde 103 €/mes'}},
    'claude': {'fuente': 'https://claude.com/pricing', 'planes': {'Free': '0 $', 'Pro': '20 $/mes'}}}}
LINE = '2025-11 | chatgpt | nuevo | Go | 9,99 €/mes | ChatGPT Go llega a España. | https://openai.com/index/go/'


def snaps(tmp_path, *pairs):
    d = tmp_path / 'tomas-precios'
    d.mkdir(exist_ok=True)
    for name, data in pairs:
        (d / name).write_text(json.dumps(data), encoding='utf-8')
    return load_snapshots(d)


def check(tmp_path, text, *pairs):
    validate_history(parse_history(text), snaps(tmp_path, *(pairs or [('2026-10-06.json', SNAP)])), FICHAS, TODAY)


def test_parse_price():
    p = parse_price('desde 103 €/mes')
    assert (p.amount, p.currency, p.period, p.desde) == (Decimal('103'), '€', '/mes', True)
    assert parse_price('9,99 €/mes').amount == Decimal('9.99')
    assert parse_price('17 $/mes (anual)').period == '/mes (anual)'
    assert parse_price('110 €/año').period == '/año' and parse_price('0 $').period == ''
    assert parse_price('9.99€') is None and parse_price('gratis') is None


def test_parse_lines_and_comments():
    text = 'Comentario sin barras.\n\n' + LINE + '\n2026-08 | chatgpt | baja | Go | 9,99 €/mes → 8 €/mes | Baja. | https://chatgpt.com/es-ES/pricing/\n'
    nuevo, baja = parse_history(text)
    assert (nuevo.date, nuevo.tool, nuevo.kind, nuevo.plan, nuevo.line) == ('2025-11', 'chatgpt', 'nuevo', 'Go', 3)
    assert nuevo.price.amount == Decimal('9.99') and nuevo.before is None and not nuevo.auto
    assert baja.before.amount == Decimal('9.99') and baja.price.amount == Decimal('8')


def test_valid_history_passes(tmp_path):
    check(tmp_path, LINE)


def test_wrong_field_count_fails():
    with pytest.raises(ValueError, match='línea 1: hacen falta 7 campos'):
        parse_history('2025-11 | chatgpt | nuevo')


ARCHIVE = 'https://web.archive.org/web/20250101000000/https://chatgpt.com/pricing'


@pytest.mark.parametrize('line, needle', [
    (LINE.replace('2025-11', '2025-13'), 'fecha'),
    (LINE.replace('2025-11', '2026-11'), 'futura'),
    (LINE.replace('2025-11', '2026-10-09'), 'futura'),
    (LINE.replace('2025-11', '2022-12'), '2023'),
    (LINE.replace('chatgpt |', 'zeta |', 1), 'zeta'),
    (LINE.replace('nuevo', 'cambia'), 'tipo'),
    (LINE.replace('9,99 €/mes', '9.99€'), 'precio'),
    (LINE.replace('| nuevo | Go | 9,99 €/mes', '| nuevo | Go | '), 'precio'),
    (LINE.replace('nuevo | Go | 9,99 €/mes', 'sube | Go | 9,99 €/mes → 8 €/mes'), 'sube'),
    (LINE.replace('nuevo | Go | 9,99 €/mes', 'baja | Go | 8 €/mes → 9,99 €/mes'), 'baja'),
    (LINE.replace('nuevo', 'sube'), '→'),
    (LINE.replace('9,99 €/mes', '8 €/mes → 9 €/mes'), '→'),
    (LINE.replace('| Go |', '| Business |'), 'empresa'),
    (LINE.replace('| Go |', '| Team Standard |'), 'empresa'),
    (LINE.replace('ChatGPT Go llega a España.', 'palabra ' * 31), '30 palabras'),
    (LINE.replace('ChatGPT Go llega a España.', 'Lo hemos probado.'), 'hemos probado'),
    (LINE.replace('https://openai.com/index/go/', 'https://pricingsaas.com/chatgpt'), 'pricingsaas.com'),
    (LINE.replace('https://openai.com/index/go/', 'http://openai.com/x'), 'https'),
    (LINE.replace('https://openai.com/index/go/', 'https://web.archive.org/web/2025/https://midjourney.com/'),
     'copia archivada'),
    (LINE.replace('https://openai.com/index/go/', 'https://notopenai.com/x'), 'notopenai.com'),
    (LINE + '\n' + LINE, 'repetido'),
])
def test_history_errors(tmp_path, line, needle):
    with pytest.raises(ValueError) as e:
        check(tmp_path, line)
    assert needle in str(e.value) and 'historial-precios.md: línea' in str(e.value)


@pytest.mark.parametrize('source', [
    'https://www.xataka.com/x', 'https://www.xatakandroid.com/x', 'https://techcrunch.com/x',
    'https://help.openai.com/x', 'https://chatgpt.com/es-ES/pricing/', ARCHIVE,
])
def test_allowed_sources(tmp_path, source):
    check(tmp_path, LINE.replace('https://openai.com/index/go/', source))


def test_archive_url_variants(tmp_path):
    for inner in ('http://chatgpt.com/pricing', 'https://www.chatgpt.com/pricing', 'chatgpt.com/pricing'):
        check(tmp_path, LINE.replace('https://openai.com/index/go/', f'https://web.archive.org/web/20250101id_/{inner}'))


def test_current_month_is_valid(tmp_path):
    check(tmp_path, LINE.replace('2025-11', '2026-10'))
    check(tmp_path, LINE.replace('2025-11', '2026-10-08'))


def test_optional_price_kinds(tmp_path):
    check(tmp_path, LINE.replace('nuevo | Go | 9,99 €/mes', 'retirado | Go | '))
    check(tmp_path, LINE.replace('nuevo | Go | 9,99 €/mes', 'condiciones | Go | 8 €/mes'))
    check(tmp_path, LINE.replace('nuevo | Go | 9,99 €/mes', 'sube | Go | 20 $/mes → 23 €/mes'))


@pytest.mark.parametrize('mutate, needle', [
    (lambda s: s['herramientas'].pop('claude'), 'claude'),
    (lambda s: s['herramientas']['chatgpt']['planes'].update(Go='9 €/mes'), '9 €'),
    (lambda s: s['herramientas']['chatgpt']['planes'].update(Go='ocho euros'), 'precio'),
    (lambda s: s['herramientas']['chatgpt']['planes'].update(Business='0 €'), 'empresa'),
    (lambda s: s['herramientas']['chatgpt'].update(fuente='https://www.xataka.com/x'), 'oficial'),
    (lambda s: s['herramientas'].update(zeta={'fuente': 'https://zeta.com', 'planes': {'Free': '0 €'}}), 'zeta'),
])
def test_snapshot_errors(tmp_path, mutate, needle):
    data = json.loads(json.dumps(SNAP))
    mutate(data)
    with pytest.raises(ValueError) as e:
        check(tmp_path, LINE, ('2026-10-06.json', data))
    assert needle in str(e.value) and 'tomas-precios/2026-10-06.json' in str(e.value)


def test_latest_snapshot_must_cover_fichas(tmp_path):
    old = json.loads(json.dumps(SNAP))
    new = json.loads(json.dumps(SNAP))
    new['herramientas'].pop('claude')
    with pytest.raises(ValueError, match=r'tomas-precios/2026-10-07\.json: falta la herramienta «claude»'):
        check(tmp_path, LINE, ('2026-10-06.json', old), ('2026-10-07.json', new))


def test_old_snapshot_prices_need_not_match_fichas(tmp_path):
    old = json.loads(json.dumps(SNAP))
    old['herramientas']['chatgpt']['planes']['Go'] = '9,99 €/mes'
    check(tmp_path, LINE, ('2026-01-06.json', old), ('2026-10-06.json', SNAP))


def test_snapshot_name_and_empty_dir(tmp_path):
    with pytest.raises(ValueError, match='AAAA-MM-DD'):
        snaps(tmp_path, ('octubre.json', SNAP))
    empty = tmp_path / 'vacio'
    empty.mkdir()
    with pytest.raises(ValueError, match='ninguna toma'):
        validate_history([], load_snapshots(empty), FICHAS, TODAY)


def test_auto_changes(tmp_path):
    old = json.loads(json.dumps(SNAP))
    old['herramientas']['chatgpt']['planes'].update(Go='9,99 €/mes', Plus='22 €/mes', Viejo='5 €/mes')
    old['herramientas']['chatgpt']['planes'].pop('Pro')
    old['herramientas']['claude']['planes']['Pro'] = '17 $/mes (anual)'
    found = {(c.tool, c.plan): c for c in auto_changes(snaps(tmp_path, ('2026-01-06.json', old),
                                                                  ('2026-10-06.json', SNAP)), [])}
    assert found[('chatgpt', 'Go')].kind == 'baja' and found[('chatgpt', 'Go')].before.amount == Decimal('9.99')
    assert found[('chatgpt', 'Plus')].kind == 'sube'
    assert found[('chatgpt', 'Pro')].kind == 'nuevo' and found[('chatgpt', 'Viejo')].kind == 'retirado'
    cond = found[('claude', 'Pro')]
    assert cond.kind == 'condiciones' and 'pasa de 17 $/mes (anual) a 20 $/mes' in cond.text
    go = found[('chatgpt', 'Go')]
    assert go.auto and go.date == '2026-10-06' and go.source == 'https://chatgpt.com/es-ES/pricing/'
    assert go.text == 'Detectado en nuestra revisión del 6 de octubre de 2026.'
    assert ('chatgpt', 'Gratis') not in found and len(found) == 5


def test_auto_change_not_duplicated(tmp_path):
    old = json.loads(json.dumps(SNAP))
    old['herramientas']['chatgpt']['planes']['Go'] = '9,99 €/mes'
    manual = parse_history('2026-10 | chatgpt | baja | Go | 9,99 €/mes → 8 €/mes | Baja. | https://chatgpt.com/x')
    s = snaps(tmp_path, ('2026-01-06.json', old), ('2026-10-06.json', SNAP))
    assert auto_changes(s, manual) == []
    manual_sept = parse_history('2026-09 | chatgpt | baja | Go | 9,99 €/mes → 8 €/mes | Baja. | https://chatgpt.com/x')
    assert len(auto_changes(s, manual_sept)) == 1


def test_first_snapshot_has_no_auto_changes(tmp_path):
    assert auto_changes(snaps(tmp_path, ('2026-10-06.json', SNAP)), []) == []


def test_chart_points(tmp_path):
    s = snaps(tmp_path, ('2026-10-06.json', SNAP))
    changes = parse_history(LINE + '\n2026-08 | chatgpt | baja | Go | 9,99 €/mes → 8 €/mes | B. | https://chatgpt.com/x')
    chart = chart_points(changes, s, 'chatgpt')
    assert chart['plan'] == 'Go' and (chart['currency'], chart['period']) == ('€', '/mes')
    assert [(d, str(p.amount)) for d, p in chart['points']] == [('2025-11', '9.99'), ('2026-08', '8'), ('2026-10-06', '8')]


def test_chart_needs_two_points(tmp_path):
    s = snaps(tmp_path, ('2026-10-06.json', SNAP))
    assert chart_points([], s, 'chatgpt') is None


def test_chart_skips_mixed_currency(tmp_path):
    s = snaps(tmp_path, ('2026-10-06.json', SNAP))
    changes = parse_history('2023-02 | chatgpt | nuevo | Plus | 20 $/mes | Nace Plus. | https://openai.com/x')
    assert chart_points(changes, s, 'chatgpt') is None
    changes += parse_history('2024-02 | chatgpt | sube | Plus | 20 $/mes → 22 €/mes | Cambio. | https://openai.com/y')
    chart = chart_points(changes, s, 'chatgpt')
    assert chart['plan'] == 'Plus' and {p.currency for _, p in chart['points']} == {'€'}
    assert [d for d, _ in chart['points']] == ['2024-02', '2026-10-06']


def test_real_snapshot_and_history_are_valid():
    from radar.content import load_pages
    fichas = {p.slug: p for p in load_pages(ROOT / 'content') if p.kind == 'ficha' and p.indexable}
    snapshots = load_snapshots(ROOT / 'data' / 'tomas-precios')
    changes = parse_history((ROOT / 'data' / 'historial-precios.md').read_text(encoding='utf-8'))
    validate_history(changes, snapshots, fichas, date.today())
    assert set(snapshots[-1].tools) == set(fichas) and len(fichas) == 15


def test_build_requires_both_history_files(tmp_path):
    from scripts.build import build
    from tests.test_build import make_root
    root = make_root(tmp_path)
    (root / 'data' / 'tomas-precios').mkdir()
    with pytest.raises(ValueError, match='historial-precios.md'):
        build(root, tmp_path / '_site')


def test_build_requires_data_for_page(tmp_path):
    from scripts.build import build
    from tests.test_build import make_root
    root = make_root(tmp_path)
    (root / 'content' / 'paginas' / 'historial-de-precios.md').write_text('titulo: H\ndescripcion: d\n\nTexto',
                                                                         encoding='utf-8')
    with pytest.raises(ValueError, match='tomas-precios'):
        build(root, tmp_path / '_site')


def test_build_rejects_snapshot_out_of_sync(tmp_path):
    import shutil
    from scripts.build import build
    real = ROOT / 'data' / 'tomas-precios' / '2026-10-06.json'
    data = json.loads(real.read_text(encoding='utf-8'))
    data['herramientas']['chatgpt']['planes']['Go'] = '7 €/mes'
    work = tmp_path / 'repo'
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('.git', '.venv', '_site', '__pycache__', 'node_modules'))
    (work / 'data' / 'tomas-precios' / '2026-10-06.json').write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(ValueError, match=r'«chatgpt» Go: el precio «7 €» no aparece en la ficha'):
        build(work, tmp_path / '_site')
