# Radar IA — Buscador

Fecha: 2026-10-06 · Rama: `buscador` · Maqueta aprobada: `_preview/maquetas/5-buscador.html` (fuera del repo) · Proyecto «Funciones», parte 1 de 5 (orden aprobado: buscador → «¿Qué IA necesito?» → comparador; newsletter y modo oscuro al final o descartados).

## 1. Objetivo

Que cualquier lector encuentre en segundos una ficha, comparativa, guía, noticia, utilidad o herramienta del catálogo escribiendo lo que busca. Debe funcionar sin servicios externos ni coste, en todas las páginas, con teclado y con lector de pantalla.

**Decisiones del titular:**
- Busca en **todo**: artículos y las 126 herramientas del catálogo.
- **A + B:**
  - A: lupa en la cabecera que abre una ventana de búsqueda.
  - B: página propia `/buscar/` con buscador grande y filtros por tipo.

**Criterio de éxito:**
- Buscar «imagen», «imágenes» o «IMAGENES» da los mismos resultados (sin tildes ni mayúsculas).
- La comparativa de imágenes, Midjourney y las herramientas de imagen del catálogo aparecen.
- Funciona a 375 px y 1440 px y solo con teclado.
- Los tests, el build y `check.py` están en verde.

## 2. Índice de búsqueda (build)

- **Módulo nuevo** `radar/search.py`, función `build_index(...)`, que genera `_site/search-index.json`. Es una lista de entradas `{t, u, k, d, x}`:

  | Campo | Contenido |
  |---|---|
  | `t` | título |
  | `u` | URL |
  | `k` | etiqueta del tipo: «Ficha», «Comparativa», «Guía», «Noticia», «Utilidad», «Página» o «Catálogo» |
  | `d` | descripción (≤ 160 caracteres) |
  | `x` | palabras clave extra |

- **Entran:**
  - **Páginas de contenido indexables:**
    - todas las fichas, comparativas, guías, noticias, utilidades y páginas (sobre, autor, legales…);
    - **no entran** la portada, los listados, la 404 ni los borradores.
  - **Palabras clave (`x`) de cada página:**
    - el texto de sus H2;
    - en las fichas, además: `ideal_para`, la categoría y el nombre de la herramienta;
    - en las noticias, además: el nombre de la empresa y el de las herramientas citadas.
  - **Herramientas del catálogo sin ficha:**
    - `t` = nombre, `u` = `/herramientas/#cat-<cat>`, `k` = «Catálogo»;
    - `d` = su descripción de `tools.json`, `x` = categoría + etiquetas.
    - Las que tienen ficha **no se duplican**, porque ya entra su ficha.
- **Noticias:** llevan además `f` (fecha en texto, «6 oct 2026»).
- **Fichas:** llevan además `p` (`precio_desde`) para mostrarlo en el resultado.
- **Versión:** el JSON se enlaza con `?v=<hash del contenido>`, igual que CSS y JS, para no servir índices viejos.
- **`check.py`:** cada `u` del índice debe existir, incluida el ancla `#cat-` en la página destino.

## 3. Interfaz

**A. Ventana de búsqueda** (todas las páginas):
- **Botón en la cabecera:**
  - «⌕ Buscar» en el menú;
  - en el móvil queda visible junto a «Menú», sin desplegar;
  - sin JS es un enlace normal a `/buscar/`.
- **Al abrirla:**
  - aparece un diálogo modal con campo de búsqueda y resultados al escribir;
  - en el móvil ocupa toda la pantalla.
- **Atajos:** «/» abre (si no se está escribiendo en otro campo), Esc cierra, ↑/↓ mueve la selección y Enter abre el resultado.
- **Resultados:**
  - hasta 8, agrupados en «Artículos» y «Herramientas del catálogo»;
  - cada uno con icono (logo o símbolo del tipo), título con la coincidencia resaltada, tipo y un dato (fecha, precio o categoría);
  - al pie, «Ver todos (N)» lleva a `/buscar/?q=…`.
