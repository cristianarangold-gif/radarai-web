# Radar IA — Fases 0 y 1: base técnica y recorte · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sustituir el HTML escrito a mano por un generador estático en Python que publica en GitHub Pages solo páginas con valor. Retirar las ~150 páginas vacías con redirecciones.

**Architecture:**
- **Generador:** un paquete `radar/` con funciones puras (carga de contenido, render, SEO, sitemap, redirecciones y validación). El CLI `scripts/build.py` lo orquesta y escribe en `_site/`.
- **Contenido y plantillas:** el contenido vive en Markdown con metadatos (extensión `meta` de Python-Markdown) y las plantillas en Jinja2.
- **Despliegue:** `deploy.yml` construye, valida y publica con `actions/deploy-pages`, sin commits del bot.

**Tech Stack:** Python 3.9+ (3.12 en CI), Jinja2, Python-Markdown, pytest y GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-06-radar-ia-adsense-design.md` (§3 arquitectura y §4.1 recorte).

**Planes siguientes (fuera de este plan):**
- Fase 2: contenido núcleo.
- Fase 3: noticias.
- Fase 4: cumplimiento AdSense.

## Global Constraints

- **Dependencias de ejecución:** solo `jinja2` y `markdown`. Para tests, `pytest`.
- **URLs:** con barra final (`/noticias/`) y canonical absoluto `https://radarai.es/...`.
- **Idioma:** `lang="es"` en todas las páginas. Textos visibles en español de España.
- **Script AdSense** en el `<head>` de toda página excepto `legal/*`, contacto y 404: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7428485851163208" crossorigin="anonymous"></script>`.
- **Mínimos de palabras para páginas indexables:**

  | Tipo | Mínimo |
  |---|---|
  | `ficha` | 1000 |
  | `comparativa`, `guia` | 1200 |
  | `noticia` | 500 |
  | `utilidad` | 300 |
  | `pagina` | 0 (legales, contacto, sobre) |

- **Borradores:** `borrador: si` implica `noindex,follow`, fuera del sitemap y exento de mínimos.
- **Sin publicación en `main`:** nada se fusiona a `main` hasta terminar la fase 2. La web publicada no cambia mientras tanto.
- **`ads.txt` y `CNAME`:** se copian sin modificar.

## Review Focus

1. **URL antigua con `index.html` explícito** (`/herramientas/runway/index.html`). Debe redirigir igual que `/herramientas/runway/`. Test en Task 6.
2. **Herramienta del catálogo sin ficha.** La tarjeta enlaza a la web oficial con `rel="noopener nofollow"`, nunca a una ficha inexistente. Test en Task 5.
3. **Caracteres no ASCII y escapes** (`í`, `&amp;`) en títulos y descripciones. Se muestran como «í» y «&» y nunca como texto literal. Test en Tasks 2 y 7.
4. **Fecha ausente o inválida en el front-matter de una noticia.** El build falla con un mensaje que nombra el archivo, en lugar de publicar sin fecha. Test en Task 3.
5. **Dos páginas con la misma ruta de salida** (una de contenido y una redirección). El build falla nombrando ambas. Test en Task 6.

---

## File Structure

```
requirements.txt            jinja2, markdown
requirements-dev.txt        -r requirements.txt + pytest
.gitignore                  _site/, .venv/, __pycache__/
radar/__init__.py
radar/models.py             dataclasses Page, Tool, Redirect
radar/content.py            load_pages(content_dir) -> list[Page]
radar/tools.py              load_tools(path) -> dict[str, Tool]
radar/seo.py                canonical(), jsonld(page), sitemap_xml(pages), rss_xml(pages)
radar/redirects.py          load_redirects(path) -> list[Redirect]; render_redirect(r) -> str
radar/render.py             make_env(templates_dir); render_page(env, page, ctx) -> str
radar/check.py              check_site(site_dir) -> list[str]  (errores)
scripts/build.py            CLI: build(root, out) -> None
scripts/check.py            CLI: sale con 1 si check_site devuelve errores
scripts/migrate_tools.py    migración única: TOOLS de index.html -> data/tools.json
templates/                  base.html, page.html, article.html, tool.html, listing.html,
                            home.html, redirect.html, partials/{header,footer,cookies,ad_slot}.html
static/css/radar.css        CSS único (paleta actual: #0D1220, #161D30, #2A3454, #F1F4FA, #9BA6C0, #FFB86B)
static/js/catalog.js        filtros y buscador del catálogo de portada
static/js/cookies.js        banner actual portado (lo sustituye el CMP en la fase 4)
static/utilidades/          herramientas-radar/* copiado tal cual (app.js + páginas)
content/paginas/            inicio.md, sobre.md, metodologia.md, autor.md, politica-editorial.md, legal/*.md
content/mejor-ia/           9 comparativas migradas como borrador
content/guias/              6 guías migradas como borrador
content/noticias/           7 noticias migradas como borrador
content/herramientas/       vacío en esta fase (lo llena la fase 2)
content/GUIA_EDITORIAL.md   reglas editoriales del spec §2 (no se publica)
data/tools.json
data/redirects.yml          formato "origen: destino" por línea (sin dependencia YAML)
tests/                      un test_*.py por módulo de radar/
.github/workflows/test.yml  pytest + build + check en PR y push
.github/workflows/deploy.yml build + check + deploy-pages en push a main
```

