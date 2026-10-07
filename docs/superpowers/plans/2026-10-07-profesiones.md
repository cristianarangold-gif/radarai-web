# IA por profesión — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear el tipo `profesion`, que va de `content/profesiones/<slug>.md` a `/ia-para-<slug>/`. Lleva un kit generado a partir de las fichas, tareas con prompts que se copian con un botón y precauciones del sector. Incluye el índice `/ia-por-profesion/`, 6 profesiones y los enlaces desde «Empieza aquí», las fichas y el buscador.

**Architecture:**
- `radar/professions.py` valida las profesiones y prepara su contexto. Reutiliza la guarda de precios de `radar/duels.py` (`prices_in` y `ficha_text`).
- La plantilla `profession.html` muestra cada profesión.
- El índice es un listado más (`LISTINGS`) con su propia rama en `listing.html`.
- `static/js/prompts.js` añade el botón «Copiar» a las citas.

**Spec:** `docs/superpowers/specs/2026-10-07-profesiones-design.md`

## Global Constraints

- **Kit:** formato `id = para qué`, con entre 2 y 4 entradas que tengan ficha.
- **Tareas:** entre 5 y 7 `###` bajo «Tareas en las que te ayuda», con al menos 5 citas.
- **Encabezados obligatorios:** «Tareas en las que te ayuda» y «Precauciones en tu profesión».
- **Mínimo de palabras:** 1.000.
- **Frases prohibidas:** «hemos probado» y «en nuestras pruebas».
- **Precios:** todos deben figurar en alguna ficha.
- **Textos fijos:**
  - eyebrow «IA por profesión»;
  - «Tu kit en 30 segundos»;
  - «Desde»;
  - «Copiar» / «Copiado»;
  - «Otras profesiones»;
  - «Recomendada para:».
- **`prompts.js`:** sin `innerHTML` y ≤ 1 KB comprimido.
- **Commits** con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **Navegador sin `navigator.clipboard`** (http o permisos denegados): el texto queda seleccionado y el botón no falla. *Task 1.*
2. **Una cita que no es un prompt:** está prohibido por convención en estas páginas, y la guía editorial lo documenta. *Task 1.*
3. **Profesión en borrador:** no aparece en el índice, ni en las fichas, ni en «Otras profesiones». *Tasks 1 y 3.*
4. **Build de fixtures sin `content/profesiones`:** no se genera el índice. *Task 1.*
5. **Kit y botón «Copiar» a 375 px:** sin scroll horizontal y sin tapar el texto. *Task 1, en el navegador.*

---

### Task 1: Motor, plantillas, índice y «IA para docentes»

- **Archivos:**
  - nuevos:
    - `radar/professions.py`, `templates/profession.html`, `static/js/prompts.js` y `tests/test_professions.py`;
    - `content/profesiones/docentes.md` y `content/paginas/ia-por-profesion.md`;
  - cambian:
    - `radar/content.py`;
    - `radar/duels.py`: hace públicos `prices_in` y `ficha_text`;
    - `radar/render.py`, `radar/seo.py` y `radar/covers.py`;
    - `scripts/build.py`: validación y `LISTINGS` (solo si existe `content/profesiones`);
    - `templates/listing.html`;
    - `static/css/radar.css`: sección 19;
    - `content/GUIA_EDITORIAL.md`: regla 11.
- **Interfaz:**
  - `parse_kit(page) -> List[Tuple[str, str]]`;
  - `validate_professions(pages, fichas) -> None`;
  - `profession_context(page, compare_by_id, professions) -> {kit: [(tool, para)], others: [Page]}`;
  - `recommended_for(professions) -> Dict[str, List[Tuple[str, str]]]`.
- **TDD:**
  - todos los casos de validación del spec;
  - la URL y el tipo;
  - el kit toma el precio de la ficha;
  - el índice se genera con sus tarjetas;
  - `prompts.js` sin `innerHTML` y pequeño;
  - el archivo real «docentes» es válido.

### Task 2: Las otras 5 profesiones

- **Archivos:** `content/profesiones/{abogados,disenadores,creadores,administrativos,periodistas}.md`.
- **Test:** hay 6 profesiones válidas, cada una con al menos 1.000 palabras.

### Task 3: Puntos de entrada, revisión y PR

- **Archivos:**
  - `data/empieza.json`;
  - `content/guias/ia-para-pequenas-empresas.md`;
  - `templates/tool.html`: «Recomendada para»;
  - `radar/search.py` + `static/js/search.js`: tipo «Profesión»;
  - `README.md` y tests.
- **Después:** revisión independiente (opus) y PR.
