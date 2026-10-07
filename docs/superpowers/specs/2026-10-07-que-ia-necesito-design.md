# Radar IA — «¿Qué IA necesito?»

Fecha: 2026-10-07 · Rama: `que-ia-necesito` · Maqueta aprobada: `_preview/maquetas/6-que-ia-necesito.html`, opción **B** (fuera del repo) · Proyecto «Funciones», parte 2 de 5.

## 1. Objetivo

Un asistente que, con 4 respuestas, recomienda la herramienta de IA que encaja con el lector y explica por qué. Enlaza siempre a nuestra ficha, a la comparativa y a la guía relacionadas. Es contenido interactivo propio, útil para el lector y para la valoración de la web (Google y AdSense).

**Decisiones del titular:**
- **4 preguntas:** tarea, presupuesto, experiencia y para quién.
- **Lógica mixta:** principal y «por qué» editoriales, más alternativas automáticas del catálogo.
- **Todo en una pantalla** (opción B).

**Criterio de éxito:**
- Las 27 combinaciones de tarea × presupuesto tienen recomendación.
- Cada «por qué» sale del texto de una comparativa o de una ficha propia, y no inventa nada.
- El resultado aparece y cambia al momento.
- Se puede compartir la URL con las respuestas.
- Funciona a 375 y 1440 px y con teclado.
- Los tests, el build y `check.py` están en verde.

## 2. Preguntas y respuestas (valores fijos)

1. **¿Para qué la quieres?**

   | id | Etiqueta | Comparativa | Guía |
   |---|---|---|---|
   | `escribir` | ✍️ Escribir | `/mejor-ia-para-escribir/` | `/guias/mejores-prompts/` |
   | `estudiar` | 📚 Estudiar | `/mejor-ia-para-estudiar/` | `/guias/ia-para-estudiar/` |
   | `imagenes` | 🎨 Imágenes | `/mejor-ia-para-imagenes/` | `/guias/mejores-prompts/` |
   | `video` | 🎬 Vídeo | `/mejor-ia-para-video/` | `/guias/mejores-prompts/` |
   | `musica` | 🎵 Música y voz | `/mejor-ia-para-crear-musica/` | `/guias/mejores-prompts/` |
   | `programar` | 💻 Programar | `/mejor-ia-para-programar/` | `/guias/automatizar-tareas/` |
   | `marketing` | 📣 Marketing | `/mejor-ia-para-marketing/` | `/guias/ia-para-pequenas-empresas/` |
   | `productividad` | ⚡ Productividad | `/mejor-ia-para-productividad/` | `/guias/automatizar-tareas/` |
   | `general` | 🧭 Un poco de todo | `/mejor-ia-gratis/` | `/guias/mejores-prompts/` |

   La comparativa y la guía se fijan en los datos, no aquí.

2. **¿Cuánto quieres gastar?** `gratis` (Gratis) · `poco` (Hasta ~10 €/mes) · `sin-limite` (Lo que haga falta).
3. **¿Qué experiencia tienes?** `empiezo` · `me-manejo` · `avanzado`.
4. **¿Para quién es?** `mi` (Para mí) · `equipo` (Para un equipo o empresa).

## 3. Datos editoriales: `data/asistente.json`

```json
{
  "tareas": {"estudiar": {"etiqueta": "Estudiar", "emoji": "📚", "comparativa": "/mejor-ia-para-estudiar/",
                          "guia": "/guias/ia-para-estudiar/", "categorias": ["educacion", "ia-general"]}, ...},
  "reglas": {
    "estudiar/gratis": {"principal": "notebooklm",
                        "porque": ["Responde solo con tus apuntes y cita de dónde sale cada dato.", "..."],
                        "alternativas": [{"id": "chatgpt", "motivo": "Para que te expliquen y te examinen"}, ...],
                        "si_avanzado": {...opcional, misma forma...}, "si_equipo": {...opcional...}},
    ...
  }
}
```

- **27 reglas** (9 tareas × 3 presupuestos), con clave `<tarea>/<presupuesto>`.
- **`principal`:** id de una herramienta **con ficha**.
- **`porque`:** 2–3 frases tomadas de la «Respuesta rápida» o el cuerpo de la comparativa de esa tarea, o del veredicto o el texto de la ficha.
- **`alternativas`:** 0–2 herramientas, cada una con su motivo (de la comparativa). Pueden no tener ficha: en ese caso enlazan a su categoría del catálogo.
- **`si_avanzado` / `si_equipo`:** sustituyen la regla cuando el lector es avanzado o es para un equipo, solo donde la comparativa lo justifica (por ejemplo, programar para avanzados → Cursor; equipos → planes Business o Team). Si se cumplen las dos, gana `si_equipo`.
- **Alternativas automáticas («Otras opciones del catálogo»):**
  - hasta 2 herramientas de `tools.json` en las `categorias` de la tarea;
  - filtradas por precio: `gratis` → `price` en {gratis, freemium}; el resto, cualquiera;
  - y por nivel: `empiezo` → `level` ≠ avanzado;
  - excluyendo la principal y las editoriales;
  - ordenadas: primero las que tienen ficha, luego por nombre.
  - Se calculan **en el build** para cada combinación tarea × presupuesto × experiencia, así que el JS no tiene lógica de negocio.
