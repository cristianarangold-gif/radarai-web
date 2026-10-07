# Cara a cara (X vs Y) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear el tipo de página `duelo` (`content/cara-a-cara/*.md` → `/a-vs-b/`), con formato «veredicto primero», tabla de datos tomada de las fichas, portada con dos marcas y 6 duelos, enlazados desde `/mejor-ia/`, las fichas, el comparador y el buscador.

**Architecture:**
- `radar/duels.py` valida los duelos y prepara su contexto: las herramientas (a partir de `compare_payload`), las tarjetas «Elige…», las filas de la tabla y los duelos relacionados.
- `render.py` pasa ese contexto a la nueva plantilla `duel.html`.
- `covers.py` admite una segunda marca en la portada.

**Spec:** `docs/superpowers/specs/2026-10-07-cara-a-cara-design.md`

## Global Constraints

- **Tipo `duelo`:** sale de la carpeta `cara-a-cara` y su URL es `/<slug>/`. Mínimo de 1.000 palabras.
- **Etiqueta:** `KIND_LABEL` «Cara a cara». La sección es Comparativas (`/mejor-ia/`) y el JSON-LD es `Article`.
- **Metadatos:**
  - `herramientas`: 2 fichas distintas;
  - `respuesta`: 60 palabras como máximo;
  - `elige_1` y `elige_2`: 2–4 frases separadas por `|`;
  - `fuentes`: al menos 1.
- **Frases prohibidas:** «hemos probado» y «en nuestras pruebas».
- **Par único:** no pueden existir a la vez `a-vs-b` y `b-vs-a`.
- **Textos fijos:**
  - eyebrow «Cara a cara»;
  - «Respuesta rápida:»;
  - «Elige {nombre} si…»;
  - filas de la tabla: «Precio desde», «Plan de pago», «Ideal para», «Plataformas», «Comprobado»;
  - enlaces «Ver en el comparador →» y «Ficha de {nombre} →»;
  - «Otros cara a cara».
- **Commits** con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **Se cambia un precio en la ficha:** la tabla del duelo cambia sin tocar el duelo. *Test en la Task 1.*
2. **Herramienta sin marca en `brands.json`:** la portada usa el monograma y no falla. *Task 1.*
3. **Duelo en borrador:** no aparece en `/mejor-ia/`, ni en las fichas, ni en el comparador, ni en los relacionados. *Task 3.*
4. **Tabla y tarjetas a 375 px:** sin scroll horizontal. *Task 1, en el navegador.*
5. **Comparador con el par en orden inverso** (Claude y ChatGPT): también sugiere el duelo. *Task 3.*

---

### Task 1: Motor, plantilla, portada y «ChatGPT vs Claude»

- **Archivos:**
  - nuevos: `radar/duels.py`, `templates/duel.html`, `content/cara-a-cara/chatgpt-vs-claude.md` y `tests/test_duels.py`;
  - cambian:
    - `radar/content.py`: `KIND_BY_DIR`, `_url_for` y `MIN_WORDS`;
    - `radar/render.py`: `TEMPLATE_BY_KIND`, `KIND_LABEL` y contexto;
    - `radar/seo.py`;
    - `radar/covers.py`: `CoverSpec.brand2`;
    - `scripts/build.py`: validación;
    - `static/css/radar.css`: sección 18;
    - `content/GUIA_EDITORIAL.md`.
- **Interfaz:**
  - `duel_tools(page) -> List[str]`;
  - `validate_duels(pages, fichas) -> None`, que lanza `ValueError('cara-a-cara/<slug>: …')`;
  - `duel_context(page, compare_by_id: Dict[str, dict], fichas, duels: List[Page]) -> dict`, que devuelve `{a, b, respuesta, elige: [(tool, [frases])], rows: [(label, va, vb)], related: [Page]}`.
- **TDD:**
  - todos los casos de validación del spec;
  - la URL y el tipo;
  - la tabla toma los datos de la ficha (con una ficha modificada);
  - la portada SVG tiene las dos marcas, y con una marca ausente usa el monograma;
  - el duelo real es válido, tiene al menos 1.000 palabras y es indexable.

### Task 2: Los otros 5 duelos

- **Archivos:** `content/cara-a-cara/{chatgpt-vs-gemini,chatgpt-vs-copilot,perplexity-vs-chatgpt,cursor-vs-github-copilot,notebooklm-vs-chatgpt}.md`.
- **Test:** hay 6 duelos válidos, cada uno con al menos 1.000 palabras.

### Task 3: Puntos de entrada, revisión y PR

- **Archivos:**
  - `templates/listing.html`: sección «Cara a cara» en `/mejor-ia/`;
  - `templates/tool.html`: lista lateral;
  - `radar/compare.py` + `static/js/compare.js`: mapa de duelos y enlace;
  - `radar/search.py` + `static/js/search.js`: tipo «Cara a cara»;
  - `README.md` y tests.
- **TDD:** cada punto de entrada aparece y los borradores se excluyen.
- **Navegador:** a 375 y 1440 px.
- **Después:** revisión independiente (opus) y PR.