**Eliminados:**
- Todos los `*.html` actuales de la raíz y subcarpetas, salvo que se migren.
- `scripts/fix_catalog.py`, `site-refresh.yml` y `sitemap-cleanup.yml`.
- `sitemap.xml` y `robots.txt` versionados: ahora se generan.

---

### Task 1: Esqueleto del proyecto y modelos

**Files:**
- Create: `requirements.txt`, `requirements-dev.txt`, `.gitignore`, `radar/__init__.py`, `radar/models.py`, `tests/test_models.py`

**Interfaces:**
- Produces:
  - `Page(kind: str, slug: str, url: str, title: str, description: str, body_html: str, date: date|None, updated: date|None, author: str, sources: list[str], draft: bool, indexable: bool, word_count: int, extra: dict)`
  - `Tool(id: str, name: str, cat: str, desc: str, price: str, level: str, platform: str, lang: str, tags: list[str], url: str, has_page: bool)`
  - `Redirect(source: str, target: str)`
  - `Page.indexable` es una propiedad: `not draft and extra.get('noindex') != 'si'`.

- [ ] **Step 1:** Escribir `tests/test_models.py::test_draft_page_not_indexable`. Verifica que `Page(..., draft=True).indexable is False` y que, con `draft=False`, devuelve `True`.
- [ ] **Step 2:** Ejecutar `python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt && .venv/bin/pytest tests/test_models.py -v`. Esperado: FAIL (ImportError).
- [ ] **Step 3:** Implementar las dataclasses de `radar/models.py`.
- [ ] **Step 4:** Ejecutar `.venv/bin/pytest -v`. Esperado: PASS.
- [ ] **Step 5:** Hacer commit: `Añadir esqueleto del generador y modelos`.

### Task 2: Migración del catálogo a `data/tools.json`

**Files:**
- Create: `scripts/migrate_tools.py`, `radar/tools.py`, `data/tools.json`, `tests/test_tools.py`

**Interfaces:**
- Produces:
  - `load_tools(path: Path, content_dir: Path) -> dict[str, Tool]`. Marca `has_page=True` cuando existe `content_dir/herramientas/<id>.md`.
  - `CATEGORIES: list[tuple[str, str]]` con estas parejas: (`ia-general`, «IA general»), (`escritura`, «Escritura»), (`imagenes`, «Imágenes»), (`video`, «Vídeo»), (`audio`, «Audio y música»), (`programacion`, «Programación»), (`educacion`, «Educación»), (`marketing`, «Marketing») y (`productividad`, «Productividad»).

- [ ] **Step 1:** Escribir `tests/test_tools.py` con estos tres tests:
  - `test_catalog_has_135_tools_with_required_fields`: comprueba `len == 135` y que cada herramienta tiene `name` y `url` no vacíos, `url` que empieza por `https://` y `cat` en `CATEGORIES`.
  - `test_no_literal_unicode_escapes`: ningún campo contiene `\u`.
  - `test_has_page_flag`: con un `tmp_path` que tiene `herramientas/claude.md`, solo `claude` tiene `has_page=True`.
- [ ] **Step 2:** Ejecutar `.venv/bin/pytest tests/test_tools.py -v`. Esperado: FAIL.
- [ ] **Step 3:** Escribir `scripts/migrate_tools.py`:
  1. Extrae el literal `const TOOLS = {...};` del `index.html` de `main` (`git show main:index.html`).
  2. Entrecomilla las claves sin comillas con la regex `(?<=[{,])\s*(\w+):` → `"\1":`.
  3. Hace `json.loads`, con lo que los `\uXXXX` quedan decodificados.
  4. Normaliza `cat` con el mapa `aliases` de `scripts/fix_catalog.py`.
  5. Escribe `data/tools.json` ordenado por id, con `ensure_ascii=False` e `indent=1`.

  Después ejecutarlo e implementar `load_tools`.