- **Validación en el build** (con un error claro si falla):
  - están las 27 reglas;
  - existen los ids;
  - la principal tiene ficha;
  - existen las URLs de comparativa y guía;
  - `porque` tiene entre 2 y 3 frases;
  - no aparece «hemos probado».

## 4. Página `/que-ia-necesito/`

- **Contenido:** `content/paginas/que-ia-necesito.md` (tipo página e indexable), con unas 500 palabras propias:
  - cómo funciona el asistente;
  - de dónde salen las recomendaciones (nuestras comparativas y fichas, con fechas de comprobación);
  - qué no hace (no hay patrocinios ni pruebas propias salvo indicación);
  - preguntas frecuentes.
- **Plantilla nueva** `assistant.html` (elegida por la URL):
  - cabecera con eyebrow «Asistente gratuito» y H1 «¿Qué *IA* necesito?»;
  - entradilla y formulario: 4 `fieldset` con `legend` y radios con aspecto de píldora;
  - región de resultado `aria-live="polite"`;
  - debajo, el cuerpo Markdown (cómo funciona y preguntas frecuentes).
- **Datos para el JS:** el build inserta `<script type="application/json" id="asistente-datos">` con:
  - las reglas resueltas;
  - la información de cada herramienta usada: nombre, URL de ficha o categoría, color, monograma, `precio_desde`, `ideal_para` y web oficial;
  - las alternativas automáticas.

  Se escapa `</` (como `to_json`).
- **`static/js/assistant.js`** (sin librerías, DOM y `textContent`):
  - lee la selección y, cuando hay respuesta a las 4 preguntas, pinta el resultado;
  - **resultado:**
    - tarjeta principal: logo o monograma, nombre, «Por qué encaja contigo» (lista), 3 datos (precio desde, ideal para, nivel) y los botones «Leer el análisis →» y «Probar <nombre> ↗» (`rel="noopener nofollow"`);
    - «También encajan»: las alternativas editoriales;
    - «Otras opciones del catálogo»: las automáticas;
    - enlaces a la comparativa y a la guía;
  - actualiza la URL (`?tarea=…&presupuesto=…&nivel=…&para=…`) con `replaceState` y la lee al cargar, para poder compartirla;
  - al mostrar el resultado por primera vez, lo desplaza a la vista en el móvil.
- **Sin JS:** debajo del formulario, la lista «Elige por tarea» con enlaces a las 9 comparativas.

## 5. Puntos de entrada

- **Portada:**
  - el botón principal pasa a «¿Qué IA necesito? →» (`/que-ia-necesito/`);
  - el secundario sigue siendo «Ver comparativas»;
  - «Explorar herramientas» sale de la banda principal (sigue en el menú).
- **Comparativas y guías:** al final del artículo, antes de las fuentes, un recuadro: «**¿No lo tienes claro?** Responde 4 preguntas y te decimos cuál encaja contigo. Hacer el test →». No se pone en noticias ni en fichas.
- **Buscador:** la página entra sola en el índice (tipo «Página»).

## 6. Pruebas

- **Python:**
  - validación de datos: falta una regla, id inexistente, principal sin ficha, URL inexistente, `porque` con 1 o 4 frases, «hemos probado»;
  - el archivo real es válido con 27 reglas;
  - alternativas automáticas: filtros de precio y nivel, exclusiones y orden;
  - la página tiene 4 `fieldset`, el JSON incrustado es válido y sin `</script` interno, y el bloque sin JS enlaza las 9 comparativas;
  - la portada tiene el botón nuevo;
  - las comparativas y guías tienen el recuadro (y las noticias y fichas no);
  - `assistant.js` sin `innerHTML` y ≤ 6 KB comprimido.
- **Navegador** a 375 y 1440 px:
  - varias combinaciones, incluidas una con `si_avanzado` y otra con `si_equipo`;
  - URL compartible al recargar;
  - teclado (Tab y flechas en los radios);
  - sin scroll horizontal ni errores de consola.

## 7. Fuera de alcance

- Recomendaciones con IA en vivo.
- Guardar respuestas o estadísticas.
- Más de 4 preguntas.
- Ordenación personalizada por idioma o plataforma (se puede añadir después con los datos de `tools.json`).
