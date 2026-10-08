# Radar IA — Biblioteca de prompts

Fecha: 2026-10-08 · Rama: `prompts` · Maqueta: `_preview/maquetas/12-prompts.html` (fuera del repo), opción **A** · Proyecto «Secciones nuevas», parte 5 de 6.

## 1. Objetivo

Una sola página `/prompts/` con unos **60 prompts listos para usar**, organizados en 8 categorías. Cada prompt tiene **huecos que se rellenan en la propia tarjeta** y un botón «Copiar» que copia el prompt ya completo. Es una herramienta útil y propia, con unas 5.000 palabras de contenido y sin riesgo de páginas delgadas, siguiendo la línea del glosario.

**Decisiones del titular:**
- una sola página (A);
- huecos rellenables en la tarjeta.

**Criterio de éxito:**
- Al menos 50 prompts válidos, con al menos 5 por categoría, todos con herramienta sugerida con ficha.
- Funciona sin JS: los prompts se leen enteros, con los huecos resaltados.
- Rellenar un hueco cambia el prompt al momento, y «Copiar» copia el texto ya completo.
- Se ve bien a 375 y 1440 px.
- Los prompts aparecen en el buscador.
- Los tests, el build y `check.py` están en verde.

## 2. Datos: `data/prompts.md`

Es un Markdown fácil de editar, con el mismo formato que `data/glosario.md`:

```markdown
## Responder un correo difícil
categoria: escribir
herramientas: chatgpt, claude
para: Contestar una queja o un retraso sin sonar a la defensiva.
consejo: Si tienes el correo original, pégalo debajo del prompt.

Redacta una respuesta breve y cordial a este correo de [quién escribe]. Reconoce el problema, explica [qué ha pasado] y ofrece [solución]. Tono profesional y cercano, máximo 120 palabras.
```

- **Categorías (8):**

  | id | Etiqueta |
  |---|---|
  | `escribir` | ✍️ Escribir |
  | `estudiar` | 📚 Estudiar |
  | `trabajo` | 💼 Trabajo |
  | `marketing` | 📣 Marketing |
  | `imagenes` | 🎨 Imágenes |
  | `programar` | 💻 Programar |
  | `dia-a-dia` | 🏠 Día a día |
  | `pensar` | 🧠 Pensar mejor |

- **Metadatos:**
  - `categoria` (obligatorio);
  - `herramientas`: 1–2 ids con ficha indexable;
  - `para`: obligatorio, 25 palabras como máximo;
  - `consejo`: opcional, 40 palabras como máximo.
- **Cuerpo:** el prompt en texto plano, sin Markdown, de entre 15 y 150 palabras. Los **huecos** se escriben `[nombre del hueco]`, sin corchetes anidados.
  - Entre 0 y 4 huecos distintos por prompt.
  - Si un hueco se repite, se rellena una sola vez.
- **Slug:** se calcula del título (reutiliza `slugify` del glosario) y es el ancla `/prompts/#slug`.
- **Orden:** por categoría y, dentro de cada una, por el orden del archivo.
- **Validación en el build** (`radar/prompt_library.py`, con un error que nombra el prompt):
  - títulos y slugs únicos;
  - categoría válida;
  - las herramientas existen y tienen ficha;
  - `para` y `consejo` dentro de su límite;
  - longitud del prompt y número de huecos;
  - corchetes bien cerrados;
  - no aparece «hemos probado» ni sus variantes;
  - no hay claves desconocidas.
- **Contenido:**
  - prompts genéricos y útiles, sin datos personales en los ejemplos;
  - no repiten literalmente los de las páginas por profesión ni los de las fichas;
  - nunca se afirma haberlos probado.

## 3. Página `/prompts/`

- **Contenido:** `content/paginas/prompts.md` (tipo página e indexable), con unas 300 palabras propias:
  - cómo usar la biblioteca;
  - cómo adaptar un prompt, con un enlace a la guía de prompts;
  - qué datos no conviene pegar, con un enlace a la guía de privacidad;
  - una invitación a proponer prompts.