- [ ] **Step 4:** Ejecutar `.venv/bin/pytest tests/test_tools.py -v`. Esperado: PASS.
- [ ] **Step 5:** Hacer commit: `Migrar catálogo de herramientas a data/tools.json`.

### Task 3: Carga de contenido Markdown

**Files:**
- Create: `radar/content.py`, `tests/test_content.py`

**Interfaces:**
- Consumes: `Page`.
- Produces:
  - `load_pages(content_dir: Path) -> list[Page]`.
  - `KIND_BY_DIR = {'mejor-ia': 'comparativa', 'guias': 'guia', 'noticias': 'noticia', 'herramientas': 'ficha', 'paginas': 'pagina'}`.
  - `MIN_WORDS = {'ficha': 1000, 'comparativa': 1200, 'guia': 1200, 'noticia': 500, 'utilidad': 300, 'pagina': 0}`.
- **Reglas de URL:**
  - `content/paginas/inicio.md` → `/`.
  - `content/paginas/legal/aviso-legal.md` → `/legal/aviso-legal/`.
  - `content/paginas/<x>.md` → `/<x>/`.
  - `content/mejor-ia/<slug>.md` → `/<slug>/`, para conservar las URL actuales `mejor-ia-para-*`.
  - `content/guias/<slug>.md` → `/guias/<slug>/`.
  - `content/noticias/<slug>.md` → `/noticias/<slug>/`.
  - `content/herramientas/<id>.md` → `/herramientas/<id>/`.
- **Metadatos:**
  - Obligatorios: `titulo`, `descripcion`.
  - Para `noticia` y `ficha`: `fecha` en formato `AAAA-MM-DD`.
  - Opcionales: `actualizado`, `autor` (por defecto «Cristian Arango»), `fuentes` (varias líneas), `borrador`, `noindex`.
  - Archivos excluidos: los que empiezan por `_` o por mayúscula (p. ej. `GUIA_EDITORIAL.md`).
- **`word_count`:** número de palabras del texto plano de `body_html`.

- [ ] **Step 1:** Escribir `tests/test_content.py` con estos tests:
  - `test_urls_by_directory`: un caso por cada regla de URL.
  - `test_meta_parsed`: título con «í», `fuentes` con 2 URL y `fecha` convertida a `date`.
  - `test_missing_date_on_news_raises`: `ValueError` cuyo mensaje contiene el nombre del archivo.
  - `test_invalid_date_raises`.
  - `test_uppercase_files_ignored`.
  - `test_word_count_excludes_markup`.
- [ ] **Step 2:** Ejecutar `.venv/bin/pytest tests/test_content.py -v`. Esperado: FAIL.
- [ ] **Step 3:** Implementar con `markdown.Markdown(extensions=['meta', 'tables', 'toc', 'attr_list'])`. Usar una instancia nueva por archivo.
- [ ] **Step 4:** Ejecutar `.venv/bin/pytest tests/test_content.py -v`. Esperado: PASS.
- [ ] **Step 5:** Hacer commit: `Añadir carga de contenido Markdown`.

### Task 4: SEO, sitemap y RSS

**Files:**
- Create: `radar/seo.py`, `tests/test_seo.py`

**Interfaces:**
- Consumes: `Page`.
- Produces:
  - `SITE = 'https://radarai.es'`.
  - `canonical(url: str) -> str`.
  - `jsonld(page: Page) -> list[dict]`: `NewsArticle` para noticia, `Article` para comparativa o guía, `SoftwareApplication` + `Review` para ficha y `WebSite` para `/`. Siempre añade `BreadcrumbList` excepto en `/`. El autor es un `Person` llamado «Cristian Arango» con `url` a `SITE + '/autor/'`.
  - `sitemap_xml(pages: list[Page]) -> str`: solo `indexable`, con `lastmod = updated or date` cuando exista.
  - `rss_xml(news: list[Page]) -> str`: las 20 noticias indexables más recientes.

