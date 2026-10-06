from datetime import date

import pytest

from radar.content import load_pages


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


NEWS = 'titulo: N\ndescripcion: d\nfecha: 2026-10-01\n\nCuerpo'
BASIC = 'titulo: T\ndescripcion: d\n\nCuerpo'


def by_url(pages):
    return {p.url: p for p in pages}


def test_urls_by_directory(tmp_path):
    write(tmp_path, 'paginas/inicio.md', BASIC)
    write(tmp_path, 'paginas/sobre.md', BASIC)
    write(tmp_path, 'paginas/legal/aviso-legal.md', BASIC)
    write(tmp_path, 'mejor-ia/mejor-ia-para-escribir.md', BASIC)
    write(tmp_path, 'guias/mejores-prompts.md', BASIC)
    write(tmp_path, 'noticias/una-noticia.md', NEWS)
    write(tmp_path, 'herramientas/claude.md', NEWS)
    pages = by_url(load_pages(tmp_path))
    assert set(pages) == {'/', '/sobre/', '/legal/aviso-legal/', '/mejor-ia-para-escribir/',
                          '/guias/mejores-prompts/', '/noticias/una-noticia/', '/herramientas/claude/'}
    assert pages['/mejor-ia-para-escribir/'].kind == 'comparativa'
    assert pages['/guias/mejores-prompts/'].kind == 'guia'
    assert pages['/herramientas/claude/'].kind == 'ficha'
    assert pages['/legal/aviso-legal/'].kind == 'pagina'


def test_meta_parsed(tmp_path):
    write(tmp_path, 'noticias/x.md',
          'titulo: Qué ocurrió\ndescripcion: Descripción\nfecha: 2026-10-01\n'
          'actualizado: 2026-10-02\nfuentes: https://a.example/1\n    https://b.example/2\n\nHola')
    p = load_pages(tmp_path)[0]
    assert p.title == 'Qué ocurrió'
    assert p.sources == ['https://a.example/1', 'https://b.example/2']
    assert p.date == date(2026, 10, 1) and p.updated == date(2026, 10, 2)
    assert p.author == 'Cristian Arango'
    assert p.draft is False


def test_draft_flag(tmp_path):
    write(tmp_path, 'guias/g.md', 'titulo: G\ndescripcion: d\nborrador: si\n\nx')
    assert load_pages(tmp_path)[0].draft is True


def test_missing_date_on_news_raises(tmp_path):
    write(tmp_path, 'noticias/sin-fecha.md', BASIC)
    with pytest.raises(ValueError, match='sin-fecha.md'):
        load_pages(tmp_path)


def test_invalid_date_raises(tmp_path):
    write(tmp_path, 'noticias/mala.md', 'titulo: N\ndescripcion: d\nfecha: 01/10/2026\n\nx')
    with pytest.raises(ValueError, match='mala.md'):
        load_pages(tmp_path)


def test_missing_title_raises(tmp_path):
    write(tmp_path, 'paginas/sin-titulo.md', 'descripcion: d\n\nx')
    with pytest.raises(ValueError, match='sin-titulo.md'):
        load_pages(tmp_path)


def test_uppercase_and_underscore_files_ignored(tmp_path):
    write(tmp_path, 'GUIA_EDITORIAL.md', BASIC)
    write(tmp_path, 'guias/_plantilla.md', BASIC)
    write(tmp_path, 'guias/README.md', BASIC)
    assert load_pages(tmp_path) == []


def test_word_count_excludes_markup(tmp_path):
    write(tmp_path, 'paginas/w.md', BASIC.replace('Cuerpo', '## Título dos\n\nuno **dos** [tres](https://x.example)'))
    assert load_pages(tmp_path)[0].word_count == 5


def test_markdown_tables_rendered(tmp_path):
    write(tmp_path, 'paginas/t.md', BASIC.replace('Cuerpo', '| a | b |\n|---|---|\n| 1 | 2 |'))
    assert '<table>' in load_pages(tmp_path)[0].body_html


def test_entities_in_meta_are_decoded(tmp_path):
    write(tmp_path, 'paginas/e.md', 'titulo: Guía &amp; trucos\ndescripcion: A &quot;B&quot;\n\nx')
    p = load_pages(tmp_path)[0]
    assert p.title == 'Guía & trucos'
    assert p.description == 'A "B"'
