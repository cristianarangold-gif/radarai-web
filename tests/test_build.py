import json
import re
import shutil
from pathlib import Path

import pytest

from scripts.build import build

ROOT = Path(__file__).resolve().parent.parent


def make_root(tmp_path):
    root = tmp_path / 'root'
    root.mkdir()
    (root / 'templates').symlink_to(ROOT / 'templates')
    shutil.copytree(ROOT / 'static', root / 'static')
    (root / 'static' / 'utilidades').mkdir(exist_ok=True)
    (root / 'static' / 'utilidades' / 'index.html').write_text(
        '<!doctype html><html lang="es"><head><title>U</title>'
        '<meta name="robots" content="noindex,follow"></head><body></body></html>')
    (root / 'content' / 'paginas' / 'legal').mkdir(parents=True)
    for slug in ('sobre', 'autor', 'metodologia', 'politica-editorial', 'contacto',
                 'legal/aviso-legal', 'legal/politica-privacidad', 'legal/politica-cookies'):
        (root / 'content' / 'paginas' / f'{slug}.md').write_text(
            f'titulo: Página {slug}\ndescripcion: Descripción {slug}\n\nTexto', encoding='utf-8')
    (root / 'content' / 'noticias').mkdir()
    (root / 'data').mkdir()
    (root / 'content' / 'paginas' / 'inicio.md').write_text(
        'titulo: Inicio\ndescripcion: Portada\n\n<div id="preguntas-frecuentes">FAQ</div>', encoding='utf-8')
    (root / 'content' / 'noticias' / 'buena.md').write_text(
        'titulo: Buena\ndescripcion: d1\nfecha: 2026-10-01\n\n' + 'palabra ' * 600, encoding='utf-8')
    (root / 'content' / 'noticias' / 'borrador.md').write_text(
        'titulo: Borrador\ndescripcion: d2\nfecha: 2026-10-02\nborrador: si\n\ncorto', encoding='utf-8')
    tools = {
        'claude': dict(name='Claude', cat='ia-general', desc='x', price='freemium', level='', platform='web',
                       lang='multi', tags=[], url='https://claude.ai/'),
        'runway': dict(name='Runway', cat='video', desc='x', price='freemium', level='', platform='web',
                       lang='en', tags=[], url='https://runwayml.com/'),
    }
    (root / 'data' / 'tools.json').write_text(json.dumps(tools), encoding='utf-8')
    (root / 'data' / 'brands.json').write_text(json.dumps({
        'openai': dict(name='OpenAI', color='#10a37f', icon=None, monograma='O'),
        'claude': dict(name='Claude', color='#d97757', icon='claude', monograma='C'),
    }), encoding='utf-8')
    (root / 'data' / 'redirects.yml').write_text('/rankings/: /noticias/\n', encoding='utf-8')
    (root / 'ads.txt').write_text('google.com, pub-1, DIRECT, f08c47fec0942fa0\n')
    (root / 'CNAME').write_text('radarai.es')
    return root


