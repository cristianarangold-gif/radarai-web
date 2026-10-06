# Rediseño visual — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar a radarai.es el estilo «Editorial claro» con el radar animado en la portada, fichas y artículos a dos columnas e imágenes de portada «radar con logotipo» (SVG en página y PNG para `og:image`).

**Architecture:** El generador estático actual (`scripts/build.py` → `_site/`) gana tres módulos pequeños:
- `radar/brands.py`: colores, logotipos y monogramas.
- `radar/editorial.py`: elección de herramientas del radar, tiempo de lectura, índice, relacionadas e imprescindibles.
- `radar/covers.py`: portadas en SVG y en PNG.

Las plantillas Jinja y `static/css/radar.css` se reescriben con el nuevo sistema visual. `radar/check.py` amplía sus validaciones (og:image, anclas del catálogo).

**Tech Stack:**
- Python 3.9 en local y 3.12 en CI.
- Jinja2 3.1.6, Markdown 3.9 y pytest 8.4.2.
- **Pillow 11.3.0**, dependencia nueva.
- CSS y JS sin librerías.
- Fuentes woff2 de Fontsource (OFL) e iconos de Simple Icons (CC0).

**Spec:** `docs/superpowers/specs/2026-10-06-rediseno-visual-design.md`

## Global Constraints

- **Tokens de color**, exactos:
  - papel: `--paper #fbf8f3` y `--paper-2 #f3ece0`;
  - texto: `--ink #151515` y `--ink-2 #444`;
  - acentos: `--rule #e0d9cc`, `--accent #e4572e` y `--amber #f3a712`;
  - radar: degradado radial `#2a2560` → `#0d1124`, líneas `rgba(130,200,210,.3–.55)`.
- **Fuentes:**
  - Fraunces 600, 800 y 600 cursiva; Inter 400, 500, 600 y 700;
  - woff2 en `static/fonts/`, con `font-display: swap`;
  - ninguna petición a `fonts.googleapis.com` ni a `fonts.gstatic.com`.
- **Pillow:** abre los mismos woff2 para los PNG (comprobado con Pillow 11.3.0 y FreeType 2.13.3). No se añaden TTF.
- **Contenido:**
  - Nunca escribir «hemos probado» ni nada que implique prueba propia; el comentario `<!-- NUESTRA PRUEBA -->` de las fichas no se toca.
  - Todo dato nuevo de precio en los metadatos de las fichas debe salir del texto de esa misma ficha (y por tanto de `content/_investigacion/precios-2026-10.md`).
- **Anuncios:**
  - `ads_enabled=False` sigue igual y no aparecen huecos vacíos;
  - AdSense no se carga en `/legal/`, `/contacto/` ni `/404`.
- **Comprobaciones:** `pytest -q`, `python scripts/build.py` y `python scripts/check.py` en verde al final de cada tarea.
- **Commits:** en la rama `rediseno-visual`, terminados con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Lectura:** `max(1, round(word_count / 220))` minutos, mostrado como «N min de lectura».
- **Radar:**
  - 5 blips; herramientas por defecto `chatgpt, claude, gemini, midjourney, perplexity`;
  - de las 6 noticias más recientes; barrido de 6 s;
  - pie «En el radar esta semana»; 260 px en el móvil.
- **Textos fijos:**
  - la cabecera usa «La IA en tu día» (eyebrow);
  - el radar lleva el pie «En el radar esta semana»;
  - la 404 dice «Esta página ha desaparecido del radar»;
  - la sección de destacados se llama «Imprescindibles».
- **Navegación:** Comparativas `/mejor-ia/`, Herramientas `/herramientas/`, Guías `/guias/`, Noticias `/noticias/` y Utilidades `/herramientas-radar/`.

## Review Focus

1. **Id inexistente** en `herramientas:` o `empresa:` de una noticia (errata del revisor): el build debe fallar con un mensaje que nombre el archivo y el id, nunca descartarlo en silencio. *Tests en la Tarea 2.*
2. **Enlaces antiguos a `/#cat-…`** en el contenido o en redirecciones tras mover el catálogo: `check.py` debe marcarlos como ancla inexistente. *Tests en la Tarea 5.*
3. **Noticia sin `empresa:`** o página de un tipo sin marca (listados, legales, utilidades, 404): se usa la portada genérica «RadarIA», sin error. *Tests en la Tarea 3.*
4. **Títulos largos o con caracteres especiales** («GPT-6.1 Sol: … ‹Astra›», comillas o `&`) en el SVG y en el JSON-LD: deben quedar escapados, sin doble escape y sin romper el SVG. *Tests en la Tarea 3.*
5. **Ficha sin los metadatos nuevos** (`precio_desde` y demás): no se muestra la casilla vacía. El build falla solo si faltan **todos**, para evitar fichas a medias en producción. *Tests en la Tarea 6.*