- [ ] **Step 1:** Escribir `tests/test_seo.py` con estos tests:
  - `test_sitemap_excludes_drafts_and_noindex`.
  - `test_sitemap_lastmod`.
  - `test_jsonld_news_has_dates_and_author`.
  - `test_canonical_absolute`.
  - `test_rss_orders_by_date_desc`.
- [ ] **Step 2:** Ejecutar `.venv/bin/pytest tests/test_seo.py -v`. Esperado: FAIL.
- [ ] **Step 3:** Implementar con `xml.sax.saxutils.escape`; nada de librerías nuevas.
- [ ] **Step 4:** Ejecutar `.venv/bin/pytest tests/test_seo.py -v`. Esperado: PASS.
- [ ] **Step 5:** Hacer commit: `Añadir SEO, sitemap y RSS`.

### Task 5: Plantillas, CSS y render

**Files:**
- Create: `templates/*`, `static/css/radar.css`, `static/js/catalog.js`, `static/js/cookies.js`, `radar/render.py`, `tests/test_render.py`

**Interfaces:**
- Consumes: `Page`, `Tool`, `CATEGORIES`, `jsonld`, `canonical`.
- Produces:
  - `make_env(templates_dir: Path) -> jinja2.Environment` con `autoescape=True`.
  - `render_page(env, page: Page, ctx: dict) -> str`. Usa `home.html` para `/`, `tool.html` para ficha, `article.html` para noticia, guía y comparativa, `page.html` para pagina y `listing.html` cuando `ctx['listing']` existe.
  - `ctx` contiene `tools`, `categories`, `latest_news` (lista de `Page`), `listing` (lista de `Page`) y `nav`.
- **Cabecera (`partials/header.html`):** marca «Radar IA» y estos enlaces: Inicio `/`, Herramientas `/#herramientas`, Comparativas `/mejor-ia/`, Guías `/guias/`, Noticias `/noticias/` y Utilidades `/herramientas-radar/`.
- **Pie (`partials/footer.html`):**
  - Lema «La IA en tu día».
  - Enlaces a Sobre, Metodología, Política editorial, Autor, Contacto, Aviso legal, Privacidad y Cookies.
- **`article.html`:**
  - Muestra autor con enlace a `/autor/`, fecha, «Actualizado el …» y lista «Fuentes».
  - Incluye `partials/ad_slot.html`, que en esta fase no renderiza nada (`{% if ads_enabled %}` con `ads_enabled=False`).
- **`home.html`:** las 135 tarjetas del catálogo se agrupan por categoría con `<details>`. Si `tool.has_page`, el enlace va a `/herramientas/<id>/`; si no, a `tool.url` con `rel="noopener nofollow" target="_blank"`.
- **CSS:** se conserva la estética actual (paleta de Global Constraints, fondo oscuro, acento naranja). Es responsive a 360 px y no produce scroll horizontal.

- [ ] **Step 1:** Escribir `tests/test_render.py` con estos tests:
  - `test_adsense_in_article_not_in_legal`.
  - `test_noindex_meta_on_draft`.
  - `test_catalog_card_without_page_links_official_nofollow`.
  - `test_catalog_card_with_page_links_internal`.
  - `test_title_escaping`: el título «A & B» se renderiza como `A &amp; B` una sola vez, sin `&amp;amp;`.
  - `test_jsonld_embedded`.
- [ ] **Step 2:** Ejecutar `.venv/bin/pytest tests/test_render.py -v`. Esperado: FAIL.
- [ ] **Step 3:** Implementar las plantillas, `render.py` y el CSS. Portar los filtros del catálogo y el banner de cookies desde el `index.html` actual a `static/js/`.
- [ ] **Step 4:** Ejecutar `.venv/bin/pytest tests/test_render.py -v`. Esperado: PASS.
- [ ] **Step 5:** Hacer commit: `Añadir plantillas, CSS y render`.

### Task 6: Redirecciones

**Files:**
- Create: `radar/redirects.py`, `data/redirects.yml`, `templates/redirect.html`, `tests/test_redirects.py`

**Interfaces:**
- Produces:
  - `load_redirects(path: Path) -> list[Redirect]`. Normaliza `origen` quitando `index.html` y forzando la barra final.
  - `output_paths(r: Redirect) -> list[str]`. Devuelve `x/index.html` y, si el origen antiguo era `x.html` (legales), también `x.html`.
  - `render_redirect(env, r) -> str`. Genera `meta refresh` a 0 s, `link rel=canonical` al destino absoluto, `meta robots noindex` y un enlace visible.
