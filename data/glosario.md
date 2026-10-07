Glosario de Radar IA. Cada término empieza con «## Término», sigue con sus metadatos (tema obligatorio;
relacionados, ver, alias y ejemplo opcionales) y, tras una línea en blanco, la definición en Markdown
(25–160 palabras). Temas: basicos, modelos, uso, precios, etica. Ver docs/superpowers/specs/2026-10-07-glosario-design.md.

## Agente de IA
tema: uso
relacionados: asistente-de-ia, automatizacion
ver: /guias/automatizar-tareas/
ejemplo: Le pides «reserva una mesa para cuatro el viernes» y el agente busca restaurantes, compara horarios y rellena el formulario de reserva.

Un asistente de IA que no se limita a responder: recibe un encargo y da **varios pasos por su cuenta** para cumplirlo. Puede buscar en internet, abrir páginas, usar otras aplicaciones o ejecutar código, y decide el siguiente paso según lo que va encontrando. Como actúa en tu nombre, conviene revisar qué permisos le das y comprobar el resultado antes de darlo por bueno.

## Alucinación
tema: basicos
relacionados: modelo-de-lenguaje, rag
ver: /guias/mejores-prompts/
ejemplo: Le pides la biografía de un autor poco conocido y te atribuye un libro que no existe, con título y año incluidos.

Cuando un asistente de IA **se inventa un dato, una cita o una fuente** y lo presenta con total seguridad. Ocurre porque el modelo genera el texto que le parece más probable, no comprueba si es verdad. Es más frecuente con temas poco conocidos, cifras exactas y referencias bibliográficas. Por eso conviene verificar siempre lo importante en una fuente fiable.

## API
tema: precios
alias: interfaz de programación
relacionados: token, modelo-de-lenguaje

Siglas de *Application Programming Interface*. Es la puerta que una empresa de IA abre para que **otros programas** usen sus modelos sin pasar por su web o su aplicación. Los desarrolladores la usan para integrar la IA en sus propios productos. Normalmente se paga por uso, midiendo la cantidad de texto que se envía y se recibe en tokens, y es independiente de la suscripción mensual de la aplicación.

## Asistente de IA
tema: basicos
alias: chatbot
relacionados: modelo-de-lenguaje, prompt, agente-de-ia
ver: /mejor-ia-gratis/

Programa con el que **conversas en lenguaje normal**, escribiendo o hablando, para pedirle que redacte, resuma, traduzca, explique o te ayude a pensar. ChatGPT, Gemini, Claude o Copilot son asistentes. Por dentro funcionan con un modelo de lenguaje, y muchos pueden además leer documentos, ver imágenes o buscar en internet.

## Automatización
tema: uso
relacionados: agente-de-ia, api
ver: /guias/automatizar-tareas/

Hacer que una tarea repetitiva se haga **sola o casi sola**, sin que tengas que repetir los mismos pasos cada vez. Con IA se puede, por ejemplo, clasificar correos, resumir reuniones o preparar borradores a partir de un formulario. Se monta con herramientas que conectan aplicaciones entre sí o con agentes de IA, y siempre conviene revisar los primeros resultados antes de confiar en ella.

## IA generativa
tema: basicos
alias: GenAI
relacionados: modelo-de-lenguaje, asistente-de-ia
ver: /mejor-ia-para-imagenes/

Tipo de inteligencia artificial que **crea contenido nuevo**: texto, imágenes, audio, música, vídeo o código, a partir de una instrucción. Aprende patrones de enormes cantidades de ejemplos y produce resultados parecidos, pero no idénticos, a lo que ha visto. ChatGPT, Midjourney, Suno o Runway son herramientas de IA generativa.

## Modelo de lenguaje
tema: modelos
alias: LLM, modelo grande de lenguaje
relacionados: token, ventana-de-contexto, alucinacion
ejemplo: Si escribes «La capital de Francia es», el modelo calcula que lo más probable es que siga «París».

Programa entrenado con enormes cantidades de texto para **predecir qué palabras vienen a continuación**. Repitiendo esa predicción una y otra vez es capaz de redactar, resumir, traducir o razonar paso a paso. Es el «motor» que hay dentro de los asistentes como ChatGPT o Claude. Como no consulta una base de datos de hechos, puede equivocarse con seguridad.

## Plan freemium
tema: precios
alias: plan gratuito
relacionados: suscripcion
ver: /mejor-ia-gratis/, /comparador/

Modelo de precios en el que la herramienta se puede usar **gratis con límites** (de mensajes, de funciones, de calidad o de velocidad) y ofrece un plan de pago que los amplía. Es lo más habitual en las herramientas de IA. Antes de pagar, merece la pena comprobar si el plan gratuito cubre lo que de verdad necesitas.

## Prompt
tema: uso
relacionados: asistente-de-ia, ventana-de-contexto
ver: /guias/mejores-prompts/, /herramientas-radar/mejorador-de-prompts/
ejemplo: En vez de «escribe un correo», prueba con «escribe un correo breve y cordial a un cliente para retrasar la entrega dos días».

La **instrucción que le das** a una herramienta de IA. Puede ser una pregunta, una orden o un texto largo con contexto, ejemplos y el formato que quieres. Cuanto más claro y concreto sea, mejor suele ser el resultado. Si la primera respuesta no te sirve, no hace falta empezar de cero: puedes pedirle que cambie lo que no te convence.

## RAG
tema: modelos
alias: generación aumentada por recuperación
relacionados: alucinacion, modelo-de-lenguaje

Técnica que consiste en que la IA **busque primero información en documentos o fuentes concretas** y responda apoyándose en lo que ha encontrado, en lugar de fiarse solo de lo que aprendió en su entrenamiento. Es lo que hacen las herramientas que responden con tus apuntes o con resultados de búsqueda citando la fuente. Reduce las alucinaciones, aunque no las elimina.

## Suscripción
tema: precios
relacionados: plan-freemium, api
ver: /comparador/

Pago periódico, normalmente mensual o anual, que da acceso a un plan de pago de una herramienta de IA: más uso, modelos más potentes o funciones extra. Los precios cambian a menudo y pueden mostrarse sin impuestos o en dólares, así que conviene mirar la página oficial y la fecha en que se comprobaron antes de suscribirse.

## Token
tema: modelos
relacionados: modelo-de-lenguaje, ventana-de-contexto, api
ejemplo: Una palabra larga como «inteligencia» puede dividirse en dos o tres tokens.

El **trozo de texto** con el que trabaja un modelo de lenguaje: puede ser una palabra corta, una parte de una palabra o un signo de puntuación. Los modelos leen y escriben token a token. Los límites de longitud de una conversación y los precios de las API se miden en tokens, no en palabras.

## Ventana de contexto
tema: modelos
relacionados: token, modelo-de-lenguaje, prompt

La **cantidad máxima de texto que un modelo puede tener en cuenta a la vez**: lo que le has escrito, los documentos que le has dado y sus propias respuestas. Se mide en tokens. Cuando una conversación la supera, el modelo deja de «ver» la parte más antigua, y por eso a veces parece olvidar lo que dijiste al principio.
