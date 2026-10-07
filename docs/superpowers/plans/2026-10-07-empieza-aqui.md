# «Empieza aquí» — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Construir `/empieza-aqui/`, con 4 tarjetas de situación, una ruta de 5 pasos y texto propio, y enlazarla desde el menú y la portada.

**Architecture:**
- `radar/start.py` carga y valida `data/empieza.json` contra las URLs del sitio.
- El build pasa los datos (`start_payload`) a la nueva plantilla `start.html`, elegida por la URL.

**Spec:** `docs/superpowers/specs/2026-10-07-empieza-aqui-design.md`

## Global Constraints

- **Recuentos:** exactamente 4 situaciones con 2–3 enlaces cada una, y exactamente 5 pasos con 1 `cta` y 0–3 `extra`.
- **URLs:** toda URL existe (una página indexable o una URL de `LISTINGS`); no puede haber enlaces a secciones futuras.
- **Textos fijos:**
  - eyebrow «Empieza aquí»;
  - H1 «¿Por dónde *empiezo*?»;
  - secciones «¿Cuál es tu situación?» y «Tu primera semana con la IA»;
  - en la portada, «¿Nuevo en la IA? Empieza aquí →».
- **Sin JS.** Commits con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **Una URL de `data/empieza.json` deja de existir** (por ejemplo, se borra una guía): el build falla con un mensaje que nombra la URL. *Task 1.*
2. **Build de fixtures sin la página:** ni el menú ni la portada enlazan a `/empieza-aqui/`. *Task 2.*
3. **Menú móvil con 6 elementos:** la píldora resaltada no rompe el menú. *Task 2, en el navegador.*
4. **Tarjetas a 375 px:** una sola columna, sin scroll horizontal. *Task 2.*
5. **Pasos sin `extra`:** no se pinta una línea vacía. *Test en la Task 1.*

---

### Task 1: Datos, validación y página

- **Archivos:**
  - nuevos: `radar/start.py`, `data/empieza.json`, `content/paginas/empieza-aqui.md`, `templates/start.html` y `tests/test_start.py`;
  - cambian: `scripts/build.py` y `radar/render.py` (`template_for` y `start_payload` en el contexto).
- **Interfaz:**
  - `load_start(path) -> dict`;
  - `validate_start(data: dict, urls: Set[str]) -> None`, que lanza `ValueError('empieza.json: …')`.
- **En el build:** si existen `data/empieza.json` y `/empieza-aqui/`, se valida contra las URLs indexables más las de `LISTINGS`, y se pone `base_ctx['start_payload'] = data`.
- **TDD:**
  - con 3 situaciones, falla;
  - con 4 pasos, falla;
  - con una URL inexistente, falla y el error nombra la URL;
  - con un título vacío, falla;
  - con una URL repetida en una tarjeta, falla;
  - el archivo real es válido;
  - el build renderiza 4 `.start-card` y 5 `.start-step`, todos los `href` de la página existen en `_site`, y un paso sin `extra` no pinta `.start-extra`;
  - la página es indexable y supera las 300 palabras.

### Task 2: Menú, portada, estilos y revisión

- **Archivos:**
  - `radar/render.py`: NAV dinámico con `nav_items(has_start)`;
  - `templates/partials/header.html`: clase `nav-start`;
  - `templates/home.html`: línea `hero-start`;
  - `static/css/radar.css`: sección «16. Empieza aquí»;
  - `README.md` y tests.
- **TDD:**
  - en la build real, el primer enlace del menú es `/empieza-aqui/` y la portada tiene la línea;
  - en la build de fixtures, no aparece ninguno de los dos.
- **Navegador:** a 375 y 1440 px.
- **Después:** revisión independiente (opus), correcciones y PR.
