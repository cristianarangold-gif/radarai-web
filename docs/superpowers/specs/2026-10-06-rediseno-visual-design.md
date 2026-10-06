# Radar IA — Rediseño visual

Fecha: 2026-10-06 · Rama: `rediseno-visual` · Maquetas aprobadas: `_preview/maquetas/1-…4-*.html` (fuera del repo)

## 1. Objetivo

La web actual es correcta en contenido, pero visualmente plana: no tiene imágenes, todas las tarjetas son iguales y no tiene identidad propia. El objetivo es que Radar IA sea **muy atractiva visualmente** y transmita la confianza de un medio editorial, con una seña de identidad propia: **el radar**.

**Decisiones del titular (aprobadas con maquetas):**

1. **Estilo general «Editorial claro» (B):**
   - fondo crema y tipografía con serifa en titulares;
   - noticia destacada grande y lista lateral;
   - herramientas con logotipo y precio.
2. **Radar oscuro animado en la cabecera de la portada (opción 1):** disco oscuro con barrido giratorio. Las herramientas «se iluminan» al pasar el barrido y cada una enlaza a su ficha.
3. **Fichas y comparativas a dos columnas** con índice lateral fijo, barra de progreso, botón a la web oficial y hueco de anuncio lateral.
4. **Imágenes de portada «radar con logotipo» (A):** se generan automáticamente para cada artículo y también sirven como imagen al compartir (`og:image`).

**Criterio de éxito:**
- Cada tipo de página (portada, ficha, comparativa, guía, noticia, listados, utilidades, legales) usa el nuevo sistema visual.
- Toda página indexable tiene imagen para compartir.
- La portada muestra el radar animado.
- No hay regresiones: tests y `check.py` en verde.
- Se ve bien a 375 px y a 1440 px.

## 2. Sistema visual

**Colores (tokens CSS en `:root`):**

| Token | Valor | Uso |
|---|---|---|
| `--paper` | `#fbf8f3` | fondo de página |
| `--paper-2` | `#f3ece0` | bloques secundarios |
| `--ink` | `#151515` | texto, líneas fuertes, cabeceras de tabla |
| `--ink-2` | `#444` | texto secundario |
| `--rule` | `#e0d9cc` | separadores |
| `--accent` | `#e4572e` | naranja de marca: kicker, números, enlaces activos |
| `--amber` | `#f3a712` | detalles (veredicto) |
| `--radar-bg` | `#2a2560` → `#0d1124` | radial del disco del radar |
| `--radar-line` | `rgba(130,200,210,.3–.55)` | anillos y barrido |

**Tipografía:**
- Titulares: **Fraunces** (800/600).
- Texto: **Inter** (400–700).
- Ambas se **alojan en la propia web** (`static/fonts/`, licencia OFL) en lugar de cargarse de Google Fonts. Así son más rápidas, no envían la IP de los visitantes a Google y los mismos TTF sirven para generar las imágenes PNG.
- Se quita la mención a Google Fonts de las políticas legales.

**Componentes:**
- **Cabecera de sitio:**
  - logotipo de texto «Radar**IA**» en Fraunces, con «IA» en `--accent`;
  - navegación: Comparativas, Herramientas, Guías, Noticias, Utilidades;
  - línea inferior de 2 px en tinta.
  - En el móvil: menú plegable (como ahora, funcionando sin JS).
- **Pie:** banda en tinta con el logotipo, el lema «La IA en tu día», un mini radar decorativo y tres columnas de enlaces.
- **Tarjeta de artículo:** imagen de portada 1200×630 (radar con logotipo), kicker en naranja («Noticia · OpenAI»), titular en Fraunces y fecha o tiempo de lectura.
- **Tarjeta de herramienta:** logotipo, nombre, frase «ideal para» y una píldora en tinta con el precio («Desde 0 € · Plus 23 €»).
- **Botones:** primario en tinta con texto blanco y secundario con borde en tinta, ambos con esquinas de 4 px.
- **Anuncios:** el componente actual se mantiene, desactivado hasta la aprobación de AdSense y con su espacio reservado solo cuando se active (no se ven huecos vacíos).

