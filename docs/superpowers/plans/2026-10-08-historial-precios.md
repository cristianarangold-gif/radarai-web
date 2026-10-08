# Historial de precios — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear `/historial-de-precios/`, con los cambios de precio de los planes individuales de las 15 herramientas desde 2023. Cada cambio va con fecha y fuente permitida. La página incluye tomas propias fechadas, gráfico SVG por herramienta y un recuadro en cada ficha.

**Architecture:**
- `radar/price_history.py` reúne la lógica:
  - lee `data/historial-precios.md` (una línea por cambio) y `data/tomas-precios/*.json` (tomas);
  - valida fuentes y precios frente a las fichas;
  - deduce los cambios entre tomas;
  - prepara el contexto, con las coordenadas del gráfico ya calculadas.
- La plantilla `price_history.html` se elige por la URL. Sin JS.

**Spec:** `docs/superpowers/specs/2026-10-08-historial-precios-design.md`

## Global Constraints

- **Tipos de cambio:** `sube`, `baja`, `nuevo`, `retirado` y `condiciones`. Las etiquetas son «↑ Subida», «↓ Bajada», «＋ Plan nuevo», «− Plan retirado» y «≈ Condiciones».
- **Precio:** `PRICE_VALUE = r'^(desde )?(\d+(?:,\d+)?) (€|\$)(/mes|/año)?$'`. En `sube` y `baja` se escribe `antes → después`.
- **Fechas:** `AAAA-MM` o `AAAA-MM-DD`, entre `2023-01` y `today`, que se pasa como parámetro (en el build, `date.today()`).
- **Planes de empresa rechazados:** `ENTERPRISE_WORDS = ('business', 'team', 'enterprise', 'empresa')`, sin distinguir mayúsculas.
- **Frase:** 30 palabras como máximo y sin `FORBIDDEN` (de `radar/duels.py`).
- **Fuentes:**
  - `PRESS` y `OFFICIAL_EXTRA` según la sección 2.1 de la spec;
  - `web.archive.org` solo vale si apunta a un dominio oficial de esa herramienta;
  - los dominios se comparan como «igual o subdominio de».
- **Mensajes de error:** empiezan por `historial-precios.md: línea N:` o `tomas-precios/<archivo>:`.
- **Textos fijos:**
  - h1 «Cómo han cambiado los precios *de la IA*»;
  - sin cambios en la página: «Sin cambios de precio verificables desde enero de 2023»;
  - sin cambios en el recuadro de la ficha: «Sin cambios registrados desde 2023»;
  - enlace del recuadro: «Ver todos los cambios →»;
  - cambio automático: «Detectado en nuestra revisión del {d} de {mes} de {aaaa}».
- **Commits** con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **Mismo plan con varias monedas o periodos** (por ejemplo, `20 $/mes` y luego `23 €/mes`): no se dibuja una línea que las mezcle. `test_chart_skips_mixed_currency`, en la tarea 1.
2. **Cambio del archivo y cambio automático en el mismo mes:** solo aparece uno. `test_auto_change_not_duplicated`, en la tarea 1.
3. **Fecha `AAAA-MM` del mes actual:** es válida y no cuenta como futura. `test_current_month_is_valid`, en la tarea 1.
4. **Captura de archive con la URL original en http o con `www.`:** se reconoce el dominio. `test_archive_url_variants`, en la tarea 1.
5. **Ficha nueva sin toma:** el build falla con un mensaje que nombra la herramienta. `test_latest_snapshot_must_cover_fichas`, en la tarea 1.

---

### Task 1 (parte 1): Datos y validación

- **Archivos:**
  - nuevos: `radar/price_history.py`, `data/tomas-precios/2026-10-06.json`, `data/historial-precios.md` (solo el comentario de cabecera, sin cambios) y `tests/test_price_history.py`;
  - cambia: `scripts/build.py`, que valida si existe `content/paginas/historial-de-precios.md` o el directorio de tomas. El fallo nombra el archivo que falta.
- **Interfaz:**
  - `Price(amount: Decimal, currency: str, period: str, desde: bool)` y `parse_price(s) -> Price`;
  - `Change(date: str, tool: str, kind: str, plan: str, before: Optional[Price], price: Optional[Price], raw_price: str, text: str, source: str, line: int, auto: bool)`;
  - `Snapshot(date: str, file: str, tools: Dict[str, {'fuente': str, 'planes': Dict[str, str]}])`;
  - `parse_history(text) -> List[Change]` y `load_snapshots(dir: Path) -> List[Snapshot]`, ordenadas por fecha;
  - `validate_history(changes, snapshots, fichas: Dict[str, Page], today: date) -> None`;
  - `auto_changes(snapshots, changes) -> List[Change]`;
  - `chart_points(tool_changes, snapshots, tool) -> Optional[dict]`, que devuelve `{plan, currency, period, points: [(date, Price)]}`.
- **TDD:** todos los casos de error de la sección 6 de la spec, los cambios automáticos, la elección de puntos del gráfico y los 5 tests de Review Focus.
- **Toma real:** `2026-10-06.json` cubre las 15 fichas y valida contra ellas.

### Task 2 (parte 2): Investigación

- **Archivo:** `data/historial-precios.md`, con los cambios de 2023 a hoy.
- **Fuentes:** cada fuente se abre y se comprueba; lo dudoso no entra.
- **Test:** `test_real_history_is_valid`.
- **Parar:** enseñar la lista a Cristian antes de la parte 3.

### Task 3 (parte 3): Página

- **Archivos:**
  - nuevos: `content/paginas/historial-de-precios.md` (al menos 250 palabras) y `templates/price_history.html`;
  - cambian: `radar/render.py` (`template_for` + contexto `price_history`) y `static/css/radar.css` (sección 21).
- **Interfaz:** `history_context(changes, snapshots, compare_by_id) -> {latest, count, recent, tools, by_tool}`. El `chart` de cada herramienta lleva `{plan, label, aria, path, dots: [(x, y, etiqueta)], years: [(x, año)]}`, con viewBox `0 0 320 100`.
- **TDD:** el build real tiene 15 `section` con `id="precios-<id>"`, el `ol` de «Últimos cambios» con 10 o menos, los SVG con `role="img"` y la página indexable.
- **Navegador:** a 375 y 1440 px, sin scroll horizontal.

### Task 4 (parte 4): Enlaces, revisión y PR

- **Archivos:**
  - `templates/tool.html`: recuadro lateral;
  - `radar/search.py` y `static/js/search.js`: tipo «Precios»;
  - `templates/partials/footer.html`;
  - `data/empieza.json`: paso 5, extra;
  - `content/mejor-ia/mejor-ia-gratis.md`;
  - `radar/check.py`: anclas de `/historial-de-precios/#`;
  - `content/GUIA_EDITORIAL.md`: regla 12;
  - `README.md`;
  - tests.
- **Después:** revisión independiente (opus), correcciones y PR.
