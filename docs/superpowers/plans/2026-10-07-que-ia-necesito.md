# «¿Qué IA necesito?» — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear el asistente de 4 preguntas en `/que-ia-necesito/`. Recomienda una herramienta con su «por qué» editorial y da alternativas editoriales y del catálogo. Se enlaza desde la portada, las comparativas y las guías.

**Architecture:**
- **Datos editoriales:** `data/asistente.json`.
- **Build:** `radar/assistant.py` valida los datos y los resuelve. Calcula las alternativas automáticas para cada combinación tarea × presupuesto × nivel y genera un JSON que se incrusta en la página.
- **Navegador:** `static/js/assistant.js` solo pinta el resultado. La página es de tipo `pagina` y se renderiza con la plantilla `assistant.html`.

**Tech Stack:** Python 3.9/3.12, Jinja2, pytest y JS sin dependencias.

**Spec:** `docs/superpowers/specs/2026-10-07-que-ia-necesito-design.md`

## Global Constraints

- **Ids fijos de las respuestas:**
  - tareas: `escribir`, `estudiar`, `imagenes`, `video`, `musica`, `programar`, `marketing`, `productividad`, `general`;
  - presupuesto: `gratis`, `poco`, `sin-limite`;
  - nivel: `empiezo`, `me-manejo`, `avanzado`;
  - para quién: `mi`, `equipo`.
- **Reglas:**
  - claves `<tarea>/<presupuesto>`, 27 en total;
  - `principal` debe tener ficha;
  - `porque` lleva 2–3 frases tomadas del texto de comparativas o fichas propias;
  - nunca «hemos probado».
- **Alternativas automáticas:**
  - como máximo 2, de las `categorias` de la tarea;
  - con `gratis`, solo `price` ∈ {gratis, freemium};
  - con `empiezo`, `level` ≠ avanzado;
  - se excluyen la principal y las editoriales;
  - orden: primero las que tienen ficha, luego por nombre.
- **Textos fijos:**
  - eyebrow «Asistente gratuito»;
  - H1 «¿Qué IA necesito?» con «IA» en cursiva naranja;
  - recuadro «¿No lo tienes claro? Responde 4 preguntas y te decimos cuál encaja contigo. Hacer el test →».
- **Seguridad y tamaño:** nada de `innerHTML` con datos, y `assistant.js` ≤ 6 KB comprimido.
- **Commits** en la rama `que-ia-necesito`, con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **URL compartida con valores inválidos** (`?tarea=xyz`): se ignora el valor, no se rompe nada y no aparece resultado hasta que haya respuestas válidas. *Task 3.*
2. **`si_avanzado` y `si_equipo` a la vez:** gana `si_equipo`, como dice la spec. *Test en la Task 1.*
3. **Herramienta alternativa sin ficha:** enlaza a `/herramientas/#cat-<cat>`, nunca a una ficha inexistente. *Test en la Task 1; `check.py` lo cubre en la Task 2.*
4. **`</script>` en un texto del JSON incrustado:** se escapa y no rompe la página. *Task 2.*
5. **Con `gratis`, el recomendado debe tener `precio_desde` igual a 0** (0 € o 0 $) en su ficha; si no, el build falla. *Test en la Task 1.*

---

### Task 1: Datos editoriales y resolución

**Files:**
- Create: `data/asistente.json`, `radar/assistant.py`, `tests/test_assistant.py`
- Modify: `scripts/build.py` (cargar, validar y resolver)

**Interfaces:**
- Produces:
  - `TASKS`, `BUDGETS`, `LEVELS` y `AUDIENCES`: tuplas de ids;
  - `load_assistant(path) -> dict`;
  - `validate_assistant(data, tools, fichas: Dict[str, Page], urls: Set[str]) -> None`: lanza `ValueError("asistente.json: <clave>: <motivo>")`;
  - `pick_rule(data, tarea, presupuesto, nivel, para) -> dict`: devuelve `si_equipo` si `para == 'equipo'` y existe; si no, `si_avanzado` si `nivel == 'avanzado'` y existe; si no, la regla base;
  - `auto_alternatives(data, tools, tarea, presupuesto, nivel, exclude: Set[str], n=2) -> List[str]`;
  - `resolve_payload(data, tools, brands, fichas) -> dict`, con la forma `{"tareas": {...}, "reglas": {clave: regla}, "auto": {"tarea/presupuesto/nivel": [ids]}, "tools": {id: {n, u, c, m, p, i, w, nivel}}}`:
    - `u` es la ficha o `/herramientas/#cat-<cat>`;
    - `c` y `m` son el color y el monograma de la marca, o tinta y la inicial;
    - `p` es `precio_desde`; `i` es `ideal_para` (o la descripción del catálogo); `w` es la web oficial (el `extra.web` de la ficha o `tool.url`);
    - `nivel` es `tool.level`.

