titulo: Mejorador de prompts gratis
descripcion: Analiza tu prompt en 6 puntos (detalle, contexto, audiencia, formato, ejemplo y límites), te dice qué le falta y lo reorganiza por bloques. Gratis y en tu navegador.
script: /herramientas-radar/app.js

¿Tienes un prompt que no termina de dar buenos resultados? Pégalo aquí: esta utilidad comprueba qué le falta, te da una puntuación de 0 a 6 y lo reorganiza en una instrucción por bloques, con huecos para completar lo que falte.

<div class="utility-app" data-tool="mejorador-de-prompts" markdown="0">
<form id="radar-form" class="utility-grid"></form>
<div class="actions"><button id="run-tool" class="btn primary" type="button">✦ Mejorar prompt</button><button id="sample-tool" class="btn secondary" type="button">Probar ejemplo</button><button id="clear-tool" class="btn secondary" type="button">Limpiar</button></div><div class="result"><div class="result-head"><h2>Prompt mejorado</h2><div id="radar-meta" class="meta">Listo para empezar.</div><button id="copy-output" class="btn secondary" type="button">Copiar</button></div><pre id="radar-output">Aquí aparecerá tu prompt mejorado y su diagnóstico.</pre></div>
</div>

## Para qué sirve

Muchas respuestas flojas de un asistente de IA se deben a una petición incompleta: falta contexto, no se dice para quién es ni qué formato se espera. Este mejorador **revisa tu prompt punto por punto**, te explica qué le falta y te devuelve una versión ordenada por bloques para que la completes y la pegues en ChatGPT, Claude, Gemini o el asistente que uses.

## Cómo usarlo paso a paso

1. **Prompt actual**: pega tu petición tal cual. Es el único campo obligatorio.
2. **Contexto adicional** (opcional): quién eres, para qué es, datos de partida.
3. **Audiencia** (opcional): para quién es el resultado.
4. **Uso o modelo** (opcional): chat, imagen, vídeo, código… Se añade al final del prompt.
5. **Formato deseado** (opcional): tabla, lista, pasos, extensión.

Pulsa **Mejorar prompt**. Arriba verás el diagnóstico y debajo, el prompt mejorado.

## Qué revisa el diagnóstico

| Punto | Se da por cumplido si… |
|---|---|
| Detalle | El prompt tiene al menos 15 palabras. |
| Contexto | Rellenas el campo de contexto o el prompt dice quién eres o para qué es («soy…», «trabajo en…», «mi empresa…», «es para…»). |
| Audiencia | Rellenas el campo de audiencia o el prompt menciona destinatarios («mis alumnos», «clientes», «dirigido a…»). |
| Formato | Rellenas el campo de formato o el prompt pide uno («tabla», «lista», «pasos», «300 palabras»…). |
| Ejemplo | El prompt incluye un ejemplo («por ejemplo…»). Es opcional, pero ayuda mucho. |
| Límites | El prompt marca límites («máximo», «extensión máxima», «evita», «no inventes», «120 palabras»…). |

Es una comprobación por palabras clave: te ayuda a no olvidar nada, pero no entiende el sentido de tu texto. Si crees que un punto ya está cubierto con otras palabras, puedes ignorar el aviso.

## Qué hace con tu prompt

El prompt mejorado ordena tu petición en bloques: **tarea**, **contexto**, **audiencia**, **formato**, **ejemplo** (si falta) y **límites**. Donde falta información, deja un hueco como «[completa: para quién es el resultado]» para que lo rellenes tú: no se inventa datos. En los límites añade siempre una instrucción útil: que la IA no invente datos y te pregunte si falta información.

## Ejemplo

El prompt «Hazme un resumen de este tema» saca **0 de 6**: es muy corto y no dice para quién es ni en qué formato. En cambio, «Soy profesor de biología de 4.º de ESO. Hazme un resumen de la fotosíntesis dirigido a mis alumnos, en una lista de 5 puntos, con máximo 120 palabras. Por ejemplo: "1. La planta capta luz…". No inventes datos» saca **6 de 6**, y la utilidad te indica que ya está bien planteado.

## Buenas prácticas

- **Una tarea por prompt**: si pides muchas cosas a la vez, divide la petición.
- **Da los datos tú**: pega el texto, las cifras o el documento que la IA debe usar, en lugar de esperar que los conozca.
- **Itera**: si la primera respuesta no te convence, pide cambios concretos («más corto», «con un ejemplo») en lugar de empezar de cero.
- **Protege tu privacidad**: no incluyas datos personales, contraseñas ni información confidencial. Lo explicamos en la guía de [privacidad al usar IA](/guias/privacidad-en-ia/).

Si prefieres construir el prompt desde cero, usa el [generador de prompts](/herramientas-radar/generador-de-prompts/), y si buscas prompts ya preparados, la [biblioteca de prompts](/prompts/). Para aprender la técnica, lee la guía de [cómo escribir buenos prompts](/guias/mejores-prompts/).

## Privacidad

La utilidad funciona por completo en tu navegador: el prompt que pegas no se envía a ningún servidor ni se guarda.

## Preguntas frecuentes

### ¿Usa inteligencia artificial para mejorar mi prompt?

No. El análisis se hace con reglas fijas en tu navegador, sin enviar nada a ninguna IA. Por eso es instantáneo y privado, pero también es más limitado que pedirle a un asistente que revise tu prompt.

### ¿Funciona para prompts de imágenes?

Está pensado para peticiones de texto. Para imágenes, usa el [generador de prompts para imágenes](/herramientas-radar/prompt-imagenes/).

### ¿Tengo que registrarme o pagar?

No. La utilidad es gratuita, no requiere cuenta y funciona directamente en tu navegador.
