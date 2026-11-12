import re
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


def test_main_feature_goes_first_in_ficha():
    text = (block('Zeta', id='z', ficha='chatgpt', principal='si') + block('Alfa', id='a', ficha='chatgpt', es='no', ue='no'))
    ctx = availability_context(parse_availability(text), TODAY)
    assert [r.title for r in ctx['by_ficha']['chatgpt']] == ['Zeta', 'Alfa']
    assert [r.title for r in ctx['rows']] == ['Alfa', 'Zeta']


def test_rejects_two_main_features_in_same_ficha():
    text = block('A', id='a', ficha='chatgpt', principal='si') + block('B', id='b', ficha='chatgpt', principal='si')
    with pytest.raises(ValueError, match='principal'):
        check(text)


def test_rejects_main_feature_without_ficha_or_bad_value():
    for extra in ({'principal': 'si'}, {'ficha': 'chatgpt', 'principal': 'sí'}):
        with pytest.raises(ValueError, match='principal'):
            check(block('A', id='a', **extra))


def _row(row_id):
    return next(f for f in _features() if f.id == row_id)


def test_real_gemini_in_chrome_is_not_available_in_spain():
    row = _row('gemini-en-chrome')
    assert (row.eeuu, row.ue, row.es) == ('si', 'no', 'no')


def test_real_recall_cites_the_eea_announcement():
    row = _row('recall-windows')
    assert row.es == 'si' and any('kb5062660' in u for u in row.fuentes)


def test_real_copilot_is_not_deduced_from_prices():
    assert _row('microsoft-copilot').es == 'sin_confirmar'


def test_real_siri_separates_mac_from_mobile():
    assert _row('siri-ai').title == 'Siri AI en iPhone, iPad y Apple Watch'
    mac = _row('siri-ai-mac')
    assert (mac.ue, mac.es) == ('sin_confirmar', 'sin_confirmar')
    assert mac.fuentes == ['https://www.apple.com/macos/feature-availability/']


def test_real_computer_history_note_matches_release_notes():
    assert 'solo para Pro en' in _row('chatgpt-computer-history').nota


def test_rows_clear_the_sticky_header():
    css = (ROOT / 'static' / 'css' / 'radar.css').read_text(encoding='utf-8')
    assert re.search(r'\.avail-table tbody tr \{[^}]*scroll-margin-top: 90px', css)


def test_real_data_has_minimum():
    features = parse_availability((ROOT / 'data' / 'disponibilidad.md').read_text(encoding='utf-8'))
    assert len(features) >= 12
    assert all(f.fuentes and f.comprobado for f in features)


def test_feature_display_helpers():
    f = parse_availability(block(fuentes='https://www.apple.com/es/ios/, '
                                         'https://web.archive.org/web/20261020120000/https://www.apple.com/es/ios/'))[0]
    assert f.fecha == '4 de noviembre de 2026' and f.empresa_nombre == 'Apple'
    assert [label for label, _ in f.links] == ['apple.com', 'copia archivada']


@pytest.fixture(scope='module')
def site():
    import subprocess
    import sys
    import tempfile
    out = Path(tempfile.mkdtemp()) / 'site'
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build.py'), '--out', str(out)], check=True,
                   capture_output=True)
    return out


@pytest.fixture(scope='module')
def page(site):
    return (site / 'funciona-en-espana' / 'index.html').read_text(encoding='utf-8')


def _features():
    return parse_availability((ROOT / 'data' / 'disponibilidad.md').read_text(encoding='utf-8'))


def test_page_lists_all_rows_without_js(page):
    rows = page.split('<tbody')[1].split('</tbody>')[0]
    assert rows.count('<tr') == len(_features())
    for f in _features():
        assert f'id="{f.id}"' in rows and f'data-es="{f.es}"' in rows
    assert '<caption' in page and 'scope="col"' in page and 'scope="row"' in page


def test_controls_hidden_in_html(page):
    import re
    assert re.search(r'<form class="avail-controls"[^>]*\bhidden\b', page)
    for attr in ('data-avail-search', 'data-avail-count'):
        assert attr in page
    for value in ('todas', 'no', 'parcial', 'sin_confirmar', 'si'):
        assert f'data-avail-filter="{value}"' in page
    assert 'js/availability.js' in page


def test_sources_and_dates_rendered(page):
    siri = page.split('id="siri-ai"')[1].split('</tr>')[0]
    assert '✕ No disponible' in siri and '4 de noviembre de 2026' in siri
    assert 'href="https://www.apple.com/ios/feature-availability/"' in siri
    assert 'href="/noticias/siri-ai-espanol-ios-27-2/"' in siri