---

### Task 1: Marcas y logotipos

**Files:**
- Create:
  - `data/brands.json`
  - `scripts/fetch_logos.py`
  - `static/logos/*.svg` (generados por el script y versionados)
  - `radar/brands.py`
  - `tests/test_brands.py`

**Interfaces:**
- Produces:
  - `Brand(id: str, name: str, color: str, icon: Optional[str], monograma: str)`, una dataclass en `radar/models.py`.
  - `load_brands(path: Path, logos_dir: Path) -> Dict[str, Brand]`.
    - Lanza `ValueError` si `color` no es `#rrggbb` o si falta `monograma`.
    - Si `icon` está declarado pero no existe `logos_dir/<icon>.svg`, lo pone a `None`, porque el monograma lo sustituye.
  - `icon_path(brand: Brand, logos_dir: Path) -> Optional[str]`: el atributo `d` del primer `<path>` del SVG, o `None`.
  - `logo_html(brand: Brand, size: int, logos_dir: Path) -> Markup`:
    - un `<span class="logo" style="--brand:#xxxxxx;width:{size}px;height:{size}px" aria-hidden="true">`;
    - dentro, un `<svg viewBox="0 0 24 24"><path fill="#fff" d="…"/></svg>` o el monograma en texto.

- [ ] **Step 1: Crear `data/brands.json`**

  Claves:
  - las 15 herramientas con ficha: chatgpt, claude, gemini, copilot, perplexity, midjourney, runway, suno, elevenlabs, github-copilot, cursor, canva-ai, deepl-write, notion-ai y notebooklm;
  - las empresas: openai, anthropic, google, microsoft, meta, mistral, nvidia, apple, adobe y huggingface.

  Iconos de Simple Icons:

  | Clave | Icono |
  |---|---|
  | chatgpt | openai |
  | claude | claude |
  | gemini | googlegemini |
  | perplexity | perplexity |
  | suno | suno |
  | elevenlabs | elevenlabs |
  | github-copilot | githubcopilot |
  | cursor | cursor |
  | canva-ai | canva |
  | deepl-write | deepl |
  | notion-ai | notion |
  | notebooklm | notebooklm |
  | openai | openai |
  | anthropic | anthropic |
  | google | google |
  | meta | meta |
  | mistral | mistralai |
  | nvidia | nvidia |
  | apple | apple |
  | adobe | adobe |
  | huggingface | huggingface |

  - **Sin icono** (`icon: null`): copilot, microsoft, midjourney y runway.
  - **Colores:** el `hex` oficial de Simple Icons de cada icono (se leen de `https://cdn.jsdelivr.net/npm/simple-icons@latest/_data/simple-icons.json` o del paquete). Para las marcas sin icono:

    | Marca | Color |
    |---|---|
    | copilot | `#0078d4` |
    | microsoft | `#0078d4` |
    | midjourney | `#151515` |
    | runway | `#151515` |

  - **Colores casi blancos o casi negros:** se sustituyen por `#151515`.
  - **Monograma:** la inicial en mayúscula del nombre (GitHub Copilot → «G», Notion AI → «N»).

- [ ] **Step 2: Escribir `scripts/fetch_logos.py`**

  Recorre `brands.json` y, para cada `icon`, descarga `https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<icon>.svg` a `static/logos/<icon>.svg`.
  - Usa solo la biblioteca estándar (`urllib`) y un timeout de 15 s.
  - Si la descarga falla, informa por pantalla y sigue.
  - Lo ejecutas una vez:

    ```bash
    .venv/bin/python scripts/fetch_logos.py
    ```

  - **Resultado esperado:** 17 o más SVG en `static/logos/`. Cada uno contiene `<path d="`.

- [ ] **Step 3: Tests que fallan** (`tests/test_brands.py`)

```python
def test_load_brands_reads_color_icon_and_monogram(tmp_path): ...
    # brands.json con {'chatgpt': {name:'ChatGPT', color:'#10a37f', icon:'openai', monograma:'C'}}
    # y logos/openai.svg con '<svg viewBox="0 0 24 24"><title>OpenAI</title><path d="M1 1z"/></svg>'
    assert b['chatgpt'].icon == 'openai' and b['chatgpt'].color == '#10a37f'
def test_missing_logo_file_falls_back_to_monogram(tmp_path):
    assert b['runway'].icon is None and 'R' in logo_html(b['runway'], 40, logos)
def test_bad_color_raises(tmp_path):
    with pytest.raises(ValueError, match='color'): ...
def test_logo_html_inlines_path_white_on_brand(tmp_path):
    html = str(logo_html(b['chatgpt'], 40, logos))
    assert 'd="M1 1z"' in html and '--brand:#10a37f' in html and 'aria-hidden="true"' in html
def test_real_brands_file_is_valid():
    b = load_brands(ROOT/'data'/'brands.json', ROOT/'static'/'logos')
    assert {'chatgpt','claude','gemini','midjourney','perplexity','openai','google','anthropic'} <= b.keys()
```

