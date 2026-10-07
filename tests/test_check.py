from radar.check import check_site

GOOD = ('<!doctype html><html lang="es"><head><title>{title}</title>'
        '<meta name="description" content="{desc}"><link rel="canonical" href="https://radarai.es{url}">'
        '{robots}{og}<meta name="radar:kind" content="{kind}"><meta name="radar:words" content="{words}">'
        '</head><body>{body}</body></html>')


def page(site, rel, url, title='T', desc=None, kind='pagina', words=10, body='', robots='', og=None):
    desc = desc or f'Descripción {title}'
    if og is None:
        img = 'og/' + (rel.replace('/index.html', '').replace('index.html', 'inicio') or 'inicio') + '.png'
        (site / img).parent.mkdir(parents=True, exist_ok=True)
        (site / img).write_bytes(b'png')
        og = f'<meta property="og:image" content="https://radarai.es/{img}">'
    p = site / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(GOOD.format(title=title, desc=desc, url=url, kind=kind, words=words,
                             body=body, robots=robots, og=og), encoding='utf-8')


def sitemap(site, *urls):
    locs = ''.join(f'<url><loc>https://radarai.es{u}</loc></url>' for u in urls)
    (site / 'sitemap.xml').write_text(f'<urlset>{locs}</urlset>', encoding='utf-8')


def test_clean_site_has_no_errors(tmp_path):
    page(tmp_path, 'index.html', '/', body='<a href="/a/">a</a> <a href="/a/#cat-x">c</a>')
    page(tmp_path, 'a/index.html', '/a/', title='A', body='<details id="cat-x"></details>')
    sitemap(tmp_path, '/', '/a/')
    assert check_site(tmp_path) == []


def test_uppercase_or_lowercase_doctype_ok(tmp_path):
    page(tmp_path, 'index.html', '/')
    s = (tmp_path / 'index.html').read_text().replace('<!doctype html>', '<!DOCTYPE html>')
    (tmp_path / 'index.html').write_text(s)
    sitemap(tmp_path, '/')
    assert check_site(tmp_path) == []


def test_missing_doctype_reported(tmp_path):
    page(tmp_path, 'index.html', '/')
    s = (tmp_path / 'index.html').read_text().replace('<!doctype html>', '')
    (tmp_path / 'index.html').write_text(s)
    sitemap(tmp_path, '/')
    assert any('DOCTYPE' in e for e in check_site(tmp_path))


def test_broken_internal_link_reported(tmp_path):
    page(tmp_path, 'index.html', '/', body='<a href="/no-existe/">x</a>')
    sitemap(tmp_path, '/')
    errors = check_site(tmp_path)
    assert any('/no-existe/' in e for e in errors)


def test_static_file_link_ok(tmp_path):
    page(tmp_path, 'index.html', '/', body='<a href="/rss.xml">rss</a>')
    (tmp_path / 'rss.xml').write_text('<rss/>')
    sitemap(tmp_path, '/')
    assert check_site(tmp_path) == []


def test_literal_escape_reported(tmp_path):
    page(tmp_path, 'index.html', '/', body='<p>v\\u00eddeo</p>')
    sitemap(tmp_path, '/')
    assert any('\\u' in e for e in check_site(tmp_path))


def test_short_indexable_page_reported(tmp_path):
    page(tmp_path, 'index.html', '/', kind='guia', words=40)
    sitemap(tmp_path, '/')
    assert any('palabras' in e for e in check_site(tmp_path))


def test_noindex_page_skips_word_minimum(tmp_path):
    page(tmp_path, 'index.html', '/')
    page(tmp_path, 'g/index.html', '/g/', title='G', kind='guia', words=40,
         robots='<meta name="robots" content="noindex,follow">')
    sitemap(tmp_path, '/')
    assert check_site(tmp_path) == []


def test_duplicate_title_reported(tmp_path):
    page(tmp_path, 'index.html', '/', title='Igual')
    page(tmp_path, 'a/index.html', '/a/', title='Igual')
    sitemap(tmp_path, '/', '/a/')
    assert any('duplicado' in e for e in check_site(tmp_path))


def test_sitemap_url_missing_reported(tmp_path):
    page(tmp_path, 'index.html', '/')
    sitemap(tmp_path, '/', '/fantasma/')
    assert any('/fantasma/' in e for e in check_site(tmp_path))


