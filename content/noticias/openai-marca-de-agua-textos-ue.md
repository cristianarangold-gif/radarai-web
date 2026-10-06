titulo: ChatGPT añadirá una marca de agua invisible a sus textos en la Unión Europea
descripcion: OpenAI marcará los textos de ChatGPT y Codex en la UE para cumplir la Ley de IA. Te explicamos cómo funciona, sus límites y qué cambia para estudiantes, empresas y creadores.
fecha: 2026-10-06
empresa: openai
herramientas: chatgpt
fuentes: https://openai.com/index/eu-text-provenance

OpenAI ha anunciado que, **en las próximas semanas, añadirá una marca de agua invisible a los textos que generan ChatGPT y Codex en la Unión Europea**. La medida responde a la Ley de Inteligencia Artificial de la UE, que exige a los proveedores de IA generativa que el texto que producen sea identificable de forma legible por máquinas. La compañía lo comunicó el 5 de octubre de 2026 en un artículo en el que, además, reconoce abiertamente las limitaciones de esta tecnología.

## Qué ha anunciado OpenAI

El plan tiene tres partes, según la propia OpenAI:

1. **API, de forma opcional.** Desde el anuncio, los clientes de la API de todo el mundo pueden activar la marca de agua de texto en algunos modelos. En la API seguirá **desactivada por defecto**.
2. **ChatGPT y Codex en la UE.** En las próximas semanas, los textos «elegibles» que generen ChatGPT y Codex en la Unión Europea llevarán una marca de agua invisible.
3. **Detector de acceso restringido.** OpenAI abre solicitudes para su detector de marcas de agua, pero inicialmente solo para investigadores y organizaciones expertas aprobadas.

La tecnología se llama **textGrain** y funciona introduciendo una señal estadística invisible en la elección de palabras del modelo. El detector busca esa señal para estimar si un fragmento contiene la marca de OpenAI. La empresa afirma que publicará la tecnología como código abierto.

## Lo que la marca de agua puede y no puede hacer

Lo más interesante del anuncio es la franqueza con la que OpenAI describe los límites de su propio sistema:

- **Los textos cortos son difíciles de detectar.** Con una tasa objetivo de falsos positivos del 1 %, el detector identificó la marca en torno al 80 % de los fragmentos de 200 *tokens* y en torno al 95 % de los de 400 *tokens* en contenidos como psicología. En matemáticas, donde hay menos libertad para elegir palabras, la detección fue sustancialmente menor.
- **Editar el texto debilita la marca.** En fragmentos de 400 *tokens*, sustituir el 10 % de las palabras por sinónimos redujo la detección de aproximadamente el 92 % al 66 %, y sustituir el 25 % la bajó al 17 %.
- **No identifica al usuario** ni dice quién escribió el texto, cuánto trabajo humano hay en él ni si es verdadero.
- **Que no aparezca la marca no demuestra que lo haya escrito una persona.** El texto puede ser demasiado corto, estar editado o traducido, o proceder de otro modelo.

Según OpenAI, en sus pruebas de rendimiento no observó diferencias significativas en la calidad de las respuestas con y sin marca de agua.

## Por qué importa en España y Latinoamérica

En **España y el resto de la UE**, la medida afecta directamente a cualquiera que use ChatGPT para escribir: estudiantes, redactores, agencias o empresas. Aunque la marca es invisible y no cambia lo que lees, deja una señal en el texto que, en el futuro, podría comprobarse con herramientas autorizadas.

En **Latinoamérica**, el anuncio no implica cambios inmediatos en ChatGPT, porque el despliegue se limita a la UE. Sin embargo, cualquier cliente de la API puede activar la marca de forma voluntaria.

## Qué cambia en la práctica

- **Para estudiantes:** la marca de agua no es un «detector de trampas» infalible y, de momento, el detector no es público. Lo sensato sigue siendo usar la IA para aprender, no para entregar trabajos ajenos. Lo explicamos en nuestra guía de [IA para estudiar](/guias/ia-para-estudiar/).
- **Para empresas y creadores:** conviene revisar si los textos generados con IA deben identificarse como tales según el uso que se les dé, y mantener siempre una revisión humana.
- **Para quien desconfía de un texto:** ni la presencia ni la ausencia de la marca resuelven por sí solas si un contenido es fiable. Hay que seguir comprobando fuentes y datos.

## La opinión de Radar IA

Es una buena noticia que OpenAI explique con cifras qué puede y qué no puede hacer su sistema, en lugar de presentarlo como una solución mágica. La transparencia sobre el origen de los contenidos es necesaria, pero las marcas de agua de texto son todavía una herramienta frágil: basta con reescribir una parte para debilitarlas. El riesgo principal es que alguien las use como prueba definitiva de autoría, algo que la propia OpenAI desaconseja. Para usuarios y docentes, el mensaje es claro: **ninguna marca sustituye al criterio humano**.

Si te preocupa cómo se tratan tus textos, repasa nuestra guía de [privacidad al usar IA](/guias/privacidad-en-ia/) y la [ficha de ChatGPT](/herramientas/chatgpt/).
