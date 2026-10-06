import json
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
    assert 'url=/#cat-video' in html


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