- **Sin texto:** sugerencias fijas («ChatGPT», «imágenes», «gratis», «estudiar», «programar»).
- **Sin resultados:** mensaje y enlaces a Comparativas y al catálogo.
- **Carga:** el índice se descarga la primera vez que se abre la ventana (o al pasar el ratón o el foco por el botón) y queda en memoria.

**B. Página `/buscar/`:**
- Eyebrow «Buscar en Radar IA», H1 «¿Qué estás buscando?», buscador grande y chips de filtro con recuento: Todo, Comparativas, Fichas, Guías, Noticias, Utilidades, Páginas y Catálogo.
- Muestra **todos** los resultados y lee y actualiza `?q=` en la URL (`history.replaceState`).
- **`noindex`** y fuera del sitemap: las páginas de resultados no deben indexarse.
- Sin JS: aviso «El buscador necesita JavaScript» y enlaces a las secciones.

## 4. Búsqueda (JS, `static/js/search.js`, sin librerías)

- **Normalización:** minúsculas, sin tildes (NFD) y signos como espacio.
- **Coincidencia:** consulta dividida en palabras; **todas** deben aparecer en `t`, `x`, `d` o `k`. Vale el inicio de una palabra o, con 3 letras o más, cualquier parte de ella. Así «chat gpt» encuentra «ChatGPT».
- **Puntuación por palabra:**

  | Coincidencia | Puntos |
  |---|---|
  | Título que empieza por la palabra | 12 |
  | Palabra del título | 8 |
  | Parte de una palabra del título | 5 |
  | Palabras clave | 4 |
  | Descripción | 2 |
  | Tipo | 1 |

  - Bonificaciones: +3 a fichas y comparativas, y +2 si el título contiene la consulta entera.
  - Desempate por título.
- **Seguridad:**
  - los resultados se pintan con nodos DOM y `textContent`, nunca con `innerHTML` de datos;
  - el resaltado se hace con `<mark>` creado por DOM.
- **Accesibilidad:**
  - la ventana es `role="dialog"` con `aria-modal`; el foco queda atrapado dentro y vuelve al botón al cerrar;
  - patrón combobox/listbox (`aria-activedescendant`);
  - una región `aria-live` anuncia «N resultados».

## 5. Archivos

| Acción | Archivos |
|---|---|
| Nuevos | `radar/search.py`, `static/js/search.js`, `templates/partials/search_dialog.html`, `templates/search.html` (página `/buscar/`), `tests/test_search.py` |
| Cambian | `scripts/build.py` (escribe el índice y la página), `radar/render.py` (plantilla de `/buscar/`, `asset()` para el JSON), `templates/partials/header.html` y `base.html` (botón, diálogo y script), `radar/check.py` (valida URLs del índice), `static/css/radar.css` (estilos), `README.md` |

## 6. Pruebas

- **Python (pytest):**
  - qué entra y qué no en el índice: borradores, portada, listados y 404 fuera; herramientas con ficha sin duplicar; catálogo con ancla;
  - los H2 y metadatos en `x`;
  - el JSON es válido;
  - `/buscar/` es noindex y no está en el sitemap;
  - el botón de la cabecera enlaza a `/buscar/`;
  - el script está versionado;
  - `check.py` detecta una URL inexistente en el índice.
- **Navegador** a 375 px y 1440 px:
  - «imagen», «IMÁGENES», «chat gpt», «gratis estudiar», «xyz» (sin resultados) y «/» para abrir;
  - flechas y Enter, Esc devuelve el foco;
  - filtros y `?q=` en `/buscar/`;
  - un resultado del catálogo abre su categoría;
  - sin errores de consola y sin scroll horizontal.
- **Peso:** el índice comprimido debe pesar ≤ 15 KB y `search.js` ≤ 8 KB.

## 7. Fuera de alcance

- Búsqueda en el texto completo de los artículos (el índice usa título, descripción, H2 y metadatos).
- Corrección de erratas («chatgtp»).
- Estadísticas de búsquedas.
- Cuadro de búsqueda de Google en los resultados (Google lo retiró en 2024).
