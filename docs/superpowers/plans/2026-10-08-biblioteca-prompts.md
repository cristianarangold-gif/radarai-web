# Biblioteca de prompts — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear `/prompts/`, una sola página con unos 60 prompts validados. Cada prompt tiene huecos que se rellenan en la tarjeta, botón «Copiar», filtro y entrada en el buscador.

**Architecture:**
- `radar/prompt_library.py` lee `data/prompts.md` (bloques `## Título` + metadatos + prompt en texto plano con `[huecos]`), lo valida y lo agrupa por categoría.
- La plantilla `prompts.html` se elige por la URL.
- `static/js/library.js` se encarga de filtrar, rellenar los huecos y copiar.

**Spec:** `docs/superpowers/specs/2026-10-08-biblioteca-prompts-design.md`

## Global Constraints

- **Categorías (en este orden):** `escribir`, `estudiar`, `trabajo`, `marketing`, `imagenes`, `programar`, `dia-a-dia` y `pensar`.
- **Claves:** `categoria` (obligatoria), `herramientas` (1–2 con ficha), `para` (≤ 25 palabras) y `consejo` (opcional, ≤ 40 palabras).
- **Prompt:** entre 15 y 150 palabras, con 0–4 huecos distintos `[…]` y corchetes bien cerrados.
- **Frases prohibidas:** las de `radar/duels.py` (`FORBIDDEN`).
- **Textos fijos:**
  - eyebrow «Biblioteca de prompts»;
  - H1 «Prompts para copiar y *usar ya*»;
  - «Sugerido:»;
  - «Copiar» / «Copiado»;
  - sin resultados: «Ningún prompt coincide. Prueba con otra palabra o sugiérenos uno.».
- **`library.js`:** sin `innerHTML` y ≤ 2,5 KB comprimido.
- **Commits** con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **Hueco repetido en un mismo prompt:** un solo campo, que rellena todas las apariciones. *Task 1.*
2. **Valor con caracteres especiales** (`<`, `&`, comillas): se muestran como texto y no rompen nada (`textContent`). *Task 1, en el navegador.*
3. **Sin portapapeles:** el texto queda seleccionado con los huecos ya rellenos. *Task 1.*
4. **`/prompts/#slug` con un filtro activo:** se quita el filtro y se muestra la tarjeta. *Task 1.*
5. **Tarjetas y campos a 375 px:** sin scroll horizontal. *Task 1.*

---

### Task 1: Motor, plantilla, JS y 12 prompts

- **Archivos:**
  - nuevos: `radar/prompt_library.py`, `data/prompts.md`, `content/paginas/prompts.md`, `templates/prompts.html`, `static/js/library.js` y `tests/test_prompt_library.py`;
  - cambian: `scripts/build.py`, `radar/render.py` y `static/css/radar.css` (sección 20).
- **Interfaz:**
  - `parse_prompts(text) -> List[Prompt]`;
  - `validate_prompts(prompts, fichas) -> None`, que lanza `ValueError('prompts.md: «título»: …')`;
  - `library_context(prompts, compare_by_id) -> {groups: [...], count}`;
  - `Prompt.segments`: lista de `('text' | 'slot', texto)`;
  - `Prompt.slots`: los huecos distintos, en orden.
- **En el build:** si existe `/prompts/` pero no `data/prompts.md`, el build falla.
- **TDD:**
  - el parser y los huecos;
  - todos los casos de validación;
  - el render (tarjetas, `mark.slot`, campos y controles con `hidden`);
  - el JS (sin `innerHTML` y pequeño).

### Task 2: Contenido

- **Archivos:** `data/prompts.md` (≥ 50 prompts, ≥ 5 por categoría) y `content/paginas/prompts.md`.
- **Test:** el archivo real es válido y la página supera las 300 palabras.

### Task 3: Buscador, enlaces, revisión y PR

- **Archivos:**
  - `radar/search.py` y `static/js/search.js`: tipo «Prompt»;
  - `radar/check.py`: anclas de `/prompts/#`;
  - `data/empieza.json`;
  - `content/guias/mejores-prompts.md`;
  - `templates/partials/footer.html`;
  - `README.md` y tests.
- **Después:** revisión independiente (opus) y PR.