def test_sitemap_url_noindex_reported(tmp_path):
    page(tmp_path, 'index.html', '/')
    page(tmp_path, 'g/index.html', '/g/', title='G', robots='<meta name="robots" content="noindex,follow">')
    sitemap(tmp_path, '/', '/g/')
    assert any('/g/' in e for e in check_site(tmp_path))


def test_redirect_pages_skipped(tmp_path):
    page(tmp_path, 'index.html', '/')
    (tmp_path / 'old').mkdir()
    (tmp_path / 'old' / 'index.html').write_text(
        '<html><head><meta http-equiv="refresh" content="0; url=/"></head></html>')
    sitemap(tmp_path, '/')
    assert check_site(tmp_path) == []


def test_double_escaped_entity_reported(tmp_path):
    page(tmp_path, 'index.html', '/', title='Guía &amp;amp; trucos')
    sitemap(tmp_path, '/')
    assert any('doble escape' in e for e in check_site(tmp_path))


def test_redirect_to_missing_target_reported(tmp_path):
    page(tmp_path, 'index.html', '/')
    (tmp_path / 'old').mkdir()
    (tmp_path / 'old' / 'index.html').write_text(
        '<html><head><meta http-equiv="refresh" content="0; url=/no-existe/"></head></html>')
    sitemap(tmp_path, '/')
    assert any('/no-existe/' in e for e in check_site(tmp_path))


def test_redirect_to_missing_category_anchor_reported(tmp_path):
    page(tmp_path, 'index.html', '/', body='<details id="cat-video"></details>')
    (tmp_path / 'old').mkdir()
    (tmp_path / 'old' / 'index.html').write_text(
        '<html><head><meta http-equiv="refresh" content="0; url=/#cat-nada"></head></html>')
    sitemap(tmp_path, '/')
    assert any('#cat-nada' in e for e in check_site(tmp_path))


def test_indexable_page_without_og_image(tmp_path):
    page(tmp_path, 'index.html', '/', og='')
    sitemap(tmp_path, '/')
    assert any('falta og:image' in e for e in check_site(tmp_path))


def test_og_image_must_exist(tmp_path):
    page(tmp_path, 'index.html', '/', og='<meta property="og:image" content="https://radarai.es/og/nada.png">')
    sitemap(tmp_path, '/')
    assert any('og:image inexistente' in e for e in check_site(tmp_path))


def test_noindex_page_needs_no_og_image(tmp_path):
    page(tmp_path, 'index.html', '/')
    page(tmp_path, 'b/index.html', '/b/', title='B', og='', robots='<meta name="robots" content="noindex,follow">')
    sitemap(tmp_path, '/')
    assert check_site(tmp_path) == []


def test_redirect_to_missing_catalog_anchor(tmp_path):
    page(tmp_path, 'index.html', '/')
    page(tmp_path, 'herramientas/index.html', '/herramientas/', title='H', body='<details id="cat-video"></details>')
    sitemap(tmp_path, '/', '/herramientas/')
    (tmp_path / 'herramientas' / 'x').mkdir()
    (tmp_path / 'herramientas' / 'x' / 'index.html').write_text(
        '<html><head><meta http-equiv="refresh" content="0; url=/herramientas/#cat-nada"></head></html>')
    errors = check_site(tmp_path)
    assert any('ancla inexistente /herramientas/#cat-nada' in e for e in errors)


def test_content_link_to_old_home_anchor(tmp_path):
    page(tmp_path, 'index.html', '/', body='<p>portada</p>')
    page(tmp_path, 'a/index.html', '/a/', title='A', body='<a href="/#cat-video">vídeo</a>')
    sitemap(tmp_path, '/', '/a/')
    assert any('ancla inexistente /#cat-video' in e for e in check_site(tmp_path))


def test_search_index_url_must_exist(tmp_path):
    page(tmp_path, 'index.html', '/')
    page(tmp_path, 'herramientas/index.html', '/herramientas/', title='H', body='<details id="cat-video"></details>')
    sitemap(tmp_path, '/', '/herramientas/')
    (tmp_path / 'search-index.json').write_text(
        '[{"u":"/no-existe/"},{"u":"/herramientas/#cat-nada"},{"u":"/herramientas/#cat-video"}]', encoding='utf-8')
    errors = check_site(tmp_path)
    assert 'search-index.json: URL inexistente /no-existe/' in errors
    assert 'search-index.json: ancla inexistente /herramientas/#cat-nada' in errors
    assert not any('cat-video' in e for e in errors)