def test_page_has_empty_state(page):
    import re
    assert re.search(r'<p[^>]*data-avail-empty[^>]*\bhidden\b', page)
    assert re.search(r'<p[^>]*data-avail-count[^>]*aria-live="polite"', page)


def test_page_indexable_and_in_sitemap(site, page):
    assert 'noindex' not in page.split('</head>')[0]
    assert '<loc>https://radarai.es/funciona-en-espana/</loc>' in (site / 'sitemap.xml').read_text()


def test_own_text_has_400_words():
    text = (ROOT / 'content' / 'paginas' / 'funciona-en-espana.md').read_text(encoding='utf-8')
    assert len(text.split()) >= 400


def test_js_has_no_innerhtml():
    assert 'innerHTML' not in (ROOT / 'static' / 'js' / 'availability.js').read_text(encoding='utf-8')


def test_js_folds_accents():
    assert "normalize('NFD')" in (ROOT / 'static' / 'js' / 'availability.js').read_text(encoding='utf-8')


def test_stale_badge_rendered(tmp_path):
    import shutil
    from scripts.build import build
    work = tmp_path / 'repo'
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('.git', '.venv', '_site', '__pycache__', '.superpowers'))
    data = work / 'data' / 'disponibilidad.md'
    data.write_text(data.read_text(encoding='utf-8').replace('id: claude\nempresa: anthropic\nficha: claude\neeuu: si\nue: si\nes: si\ncomprobado: 2026-11-04',
                                                              'id: claude\nempresa: anthropic\nficha: claude\neeuu: si\nue: si\nes: si\ncomprobado: 2026-01-01'),
                    encoding='utf-8')
    build(work, tmp_path / '_site')
    html = (tmp_path / '_site' / 'funciona-en-espana' / 'index.html').read_text(encoding='utf-8')
    assert 'Pendiente de revisar' in html.split('id="claude"')[1].split('</tr>')[0]
    assert 'Pendiente de revisar' not in html.split('id="chatgpt"')[1].split('</tr>')[0]


def test_home_links_page(site):
    assert 'href="/funciona-en-espana/"' in (site / 'index.html').read_text(encoding='utf-8')


def test_start_links_page(site):
    assert 'href="/funciona-en-espana/"' in (site / 'empieza-aqui' / 'index.html').read_text(encoding='utf-8')


def test_box_in_ficha_with_features(site):
    html = (site / 'herramientas' / 'gemini' / 'index.html').read_text(encoding='utf-8')
    box = html.split('class="tool-duels tool-avail"')[1].split('</nav>')[0]
    assert 'Disponibilidad en España' in box and box.count('<li') == 3
    assert '✕ No disponible' in box and 'href="/funciona-en-espana/#' in box
    assert 'href="/funciona-en-espana/">' in box


def test_box_shows_main_feature_first_and_counts_the_rest(site):
    html = (site / 'herramientas' / 'gemini' / 'index.html').read_text(encoding='utf-8')
    box = html.split('class="tool-duels tool-avail"')[1].split('</nav>')[0]
    first = box.split('<li')[1]
    assert '#gemini-app' in first and '✓ Disponible' in first
    assert 'Ver las otras 4 en la tabla completa' in box


def test_box_absent_without_features(site):
    assert 'tool-avail' not in (site / 'herramientas' / 'suno' / 'index.html').read_text(encoding='utf-8')


def test_search_index_has_features(site):
    import json
    idx = json.loads((site / 'search-index.json').read_text(encoding='utf-8'))
    entries = [e for e in idx if e['k'] == 'Disponibilidad']
    assert len(entries) == len(_features())
    siri = [e for e in entries if e['u'] == '/funciona-en-espana/#siri-ai'][0]
    assert siri['t'] == 'Siri AI en iPhone, iPad y Apple Watch' and siri['d'].startswith('España: ✕ No disponible')
    assert "'Disponibilidad'" in (ROOT / 'static' / 'js' / 'search.js').read_text(encoding='utf-8')


def test_nav_unchanged():
    from radar.render import NAV
    assert '/funciona-en-espana/' not in [url for _, url in NAV]


def test_routine_and_guide_document_it():
    for doc in ('docs/rutina-noticias.md', 'content/GUIA_EDITORIAL.md', 'README.md'):
        assert 'data/disponibilidad.md' in (ROOT / doc).read_text(encoding='utf-8'), doc