def test_build_outputs_expected_files(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    for rel in ('index.html', 'noticias/index.html', 'noticias/buena/index.html', 'noticias/borrador/index.html',
                'sitemap.xml', 'rss.xml', 'robots.txt', '404.html', 'ads.txt', 'CNAME',
                'static/css/radar.css', 'rankings/index.html'):
        assert (out / rel).exists(), rel
    sm = (out / 'sitemap.xml').read_text()
    assert '/noticias/buena/' in sm and 'borrador' not in sm
    assert 'Sitemap: https://radarai.es/sitemap.xml' in (out / 'robots.txt').read_text()
    assert 'href="/noticias/buena/"' in (out / 'index.html').read_text()


def test_build_passes_check(tmp_path):
    from radar.check import check_site
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    assert check_site(out) == []


def test_old_tool_url_redirects(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    html = (out / 'herramientas' / 'runway' / 'index.html').read_text()
    assert 'url=/herramientas/#cat-video' in html


def test_duplicate_output_path_raises(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'data' / 'redirects.yml').write_text('/noticias/buena/: /\n', encoding='utf-8')
    with pytest.raises(ValueError, match='noticias/buena/index.html') as exc:
        build(root, out)
    assert 'content /noticias/buena/' in str(exc.value) and 'redirección' in str(exc.value)


def test_404_has_no_canonical(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    assert 'rel="canonical"' not in (out / '404.html').read_text()


def test_refuses_out_dir_with_sources(tmp_path):
    root = make_root(tmp_path)
    (root / 'scripts').mkdir()
    (root / 'scripts' / 'build.py').write_text('')
    with pytest.raises(ValueError, match='código fuente'):
        build(root, root)


def test_utilities_listing(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'static' / 'utilidades' / 'index.html').unlink()
    (root / 'content' / 'utilidades').mkdir()
    (root / 'content' / 'utilidades' / 'contador.md').write_text(
        'titulo: Contador\ndescripcion: Cuenta palabras\n\n' + 'palabra ' * 320, encoding='utf-8')
    build(root, out)
    assert 'href="/herramientas-radar/contador/"' in (out / 'herramientas-radar' / 'index.html').read_text()


def test_home_shows_featured_sections(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'content' / 'mejor-ia').mkdir()
    (root / 'content' / 'mejor-ia' / 'mejor-ia-para-x.md').write_text(
        'titulo: Comparativa X\ndescripcion: dx\n\n' + 'palabra ' * 1300, encoding='utf-8')
    (root / 'content' / 'guias').mkdir()
    (root / 'content' / 'guias' / 'guia-y.md').write_text(
        'titulo: Guía Y\ndescripcion: dy\n\n' + 'palabra ' * 1300, encoding='utf-8')
    build(root, out)
    home = (out / 'index.html').read_text()
    assert 'href="/mejor-ia-para-x/"' in home
    assert 'href="/guias/guia-y/"' in home


def test_news_with_unknown_tool_fails_build(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'content' / 'noticias' / 'buena.md').write_text(
        'titulo: Buena\ndescripcion: d1\nfecha: 2026-10-01\nherramientas: inexistente\n\n' + 'palabra ' * 600,
        encoding='utf-8')
    with pytest.raises(ValueError, match='noticias/buena: herramienta desconocida «inexistente»'):
        build(root, out)


def test_draft_news_is_validated_too(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'content' / 'noticias' / 'borrador.md').write_text(
        'titulo: Borrador\ndescripcion: d2\nfecha: 2026-10-02\nborrador: si\nempresa: openia\n\ncorto',
        encoding='utf-8')
    with pytest.raises(ValueError, match='empresa desconocida «openia»'):
        build(root, out)


def test_imprescindibles_with_unknown_url_fails_build(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'data' / 'imprescindibles.txt').write_text('/no-existe/\n', encoding='utf-8')
    with pytest.raises(ValueError, match='/no-existe/'):
        build(root, out)


def test_og_images_generated_and_declared(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    assert (out / 'og' / 'inicio.png').exists() and (out / 'og' / 'noticias' / 'buena.png').exists()
    assert not (out / 'og' / 'noticias' / 'borrador.png').exists()
    html = (out / 'noticias' / 'buena' / 'index.html').read_text()
    assert '<meta property="og:image" content="https://radarai.es/og/noticias/buena.png">' in html
    assert '<meta name="twitter:card" content="summary_large_image">' in html
    assert '"image": "https://radarai.es/og/noticias/buena.png"' in html
    assert 'og:image' not in (out / '404.html').read_text()


def test_no_google_fonts_anywhere(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    for f in out.rglob('*.html'):
        assert 'Google Fonts' not in f.read_text() and 'fonts.googleapis' not in f.read_text(), f


def test_real_legal_pages_do_not_mention_google_fonts():
    for name in ('politica-cookies', 'politica-privacidad'):
        assert 'Google Fonts' not in (ROOT / 'content' / 'paginas' / 'legal' / f'{name}.md').read_text()


def test_css_defines_editorial_tokens():
    css = (ROOT / 'static' / 'css' / 'radar.css').read_text()
    for token in ('--paper: #fbf8f3', '--paper-2: #f3ece0', '--ink: #151515', '--ink-2: #444',
                  '--rule: #e0d9cc', '--accent: #e4572e', '--amber: #f3a712'):
        assert token in css, token
    assert css.count('@font-face') == 7 and 'font-display: swap' in css


def test_home_radar_and_catalog_in_tools_page(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'content' / 'herramientas').mkdir()
    (root / 'content' / 'herramientas' / 'claude.md').write_text(
        'titulo: Claude\ndescripcion: dc\nfecha: 2026-10-01\nideal_para: Escribir\nprecio_desde: 0 $\n\n'
        + 'palabra ' * 1100, encoding='utf-8')
    (root / 'data' / 'imprescindibles.txt').write_text('/herramientas/claude/\n', encoding='utf-8')
    build(root, out)
    home = (out / 'index.html').read_text()
    assert 'class="radar"' in home and 'En el radar esta semana' in home
    blips = re.findall(r'<a class="blip" href="([^"]+)"', home)
    assert blips == ['/herramientas/claude/']  # solo herramientas con ficha
    assert 'Imprescindibles' in home and 'id="cat-' not in home
    assert 'href="/herramientas/"' in home and '0 $' in home
    tools_page = (out / 'herramientas' / 'index.html').read_text()
    assert 'id="cat-ia-general"' in tools_page and '/static/js/catalog.js' in tools_page


def test_404_is_radar_page_without_canonical(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    html = (out / '404.html').read_text()
    assert 'Esta página ha desaparecido del radar' in html and 'class="radar' in html
    assert 'rel="canonical"' not in html and 'href="/noticias/"' in html


def test_news_listing_has_covers(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    html = (out / 'noticias' / 'index.html').read_text()
    assert html.count('<svg class="cover"') == 1 and 'href="/noticias/buena/"' in html


def test_radar_labels_keep_readable_opacity():
    css = (ROOT / 'static' / 'css' / 'radar.css').read_text()
    block = css[css.index('@keyframes radar-ping'):]
    block = block[:block.index('}\n') + 2]
    rule = css[css.index('.blip-in {'):]
    rule = rule[:rule.index('}')]
    import re as _re
    values = [float(v) for v in _re.findall(r'opacity:\s*([\d.]+)', block + rule)]
    assert values and min(values) >= .75, values


def test_real_fichas_price_pill_reads_well():
    from radar.content import load_pages
    for p in load_pages(ROOT / 'content'):
        if p.kind == 'ficha':
            assert not p.extra.get('plan_pago', '').lower().startswith('desde'), p.slug


def test_catalog_js_does_not_yank_reader_after_load():
    js = (ROOT / 'static' / 'js' / 'catalog.js').read_text()
    assert 'scrollY' in js


def test_search_index_written_and_linked(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    idx = json.loads((out / 'search-index.json').read_text())
    urls = {e['u'] for e in idx}
    assert '/noticias/buena/' in urls and '/' not in urls and '/noticias/' not in urls
    assert '/noticias/borrador/' not in urls and '/herramientas/#cat-video' in urls
    assert 'search-index.json?v=' in (out / 'noticias' / 'buena' / 'index.html').read_text()


def test_search_page_noindex_not_in_sitemap(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    html = (out / 'buscar' / 'index.html').read_text()
    assert 'name="robots" content="noindex' in html and '¿Qué estás buscando?' in html
    assert 'id="search-page-input"' in html and 'data-search-page' in html
    assert 'El buscador necesita JavaScript' in html and 'og:image' not in html
    assert '/buscar/' not in (out / 'sitemap.xml').read_text()


def test_header_has_search_link(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    build(root, out)
    assert 'class="search-open" href="/buscar/"' in (out / 'index.html').read_text()


def test_invalid_assistant_data_fails_build(tmp_path):
    root, out = make_root(tmp_path), tmp_path / '_site'
    (root / 'data' / 'asistente.json').write_text('{"tareas": {}, "reglas": {}}', encoding='utf-8')
    with pytest.raises(ValueError, match='asistente.json: falta la tarea escribir'):
        build(root, out)