- [ ] **Step 4:** Ejecuta:

  ```bash
  .venv/bin/pytest tests/test_brands.py -q
  ```

  **Resultado esperado:** FAIL (no existe el módulo).

- [ ] **Step 5: Implementar** `Brand` en `radar/models.py` y `radar/brands.py` según las interfaces.

- [ ] **Step 6:** Ejecuta:

  ```bash
  .venv/bin/pytest -q
  ```

  **Resultado esperado:** todo en verde.

- [ ] **Step 7: Commit** con el mensaje «Añadir marcas y logotipos (Simple Icons)».

---

### Task 2: Metadatos editoriales y lógica del radar

**Files:**
- Create:
  - `radar/editorial.py`
  - `data/imprescindibles.txt`
  - `tests/test_editorial.py`
- Modify:
  - `scripts/build.py`: validación y contexto.
  - Las 6 noticias de `content/noticias/*.md`: añadir `empresa:` y `herramientas:`.
  - `docs/rutina-noticias.md` y `content/GUIA_EDITORIAL.md`: documentar los dos campos nuevos.

**Interfaces:**
- Consumes: `load_brands` y `Dict[str, Tool]`, que ya existe.
- Produces (en `radar/editorial.py`):
  - `DEFAULT_RADAR = ['chatgpt', 'claude', 'gemini', 'midjourney', 'perplexity']`
  - `split_ids(value: str) -> List[str]`: separa por comas, quita espacios, pasa a minúsculas y descarta vacíos.
  - `validate_news_meta(pages: List[Page], tools: Dict[str, Tool], brands: Dict[str, Brand]) -> None`:
    - lanza `ValueError` con el formato `"noticias/<slug>: herramienta desconocida «x»"` o `"…: empresa desconocida «x»"`;
    - `herramientas` admite cualquier id de `tools.json`;
    - `empresa` solo admite ids de `brands`.
  - `radar_tools(news: List[Page], tools: Dict[str, Tool], n: int = 5, recent: int = 6) -> List[Tool]`:
    - `news` llega ordenado de más reciente a más antigua;
    - toma los ids de `herramientas` de las `recent` primeras, en orden de aparición y sin duplicados;
    - descarta los ids sin `has_page`;
    - completa con `DEFAULT_RADAR` (también filtrado por `has_page`) hasta `n`.
  - `reading_minutes(page: Page) -> int`
  - `toc(body_html: str) -> List[Tuple[str, str]]`: pares `(id, texto plano)` de cada `<h2 id="…">`, con el texto sin etiquetas y con las entidades decodificadas.
  - `related_news(page: Page, news: List[Page], n: int = 3) -> List[Page]`: las `n` más recientes distintas de `page`.
  - `load_imprescindibles(path: Path, by_url: Dict[str, Page]) -> List[Page]`:
    - una URL por línea; ignora líneas vacías y `#`;
    - si una URL no existe o no es indexable, lanza `ValueError` con esa URL;
    - devuelve como máximo 4.

- [ ] **Step 1: Tests que fallan**

```python
def test_radar_tools_takes_recent_news_order_then_defaults():
    # news[0].extra={'herramientas':'claude, cursor'} ; news[1]: 'claude,runway'(runway sin ficha)
    assert [t.id for t in radar_tools(news, tools)] == ['claude','cursor','chatgpt','gemini','midjourney']
def test_radar_tools_ignores_news_older_than_six(): ...
def test_radar_tools_never_returns_tools_without_page(): ...
def test_validate_news_meta_unknown_tool_names_file_and_id():
    with pytest.raises(ValueError, match=r'noticias/x: herramienta desconocida «chatgtp»'): ...
def test_validate_news_meta_unknown_company(): ...   # match 'empresa desconocida «openia»'
def test_news_without_empresa_or_herramientas_is_fine(): ...
def test_reading_minutes(): assert reading_minutes(make_page(word_count=100)) == 1; ...(word_count=1100) == 5
def test_toc_reads_h2_ids_and_plain_text():
    assert toc('<h2 id="a">Planes &amp; <em>precios</em></h2><h3 id="b">x</h3>') == [('a','Planes & precios')]
def test_related_news_excludes_self_and_limits_to_three(): ...
def test_imprescindibles_unknown_url_raises(tmp_path): ...  # match '/no-existe/'
```

- [ ] **Step 2:** Ejecuta:

  ```bash
  .venv/bin/pytest tests/test_editorial.py -q
  ```

  **Resultado esperado:** FAIL.

