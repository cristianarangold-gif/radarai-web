from pathlib import Path

from radar.models import Redirect
from radar.redirects import load_redirects, output_paths, render_redirect
from radar.render import make_env

ROOT = Path(__file__).resolve().parent.parent


def test_index_html_source_normalized(tmp_path):
    f = tmp_path / 'r.yml'
    f.write_text('# comentario\n/herramientas/runway/index.html: /#cat-video\nrankings: /mejor-ia/\n\n',
                 encoding='utf-8')
    assert load_redirects(f) == [Redirect('/herramientas/runway/', '/#cat-video'),
                                 Redirect('/rankings/', '/mejor-ia/')]


def test_output_paths_for_directory_source():
    assert output_paths(Redirect('/rankings/', '/mejor-ia/')) == ['rankings/index.html']


def test_legal_html_source_outputs_both_paths(tmp_path):
    f = tmp_path / 'r.yml'
    f.write_text('/legal/aviso-legal.html: /legal/aviso-legal/\n', encoding='utf-8')
    (r,) = load_redirects(f)
    assert r.source == '/legal/aviso-legal.html'
    assert output_paths(r) == ['legal/aviso-legal.html']


def test_redirect_html_has_refresh_canonical_noindex():
    html = render_redirect(make_env(ROOT / 'templates'), Redirect('/rankings/', '/mejor-ia/'))
    assert '<meta http-equiv="refresh" content="0; url=/mejor-ia/">' in html
    assert '<link rel="canonical" href="https://radarai.es/mejor-ia/">' in html
    assert '<meta name="robots" content="noindex,follow">' in html
    assert 'href="/mejor-ia/"' in html


def test_project_redirects_file_loads():
    rs = load_redirects(ROOT / 'data' / 'redirects.yml')
    sources = {r.source for r in rs}
    assert {'/rankings/', '/reviews/', '/precios/', '/alternativas/', '/cambios/',
            '/publicacion/', '/preguntas-frecuentes/', '/legal/aviso-legal.html'} <= sources
