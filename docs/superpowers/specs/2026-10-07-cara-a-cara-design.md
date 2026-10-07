# Radar IA — Páginas «X vs Y» (Cara a cara)

Fecha: 2026-10-07 · Rama: `cara-a-cara` · Maqueta: `_preview/maquetas/10-x-vs-y.html` (fuera del repo), opción **A «Veredicto primero»** · Proyecto «Secciones nuevas», parte 3 de 6.

## 1. Objetivo

Páginas que responden a búsquedas como «ChatGPT vs Claude» con un veredicto claro y datos con fuente y fecha. Se basan en lo que ya documentan nuestras fichas, sin marcadores ni puntuaciones que sugieran pruebas propias.

**Decisiones del titular:**
- **Formato A:**
  - respuesta rápida;
  - «Elige X si… / Elige Y si…»;
  - tabla de datos;
  - secciones por criterio.
- **6 duelos en la primera tanda:**
  1. ChatGPT vs Claude
  2. ChatGPT vs Gemini
  3. ChatGPT vs Copilot
  4. Perplexity vs ChatGPT
  5. Cursor vs GitHub Copilot
  6. NotebookLM vs ChatGPT

**Criterio de éxito:**
- Cada duelo tiene al menos 1.000 palabras propias (objetivo, unas 1.200), con fuentes oficiales y fecha de comprobación.
- Ningún dato de la tabla se escribe a mano: sale de las fichas.
- No se afirma ninguna prueba propia.
- Los tests, el build y `check.py` están en verde, y la página se ve bien a 375 y 1440 px.

## 2. Contenido: `content/cara-a-cara/<a>-vs-<b>.md`

- Tipo nuevo `duelo`, con URL en la raíz: `/chatgpt-vs-claude/`, igual que las comparativas `/mejor-ia-para-…/`.
- **Metadatos:**

  ```
  titulo: ChatGPT vs Claude: cuál elegir en 2026
  descripcion: …
  fecha: 2026-10-07
  herramientas: chatgpt, claude
  respuesta: Una o dos frases con la respuesta corta (máximo 60 palabras).
  elige_1: Frase | Frase | Frase
  elige_2: Frase | Frase
  fuentes: https://… (las páginas oficiales de precios y ayuda usadas)
  ```

  - `herramientas`: exactamente 2 ids distintos, los dos con ficha indexable. El orden es el del título.
  - `elige_1` y `elige_2`: 2–4 frases cada uno, separadas por `|`, para «Elige X si…» y «Elige Y si…».
- **Cuerpo Markdown** con `##` por criterio. Los criterios cambian según el duelo; por ejemplo:
  - precios y planes (siempre);
  - lo que hace mejor cada uno;
  - límites;
  - privacidad (siempre);
  - preguntas frecuentes.
- **Validación en el build** (`radar/duels.py`, con un error que nombra el archivo):
  - herramientas válidas;
  - `respuesta` presente y de 60 palabras como máximo;
  - `elige_1` y `elige_2` con 2–4 frases cada uno;
  - al menos 1 fuente;
  - no aparece «hemos probado» ni «en nuestras pruebas»;
  - no se repite el par (si existe `a-vs-b`, no puede haber `b-vs-a`).
- **Mínimo de palabras:** `MIN_WORDS['duelo'] = 1000`. `check.py` lo aplica, como con los demás tipos.
- **Reglas editoriales** (se añaden a `content/GUIA_EDITORIAL.md`):
  - todo dato sale de las fichas o de sus fuentes oficiales;
  - los precios se citan tal como aparecen en la ficha, con moneda y periodicidad;
  - el «mejor en…» solo se dice cuando un dato lo respalda (por ejemplo, «el plan de pago más barato en euros»), nunca por impresión de uso.

## 3. Plantilla `duel.html`