- [ ] **Step 3: Implementar** `radar/editorial.py`.

- [ ] **Step 4: Integrar en `scripts/build.py`**
  - Carga las marcas con `brands = load_brands(root/'data'/'brands.json', root/'static'/'logos')`.
  - Llama a `validate_news_meta(news_all, tools, brands)` con todas las noticias, borradores incluidos.
  - Añade al `base_ctx`:
    - `brands`;
    - `radar=radar_tools(news, tools)`;
    - `imprescindibles`: si existe `data/imprescindibles.txt`, el resultado de `load_imprescindibles(...)`; si no, `[]`.
  - En `tests/test_build.py`, `make_root` crea `data/brands.json` mínimo y enlaza `static/logos`. Añade un test: una noticia con `herramientas: inexistente` hace que `build` lance `ValueError`.

- [ ] **Step 5: Rellenar el contenido**
  - Pon `empresa:` y `herramientas:` en las 6 noticias, según de qué trata cada una: `openai` y `chatgpt` en las de OpenAI; `google` y `gemini` en las de Google.
  - Crea `data/imprescindibles.txt` con:
    - `/herramientas/chatgpt/`
    - `/mejor-ia-gratis/`
    - `/guias/mejores-prompts/`
    - `/guias/privacidad-en-ia/`
  - Documenta los dos campos en `docs/rutina-noticias.md` (la rutina debe rellenarlos) y en la guía editorial.

- [ ] **Step 6:** Ejecuta:

  ```bash
  .venv/bin/pytest -q && .venv/bin/python scripts/build.py && .venv/bin/python scripts/check.py
  ```

  **Resultado esperado:** todo en verde.

- [ ] **Step 7: Commit** con el mensaje «Añadir metadatos editoriales, lógica del radar e imprescindibles».

---

### Task 3: Portadas SVG y PNG, og:image

**Files:**
- Create:
  - `radar/covers.py`
  - `tests/test_covers.py`
  - `static/fonts/` con 7 woff2 de Fontsource:
    - `fraunces-latin-600-normal`
    - `fraunces-latin-800-normal`
    - `fraunces-latin-600-italic`
    - `inter-latin-400-normal`
    - `inter-latin-500-normal`
    - `inter-latin-600-normal`
    - `inter-latin-700-normal`
  - `static/fonts/LICENSE-OFL.txt`
- Modify:
  - `requirements-dev.txt`: añadir `pillow==11.3.0`.
  - `scripts/build.py`
  - `radar/render.py`
  - `radar/seo.py`: imagen en el JSON-LD.
  - `templates/base.html`: meta de og y twitter.
  - `radar/check.py`
  - `.gitignore`: no aplica, porque `_site` ya está ignorado.

**Interfaces:**
- Consumes: `Brand`, `logo_html` e `icon_path` (Task 1).
- Produces:
  - `CoverSpec(label: str, brand: Optional[Brand], symbol: Optional[str])`:
    - `symbol` vale `'star'` (comparativa), `'book'` (guía) o `None`;
    - sin `brand` ni `symbol`, la portada es la genérica de RadarIA.
  - `cover_for(page: Page, brands: Dict[str, Brand], tools: Dict[str, Tool]) -> CoverSpec`:

    | Página | Etiqueta | Marca o símbolo |
    |---|---|---|
    | ficha | nombre de la herramienta | `brands[page.slug]`, si existe |
    | noticia con `empresa` | nombre de la empresa | `brands[empresa]` |
    | noticia sin `empresa` | `'Noticia'` | sin marca |
    | comparativa | `'Comparativa'` | `star` |
    | guía | `'Guía'` | `book` |
    | resto | `'Radar IA'` | sin marca |

  - `cover_svg(spec: CoverSpec, logos_dir: Path) -> Markup`:
    - un `<svg viewBox="0 0 1200 630" role="img" aria-label="…">` con el disco radial, 4 anillos y la cuña de barrido;
    - en el centro, el logotipo o el símbolo;
    - la etiqueta abajo a la izquierda (en mayúsculas mediante CSS o atributo, escapada) y «Radar**IA**» abajo a la derecha.
  - `og_rel(url: str) -> str`: `'/'` da `'og/inicio.png'`; `'/noticias/x/'` da `'og/noticias/x.png'`.
  - `write_cover_png(spec: CoverSpec, dest: Path, fonts_dir: Path) -> None`:
    - PNG RGB de 1200×630 dibujado con `ImageDraw`: fondo radial (círculos concéntricos interpolando `#2a2560` → `#0d1124`), anillos `rgba(130,200,210,.3)` y cuña con `pieslice` semitransparente;
    - círculo del color de la marca con el monograma en Inter 700 (o «★» / «G» para guía y «R» para la genérica);
    - la etiqueta en Inter 700 y «RadarIA» en Fraunces 800, con «IA» en `#ff8a5c`.
  - Nuevas claves de render: `og_image` (URL absoluta `SITE + '/' + og_rel`) y `cover` (Markup del SVG). Las rellena `render_page` mediante el ctx.

