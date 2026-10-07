"""Genera el sitio estático de Radar IA en _site/.

Uso: python scripts/build.py [--out _site]
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from radar.assistant import load_assistant, resolve_payload, validate_assistant  # noqa: E402
from radar.brands import load_brands  # noqa: E402
from radar.compare import compare_payload  # noqa: E402
from radar.content import load_pages  # noqa: E402
from radar.covers import cover_for, og_rel, write_cover_png  # noqa: E402
from radar.editorial import load_imprescindibles, radar_tools, validate_fichas, validate_news_meta  # noqa: E402
from radar.models import Page, Redirect  # noqa: E402
from radar.redirects import load_redirects, output_paths, render_redirect  # noqa: E402
from radar.render import make_env, render_page  # noqa: E402
from radar.search import build_index, index_json  # noqa: E402
from radar.glossary import defined_term_set, glossary_context, parse_glossary, validate_glossary  # noqa: E402
from radar.start import load_start, validate_start  # noqa: E402
from radar.seo import SITE, rss_xml, sitemap_xml  # noqa: E402
from radar.tools import CATEGORIES, load_tools  # noqa: E402

LISTINGS = [
    # (url, tipo listado, título, descripción)
    ('/noticias/', 'noticia', 'Noticias de inteligencia artificial',
     'Las novedades de IA que importan, explicadas en español y con lo que cambian para ti.'),
    ('/guias/', 'guia', 'Guías prácticas de IA',
     'Guías paso a paso para sacar partido a la inteligencia artificial en el estudio, el trabajo y el día a día.'),
    ('/mejor-ia/', 'comparativa', 'Comparativas: la mejor IA para cada tarea',
     'Comparativas actualizadas para elegir la herramienta de IA adecuada según lo que necesitas hacer.'),
    ('/herramientas/', 'ficha', 'Análisis de herramientas de IA',
     'Fichas completas de las herramientas de IA más usadas: qué hacen, cuánto cuestan y para quién son.'),
    ('/herramientas-radar/', 'utilidad', 'Utilidades gratuitas de Radar IA',
     'Pequeñas herramientas gratuitas que funcionan en tu navegador para preparar prompts, títulos, hashtags y textos.'),
]


def _synthetic(url: str, title: str, description: str, noindex: bool = False) -> Page:
    return Page(kind='pagina', slug=url.strip('/') or 'inicio', url=url, title=title,
                description=description, body_html='', date=None, updated=None,
                author='Cristian Arango', sources=[], draft=False, word_count=0,
                extra={'noindex': 'si'} if noindex else {})


class Writer:
    """Escribe archivos en `out` y detecta dos orígenes para la misma ruta."""

    def __init__(self, out: Path):
        self.out = out
        self.owners: Dict[str, str] = {}

    def write(self, rel: str, text: str, owner: str) -> None:
        if rel in self.owners:
            raise ValueError(f'Ruta duplicada {rel}: la generan «{self.owners[rel]}» y «{owner}»')
        self.owners[rel] = owner
        dest = self.out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')


def _out_path(url: str) -> str:
    return 'index.html' if url == '/' else url.strip('/') + '/index.html'


def build(root: Path, out: Path) -> None:
    root, out = Path(root), Path(out)
    if (out / 'scripts' / 'build.py').exists() or (out / 'content').is_dir():
        raise ValueError(f'{out} contiene código fuente; elige otra carpeta de salida')
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    env = make_env(root / 'templates')
    pages = load_pages(root / 'content')
    tools = load_tools(root / 'data' / 'tools.json', root / 'content')
    brands = load_brands(root / 'data' / 'brands.json', root / 'static' / 'logos')
    validate_news_meta(pages, tools, brands)
    validate_fichas(pages)
    by_url = {p.url: p for p in pages}
    news = sorted((p for p in pages if p.kind == 'noticia' and p.indexable),
                  key=lambda p: p.date, reverse=True)
    def featured(kind):
        return sorted((p for p in pages if p.kind == kind and p.indexable), key=lambda p: p.title)
    base_ctx = dict(tools=tools, categories=CATEGORIES, latest_news=news[:7], news=news, listing=None,
                    comparativas=featured('comparativa'), guias=featured('guia'),
                    utilidades=featured('utilidad'), brands=brands, radar=radar_tools(news, tools),
                    imprescindibles=[], logos_dir=root / 'static' / 'logos',
                    fichas={p.slug: p for p in pages if p.kind == 'ficha' and p.indexable})
    assistant_file = root / 'data' / 'asistente.json'
    if assistant_file.exists():
        assistant = load_assistant(assistant_file)
        fichas = {p.slug: p for p in pages if p.kind == 'ficha' and p.indexable}
        validate_assistant(assistant, tools, fichas, {p.url for p in pages if p.indexable})
        base_ctx['assistant_payload'] = resolve_payload(assistant, tools, brands, fichas)
    if '/comparador/' in by_url:
        base_ctx['compare_payload'] = compare_payload(
            {p.slug: p for p in pages if p.kind == 'ficha' and p.indexable}, tools, brands, CATEGORIES)
    site_urls = {p.url for p in pages if p.indexable} | {url for url, *_ in LISTINGS}
    glossary_file = root / 'data' / 'glosario.md'
    if '/glosario/' in by_url:
        if not glossary_file.exists():
            raise ValueError('content/paginas/glosario.md necesita data/glosario.md')
        terms = parse_glossary(glossary_file.read_text(encoding='utf-8'))
        validate_glossary(terms, site_urls)
        titles = {p.url: p.title for p in pages}
        titles.update({url: title for url, _, title, _ in LISTINGS})
        base_ctx['glossary'] = glossary_context(terms, titles)
        base_ctx['glossary_jsonld'] = defined_term_set(terms)
    start_file = root / 'data' / 'empieza.json'
    if '/empieza-aqui/' in by_url and not start_file.exists():
        raise ValueError('content/paginas/empieza-aqui.md necesita data/empieza.json')
    if start_file.exists() and '/empieza-aqui/' in by_url:
        start = load_start(start_file)
        validate_start(start, site_urls)
        base_ctx['start_payload'] = start
    imprescindibles = root / 'data' / 'imprescindibles.txt'
    if imprescindibles.exists():
        base_ctx['imprescindibles'] = load_imprescindibles(imprescindibles, by_url)
    w = Writer(out)
    search_json = index_json(build_index(pages, tools, brands, base_ctx.get('glossary', {}).get('terms')))
    base_ctx['search_index_url'] = '/search-index.json?v=' + hashlib.sha256(search_json.encode('utf-8')).hexdigest()[:10]
    w.write('search-index.json', search_json, 'índice de búsqueda')

    all_pages: List[Page] = list(pages)
    for p in pages:
        w.write(_out_path(p.url), render_page(env, p, base_ctx), f'content {p.url}')

    for url, kind, title, desc in LISTINGS:
        if kind == 'utilidad' and not (root / 'content' / 'utilidades').is_dir():
            continue
        items = sorted((p for p in pages if p.kind == kind and p.indexable),
                       key=lambda p: (p.date is None, p.date), reverse=(kind == 'noticia'))
        if kind != 'noticia':
            items = sorted(items, key=lambda p: p.title)
        page = by_url.get(url) or _synthetic(url, title, desc, noindex=not items)
        if url in by_url:
            del w.owners[_out_path(url)]
        else:
            all_pages.append(page)
        w.write(_out_path(url), render_page(env, page, dict(base_ctx, listing=items)), f'listado {url}')

    redirects = load_redirects(root / 'data' / 'redirects.yml')
    redirects += [Redirect(f'/herramientas/{t.id}/', f'/herramientas/#cat-{t.cat}')
                  for t in tools.values() if not t.has_page]
    for r in redirects:
        for rel in output_paths(r):
            w.write(rel, render_redirect(env, r), f'redirección {r.source}')

    search_page = _synthetic('/buscar/', 'Buscar en Radar IA',
                             'Busca fichas, comparativas, guías, noticias y herramientas de IA.', noindex=True)
    all_pages.append(search_page)
    w.write(_out_path('/buscar/'), render_page(env, search_page, base_ctx), 'buscador')

    not_found = _synthetic('/404/', 'Página no encontrada',
                           'La página que buscas no existe o se ha movido.', noindex=True)
    not_found.body_html = ('<p>Puede que la dirección haya cambiado. Prueba desde la '
                           '<a href="/">portada</a>, las <a href="/noticias/">noticias</a> '
                           'o las <a href="/mejor-ia/">comparativas</a>.</p>')
    w.write('404.html', render_page(env, not_found, base_ctx), '404')

    for p in all_pages:
        if not p.indexable:
            continue
        rel = og_rel(p.url)
        if rel in w.owners:
            raise ValueError(f'Ruta duplicada {rel}: la generan «{w.owners[rel]}» y «portada {p.url}»')
        w.owners[rel] = f'portada {p.url}'
        write_cover_png(cover_for(p, brands, tools), out / rel, root / 'static' / 'fonts')

    w.write('sitemap.xml', sitemap_xml(all_pages), 'sitemap')
    w.write('rss.xml', rss_xml(news), 'rss')
    w.write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n', 'robots')

    static = root / 'static'
    for src in static.rglob('*'):
        if src.is_dir():
            continue
        rel = src.relative_to(static).as_posix()
        dest_rel = ('herramientas-radar/' + rel[len('utilidades/'):]) if rel.startswith('utilidades/') \
            else 'static/' + rel
        if dest_rel in w.owners:
            raise ValueError(f'Ruta duplicada {dest_rel}: la generan «{w.owners[dest_rel]}» y «static/{rel}»')
        w.owners[dest_rel] = f'static/{rel}'
        (out / dest_rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out / dest_rel)

    for name in ('ads.txt', 'CNAME'):
        if (root / name).exists():
            shutil.copyfile(root / name, out / name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default=str(ROOT / '_site'))
    args = parser.parse_args()
    build(ROOT, Path(args.out))
    print(f'OK: sitio generado en {args.out}')


if __name__ == '__main__':
    main()
