# «¿Funciona en España?» — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Página `/funciona-en-espana/` con la disponibilidad de funciones de IA en EE. UU., la UE y España, con fecha y fuente oficial.

**Architecture:** Datos en `data/disponibilidad.md`, validados y preparados por `radar/availability.py` (mismo patrón que `radar/glossary.py`). `scripts/build.py` pasa `availability` al contexto; `templates/availability.html` pinta la tabla y `static/js/availability.js` añade buscador y filtros sobre el HTML ya completo.

**Tech Stack:** Python 3, Jinja2, Markdown, JS sin dependencias, pytest.

**Spec:** `docs/superpowers/specs/2026-11-04-funciona-en-espana-design.md`

## Global Constraints

- **Estados:** `si`, `parcial`, `no`, `sin_confirmar`. Etiquetas: «✓ Disponible», «◐ Parcial», «✕ No disponible», «? Sin confirmar».
- **Fuentes:** de 1 a 3 URL `https`; dominio oficial de la empresa o copia suya en web.archive.org. Prensa no.
- **Antigüedad:** más de 60 días desde `comprobado` → aviso «Pendiente de revisar»; nunca detiene el build.
- **Publicación:** mínimo 12 funciones. Ningún estado deducido; ante la duda, `sin_confirmar`.
- **No tocar:** precios, anuncios, menú principal (`NAV`). Sin `innerHTML` en JS.
- **Colores:** solo tokens, con versión oscura en los dos bloques; contraste AA.
- **Commits** con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian. Rutas relativas al repo.

## Review Focus

1. **Filtro y búsqueda combinados**, con mayúsculas o acentos («espanol» encuentra «español»): se aplican los dos y se ignoran acentos. `test_js_folds_accents` (tarea 2) y navegador.
2. **Ningún resultado:** se ve el mensaje y el recuento dice 0, sin tabla vacía confusa. `test_page_has_empty_state` (tarea 2) y navegador.
3. **Fila cumpliendo justo 60 días frente a 61:** solo la de 61 lleva aviso. `test_stale_boundary` (tarea 1).
4. **URL de archive.org de otra web o con dominio parecido** (`apple.com.evil.es`): se rechaza. `test_rejects_lookalike_and_foreign_archive` (tarea 1).
5. **Ficha sin funciones:** sin recuadro vacío. `test_box_absent_without_features` (tarea 3).

---

### Task 1 (parte 1): Datos y validador

**Files:**
- Create: `radar/availability.py`, `data/disponibilidad.md`, `content/_investigacion/disponibilidad-2026-11.md`
- Modify: `scripts/build.py` (carga y validación junto al glosario, si existe `data/disponibilidad.md`)
- Test: `tests/test_availability.py`

**Interfaces — Produces:**
- `Feature` (dataclass): `title, id, empresa, ficha, eeuu, ue, es, nota, comprobado (date), fuentes (List[str]), noticia, stale (bool)`.
- `OFICIALES: Dict[str, List[str]]`, empresa → dominios (`openai`, `anthropic`, `google`, `microsoft`, `apple`, `meta`, `github`, y las que requiera la investigación).
- `ESTADOS: Dict[str, Tuple[str, str]]`, estado → (etiqueta, clase CSS `avail-si|parcial|no|duda`).
- `parse_availability(text: str) -> List[Feature]`
- `validate_availability(features: List[Feature], fichas: Dict[str, Page], site_urls: Set[str], today: date) -> None` (lanza `ValueError` con el título del bloque).
- `availability_context(features: List[Feature], today: date) -> dict` con claves `rows`, `count`, `latest` (fecha larga), `stale` (lista), `by_ficha` (dict ficha → filas).
- `build.py` deja `base_ctx['availability']` y, solo con `content/paginas/funciona-en-espana.md`, falla si falta el archivo de datos.

- [ ] **Step 1: Tests que fallan** en `tests/test_availability.py`: `test_parse_block`; `test_rejects_*` para campo ausente, estado desconocido, `id` repetido, título repetido, `id` con mayúsculas, empresa desconocida, ficha desconocida, fecha futura, dominio no oficial, prensa (`techcrunch.com`), más de 3 fuentes, `http://`, nota ausente con `parcial`, nota de 31 palabras, noticia inexistente y `ue: no` con `es: parcial`; `test_rejects_lookalike_and_foreign_archive` (`apple.com.evil.es`, copia de `example.com`); `test_accepts_subdomain_and_official_archive` (`support.apple.com`, copia archivada de `apple.com`); `test_sort_order` (`no`, `parcial`, `sin_confirmar`, `si`, y título con acentos dentro de cada grupo); `test_stale_boundary` (60 días `False`, 61 `True`).
- [ ] **Step 2:** `.venv/bin/pytest -q tests/test_availability.py` → FALLA (módulo inexistente).
- [ ] **Step 3: Implementar `radar/availability.py`**. Reutilizar `ARCHIVE_HOST`, `ARCHIVE_PATH`, `_host` y `_matches` de `radar/price_history.py`.
- [ ] **Step 4:** `.venv/bin/pytest -q tests/test_availability.py` → PASA.
- [ ] **Step 5: Investigación.** Abrir en el navegador pane (desde España) o con `scripts/fetch_source.py` las páginas oficiales de disponibilidad por país de las funciones candidatas: Siri con IA, Apple Intelligence, ChatGPT (voz, memoria, agente, Work), Gemini (Live, Deep Research, funciones en Workspace, Modo IA), Claude, Copilot, Meta AI, NotebookLM/Gemini Notebook, Antigravity, Codex, Perplexity, Canva, DeepL, Suno, Runway, ElevenLabs. Anotar en `content/_investigacion/disponibilidad-2026-11.md` lo leído, con URL y fecha, incluidas las descartadas. Revisar Siri aunque ya figure en la noticia.
- [ ] **Step 6: Escribir `data/disponibilidad.md`** solo con lo comprobado (mínimo 12). Añadir `test_real_data_has_minimum` (≥ 12, y `validate_availability` sobre los datos reales pasa en el build).
- [ ] **Step 7:** `.venv/bin/pytest -q` y `scripts/build.py` → verde.
- [ ] **Step 8: Commit** y mostrar a Cristian la tabla de lo encontrado.