- [ ] **Step 1: Tests que fallan**
  - **Validación:** falta una regla, id desconocido, principal sin ficha, URL inexistente, `porque` con 1 o con 4 frases, «hemos probado», y principal de una regla `gratis` cuyo `precio_desde` no empieza por «0».
  - **`pick_rule`:** con los dos overrides gana el de equipo.
  - **`auto_alternatives`:** filtros de precio y nivel, exclusiones, orden y n=2.
  - **`resolve_payload`:** una herramienta sin ficha lleva una `u` con `#cat-`.
  - **Archivo real:** `data/asistente.json` es válido y tiene 27 reglas.
- [ ] **Step 2:** Comprueba que fallan.
- [ ] **Step 3: Implementa `radar/assistant.py`** y redacta `data/asistente.json` a partir de la «Respuesta rápida» y del texto de las 9 comparativas y las fichas.
- [ ] **Step 4:** Integra en el build: valida y guarda `assistant_payload` en el contexto.
- [ ] **Step 5:** Ejecuta pytest, el build y check. **Resultado esperado:** todo en verde. Después, commit.

### Task 2: Página `/que-ia-necesito/`

**Files:**
- Create: `content/paginas/que-ia-necesito.md` (unas 500 palabras), `templates/assistant.html`
- Modify: `radar/render.py` (`template_for` y paso del payload), tests

**Contenido de `assistant.html`:**
- el formulario con 4 `fieldset`, `legend` y `input type=radio name=tarea|presupuesto|nivel|para` con aspecto de píldora;
- `<div class="assistant-result" aria-live="polite">`;
- `<noscript>` con «Elige por tarea»: los 9 enlaces a las comparativas;
- el cuerpo Markdown;
- `<script type="application/json" id="asistente-datos">{{ assistant_payload | to_json }}</script>`.

- [ ] **Steps (TDD):** los tests de la plantilla:
  - 4 `fieldset`;
  - el JSON incrustado es válido;
  - `</script` solo aparece como cierre;
  - el bloque sin JS tiene 9 enlaces;
  - la página es indexable y supera las 400 palabras.

  Después implementa, ejecuta pytest, el build y check, y haz commit.

### Task 3: `assistant.js` y estilos

**Files:**
- Create: `static/js/assistant.js`
- Modify: `static/css/radar.css` (sección «14. Asistente»), tests

**Comportamiento:**
- con las 4 respuestas, pinta el resultado de la spec §4;
- lee y escribe `?tarea&presupuesto&nivel&para` e ignora los valores inválidos;
- en el móvil, desplaza el resultado a la vista la primera vez.

- [ ] **Steps (TDD):**
  - test estático: sin `innerHTML`, contiene `textContent` y `replaceState`, y pesa ≤ 6 KB comprimido;
  - implementa;
  - verifica en el navegador: combinaciones, override de avanzado y de equipo, URL compartida, valores inválidos, teclado, 375/1440 px y consola;
  - commit.

### Task 4: Puntos de entrada, revisión y PR

**Files:** `templates/home.html`, `templates/article.html` (recuadro en comparativas y guías), `README.md`, tests

- [ ] **Steps (TDD):**
  - tests: la portada tiene `href="/que-ia-necesito/"` como botón principal; las comparativas y guías tienen el recuadro; las noticias y fichas no;
  - implementa y verifica en el navegador;
  - revisión independiente (opus) y correcciones con RED→GREEN;
  - push y PR (no se fusiona sin el OK de Cristian).
