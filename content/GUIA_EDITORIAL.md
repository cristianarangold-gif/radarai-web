# Guía editorial de Radar IA (uso interno, no se publica)

Se aplica a todo el contenido, incluidos los borradores automáticos de noticias.

1. **Valor propio.** Cada página responde a una necesidad concreta del lector hispanohablante (qué elegir, cuánto cuesta, cómo usarla, límites). No basta con describir el producto.
2. **Honestidad.** Nunca escribir «lo hemos probado» si no es verdad. La investigación se marca como tal («según la documentación oficial, a fecha X»). Las pruebas propias van en `<div class="nuestra-prueba">` y solo las rellena Cristian.
3. **Fuentes y fechas.** Metadatos `fecha`, `actualizado` y `fuentes` siempre. Precios con fecha de comprobación y en EUR cuando exista.
4. **Sin copia.** Resumir con palabras propias. Citas literales de una frase como máximo, atribuidas.
5. **Mínimos de palabras (páginas indexables):** ficha 1.000 · comparativa 1.200 · guía 1.200 · noticia 500–900.
6. **Estructura de noticia:** qué ha pasado · por qué importa a un usuario hispanohablante · qué cambia en la práctica (precio, disponibilidad en España/UE) · opinión de Radar IA · fuentes.
7. **Autor:** Cristian Arango. Español de España, tono cercano y claro, sin tecnicismos innecesarios.
8. **Nunca** publicar sin revisión humana ni traducir artículos enteros de otros medios.
9. **Metadatos de diseño en noticias:** `empresa` (id de `data/brands.json`) y `herramientas` (ids de `data/tools.json`, separados por comas). Alimentan la imagen de portada y el radar de la portada; un id inexistente hace fallar el build.
10. **Cara a cara (X vs Y)** en `content/cara-a-cara/<a>-vs-<b>.md`: solo entre herramientas con ficha. Todo dato sale de las fichas o de sus fuentes oficiales; los precios se citan como en la ficha, con moneda y periodicidad. «Mejor en…» solo cuando un dato lo respalda (por ejemplo, el plan de pago más barato en euros), nunca por impresión de uso. Metadatos obligatorios: `herramientas`, `respuesta` (≤ 60 palabras), `elige_1` y `elige_2` (2–4 frases separadas por `|`) y `fuentes`. La tabla de datos de la página la genera el build a partir de las fichas.
11. **IA por profesión** en `content/profesiones/<slug>.md` (URL `/ia-para-<slug>/`): metadatos `profesion`, `emoji`, `kit` (2–4 `id = para qué`, todas con ficha) y `fuentes` oficiales (AEPD, colegios profesionales…). Cuerpo con `## Tareas en las que te ayuda` (5–7 `###`, cada una con su prompt), `## Precauciones en tu profesión`, `## Qué no conviene delegar en la IA` y `## Preguntas frecuentes`. **En estas páginas toda cita (`>`) es un prompt** y recibe un botón «Copiar»: no uses citas para otra cosa. Sin consejos legales ni médicos: se explican riesgos y se remite a las fuentes. Todo precio citado debe figurar en una ficha.
