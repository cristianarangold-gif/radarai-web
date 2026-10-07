# Radar IA — Comparador de herramientas

Fecha: 2026-10-07 · Rama: `comparador` · Maqueta aprobada: `_preview/maquetas/7-comparador.html`, opción **B** (fuera del repo) · Proyecto «Funciones», parte 3 de 5.

## 1. Objetivo

Permitir comparar lado a lado 2 o 3 herramientas de IA con los datos de nuestras fichas: precio desde, plan de pago, ideal para, plataformas y veredicto. Así se decide sin abrir varias pestañas. Es una herramienta útil y propia, y enlaza a nuestras fichas.

**Decisiones del titular:**
- solo las herramientas **con ficha** (hoy, 15; las nuevas entran solas);
- selección con **logotipos para marcar**, hasta 3 (opción B).

**Criterio de éxito:**
- con 2–3 herramientas marcadas, la tabla aparece al momento;
- la URL se puede compartir;
- funciona con teclado y sin JS (tabla resumen estática);
- se ve bien a 375 y a 1440 px;
- los tests, el build y `check.py` están en verde.

## 2. Datos

En el build, `radar/compare.py` genera la lista de herramientas comparables. Entran todas las fichas indexables, ordenadas por nombre, con:

| Campo | Contenido |
|---|---|
| `id` | slug |
| `n` | nombre de marca (o de `tools.json`) |
| `c` / `m` | color y monograma |
| `u` | URL de la ficha |
| `w` | web oficial (`extra.web`) |
| `desde` | `precio_desde` |
| `pago` | `plan_pago` |
| `ideal` | `ideal_para` |
| `plataformas` | `plataforma` |
| `veredicto` | `veredicto` |
| `cat` | etiqueta de la categoría |

Un campo vacío se muestra como «—». **No se marca ninguna herramienta como «la más barata»**: hay precios en euros y en dólares, y planes mensuales y anuales, así que una marca automática podría engañar.

## 3. Página `/comparador/`

- **Contenido:** `content/paginas/comparador.md` (tipo página e indexable), con unas 350 palabras propias:
  - cómo leer la comparación;
  - de dónde salen los datos (nuestras fichas, con su fecha de comprobación);
  - aviso sobre monedas, planes anuales e impuestos;
  - preguntas frecuentes.
- **Plantilla** `compare.html` (elegida por la URL):
  - eyebrow «Comparador» y H1 «Compara herramientas de IA»;
  - `fieldset` con `legend` «Elige hasta 3 herramientas» y una casilla (checkbox) con aspecto de píldora con logo por herramienta;
  - línea de estado `aria-live`: «Elige al menos 2», «2 de 3 elegidas»…;
  - zona de resultado;
  - **tabla resumen estática** de todas las fichas (herramienta, precio desde, plan de pago e ideal para, con enlace a cada ficha), siempre visible debajo, generada en el build, útil sin JS y para buscadores;
  - el cuerpo Markdown.
- **Datos para el JS:** `<script type="application/json" id="comparador-datos">` (con `</` escapado).

## 4. `static/js/compare.js` (sin librerías, DOM y `textContent`)

- **Selección:**
  - con 3 marcadas, las demás quedan desactivadas (`disabled`) y la línea de estado lo explica;
  - con menos de 2, no hay tabla.
- **Tabla de comparación:**
  - es una `<table>` con `<caption>` oculto («Comparación de X, Y y Z»);
  - cabecera con logo y nombre;
  - filas: Precio desde, Plan de pago, Ideal para, Plataformas, Veredicto;
  - una fila final con «Leer la ficha →» y «Web oficial ↗» (`target="_blank" rel="noopener nofollow"`);
  - los encabezados de fila llevan `th scope="row"`.
- **URL compartible:**
  - `?h=chatgpt,claude,gemini` con `replaceState`;
  - al cargar se marcan solo los ids válidos (máximo 3) y los inválidos se ignoran.
- **Móvil:** la tabla se desplaza en horizontal con la primera columna fija (`position: sticky`).

## 5. Puntos de entrada

- **Ficha:** en la columna lateral, debajo de «Visitar …», un botón secundario «Comparar <nombre> con… →» que lleva a `/comparador/?h=<id>`.
- **`/herramientas/`:** encima de las fichas, el botón «⇄ Comparar herramientas».
- **Asistente:** en el resultado, «Comparar con las alternativas →» lleva a `/comparador/?h=<principal>,<alternativas con ficha>` (máximo 3). Solo aparece si al menos 2 tienen ficha.
- **Buscador:** la página entra sola en el índice.

## 6. Pruebas

- **Python:**
  - el payload solo incluye fichas indexables, está ordenado y vale «—» donde falta un campo;
  - la página tiene una casilla por ficha, el JSON incrustado es válido y la tabla estática tiene todas las fichas con enlace;
  - es indexable y supera las 300 palabras;
  - el botón aparece en la ficha y en `/herramientas/`;
  - `compare.js` no usa `innerHTML` y pesa ≤ 5 KB comprimido.
- **Navegador** a 375 y 1440 px:
  - marcar 2 y 3 herramientas, ver la cuarta desactivada y desmarcar;
  - URL compartida (válida, inválida y con más de 3 ids);
  - botón desde una ficha;
  - enlace desde el asistente;
  - teclado;
  - sin scroll horizontal de la página (solo la tabla) y sin errores de consola.

## 7. Fuera de alcance

- Comparar herramientas sin ficha.
- Páginas estáticas «X vs Y» (proyecto «Secciones nuevas»).
- Conversión de monedas.
- Guardar comparaciones.