- **Contenido de `data/redirects.yml`:**
  - Cada `herramientas/<id>/` sin ficha redirige a `/#cat-<categoria>`.
  - Hay 8 secciones vacías:

    | Origen | Destino |
    |---|---|
    | rankings, reviews, alternativas, precios | `/mejor-ia/` |
    | cambios, publicacion | `/noticias/` |
    | mejor-ia | ninguno: se convierte en índice real |
    | preguntas-frecuentes | `/#preguntas-frecuentes` |

  - Las legales `legal/x.html` redirigen a `/legal/x/`.
  - El build añade automáticamente las redirecciones de herramientas sin ficha a partir de `tools.json`. El archivo solo lista las manuales.

- [ ] **Step 1:** Escribir `tests/test_redirects.py` con estos tests:
  - `test_index_html_source_normalized`.
  - `test_redirect_html_has_refresh_canonical_noindex`.
  - `test_legal_html_source_outputs_both_paths`.
- [ ] **Step 2:** Ejecutar `.venv/bin/pytest tests/test_redirects.py -v`. Esperado: FAIL.
- [ ] **Step 3:** Implementar `radar/redirects.py` y `templates/redirect.html`, y escribir `data/redirects.yml`.
- [ ] **Step 4:** Ejecutar `.venv/bin/pytest tests/test_redirects.py -v`. Esperado: PASS.
- [ ] **Step 5:** Hacer commit: `Añadir redirecciones de URLs retiradas`.

### Task 7: Build completo y validación del sitio

**Files:**
- Create: `scripts/build.py`, `radar/check.py`, `scripts/check.py`, `tests/test_build.py`, `tests/test_check.py`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces:
  - `build(root: Path, out: Path) -> None`. Borra `out` y genera:
    - todas las páginas y listados (`/noticias/`, `/guias/`, `/mejor-ia/`, `/herramientas/`);
    - redirecciones, `sitemap.xml`, `rss.xml`, `robots.txt` (con `Sitemap: https://radarai.es/sitemap.xml`) y `404.html`;
    - copias de `static/` → `/static/` y de `static/utilidades/` → `/herramientas-radar/`, más `ads.txt` y `CNAME`.
  - Si dos fuentes escriben la misma ruta, lanza `ValueError` con ambas.
  - `check_site(site_dir: Path) -> list[str]` comprueba en cada `.html` que no sea redirección ni `noindex`:
    - `<!doctype html>` sin distinguir mayúsculas;
    - un único `<title>` y una `description` no vacía, ambos sin duplicados en otras páginas;
    - canonical y `lang="es"`;
    - que no haya `\u[0-9a-fA-F]{4}` literal en el texto;
    - que todos los enlaces internos `href="/..."` existan en `site_dir`;
    - que se cumplan los mínimos de palabras por tipo (lee `<meta name="radar:kind">` y `<meta name="radar:words">`, emitidos por `base.html`);
    - que toda URL de `sitemap.xml` exista y no sea `noindex`.

- [ ] **Step 1:** Escribir los tests de `tests/test_check.py`. Cada uno trabaja sobre un `_site` mínimo en `tmp_path`:
  - `test_uppercase_or_lowercase_doctype_ok`;
  - `test_broken_internal_link_reported`;
  - `test_literal_escape_reported`;
  - `test_short_indexable_page_reported`;
  - `test_noindex_page_skips_word_minimum`;
  - `test_duplicate_title_reported`;
  - `test_sitemap_url_missing_reported`.
- [ ] **Step 2:** Escribir los tests de `tests/test_build.py`, que trabajan sobre un `root` de prueba con 1 noticia, 1 borrador y 2 herramientas:
  - `test_build_outputs_expected_files`;
  - `test_duplicate_output_path_raises`;
  - `test_old_tool_url_redirects`.
- [ ] **Step 3:** Ejecutar `.venv/bin/pytest -v`. Esperado: FAIL en los tests nuevos.
- [ ] **Step 4:** Implementar `scripts/build.py`, `radar/check.py` y `scripts/check.py`.
- [ ] **Step 5:** Ejecutar `.venv/bin/pytest -v`. Esperado: PASS.
- [ ] **Step 6:** Hacer commit: `Añadir build completo y validación del sitio`.

### Task 8: Migración del contenido que se conserva y recorte