- [ ] **Step 1: Descargar las fuentes y la licencia**
  - Las fuentes salen de `https://cdn.jsdelivr.net/npm/@fontsource/<familia>@5/files/<archivo>.woff2`.
  - La licencia OFL sale de `https://cdn.jsdelivr.net/npm/@fontsource/fraunces@5/LICENSE`.
  - **Resultado esperado:** 7 archivos, cada uno de más de 10 KB.

- [ ] **Step 2: Tests que fallan**

```python
def test_cover_for_kinds(): # ficha chatgpt→label 'ChatGPT', brand.id 'chatgpt'; noticia empresa google; noticia sin empresa→'Noticia', None; comparativa→symbol 'star'; guia→'book'; pagina→'Radar IA'
def test_cover_svg_escapes_label_and_is_wellformed():
    svg = str(cover_svg(CoverSpec('A & B <x>', None, None), logos)); ET.fromstring(svg)  # xml.etree
    assert 'A &amp; B &lt;x&gt;' in svg and '&amp;amp;' not in svg
def test_og_rel(): assert og_rel('/') == 'og/inicio.png' and og_rel('/noticias/x/') == 'og/noticias/x.png'
def test_write_cover_png_size(tmp_path):
    write_cover_png(spec, tmp_path/'a.png', ROOT/'static'/'fonts'); assert Image.open(tmp_path/'a.png').size == (1200, 630)
def test_fonts_load_with_pillow():  # garantiza soporte woff2 también en CI (Linux, py3.12)
    for f in (ROOT/'static'/'fonts').glob('*.woff2'): ImageFont.truetype(str(f), 20)
```

  Añade también estos tests:
  - **en `tests/test_build.py`:**
    - `_site/og/inicio.png` existe y la ficha o noticia de prueba tiene su PNG;
    - el HTML contiene `<meta property="og:image" content="https://radarai.es/og/...png">` y `twitter:card" content="summary_large_image"`;
    - el JSON-LD del artículo tiene `"image"`.
  - **en `tests/test_check.py`:**
    - una página indexable sin `og:image` da el error `falta og:image`;
    - un `og:image` que apunta a un archivo inexistente da el error `og:image inexistente`.

- [ ] **Step 3:** Ejecuta:

  ```bash
  .venv/bin/pip install pillow==11.3.0 && .venv/bin/pytest tests/test_covers.py -q
  ```

  **Resultado esperado:** FAIL.

- [ ] **Step 4: Implementar**
  - `radar/covers.py`.
  - **build:** genera el PNG en `out/og_rel(url)` para cada página indexable (contenido y listados) y para la portada. Registra la ruta en `Writer.owners` para detectar colisiones.
  - **render:** pasa `og_image` y `cover`.
  - **`base.html`:** `og:image`, `og:image:width` 1200, `og:image:height` 630, `twitter:card summary_large_image` y `twitter:image`, todo solo `{% if og_image %}`.
  - **`seo.jsonld`:** recibe `image: Optional[str] = None` y lo añade al Article o NewsArticle.
  - **`check.py`:**
    - toda página indexable que no sea redirección debe tener un `og:image` con prefijo `SITE`;
    - el archivo `_site/<ruta>` debe existir.

- [ ] **Step 5:** Ejecuta la suite completa, el build y check. Abre `_site/og/noticias/gpt-6-1-sol-openai.png` con Read y comprueba que se parece a la maqueta 4A.

- [ ] **Step 6: Commit** con el mensaje «Generar portadas radar (SVG y PNG) y og:image».

---

### Task 4: Sistema visual base (CSS, cabecera, pie, páginas)

**Files:**
- Rewrite: `static/css/radar.css`. El orden es:
  1. `@font-face`;
  2. tokens;
  3. reset;
  4. tipografía;
  5. cabecera, pie y botones;
  6. tarjetas (`.card-cover`, `.tool-card2`);
  7. prosa y tablas;
  8. utilidades;
  9. catálogo;
  10. radar;
  11. artículo y TOC;
  12. 404;
  13. `@media (max-width: 760px)`;
  14. `prefers-reduced-motion`.
- Modify:
  - `templates/base.html`: quitar Google Fonts y añadir `<link rel="preload" as="font" type="font/woff2" crossorigin>` para Fraunces 800 e Inter 400.
  - `templates/partials/header.html`
  - `templates/partials/footer.html`: banda en tinta, lema «La IA en tu día» y mini radar decorativo `aria-hidden`.
  - `templates/page.html`
  - `templates/utility.html`
  - `radar/render.py`: `NAV`.
  - `content/paginas/legal/politica-privacidad.md` y `politica-cookies.md`: quitar el párrafo o la fila de Google Fonts y actualizar la fecha de «Última actualización» al día de la tarea.
  - `static/utilidades/*` CSS, si tienen colores propios oscuros.
  - `tests/test_render.py`

