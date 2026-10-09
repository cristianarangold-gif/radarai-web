titulo: Generador de prompts gratis
descripcion: Crea prompts claros y completos para ChatGPT, Claude o Gemini rellenando objetivo, contexto, audiencia, formato, tono y restricciones. Gratis y sin registro.
script: /herramientas-radar/app.js

Este generador te ayuda a escribir peticiones completas para cualquier asistente de inteligencia artificial. Rellenas unos pocos campos y obtienes un prompt estructurado, listo para copiar en ChatGPT, Claude, Gemini o la herramienta que uses.

<div class="utility-app" data-tool="generador-de-prompts" markdown="0">
<form id="radar-form" class="utility-grid"></form>
<div class="actions"><button id="run-tool" class="btn primary" type="button">✦ Crear prompt</button><button id="sample-tool" class="btn secondary" type="button">Probar ejemplo</button><button id="clear-tool" class="btn secondary" type="button">Limpiar</button></div><div class="result"><div class="result-head"><h2>Resultado</h2><div id="radar-meta" class="meta">Listo para empezar.</div><button id="copy-output" class="btn secondary" type="button">Copiar</button></div><pre id="radar-output">Aquí aparecerá tu prompt completo.</pre></div>
</div>

## Para qué sirve

La mayoría de respuestas mediocres de la IA se deben a peticiones incompletas. Este generador te obliga a pensar en los elementos que marcan la diferencia: **qué quieres conseguir, el contexto, para quién es, en qué formato y con qué tono**, además de las restricciones que debe respetar. Es la misma estructura que explicamos en nuestra guía de [cómo escribir buenos prompts](/guias/mejores-prompts/), convertida en un formulario.

## Cómo usarlo paso a paso

1. **Objetivo**: describe el resultado con un verbo claro («redactar un correo para…», «resumir este informe para…»).
2. **Contexto**: añade los datos que la IA no puede adivinar: tu situación, antecedentes y cifras relevantes.
3. **Audiencia**: indica para quién es el resultado (un cliente, tu responsable, alumnos de secundaria).
4. **Formato**: tabla, lista de pasos, correo breve, guion, tres opciones…
5. **Tono**: profesional, cercano, técnico, divertido.
6. **Restricciones**: longitud máxima, cosas que debe evitar o requisitos obligatorios.

Pulsa **Crear prompt**, revísalo y cópialo en tu asistente. Si no sabes por dónde empezar, usa **«Probar ejemplo»**. Solo el objetivo es obligatorio.

## Qué contiene el prompt generado

El resultado es un prompt ordenado en bloques con títulos en mayúsculas, que los asistentes de IA interpretan bien:

| Bloque | Qué incluye | Si dejas el campo vacío |
|---|---|---|
| ROL | Pide a la IA que actúe como especialista en la tarea. | Siempre se incluye. |
| OBJETIVO | Tu objetivo, tal cual lo escribes. | Es obligatorio. |
| CONTEXTO | Tus datos y antecedentes. | Pide a la IA que no invente información y que señale los datos que falten. |
| AUDIENCIA | Para quién es el resultado. | Pide adaptar el nivel al lector. |
| INSTRUCCIONES | Analizar la petición, dividirla en pasos, explicar supuestos y dar ejemplos concretos. | Siempre se incluye. |
| FORMATO | Cómo quieres la respuesta. | Pide una respuesta clara y estructurada. |
| TONO | El tono que elijas. | Claro y profesional. |
| RESTRICCIONES | Tus límites y requisitos. | Pide no inventar datos y señalar las dudas. |
| CONTROL DE CALIDAD | Pide revisar objetivo, formato, precisión y restricciones antes de responder. | Siempre se incluye. |

Los valores por defecto evitan que el prompt quede cojo, pero el resultado siempre mejora cuanto más concretos sean tus campos, sobre todo el contexto.

## Ejemplo

Con el objetivo «pedir una reunión para revisar mi salario», un contexto con tus logros del último año, la audiencia «mi responsable directa», el formato «correo de menos de 150 palabras» y el tono «profesional y seguro», obtendrás un prompt mucho más preciso que un simple «escribe un correo para pedir un aumento».

## Consejos para sacarle partido

- **Un objetivo por prompt**: si necesitas varias cosas, genera un prompt para cada una.
- **El contexto es lo que más cambia el resultado**: datos, cifras, el texto original o la situación concreta. La IA no puede adivinarlos.
- **Pide un formato que puedas usar**: «tabla con tres columnas», «correo de menos de 150 palabras», «5 opciones numeradas».
- **Revisa la respuesta**: los asistentes pueden equivocarse con total seguridad. Comprueba siempre los datos importantes.
- **Guarda los prompts que te funcionen** para reutilizarlos y adaptarlos.

## ¿Generador, mejorador o biblioteca?

- **Generador de prompts** (esta utilidad): cuando partes de cero y quieres que el formulario te recuerde todo lo importante.
- **[Mejorador de prompts](/herramientas-radar/mejorador-de-prompts/)**: cuando ya tienes un prompt escrito y quieres saber qué le falta.
- **[Biblioteca de prompts](/prompts/)**: cuando buscas un prompt ya preparado para una tarea habitual (un correo difícil, un resumen, un plan de estudio) y solo quieres rellenar los huecos.

## Privacidad

La utilidad funciona por completo en tu navegador: no envía lo que escribes a ningún servidor ni lo guarda. Aun así, recuerda no incluir datos sensibles cuando pegues el prompt en un asistente de IA; lo explicamos en la guía de [privacidad al usar IA](/guias/privacidad-en-ia/).

## Preguntas frecuentes

### ¿Sirve para cualquier IA?

Sí. El prompt resultante funciona en ChatGPT, Claude, Gemini, Copilot y otros asistentes de texto.

### ¿Puedo escribir el prompt en inglés?

Puedes escribir los campos en el idioma que quieras, pero los títulos de los bloques están en español. Los asistentes actuales entienden prompts en español sin problema; si necesitas la respuesta en otro idioma, indícalo en el formato («responde en inglés»).

### ¿Tengo que registrarme o pagar?

No. La utilidad es gratuita, no requiere cuenta y funciona directamente en tu navegador.
