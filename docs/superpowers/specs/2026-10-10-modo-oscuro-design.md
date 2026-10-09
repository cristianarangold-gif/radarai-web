# Radar IA — Modo oscuro

Fecha: 2026-10-10 · Rama: `modo-oscuro` · Maqueta: `_preview/maquetas/15-modo-oscuro.html` (fuera del repo), paleta **2 · Oscuro cálido**.

## 1. Objetivo

Que radarai.es tenga un modo oscuro completo:

- **Automático**: por defecto la web sigue el ajuste del dispositivo (`prefers-color-scheme`).
- **Manual**: un botón en la cabecera (luna en modo claro, sol en modo oscuro) cambia al otro modo y la elección se recuerda en ese navegador.

**Decisiones del titular:** paleta oscura cálida (marrón casi negro, letras crema, naranja de la marca); botón de dos estados que se recuerda; sin menú de tres opciones.

**Criterio de éxito:**

- Todas las páginas se leen bien en claro y en oscuro: contraste AA (4,5:1 en texto normal y 3:1 en texto grande y bordes de controles) en los pares de tokens.
- Sin destello: la página carga directamente en el modo correcto.
- Funciona sin JS en modo automático; el botón solo aparece si hay JS.
- Ningún cambio visible en modo claro.
- Tests, build y `check.py` en verde.

## 2. Tokens

La hoja `static/css/radar.css` ya define los colores como variables en `:root`. Se añaden dos tokens semánticos y se reparten los usos actuales de `var(--white)`:

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--paper` | #fbf8f3 | #17150f | Fondo de la página |
| `--paper-2` | #f3ece0 | #221f18 | Fondos suaves (citas, avisos) |
| `--surface` (nuevo) | #ffffff | #1f1c16 | Tarjetas, tablas, campos (hoy `var(--white)` como fondo) |
| `--on-ink` (nuevo) | #ffffff | #17150f | Texto sobre fondos `--ink` o `--accent-ink` (hoy `var(--white)` como color) |
| `--ink` | #151515 | #f2ede4 | Texto principal y bordes fuertes |
| `--ink-2` | #444 | #cfc8bb | Texto secundario |
| `--ink-3` | #6b6b6b | #a39b8d | Texto terciario |
| `--rule` / `--rule-2` | #e0d9cc / #eee5d6 | #3a352b / #2d2922 | Líneas |
| `--accent` | #e4572e | #ff7a4d | Acento |
| `--accent-ink` | #c2401b | #ff8f66 | Enlaces y textos en acento |
| `--amber` | #f3a712 | #f3b23a | Resaltados (huecos de prompts) |

- `--white` se mantiene solo donde de verdad debe ser blanco en ambos modos (por ejemplo, iconos sobre los círculos de marca).
- Los colores fijos sueltos (unos 20: etiquetas del historial de precios, avisos, botones, código) pasan a tokens con versión oscura.
- Las portadas SVG de artículos, los logos de marca y el radar de la portada ya tienen fondo propio y no cambian.

## 3. Cambio de modo

- **Atributo:** `<html data-theme="light|dark">` solo cuando el visitante ha elegido; sin elección no hay atributo y manda `prefers-color-scheme`.
- **CSS:** valores claros en `:root`; oscuros en `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {…} }` y en `:root[data-theme="dark"] {…}`, con `color-scheme: dark` en ambos.
- **Sin destello:** un script mínimo en línea, en el `<head>` y antes de la hoja de estilos, lee `localStorage['radar-tema']` (dentro de `try/catch`) y pone `data-theme` antes de pintar.
- **Metas:** `<meta name="color-scheme" content="light dark">` y dos `<meta name="theme-color">` con `media`.
- **Botón** en `templates/partials/header.html`, junto a «Buscar»:
  - `button.theme-toggle` con `hidden`, que `site.js` muestra;
  - icono SVG de luna o sol según el modo **efectivo**;
  - `aria-label` «Activar modo oscuro» o «Activar modo claro»;
  - al pulsar, fija el otro modo, lo guarda y actualiza icono y etiqueta;
  - si cambia el ajuste del sistema y no hay elección guardada, el icono se actualiza.

## 4. Componentes a revisar

- **Toda la hoja de estilos:**
  - los 68 usos de `var(--white)`;
  - los 27 fondos `var(--ink)`, que en oscuro pasan a ser claros con texto `--on-ink`;
  - las 8 `rgba()`;
  - los ~20 colores fijos.
- **Elementos concretos:**
  - cabecera y menú móvil;
  - tarjetas, tablas y bloques de código;
  - utilidades (campos y resultados);
  - buscador (ventana y resultados, colores de `search.js`);
  - asistente, comparador, glosario y biblioteca de prompts (huecos ámbar y botones «Copiar»);
  - historial de precios (etiquetas y gráfico SVG);
  - portada, fichas, «Cara a cara», profesiones, noticias, páginas legales y 404.
- **Imágenes:** la foto del autor y los logos se ven igual en ambos modos.

## 5. Tests

- **`tests/test_theme.py`:**
  - el script de cabecera está antes de la hoja de estilos y usa `try`;
  - existe el botón con `hidden` y `aria-label`;
  - existen los metas `color-scheme` y `theme-color`;
  - cada token claro tiene su versión oscura en los dos bloques, y los dos bloques son idénticos;
  - contraste AA calculado en Python para los pares texto/fondo de ambos modos;
  - fuera de los bloques de tokens no quedan colores fijos, salvo una lista blanca justificada.
- **Navegador:** unas 12 páginas tipo en claro y oscuro, en móvil y ordenador, el botón y la recarga sin destello.

## 6. Partes

1. **Mecanismo y tokens:** script anti-destello, botón, metas, tokens oscuros y los cambios de `--white` a `--surface` / `--on-ink`. Vista previa de la portada y una ficha en ambos modos.
2. **Componentes:** colores fijos, utilidades, buscador, historial, prompts, asistente, comparador… Vista previa de todas las páginas tipo.
3. **Pulido:** contraste, revisión independiente y PR.