**Interfaces:**
- Consumes: nada nuevo.
- Produces:
  - clases CSS que usan las tareas 5–7: `.wrap`, `.btn` (primario en tinta), `.btn-ghost`, `.eyebrow`, `.kicker`, `.card-grid`, `.card-cover`, `.prose` y `.logo`;
  - una cabecera con `.brand` «Radar<span>IA</span>».

- [ ] **Step 1: Tests que fallan** en `tests/test_render.py`:
  - `test_nav_order_and_targets`: el NAV es exactamente la lista de *Global Constraints*.
  - `test_no_google_fonts`: la página renderizada no contiene `fonts.googleapis` ni `fonts.gstatic`.
  - `test_fonts_preloaded`: contiene `/static/fonts/fraunces-latin-800-normal.woff2`.

  Además, en `tests/test_build.py`, ningún HTML de `_site` contiene `Google Fonts` (cubre las legales).

- [ ] **Step 2:** Comprueba que los tests fallan.

- [ ] **Step 3: Implementar**
  - CSS: toma como referencia visual `_preview/maquetas/2-radar-en-b.html` (fuera del repo, en `/Users/cristianarango/CLAUDE CODE/_preview/maquetas/`).
  - Las tablas tienen la cabecera en tinta y `overflow-x:auto` en el móvil (`.prose table` dentro de un contenedor con desplazamiento; mantén el mecanismo actual).
  - El foco es visible: `:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px }`.

- [ ] **Step 4:** Ejecuta pytest, el build y check. Copia `_site` a `/Users/cristianarango/CLAUDE CODE/_preview` y revisa a 375 px y 1440 px una legal y una utilidad.

- [ ] **Step 5: Commit** con el mensaje «Nuevo sistema visual editorial: fuentes propias, cabecera y pie».

---

### Task 5: Portada con radar y catálogo en /herramientas/

**Files:**
- Create:
  - `templates/partials/radar.html`
  - `templates/partials/card.html`: tarjeta de artículo con portada.
  - `templates/partials/tool_card.html`
  - `templates/partials/catalog.html`: el catálogo actual de `home.html`, movido.
- Modify:
  - `templates/home.html`
  - `templates/listing.html`: `/herramientas/` incluye el catálogo y carga `catalog.js`.
  - `scripts/build.py`: las redirecciones automáticas pasan a `/herramientas/#cat-<cat>`.
  - `radar/check.py`: validación de anclas.
  - `data/redirects.yml`: el comentario de cabecera.
  - `content/**/*.md`: enlaces `(/#cat-x)` → `(/herramientas/#cat-x)`. Son 5: automatizar-tareas, suno, elevenlabs, canva-ai y deepl-write; vuelve a buscarlos con grep.
  - `static/js/catalog.js`: el comentario «de la portada».
  - `tests/test_build.py`, `tests/test_check.py` y `tests/test_render.py`

**Interfaces:**
- Consumes: el ctx `radar`, `imprescindibles`, `brands`, `latest_news` y `cover` de cada tarjeta (ver abajo), `logo_html` y `reading_minutes`.
- Produces:
  - un filtro Jinja `cover(page)` → Markup del SVG, registrado en `make_env` mediante una función de contexto que usa `brands`, `tools` y `logos_dir`; lo reutilizan las tareas 6 y 7;
  - un filtro `logo(brand_id, size)` y un global `reading_minutes`.

**Portada, en el orden de la spec §6:**
- **Banda principal:**
  - eyebrow «La IA en tu día»;
  - H1 con `page.title`, con «inteligencia artificial» en `<em>` naranja si aparece en el título; si no, el título tal cual;
  - entradilla;
  - botones «Ver comparativas» → `/mejor-ia/` y «Explorar herramientas» → `/herramientas/`;
  - `partials/radar.html` a la derecha.
- **`partials/radar.html`:**
  - `<figure class="radar" aria-label="Radar de herramientas de IA destacadas">`;
  - disco, anillos y barrido en CSS (`conic-gradient` y `animation: spin 6s linear infinite`);
  - por cada herramienta i (0–4), un blip: un `<a class="blip" href="/herramientas/<id>/" style="--a:<ángulo>deg;--d:<retardo>s">` con su logo y su nombre.
    - Ángulos fijos: 30, 100, 170, 245 y 315.
    - Retardo: `ángulo/360*6` s, para que el ping coincida con el barrido.
  - `<figcaption>`: «En el radar esta semana».
  - Con `prefers-reduced-motion: reduce`, el barrido no gira y los blips tienen la opacidad a 1 y sin animación.
