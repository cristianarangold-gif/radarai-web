titulo: Contador de palabras y analizador de texto
descripcion: Cuenta palabras, caracteres, frases y párrafos, calcula el tiempo de lectura y de locución y detecta las palabras que más repites. Gratis, sin registro y sin enviar tu texto a ningún servidor.
script: /herramientas-radar/app.js

Pega cualquier texto y obtén al instante el número de palabras, caracteres, frases y párrafos, el tiempo estimado de lectura, las palabras que más repites y las frases demasiado largas.

<div class="utility-app" data-tool="contador-de-palabras" markdown="0">
<form id="radar-form" class="utility-grid"></form>
<div class="actions"><button id="run-tool" class="btn primary" type="button">✦ Analizar texto</button><button id="sample-tool" class="btn secondary" type="button">Probar ejemplo</button><button id="clear-tool" class="btn secondary" type="button">Limpiar</button></div><div class="result"><div class="result-head"><h2>Análisis</h2><div id="radar-meta" class="meta">Listo para empezar.</div><button id="copy-output" class="btn secondary" type="button">Copiar</button></div><pre id="radar-output">Aquí aparecerán las métricas del texto.</pre></div>
</div>

## Para qué sirve

Muchos textos tienen límites de extensión: trabajos académicos, descripciones de productos, publicaciones en redes, guiones de vídeo o formularios de candidaturas. Este contador te da en un momento las cifras clave de tu texto y, además, te señala dos defectos muy habituales, también en los textos generados con IA: las **palabras repetidas** y las **frases demasiado largas**.

## Qué datos te da

| Dato | Qué significa |
|---|---|
| Palabras | Número de palabras del texto (los números también cuentan). |
| Caracteres | Todos los caracteres, con espacios y signos. |
| Sin espacios | Los caracteres sin contar espacios ni saltos de línea. |
| Frases | Fragmentos separados por punto, signo de exclamación, de interrogación o puntos suspensivos, o por un salto de línea (así, un título o un elemento de lista cuentan como frase propia). Si el texto no termina en punto, la última frase también cuenta. |
| Párrafos | Bloques separados por una línea en blanco. |
| Media por frase | Palabras por frase, de media. |
| Frases de más de 30 palabras | Cuántas frases conviene revisar por si se pueden dividir. |
| Lectura | Minutos aproximados de lectura, calculados a 200 palabras por minuto. |
| Locución | Minutos aproximados leyendo en voz alta, calculados a 130 palabras por minuto. |
| Palabras más repetidas | Hasta 8 palabras de 4 letras o más (sin contar números) que aparecen al menos 2 veces. No cuenta palabras muy comunes del español como «para», «como», «este» o «tiene». |

Las velocidades de lectura y de locución son una referencia fija para hacer el cálculo: cada persona lee a su ritmo, así que tómalas como una estimación.

## Cómo usarlo

1. Pega o escribe tu texto en el campo **Texto**.
2. Pulsa **Analizar texto**. Si solo quieres ver cómo funciona, pulsa **Probar ejemplo**.
3. Revisa las cifras y, sobre todo, las palabras repetidas y las frases largas.
4. Pulsa **Copiar** si quieres guardar el análisis.

## Ejemplo

Con el texto de ejemplo, que repite tres veces «inteligencia artificial» en tres frases, el contador indica 30 palabras, 3 frases, una media de 10 palabras por frase y, como palabras más repetidas, «artificial (×3) · inteligencia (×3)». Es una pista clara para cambiar alguna de ellas por «la IA», «estas herramientas» o un pronombre.

## Usos habituales

- **Estudiantes**: comprobar que un trabajo o una redacción cumple el número de palabras exigido.
- **Redactores y creadores**: ajustar textos a los límites de cada red social o calcular la duración aproximada de un guion leído en voz alta.
- **Búsqueda de empleo**: ajustar cartas de presentación y respuestas a formularios con límite de caracteres.
- **Revisión de textos de IA**: si un texto generado repite palabras o encadena frases largas, el análisis te ayuda a localizarlas.

## Consejos para mejorar tu texto

- **Palabras repetidas**: si una palabra aparece muchas veces, busca un sinónimo, usa un pronombre o reformula la frase. Las repeticiones de términos técnicos a veces son necesarias para no confundir al lector; no hace falta eliminarlas todas.
- **Frases largas**: una frase de más de 30 palabras suele poder dividirse en dos. Busca los «y», «que» o «porque» que encadenan ideas distintas.
- **Extensión**: si te pasas del límite, empieza por quitar repeticiones y frases de relleno antes de recortar ideas.
- **Estilo y gramática**: este contador no corrige errores. Para eso, combínalo con alguna de las herramientas que comparamos en [la mejor IA para escribir](/mejor-ia-para-escribir/).

## Límites que conviene conocer

- Las abreviaturas con punto, como «Sr.» o «etc.», pueden contarse como final de frase.
- Los resultados pueden variar ligeramente respecto a Word o Google Docs, según cómo trate cada programa los números, los guiones o los signos.
- El análisis de repeticiones distingue palabras exactas: «estudiar» y «estudio» cuentan por separado.

## Privacidad

El análisis se hace por completo en tu navegador: el texto que pegas no se envía a ningún servidor ni se guarda. Puedes usarlo con tranquilidad incluso con documentos de trabajo.

## Preguntas frecuentes

### ¿Cuenta igual que Word o Google Docs?

Los resultados pueden variar ligeramente según cómo trate cada programa los números, los guiones o los signos, pero son equivalentes para comprobar límites de extensión.

### ¿Por qué no aparecen palabras como «para» o «como» entre las repetidas?

Porque son palabras que cualquier texto en español repite de forma natural. Las excluimos para que la lista muestre solo las repeticiones que sí conviene revisar.

### ¿Tengo que registrarme o pagar?

No. La utilidad es gratuita, no requiere cuenta y funciona directamente en tu navegador.