## 3. Radar animado (portada)

- **Construcción:** SVG y CSS en línea, sin librerías.
  - Disco con degradado radial oscuro y 4 anillos.
  - Barrido: `conic-gradient` que gira con `@keyframes` en 6 s.
  - 5 «blips» con el logotipo y el nombre, cuya animación `ping` se desfasa según su ángulo para que se iluminen al paso del barrido.
- **Qué herramientas aparecen:**
  1. Se calculan en el build: herramientas citadas en las 6 noticias más recientes (nuevo metadato `herramientas:` con ids de `tools.json`), por orden de aparición.
  2. Se completan hasta 5 con una lista por defecto: chatgpt, claude, gemini, midjourney, perplexity.
  3. Solo entran ids con ficha publicada, porque cada blip enlaza a `/herramientas/<id>/`.
- **Pie del radar:** «En el radar esta semana».
- **Accesibilidad:**
  - con `prefers-reduced-motion` el barrido se detiene y todos los blips quedan visibles;
  - el radar lleva `aria-label`;
  - los blips son enlaces reales con texto.
- **Móvil:** el radar se muestra a 260 px debajo del titular.

## 4. Logotipos y colores de marca

- **Datos nuevos en `data/brands.json`:** por cada marca (herramienta o empresa), su color (`color`), su icono de Simple Icons (`icon`) y su monograma de respaldo (`monograma`).
- **Iconos:** SVG monocromos de **Simple Icons** (CC0) guardados en `static/logos/<icono>.svg` mediante un script de descarga único (`scripts/fetch_logos.py`). Uso nominativo, solo para identificar cada producto.
- **Marcas sin icono** (Midjourney, Runway, Microsoft Copilot…): **monograma** (inicial en blanco sobre su color).
- **Pintado en las páginas:** el logotipo es un círculo con el color de la marca y el icono en blanco (SVG en línea).
- **Relación con el contenido:**
  - las fichas usan su id;
  - las noticias usan un metadato nuevo `empresa:` (openai, google, anthropic…);
  - comparativas y guías usan un icono de sección propio (estrella o libro, dibujado en SVG).

## 5. Imágenes de portada y `og:image`

- **Generador** `radar/covers.py`, con dos salidas para cada página indexable:
  1. **SVG en línea** para las tarjetas y la cabecera del artículo: nítido y sin peso extra.
  2. **PNG 1200×630** en `_site/og/<ruta>.png` para `og:image` y `twitter:image`, dibujado con **Pillow** (nueva dependencia, fijada): radar, logotipo o monograma, etiqueta de fuente («OPENAI», «COMPARATIVA») y la marca «RadarIA».
     - En el PNG, el logotipo es el monograma: Pillow no dibuja SVG.
     - Los PNG se generan en cada build y no se versionan en git.
- **Metadatos:** `base.html` añade `og:image`, `og:image:width/height`, `twitter:card=summary_large_image` e imagen en el JSON-LD de los artículos.
- **`check.py`:** cada página indexable debe declarar un `og:image` que exista en `_site`.

## 6. Plantillas por tipo de página

- **Portada (`home.html`), en este orden:**
  1. Cabecera.
  2. **Banda principal:** eyebrow «La IA en tu día», H1 en Fraunces con «inteligencia artificial» en cursiva naranja, entradilla, botones «Ver comparativas» y «Explorar herramientas», y radar a la derecha.
  3. **Bloque editorial:** noticia más reciente en grande (portada, kicker, titular y entradilla) y, a la derecha, **«Imprescindibles»**: 4 piezas de fondo elegidas a mano en `data/imprescindibles.txt` y numeradas en naranja. No se llama «Lo más leído» porque no medimos visitas y sería falso.
  4. Últimas noticias en cuadrícula de 3 con portada.
  5. Comparativas en cuadrícula con portada.
  6. «Herramientas analizadas» en cuadrícula con logotipo y precio.
  7. Guías.
  8. Utilidades en fila de píldoras.
  9. Preguntas frecuentes.
  10. Pie.
  - **Catálogo de 126 herramientas:** **sale de la portada** y pasa a `/herramientas/`, debajo de las fichas. Las redirecciones de fichas retiradas apuntan ahora a `/herramientas/#cat-<categoría>`, y `check.py` valida el ancla en esa página.