- **Bloque editorial:**
  - `latest_news[0]` grande con portada, kicker «Noticia · <empresa>», titular y entradilla;
  - lista «Imprescindibles» numerada en `--accent`;
  - si `imprescindibles` está vacío, la noticia ocupa todo el ancho.
- **Cuadrículas de tres:**
  - noticias: `latest_news[1:7]`;
  - comparativas;
  - «Herramientas analizadas»: tools con `has_page`, con logotipo, la frase `ideal_para` de su ficha (o `t.desc` si no hay) y la píldora `precio_desde`;
  - guías.
- **Utilidades** en píldoras.
- **`page.body_html`:** contiene «Qué encontrarás» y las preguntas frecuentes con `id="preguntas-frecuentes"`, que debe seguir existiendo porque lo usa una redirección.
- **Sin catálogo.**

Para la píldora, el build pasa `fichas: Dict[str, Page]` (por id de herramienta) en el ctx.

- [ ] **Step 1: Tests que fallan**
  - **build:**
    - la portada contiene `class="radar"` y 5 enlaces `class="blip"` a fichas existentes;
    - contiene «En el radar esta semana» e «Imprescindibles»;
    - **no** contiene `id="cat-`;
    - `/herramientas/index.html` contiene `id="cat-ia-general"` y `catalog.js`;
    - la redirección de runway contiene `url=/herramientas/#cat-video`.
  - **check:**
    - `test_redirect_to_missing_catalog_anchor` con `/herramientas/#cat-nada` da error;
    - `test_content_link_to_old_home_anchor` con `<a href="/#cat-video">` en una página da `ancla inexistente`.

  Generaliza la regla: todo `href` interno con `#cat-` debe tener `id="cat-…"` en el HTML de destino.
  - Actualiza los tests existentes que usaban `/#cat-video` (`test_redirects.py` solo prueba el parseo y puede quedarse igual).

- [ ] **Step 2:** Comprueba que fallan.

- [ ] **Step 3: Implementar.** Mantén `scroll-margin-top` en `.catalog-group`.

- [ ] **Step 4:** Ejecuta pytest, el build y check (sin anclas rotas). Revisa en el preview:
  - a 1440 px, el radar a la derecha;
  - a 375 px, el radar de 260 px debajo del H1;
  - `/herramientas/#cat-video` abre el grupo de vídeo.

- [ ] **Step 5: Commit** con el mensaje «Portada editorial con radar animado y catálogo en /herramientas/».

---

### Task 6: Fichas y artículos a dos columnas

**Files:**
- Create:
  - `templates/partials/toc.html`
  - `templates/partials/related.html`
  - `static/js/toc.js`
- Modify:
  - `templates/tool.html`
  - `templates/article.html`
  - `templates/partials/byline.html`: añade «· N min de lectura».
  - `scripts/build.py`: valida los metadatos de las fichas y pasa `related` y `toc`.
  - `radar/render.py`
  - las 15 fichas de `content/herramientas/*.md`
  - `tests/test_build.py` y `tests/test_render.py`

**Interfaces:**
- Consumes: `toc`, `related_news`, `reading_minutes` (Task 2), `cover` y `logo` (Task 5).
- Produces:
  - `FICHA_FIELDS = ('precio_desde', 'plan_pago', 'ideal_para', 'veredicto')`, en `radar/editorial.py`;
  - `validate_fichas(pages) -> None`: lanza `ValueError("herramientas/<slug>: faltan precio_desde, plan_pago, ideal_para y veredicto")` solo si faltan **los cuatro**.

**Plantillas:**
- **`tool.html`:**
  - cabecera: migas Inicio › Herramientas › Nombre, logotipo de 76 px, kicker «Ficha · <categoría>» (de `CATEGORIES` y `tools[slug].cat`), H1 y byline;
  - columna principal:
    - `.summary`, con 4 casillas: Precio desde, Plan de pago, Ideal para y Plataformas. Cada casilla aparece solo si tiene valor;
    - `.verdict`: «Veredicto en una línea» y el texto;
    - el cuerpo;
    - el anuncio (desactivado);
    - las fuentes.
  - lateral en un `<aside>`:
    - `<details class="toc" open>` con `<summary>En esta página</summary>`, la barra `.progress` y los enlaces;
    - el botón «Visitar <Nombre> →» a `page.extra.web` (`rel="noopener nofollow" target="_blank"`);
    - el anuncio lateral (desactivado).
- **`article.html`:**
  - el mismo esquema;
  - la portada SVG bajo el titular;
  - el kicker es «Noticia · <empresa>», «Guía» o «Comparativa»;
  - en las noticias, `related.html` al final con 3 tarjetas;
  - sin botón de visitar.