### Task 2 (parte 2): Página

**Files:**
- Create: `content/paginas/funciona-en-espana.md`, `templates/availability.html`, `static/js/availability.js`
- Modify: `radar/render.py` (plantilla para `/funciona-en-espana/` si `ctx.get('availability')`; pasar `availability` al render), `static/css/radar.css` (estilos y tokens), `tests/test_theme.py` (pares nuevos en `test_component_contrast`)
- Test: `tests/test_availability.py`

**Interfaces — Consumes:** `availability_context` (tarea 1). **Produces:** clases `.avail-table`, `.avail-st`, atributos `data-avail-search`, `data-avail-filter`, `data-avail-count`, `data-avail-empty`, `tr[data-es]`.

- [ ] **Step 1: Tests que fallan** con la fixture `site`: `test_page_lists_all_rows_without_js` (todas las filas con `id`), `test_controls_hidden_in_html`, `test_stale_badge_rendered`, `test_sources_and_dates_rendered`, `test_page_has_empty_state` (elemento `data-avail-empty` con `hidden` y `aria-live` en el recuento), `test_page_indexable_and_in_sitemap`, `test_own_text_has_400_words` (cuerpo de `content/paginas/funciona-en-espana.md`); `test_js_has_no_innerhtml`; `test_js_folds_accents` (el JS usa `normalize('NFD')`). Tokens `avail-{si,parcial,no,duda}-{bg,fg}` en `test_component_contrast`.
- [ ] **Step 2:** `.venv/bin/pytest -q tests/test_availability.py tests/test_theme.py` → FALLA.
- [ ] **Step 3: Implementar** plantilla (con `caption` y `scope`), CSS (ficha apilada por debajo de 760 px con `data-l`, como la maqueta, y controles de 44 px), JS (muestra controles, combina filtro y búsqueda sin acentos, actualiza recuento y mensaje vacío) y texto propio: qué significa cada estado, cómo comprobamos, por qué llegan más tarde y preguntas frecuentes, sin consejos legales y con al menos 400 palabras.
- [ ] **Step 4:** `.venv/bin/pytest -q`, `scripts/build.py`, `scripts/check.py --site _site` → verde.
- [ ] **Step 5: Navegador:** búsqueda, filtros, combinación, sin resultados, móvil y 1280 px, claro y oscuro, sin errores de consola. Commit y vista previa para Cristian.

### Task 3 (parte 3): Entradas y mantenimiento

**Files:**
- Modify: `templates/home.html` (línea enlazada junto a `hero-start`), `data/empieza.json`, `templates/tool.html` (recuadro tras «Historial de precios», hasta 3 filas de `availability.by_ficha`), `radar/search.py` (`build_index(..., availability: Optional[list] = None)`, tipo `Disponibilidad`), `static/js/search.js` si lista los tipos, `scripts/build.py`, `docs/rutina-noticias.md`, `content/GUIA_EDITORIAL.md` (regla 13), `README.md`
- Test: `tests/test_availability.py`

- [ ] **Step 1: Tests que fallan:** `test_home_links_page`, `test_start_links_page`, `test_box_in_ficha_with_features` (máximo 3), `test_box_absent_without_features`, `test_search_index_has_features` (`k == 'Disponibilidad'`, `u` con `/funciona-en-espana/#id`), `test_nav_unchanged` (`NAV` no incluye la página), `test_routine_and_guide_document_it`.
- [ ] **Step 2:** comprobar que fallan.
- [ ] **Step 3: Implementar.** En la rutina: si la noticia confirma con fuente oficial un cambio de disponibilidad, actualizar o añadir el bloque en el mismo PR con la nueva fecha y decirlo en el cuerpo; sin confirmación oficial, no tocarlo.
- [ ] **Step 4:** `.venv/bin/pytest -q`, build y `check.py` → verde. Comprobar en el navegador portada, una ficha y el buscador. Commit y vista previa.

### Task 4 (parte 4): Revisión y PR

- [ ] **Step 1:** Revisión independiente (opus) de la rama contra spec y Review Focus, incluida una muestra de filas contra sus fuentes.
- [ ] **Step 2:** Corregir hallazgos con test cuando aplique; `.venv/bin/pytest -q`, build y `check.py` → verde.
- [ ] **Step 3:** Abrir la PR y esperar el OK de Cristian («Sí, fusiónalo y publícalo»).
- [ ] **Step 4 (tras el OK):** Fusionar cuando pasen los checks, confirmar el despliegue y la página en directo, y actualizar el resumen de la rutina en la nube con `RemoteTrigger`.
