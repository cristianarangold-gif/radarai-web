titulo: OpenAI lanza la Decisions API: respuestas tipadas y 10 veces más rápidas que la Responses API
descripcion: La Decisions API ya es de disponibilidad general: clasifica, puntúa y enruta texto, imágenes y JSON con gpt-6-luna a 0,10 $ por millón de tokens de entrada.
fecha: 2026-10-23
empresa: openai
herramientas: chatgpt
fuentes: https://developers.openai.com/api/docs/guides/decisions

OpenAI ha declarado en su documentación oficial que la **Decisions API**, hasta ahora en beta pública, pasa a estar disponible de forma general. Se trata de un endpoint pensado para que una aplicación obtenga respuestas cerradas y medibles —una probabilidad, una opción de una lista o una puntuación— en lugar de un texto libre. Según la documentación oficial de OpenAI, consultada hoy, es unas diez veces más rápida que la Responses API para este tipo de tareas.

## Qué ha anunciado OpenAI

La Decisions API se llama con una petición a `POST /v1/decisions` y, por ahora, solo admite un modelo: **gpt-6-luna**, el escalón rápido y económico de la familia GPT-6. La petición lleva tres piezas: el modelo, la información de entrada (texto, imágenes o JSON) y una lista de preguntas. Cada pregunta tiene un nombre y devuelve un tipo de respuesta concreto:

- **Predicado:** la probabilidad, de 0 a 1, de que se cumpla una condición. Por ejemplo, si una foto de producto muestra un daño visible.
- **Elección:** una opción entre varias que defines tú, como el departamento al que enviar un mensaje de soporte.
- **Puntuación:** una nota sobre niveles ordenados, como la gravedad de una incidencia.

Desde la beta, la documentación enumera varias mejoras: caché de prompts con descuento, imágenes distintas en cada pregunta, entrada directa de JSON, hasta 400 preguntas por petición (antes 200), imágenes por URL pública, evaluación de historiales de conversación con llamadas a herramientas, informes de uso por organización, integración nativa con GPT-Live y conexión por Private Link.

En precios, OpenAI indica que la entrada sin caché cuesta **0,10 $ por millón de tokens** y que **los tokens de salida no se cobran**. Se aplican los recargos habituales por procesamiento regional y por contextos largos. Todas las cifras, incluida la de velocidad, proceden de la propia empresa.

## Por qué importa en España y Latinoamérica

Muchas pymes y equipos de desarrollo hispanohablantes no necesitan que una IA redacte textos: necesitan que **ordene** cosas. Clasificar correos de clientes, priorizar tickets, detectar si una reclamación es un cobro duplicado o decidir si una respuesta contesta de verdad a la pregunta son tareas repetitivas donde importan el coste y la latencia más que la prosa.

Hay un detalle relevante para quien trabaja con datos de clientes europeos: OpenAI afirma que el procesamiento regional está disponible en Estados Unidos y en Europa (EEE más Suiza), que existe residencia de datos en las regiones de API compatibles y que la API admite retención cero de datos para clientes elegibles. Para una empresa en España sujeta al RGPD, eso puede facilitar el análisis de riesgos, aunque las condiciones exactas dependen de los acuerdos y requisitos que OpenAI detalla en su documentación de controles de datos. Si tratas datos personales, conviene repasar antes nuestra [guía de privacidad en IA](/guias/privacidad-en-ia/).

## Qué cambia en la práctica

Para un usuario final de [ChatGPT](/herramientas/chatgpt/) no cambia nada de forma directa: esto es una herramienta para quienes construyen productos sobre la API. Aun así, sus efectos llegarán a las aplicaciones que usas. Para un desarrollador o una pyme con un equipo técnico, lo práctico es:

- **Sustituir llamadas genéricas por decisiones tipadas.** Si hoy pides a un modelo que «responda sí o no» y luego interpretas el texto, la Decisions API devuelve directamente una probabilidad que puedes comparar con un umbral propio.
- **Ajustar umbrales según el coste del error.** OpenAI recomienda calibrar con ejemplos propios, porque no cuesta lo mismo un falso positivo que un falso negativo.
- **Abaratar con caché.** Si reutilizas un documento o una imagen de referencia y solo cambias las preguntas, el prefijo compartido (mínimo 1.024 tokens) puede beneficiarse de la caché.
- **Respetar los límites.** Solo hay un modelo disponible, no se admiten archivos por identificador, audio ni referencias a elementos, y la API no genera texto libre: para extraer campos o redactar explicaciones, OpenAI sigue señalando las salidas estructuradas de la Responses API.

Nadie debería delegar en una probabilidad una decisión con consecuencias legales, médicas o laborales sin supervisión humana. El propio diseño de la API deja la acción final en manos de tu aplicación.

## La opinión de Radar IA

Es una pieza menos vistosa que un modelo nuevo, pero probablemente más útil para el día a día de las empresas. Convertir la IA en un «detector» barato y rápido, con una salida que se puede medir, encaja mejor con muchos procesos reales que pedirle un párrafo cada vez. El precio de entrada declarado es muy bajo y que la salida no se cobre simplifica los cálculos de coste.

Con cautela: la velocidad y la calidad que anuncia OpenAI son datos del fabricante y no hemos visto comparativas independientes. Tampoco queda claro, a falta de pruebas de cada equipo, cómo se comportará con textos en español de Latinoamérica o con jerga sectorial. Si piensas adoptarla, empieza con un conjunto de casos reales etiquetados por personas y mide la tasa de aciertos antes de automatizar nada. Si tienes un negocio pequeño y quieres ideas de dónde aplicar IA con sentido, nuestra [guía de IA para pequeñas empresas](/guias/ia-para-pequenas-empresas/) es un buen punto de partida.

*Fuente: guía de la Decisions API en la documentación oficial para desarrolladores de OpenAI (consultada el 23 de octubre de 2026).*