- **Ficha (`tool.html`):**
  - **Cabecera:** migas, logotipo grande, kicker «Ficha · <categoría>», H1, autor, «Actualizado el…» y tiempo de lectura.
  - **Columna principal:**
    - **resumen en 4 casillas** (`precio_desde`, `plan_pago`, `ideal_para`, `plataforma`), con metadatos nuevos en las 15 fichas tomados de su propio texto;
    - **veredicto** en caja de tinta (metadato `veredicto`);
    - el cuerpo.
  - **Columna lateral fija (escritorio):** índice generado de los H2 con la sección activa resaltada, barra de progreso, botón «Visitar <herramienta> →» y hueco de anuncio.
- **Comparativa, guía y noticia (`article.html`):**
  - mismo esquema de dos columnas, con imagen de portada bajo el titular;
  - en comparativas, la lista tras «Respuesta rápida» se presenta como caja destacada mediante CSS sobre `#respuesta-rapida + ul`, sin tocar el contenido;
  - las noticias muestran «Noticia · <Empresa>» y, al final, 3 noticias relacionadas (las más recientes).
- **Listados (`listing.html`):**
  - cuadrícula de tarjetas con portada;
  - `/herramientas/` usa tarjetas de herramienta y, debajo, el catálogo completo con buscador.
- **Página (`page.html`):** columna centrada de lectura con el nuevo estilo (legales, sobre, autor…).
- **Utilidad (`utility.html`):** el widget se adapta a la paleta clara.
- **404:** radar pequeño con el mensaje «Esta página ha desaparecido del radar».
- **Tablas:** cabecera en tinta, filas con separador `--rule` y desplazamiento horizontal en el móvil (como ahora).
- **Tiempo de lectura:** `max(1, round(word_count / 220))` minutos.

## 7. JavaScript (mínimo, sin librerías)

- `site.js`: menú móvil (ya existe).
- `toc.js`, nuevo:
  - resalta la sección activa con `IntersectionObserver`;
  - actualiza la barra de progreso;
  - en el móvil el índice es un `<details>` plegable.
- `catalog.js`: se carga solo en `/herramientas/`.
- El radar no usa JS.
- Todo funciona sin JS, salvo los resaltados.

## 8. Calidad, accesibilidad y rendimiento

- **Contraste AA:** texto `--ink` sobre `--paper` y blanco sobre el disco del radar.
- **Accesibilidad:** foco visible, `prefers-reduced-motion` respetado y logotipos con `aria-hidden` cuando acompañan a texto.
- **Peso orientativo:** ≤ 120 KB por página sin contar fuentes; las fuentes en woff2 con subconjunto latino y `font-display: swap`.
- **Tests nuevos:**
  - elección de herramientas del radar;
  - generación de portadas (dimensiones del PNG, SVG válido);
  - tiempo de lectura;
  - índice generado desde los H2;
  - `og:image` presente en las páginas indexables;
  - redirecciones al nuevo ancla del catálogo.
- **Verificación visual** en el navegador a 375 px y 1440 px de: portada, ficha, comparativa, guía, noticia, `/herramientas/`, una utilidad, una legal y la 404.
- **Revisión independiente** al final, más la skill de accesibilidad si el plugin Design o Axe está instalado.

## 9. Fuera de alcance (proyecto siguiente: «Funciones»)

Buscador global, «¿Qué IA necesito?», comparador, newsletter, modo oscuro y secciones nuevas (X vs Y, prompts, glosario). En este rediseño, el botón principal de la portada apunta a las comparativas; se cambiará cuando exista el asistente.
