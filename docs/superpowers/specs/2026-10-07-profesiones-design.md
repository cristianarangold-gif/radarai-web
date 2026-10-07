# Radar IA — IA por profesión

Fecha: 2026-10-07 · Rama: `profesiones` · Maqueta: `_preview/maquetas/11-profesiones.html` (fuera del repo), opción **A «Por tareas»** · Proyecto «Secciones nuevas», parte 4 de 6.

## 1. Objetivo

Páginas prácticas para quien quiere usar la IA en su trabajo. Cada una explica las tareas habituales de una profesión, con qué herramienta hacer cada tarea y un prompt listo para copiar, y las precauciones propias del sector. Es contenido nuevo y aplicado, que no repite las fichas ni las comparativas.

**Decisiones del titular:**
- **Formato A:**
  - kit en 30 segundos;
  - tareas, con herramienta y prompt;
  - precauciones del sector.
- **6 profesiones:**
  1. Docentes
  2. Abogados y despachos
  3. Diseñadores
  4. Creadores de contenido y community managers
  5. Administrativos y oficina
  6. Periodistas y redactores

**Criterio de éxito:**
- Cada página tiene al menos 1.000 palabras propias (objetivo, unas 1.200), entre 5 y 7 tareas con su prompt y una sección de precauciones con fuentes oficiales (por ejemplo, la AEPD o los códigos deontológicos).
- Los datos de las herramientas salen de las fichas y no se afirma ninguna prueba propia.
- No se dan consejos legales ni médicos: se explican riesgos y se remite a las fuentes.
- Los tests, el build y `check.py` están en verde, y la página se ve bien a 375 y 1440 px.

## 2. Contenido: `content/profesiones/<slug>.md`

- **Tipo y URL:** tipo nuevo `profesion`; `docentes.md` → `/ia-para-docentes/`.
- **Metadatos:**

  ```
  titulo: IA para docentes: herramientas y prompts para preparar clases
  descripcion: …
  fecha: 2026-10-07
  profesion: docentes
  emoji: 🍎
  kit: notebooklm = Preparar temas con tus fuentes | chatgpt = Ideas, ejercicios y rúbricas | canva-ai = Presentaciones y fichas visuales
  fuentes: https://www.aepd.es/…
  ```

  - `profesion`: el nombre en minúsculas para el H1 y las tarjetas («IA para *docentes*»).
  - `kit`: entre 2 y 4 entradas `id = para qué`. Cada id tiene que tener ficha indexable.
- **Cuerpo Markdown**, con esta estructura fija:
  1. una entradilla;
  2. `## Tareas en las que te ayuda`, con un `###` por tarea (entre 5 y 7). Cada tarea explica cómo hacerla, enlaza a la ficha o a la guía de la herramienta y termina con **un prompt en cita** (`> «…»`);
  3. `## Precauciones en tu profesión`: privacidad, deontología y revisión humana, con enlaces a las fuentes oficiales;
  4. `## Qué no conviene delegar en la IA`;
  5. `## Preguntas frecuentes`.
- **Convención de los prompts:** en estas páginas, toda cita (`blockquote`) es un prompt y recibe un botón «Copiar».
- **Validación en el build** (`radar/professions.py`, con un error que nombra el archivo):
  - `profesion` y `emoji` presentes;
  - `kit` con 2–4 entradas válidas;
  - al menos 1 fuente;
  - existen los encabezados «Tareas en las que te ayuda» y «Precauciones en tu profesión»;
  - hay entre 5 y 7 `###` de tareas y al menos 5 citas;
  - no aparece «hemos probado» ni «en nuestras pruebas»;
  - **todo precio citado aparece en alguna ficha**: se reutiliza la guarda de precios de los duelos, ahora contra todas las fichas.
- **Mínimo de palabras:** `MIN_WORDS['profesion'] = 1000`.

## 3. Plantillas

- **`profession.html`:**
  - migas de pan: Inicio › IA por profesión;
  - eyebrow «IA por profesión», emoji y H1 (el título), con entradilla y firma;
  - **«Tu kit en 30 segundos»:** de 2 a 4 tarjetas con logo, nombre, «para qué» y «Desde X», enlazando a la ficha. Los datos salen de `compare_by_id`;
  - el cuerpo Markdown con índice lateral (TOC);
  - el recuadro del asistente, las fuentes y «Otras profesiones» (las demás).
- **`static/js/prompts.js`** (sin librerías, ≤ 1 KB comprimido):
  - añade un botón «Copiar» a cada cita de `.prompt-page .prose`;
  - usa `navigator.clipboard` y, si no está disponible, deja el texto seleccionado;
  - el botón cambia a «Copiado» durante 2 segundos y avisa con `aria-live`.

  Se reutilizará en la biblioteca de prompts (parte 5).
- **Índice `/ia-por-profesion/`:**
  - se genera como un listado nuevo (`LISTINGS`), con el texto propio de `content/paginas/ia-por-profesion.md`, de unas 300 palabras;
  - muestra una tarjeta por profesión: emoji, «IA para docentes», la descripción y las herramientas del kit (logos).
- **Portada y `og:image`:** el disco de Radar IA con la etiqueta «IA para docentes» (`CoverSpec` sin marca).
- **JSON-LD:** `Article` y miga de pan. La sección de `profesion` es («IA por profesión», `/ia-por-profesion/`).
- **Estilos:** sección «19. IA por profesión» en `radar.css`. En móvil, el kit va en una columna y el botón «Copiar» no tapa el texto.

## 4. Puntos de entrada

- **«Empieza aquí»:** en la tarjeta «La quiero para estudiar o trabajar», el enlace «Crear presentaciones con IA» se sustituye por «IA para tu profesión» (`/ia-por-profesion/`).
- **Guía «IA para pequeñas empresas»:** al final, un enlace al índice.
- **Fichas:** en el lateral, «Recomendada para: Docentes · Diseñadores…» cuando la herramienta está en el kit de alguna profesión.
- **Buscador:** las páginas entran con el tipo «Profesión», con su filtro en la página de búsqueda.
- **Sitemap:** sí. **RSS:** no.

## 5. Pruebas

- **Python:**
  - validación: falta `profesion`, kit con 1 o 5 entradas, herramienta sin ficha, sin fuentes, sin la sección de precauciones, 4 u 8 tareas, menos de 5 citas, «hemos probado» y precio que no está en ninguna ficha (deben fallar);
  - la URL y el tipo;
  - el kit toma el precio de la ficha;
  - el índice lista las 6 profesiones;
  - las fichas muestran «Recomendada para»;
  - el buscador incluye las profesiones;
  - `prompts.js` no usa `innerHTML` y pesa ≤ 1 KB comprimido;
  - los archivos reales son válidos: 6 profesiones con al menos 1.000 palabras cada una.
- **Navegador** a 375 y 1440 px:
  - una profesión completa;
  - botón «Copiar»;
  - el índice;
  - los enlaces desde «Empieza aquí» y desde una ficha;
  - sin scroll horizontal ni errores de consola.

## 6. Construcción por partes

1. **Motor, plantillas, índice y «IA para docentes» completa.** Vista previa.
2. **Las otras 5 profesiones.**
3. **Puntos de entrada y buscador;** después, la revisión independiente y la PR.

## 7. Fuera de alcance

- Profesiones sanitarias, finanzas o asesoría fiscal: son temas delicados para Google (YMYL) y se dejan para más adelante, con más cuidado.
- Recomendar herramientas sin ficha en el kit. Sí pueden mencionarse en el texto, enlazando al catálogo.
- Personalizar por país.