- **CSS:**
  - `.article-grid { display:grid; grid-template-columns: minmax(0,1fr) 300px; gap:40px }`;
  - el lateral es `position:sticky; top:16px`;
  - por debajo de 960 px, una sola columna con el índice antes del cuerpo;
  - `#respuesta-rapida + ul` se ve como caja destacada (borde en tinta y fondo `--paper-2`).
- **`toc.js`:**
  - marca con `IntersectionObserver` el `a.on` de la sección visible;
  - la barra `.progress > i` se ensancha según el scroll del `<article>`;
  - en anchos menores de 960 px, cierra el `<details>` al cargar.

**Contenido:**
- Cada ficha recibe `precio_desde`, `plan_pago`, `ideal_para` (2–4 palabras) y `veredicto` (una frase de 25 palabras o menos).
- Todo sale **del texto de esa ficha**: precios exactos de su tabla y veredicto basado en su sección de conclusión o de «para quién».
- Sin afirmaciones de prueba propia.
- **No modifiques** `plataforma` si ya existe.

- [ ] **Step 1: Tests que fallan**
  - **render, ficha con los 4 campos:**
    - el HTML contiene `class="summary"`, «Precio desde», `class="verdict"`;
    - un enlace `href="#<id del primer h2>"` dentro de `class="toc"` y «min de lectura».
  - **render, ficha solo con `precio_desde`:** contiene «Precio desde» y no contiene «Plan de pago».
  - **build:**
    - `validate_fichas` con una ficha sin ninguno de los 4 lanza el error indicado;
    - una noticia muestra 3 relacionadas que no incluyen la propia: en el fixture se crean 4 noticias.

- [ ] **Step 2:** Comprueba que fallan.

- [ ] **Step 3: Implementar** las plantillas, el CSS y `toc.js`, y rellenar las 15 fichas.

- [ ] **Step 4:** Ejecuta pytest, el build y check. Revisa en el preview la ficha de ChatGPT, una comparativa y una noticia:
  - el índice sigue el scroll y la barra avanza;
  - a 375 px el índice es plegable y no hay scroll horizontal.

- [ ] **Step 5: Commit** con el mensaje «Fichas y artículos a dos columnas con índice, resumen y veredicto».

---

### Task 7: Listados, 404 y verificación final

**Files:**
- Modify:
  - `templates/listing.html`: cuadrícula de `card.html` con portada; en `/herramientas/`, `tool_card.html` y debajo el catálogo (Task 5).
  - `scripts/build.py`: el 404 usa un cuerpo nuevo.
  - `templates/page.html` o una nueva `templates/404.html`, elegida en `template_for` cuando `page.url == '/404/'`.
  - `README.md`: una sección «Diseño» que explica `brands.json`, `fetch_logos.py`, `imprescindibles.txt` y los metadatos nuevos de fichas y noticias.

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: nada.

**404:**
- un radar pequeño de 180 px, decorativo con `aria-hidden`;
- H1 «Esta página ha desaparecido del radar»;
- el párrafo de enlaces actual.

- [ ] **Step 1: Tests que fallan**
  - la 404 contiene «Esta página ha desaparecido del radar» y sigue sin canonical;
  - `/noticias/index.html` contiene `<svg` de portada por cada noticia.

- [ ] **Step 2: Implementar.**

- [ ] **Step 3: Verificación completa**
  - Ejecuta:

    ```bash
    .venv/bin/pytest -q && .venv/bin/python scripts/build.py && .venv/bin/python scripts/check.py
    ```

  - Copia el sitio a `_preview`.
  - Revisa en el navegador a 375 px y a 1440 px:
    - la portada;
    - la ficha de ChatGPT;
    - `/mejor-ia-para-imagenes/`;
    - una guía;
    - una noticia;
    - `/herramientas/`;
    - una utilidad;
    - `/legal/politica-cookies/`;
    - `/404.html`.
  - Comprueba en cada página que no hay scroll horizontal (`document.documentElement.scrollWidth <= innerWidth`) y que la consola no da errores.
  - Emula `prefers-reduced-motion` en la portada.
  - Mide el peso: HTML + CSS + JS de la portada ≤ 120 KB sin contar fuentes.

- [ ] **Step 4: Revisión independiente**
  - Un subagente opus revisa toda la rama frente a la spec.
  - Si está disponible, usa la skill de accesibilidad (plugins Design o Axe).
  - Corrige lo que salga.

- [ ] **Step 5: Commit, push y PR**
  - Abre la PR «Rediseño visual editorial con radar», con capturas descritas y el pie de Claude Code.
  - Fusionar despliega en producción, así que **espera el OK de Cristian** después de que vea la previsualización.