- **Migas de pan:** Inicio › Comparativas › título. La sección de los duelos es `/mejor-ia/`.
- **Cabecera:**
  - eyebrow «Cara a cara»;
  - los dos logotipos con «vs» entre ellos;
  - H1 (el título), entradilla y firma (`byline`).
- **Respuesta rápida:** un recuadro oscuro con «Respuesta rápida:» y el texto de `respuesta`.
- **«Elige X si… / Elige Y si…»:** dos tarjetas, una por herramienta, con su logo y las frases en lista.
- **Tabla de datos:** «Precio desde», «Plan de pago», «Ideal para», «Plataformas» y «Comprobado».
  - Los datos salen del mismo payload que el comparador (`compare_payload`), más la fecha de la ficha.
  - Lleva `caption` y `th scope`.
- **Enlaces:** «Ver en el comparador →» (`/comparador/?h=a,b`), «Ficha de X →» y «Ficha de Y →».
- **Cuerpo:** el cuerpo Markdown, con índice lateral (TOC), como los artículos.
- **Al final:**
  - el recuadro del asistente;
  - las fuentes;
  - «Otros cara a cara»: hasta 3 duelos más, primero los que comparten herramienta.
- **Portada (`og:image` y portada SVG):** los dos logotipos de marca con «vs». Se añade a `radar/covers.py` un `CoverSpec` con una segunda marca.
- **JSON-LD:** `Article` y miga de pan.
- **Estilos:** sección «18. Cara a cara» en `radar.css`. En móvil, las tarjetas «Elige…» van en una columna y la tabla no desborda.

## 4. Puntos de entrada

- **`/mejor-ia/`:** antes del listado de comparativas, una sección «Cara a cara» con tarjetas de duelo («ChatGPT *vs* Claude», con los logos).
- **Fichas:** en el lateral, debajo de «Comparar … con…», la lista «Cara a cara» con los duelos en los que aparece esa herramienta.
- **Comparador:** si las herramientas marcadas son exactamente las de un duelo (en cualquier orden), aparece debajo de la tabla «Lee nuestro análisis ChatGPT vs Claude →». El payload del comparador incluye el mapa de duelos.
- **Buscador:** los duelos entran como «Cara a cara»; en la página de búsqueda hay un filtro con ese nombre.
- **Sitemap y RSS:** entran en el sitemap como el resto de páginas indexables, pero no en el RSS (que es solo de noticias).

## 5. Pruebas

- **Python:**
  - validación: menos o más de 2 herramientas, herramienta sin ficha, la misma herramienta dos veces, `respuesta` demasiado larga, `elige` con 1 o 5 frases, sin fuentes, «hemos probado» y par repetido (deben fallar);
  - el URL y el tipo de los duelos;
  - la tabla toma los datos de la ficha (si cambia un precio en la ficha, cambia en el duelo);
  - la portada tiene las dos marcas;
  - las fichas listan sus duelos;
  - `/mejor-ia/` tiene la sección «Cara a cara»;
  - el índice de búsqueda incluye los duelos;
  - los archivos reales son válidos: 6 duelos, cada uno con al menos 1.000 palabras.
- **Navegador** a 375 y 1440 px:
  - un duelo completo;
  - el enlace desde una ficha;
  - el comparador con un par de duelo marcado;
  - sin scroll horizontal ni errores de consola.

## 6. Construcción por partes

1. **Motor y primer duelo:** el tipo `duelo`, la validación, la plantilla, la portada con dos marcas y **ChatGPT vs Claude** completo. Vista previa.
2. **Los otros 5 duelos**, escritos a partir de las fichas y sus fuentes.
3. **Puntos de entrada:** `/mejor-ia/`, fichas, comparador y buscador; después, la revisión independiente y la PR.

## 7. Fuera de alcance

- Duelos con herramientas sin ficha.
- Marcadores o puntuaciones.
- Duelos de 3 herramientas: para eso está el comparador.
- Generar duelos automáticamente.