**Files:**
- Create: `content/paginas/{inicio,sobre,metodologia,autor,politica-editorial,contacto}.md`, `content/paginas/legal/{aviso-legal,politica-privacidad,politica-cookies}.md`, `content/mejor-ia/*.md` (9), `content/guias/*.md` (6), `content/noticias/*.md` (7), `content/GUIA_EDITORIAL.md`, `static/utilidades/**`
- Delete: los HTML antiguos migrados o retirados, `scripts/fix_catalog.py`, `sitemap.xml`, `robots.txt`, `404.html`, `index.html`, `herramientas/`, `herramientas-radar/` (se mueve) y las 8 secciones vacías

**Reglas de migración:**
- **Legales y contacto:** se convierten a Markdown con el texto actual íntegro. Llevan `borrador: no`.
- **Sobre y metodología:** texto actual. `autor.md` es nuevo:
  - nombre «Cristian Arango»;
  - lemas «La IA en tu día», «Con IA todo es más fácil» y «Pon IA en tu vida»;
  - contacto `contacto@radarai.es`;
  - biografía basada únicamente en lo que ya figura en la web, sin inventar datos.
- **`politica-editorial.md`:** se redacta a partir del spec §2.
- **`inicio.md`:** se migran las secciones de texto útiles del `index.html` actual (`sobre-nosotros`, `preguntas-frecuentes`, `editorial`, `que-quieres-hacer`). Se eliminan los bloques «FASE», ranking inventado y tendencias sin fuente.
- **Comparativas (9), guías (6) y noticias (7):** se migra el texto actual con `borrador: si`, con lo que quedan `noindex`. La fase 2 las reescribe y las publica.
- **`herramientas-radar/*`:** se copia a `static/utilidades/` cambiando los enlaces de cabecera a las rutas nuevas. Se añade `<meta name="robots" content="noindex,follow">` hasta que la fase 2 les añada texto explicativo.

- [ ] **Step 1:** Hacer la migración y borrar los archivos según las reglas.
- [ ] **Step 2:** Ejecutar `.venv/bin/python scripts/build.py && .venv/bin/python scripts/check.py`. Esperado: `OK` sin errores.
- [ ] **Step 3:** Ejecutar `grep -c '<loc>' _site/sitemap.xml`. Esperado: solo las páginas `pagina` publicadas (≈ 10). El resto entra en la fase 2.
- [ ] **Step 4:** Ejecutar `.venv/bin/python -m http.server -d _site 8000` y revisar en el navegador la portada, una legal, una redirección antigua (`/herramientas/runway/`, `/rankings/`) y las utilidades. Hacerlo a 375 px y en escritorio.
- [ ] **Step 5:** Hacer commit: `Migrar contenido conservado y retirar páginas vacías`.

### Task 9: Workflows de GitHub Actions

**Files:**
- Create: `.github/workflows/test.yml`, `.github/workflows/deploy.yml`
- Delete: `.github/workflows/site-refresh.yml`, `.github/workflows/sitemap-cleanup.yml`

**Contenido:**
- **`test.yml`:** se dispara con `pull_request` y con `push` a ramas distintas de `main`. Usa `actions/setup-python@v5` con `python-version: '3.12'` y ejecuta `pip install -r requirements-dev.txt`, `pytest -q`, `python scripts/build.py` y `python scripts/check.py`.
- **`deploy.yml`:** se dispara con `push` a `main` y con `workflow_dispatch`.
  - Permisos: `pages: write`, `id-token: write`, `contents: read`.
  - Pasos: setup → build → check → `actions/upload-pages-artifact@v3` con `path: _site` → `actions/deploy-pages@v4`.
  - `concurrency: pages`.
  - Ningún paso hace `git push`.

- [ ] **Step 1:** Crear los workflows y borrar los antiguos.
- [ ] **Step 2:** Subir la rama: `git push -u origin rediseno-adsense`. Esperado: `test.yml` en verde (`gh run list --branch rediseno-adsense`).
- [ ] **Step 3:** Hacer commit: `Sustituir workflows por test y despliegue a Pages`. Va incluido en el push del paso 2 si se hace antes.

**Nota:** el cambio de origen de GitHub Pages a «GitHub Actions» y la fusión a `main` **no** forman parte de este plan. Se hacen al cerrar la fase 2, con confirmación del titular.

### Task 10: Limpieza de la rama de pruebas

- [ ] **Step 1:** Pedir confirmación al titular y ejecutar `git push origin --delete publicacion-zip-exacta`.
- [ ] **Step 2:** Comprobar con `git ls-remote --heads origin` que solo quedan `main` y `rediseno-adsense`.