- **Plantilla nueva `prompts.html`** (elegida por la URL):
  - eyebrow «Biblioteca de prompts» y H1 «Prompts para copiar y *usar ya*», con la entradilla;
  - **controles** (`hidden` hasta que carga el JS):
    - buscador `input type="search"` con etiqueta;
    - chips de categoría (`button` con `aria-pressed`);
    - recuento `aria-live`;
  - **por cada categoría:** un `h2` con emoji y etiqueta, y una rejilla de tarjetas;
  - **por cada prompt:** `article.prompt-card` con `id="<slug>"` y `data-cat`, que contiene:
    - la etiqueta de la categoría y un `h3` con el título;
    - «para qué» y el prompt en `<p class="prompt-text">`, con cada hueco en `<mark class="slot" data-slot="…">[…]</mark>`;
    - los campos de los huecos (`.prompt-fill`, `hidden` sin JS): un `label` + `input` por hueco distinto;
    - el consejo, si lo hay;
    - «Sugerido:» con logo y nombre de cada herramienta, enlazando a su ficha;
    - el botón «Copiar» (lo añade el JS);
  - debajo, el cuerpo Markdown.
- **`static/js/library.js`** (sin librerías, sin `innerHTML`, ≤ 2,5 KB comprimido):
  - **filtro** por texto (título, para qué y prompt, sin tildes) y por categoría, que oculta los grupos vacíos; si no hay resultados, «Ningún prompt coincide…»;
  - **huecos:** al escribir en un campo, los `mark` de ese hueco muestran el valor (o `[hueco]` si está vacío) y se marcan como rellenos;
  - **copiar:** copia el `textContent` actual del prompt con `navigator.clipboard` y, si no se puede, selecciona el texto. El botón cambia a «Copiado» y se anuncia con `aria-live`, con el mismo comportamiento que `prompts.js`;
  - al llegar con `#slug`, si el filtro oculta la tarjeta, se quita el filtro.
- **Datos estructurados:** la miga de pan habitual.
- **Estilos:** sección «20. Biblioteca de prompts» en `radar.css`, con 2 columnas en escritorio y 1 en móvil; los huecos van en ámbar sobre el fondo oscuro del prompt.

## 4. Buscador y enlaces

- **Buscador:** cada prompt entra en el índice como:
  - `t`: el título;
  - `u`: `/prompts/#slug`;
  - `k`: «Prompt»;
  - `d`: el «para qué»;
  - `x`: la categoría y los nombres de las herramientas.

  En la página de búsqueda hay un filtro «Prompt». `check.py` valida también las anclas `/prompts/#…`.
- **«Empieza aquí»:** en el paso 3 («Aprende a pedírselo bien»), un enlace extra «Biblioteca de prompts».
- **Guía de prompts** (`/guias/mejores-prompts/`): al final, un enlace a la biblioteca.
- **Pie de página:** «Biblioteca de prompts» junto a «Glosario de IA», solo si la página existe.
- **Menú:** no se añade; ya tiene 6 elementos.

## 5. Pruebas

- **Python:**
  - el parser lee metadatos, cuerpo y huecos (incluidos los repetidos);
  - la validación falla con: categoría inválida, herramienta sin ficha, `para` demasiado largo, prompt demasiado corto o largo, 5 huecos, corchete sin cerrar, «hemos probado», título duplicado o clave desconocida;
  - el archivo real es válido, con al menos 50 prompts y al menos 5 por categoría;
  - la página renderiza un `article.prompt-card` por prompt con su `id`, un `mark.slot` por cada aparición de un hueco, los campos ocultos y los controles ocultos;
  - es indexable y supera las 300 palabras;
  - el índice de búsqueda tiene los prompts con su ancla;
  - `check.py` detecta un ancla de prompt inexistente;
  - `library.js` no usa `innerHTML` y pesa ≤ 2,5 KB comprimido;
  - existen los enlaces desde «Empieza aquí», la guía y el pie.
- **Navegador** a 375 y 1440 px:
  - filtrar por texto y por categoría;
  - rellenar huecos y copiar;
  - abrir `/prompts/#slug` desde el buscador;
  - sin scroll horizontal ni errores de consola.

## 6. Construcción por partes

1. **Motor, plantilla, JS y unos 12 prompts.** Vista previa.
2. **Contenido completo:** unos 60 prompts y el texto de la página.
3. **Buscador y enlaces;** después, la revisión independiente y la PR.

## 7. Fuera de alcance

- Guardar prompts favoritos.
- Que los usuarios envíen prompts desde la web (se proponen por Contacto).
- Páginas individuales por prompt o por categoría.
- Enviar el prompt directamente a una herramienta.
