# Modo oscuro — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Modo oscuro cálido en radarai.es, automático según el dispositivo y con un botón sol/luna en la cabecera que recuerda la elección.

**Architecture:**
- Tokens de color en `:root` (claro) y redefinidos para oscuro en `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])` y en `:root[data-theme="dark"]`.
- Un script en línea en el `<head>` aplica la elección guardada antes de pintar.
- El botón vive en `header.html` y su lógica en `static/js/site.js`.

**Spec:** `docs/superpowers/specs/2026-10-10-modo-oscuro-design.md`

## Global Constraints

- **Paleta oscura:** exactamente la de la sección 2 de la spec. El modo claro no cambia ningún valor.
- **Clave de almacenamiento:** `localStorage['radar-tema']`, con valores `light` o `dark`. Todo acceso va dentro de `try/catch`.
- **Textos fijos:** botón `aria-label` «Activar modo oscuro» o «Activar modo claro», con `title` igual.
- **Visibilidad:** el botón lleva `hidden` en el HTML y `site.js` lo muestra.
- **Seguridad:** sin `innerHTML` con datos externos; los iconos son SVG fijos del código.
- **Contraste AA** en los pares de tokens: 4,5 en texto y 3 en bordes y controles.
- **Commits** con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **Destello al cargar con `data-theme="dark"` guardado y el sistema en claro:** la página se pinta oscura desde el primer fotograma. `test_head_script_before_stylesheet`, en la tarea 1, más comprobación en el navegador.
2. **`localStorage` bloqueado** (ventana privada o cookies bloqueadas): el botón cambia el modo en la página sin errores en la consola. Comprobación en el navegador en la tarea 1.
3. **Fondos `var(--ink)` con texto `var(--white)`** (botones, cabeceras de tabla, píldoras): en oscuro deben quedar legibles. `test_no_white_text_on_ink`, en la tarea 1.
4. **Colores fijos fuera de los bloques de tokens:** ninguno queda sin versión oscura. `test_no_literal_colors_outside_tokens`, en la tarea 2, con una lista blanca justificada.
5. **Portadas SVG, logos y radar:** se ven igual en ambos modos y no quedan cajas blancas alrededor. Comprobación en el navegador en la tarea 2.

---

### Task 1 (parte 1): Mecanismo y tokens

- **Archivos:**
  - `templates/base.html`: script anti-destello antes del `<link>` CSS, y metas `color-scheme` y `theme-color` (claro #fbf8f3, oscuro #17150f);
  - `templates/partials/header.html`: botón `button.theme-toggle` con `hidden`, entre «Buscar» y «Menú»;
  - `static/js/site.js`: lógica del botón;
  - `static/css/radar.css`: bloques de tokens oscuros, nuevos `--surface` y `--on-ink`, y paso de `var(--white)` a uno de los dos según su uso;
  - nuevo: `tests/test_theme.py`.
- **Interfaz** (en `site.js`):
  - `effectiveTheme() -> 'light'|'dark'`: lee `data-theme` y, si no hay, `matchMedia('(prefers-color-scheme: dark)')`;
  - `applyTheme(t)`: pone el atributo, guarda la elección y actualiza el icono y el `aria-label`.
- **TDD** (`tests/test_theme.py`, sobre el HTML construido y el CSS):
  - el script del `<head>` va antes de `radar.css` y contiene `try`;
  - el botón existe, con `hidden` y `aria-label`;
  - los metas están presentes;
  - los dos bloques oscuros definen los mismos tokens y con los mismos valores;
  - cada token del claro tiene versión oscura;
  - contraste AA de los pares `ink/paper`, `ink-2/paper`, `ink-3/paper`, `ink/surface`, `accent-ink/paper`, `accent-ink/surface` y `on-ink/ink` en ambos modos;
  - ningún `color: var(--white)` sobre fondos que cambian.
- **Navegador:** portada y una ficha en claro, en oscuro automático (emulado) y con el botón; recarga sin destello; `localStorage` bloqueado.

### Task 2 (parte 2): Componentes

- **Archivos:**
  - `static/css/radar.css`: colores fijos a tokens, con variantes oscuras para las etiquetas del historial, los avisos y el código;
  - `static/js/search.js`, si sus colores no funcionan en oscuro;
  - plantillas con estilos en línea, si las hay.
- **TDD:** `test_no_literal_colors_outside_tokens` (lista blanca: portadas, logos, radar y colores de marca).
- **Navegador:** en claro y en oscuro, móvil y 1280 px:
  - portada, ficha, comparativa, «Cara a cara», profesión y noticia;
  - glosario, prompts, historial de precios, comparador, asistente;
  - una utilidad, el buscador, autor y 404.

### Task 3 (parte 3): Pulido, revisión y PR

- **Ajustes** de contraste o detalles vistos en la tarea 2.
- **Cierre:** README (una línea), revisión independiente (opus), correcciones y PR.
