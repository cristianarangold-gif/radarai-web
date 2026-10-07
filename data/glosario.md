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

Cuando un asistente de IA **se inventa un dato, una cita o una fuente** y lo presenta con total seguridad. Ocurre porque el modelo genera el texto que le parece más probable y no comprueba si es verdad. Es más frecuente con temas poco conocidos, cifras exactas y referencias bibliográficas. Por eso conviene verificar siempre lo importante en una fuente fiable.

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

Conseguir que una tarea repetitiva se haga **sola o casi sola**, sin que tengas que repetir los mismos pasos cada vez. Con IA se puede, por ejemplo, clasificar correos, resumir reuniones o preparar borradores a partir de un formulario. Se monta con herramientas que conectan aplicaciones entre sí o con agentes de IA, y siempre conviene revisar los primeros resultados antes de confiar en ella.

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
ejemplo: Una palabra larga como «inteligencia» puede dividirse en varios tokens.

El **trozo de texto** con el que trabaja un modelo de lenguaje: puede ser una palabra corta, una parte de una palabra o un signo de puntuación. Los modelos leen y escriben token a token. Los límites de longitud de una conversación y los precios de las API se miden en tokens, no en palabras.

## Ventana de contexto
tema: modelos
relacionados: token, modelo-de-lenguaje, prompt

La **cantidad máxima de texto que un modelo puede tener en cuenta a la vez**: lo que le has escrito, los documentos que le has dado y sus propias respuestas. Se mide en tokens. Cuando una conversación la supera, según la herramienta se recorta o se resume la parte más antigua, o te pide empezar una conversación nueva; por eso a veces parece olvidar lo que dijiste al principio.

## Inteligencia artificial
tema: basicos
alias: IA, AI
relacionados: aprendizaje-automatico, ia-generativa, modelo-de-lenguaje
ver: /mejor-ia/

Rama de la informática que crea programas capaces de hacer tareas que asociamos con la inteligencia humana: entender y escribir texto, reconocer imágenes y voz, traducir, recomendar o tomar decisiones a partir de datos. Hoy, cuando se habla de IA en el día a día, casi siempre se habla de **herramientas como los asistentes de chat o los generadores de imágenes**, que son solo una parte de un campo mucho más amplio.

## Aprendizaje automático
tema: basicos
alias: machine learning, ML
relacionados: inteligencia-artificial, entrenamiento, aprendizaje-profundo

Forma de crear inteligencia artificial en la que el programa **aprende a partir de ejemplos** en lugar de seguir reglas escritas a mano. Se le muestran muchos datos (correos marcados como spam o no, fotos etiquetadas, textos) y ajusta su funcionamiento hasta acertar con datos nuevos. Casi toda la IA actual, incluidos los asistentes de chat, se basa en aprendizaje automático.

## Aprendizaje profundo
tema: basicos
alias: deep learning
relacionados: red-neuronal, aprendizaje-automatico, transformer

Tipo de aprendizaje automático que usa **redes neuronales con muchas capas**. Cada capa aprende a reconocer patrones cada vez más complejos: en una imagen, primero bordes, luego formas y después objetos. Es la técnica que ha hecho posibles los avances recientes en reconocimiento de voz, traducción, generación de imágenes y modelos de lenguaje.

## Red neuronal
tema: basicos
relacionados: aprendizaje-profundo, parametros, entrenamiento

Modelo matemático inspirado de forma muy libre en el cerebro: está formado por muchas unidades sencillas conectadas entre sí, organizadas en capas. Cada conexión tiene un peso que se ajusta durante el entrenamiento. Por sí sola, una neurona artificial hace un cálculo muy simple; la capacidad de la red sale de **millones o miles de millones de conexiones trabajando juntas**.

## Algoritmo
tema: basicos
relacionados: aprendizaje-automatico, sesgo

Conjunto de pasos ordenados para resolver un problema o hacer una tarea, como una receta. Los programas informáticos están hechos de algoritmos. En el contexto de la IA, se habla a menudo de «el algoritmo» para referirse al sistema que decide qué te recomienda una red social o una tienda, aunque detrás suele haber un modelo entrenado con datos y no una lista de reglas fija.

## Entrenamiento
tema: basicos
relacionados: aprendizaje-automatico, datos-de-entrenamiento, ajuste-fino, fecha-de-corte

Proceso en el que un modelo de IA **aprende a partir de grandes cantidades de datos**, ajustando poco a poco sus parámetros para equivocarse cada vez menos. Entrenar un modelo grande exige muchísima potencia de cálculo y puede durar semanas o meses. Una vez entrenado, el modelo ya no aprende por sí solo de cada conversación, salvo que la empresa lo vuelva a entrenar o lo ajuste.

## IA multimodal
tema: basicos
alias: multimodalidad
relacionados: modelo-de-lenguaje, texto-a-imagen, sintesis-de-voz
ejemplo: Haces una foto a la nevera y le pides al asistente una receta con lo que ve.

Modelo o herramienta capaz de **trabajar con varios tipos de información a la vez**: texto, imágenes, audio, vídeo o documentos. Un asistente multimodal puede, por ejemplo, leer una foto de una factura, escuchar una pregunta en voz alta y responder hablando. La mayoría de los asistentes generalistas actuales ya son multimodales en mayor o menor medida.

## Inferencia
tema: modelos
relacionados: entrenamiento, token, api

Momento en el que un modelo ya entrenado **se usa para responder**: recibe tu prompt y genera la respuesta. Es lo que ocurre cada vez que escribes a un asistente. Distinguirlo del entrenamiento ayuda a entender los precios y los límites: el coste de la inferencia depende de cuánto texto se procesa y de lo grande que sea el modelo, y por eso los planes limitan los mensajes.

## IA general
tema: basicos
alias: AGI, inteligencia artificial general
relacionados: inteligencia-artificial, modelo-de-lenguaje

Idea de una inteligencia artificial capaz de **aprender y hacer prácticamente cualquier tarea intelectual** que haga una persona, y no solo tareas concretas. No existe una definición acordada ni una prueba que diga cuándo se ha alcanzado. Algunas empresas la presentan como su objetivo, pero conviene leer con prudencia los titulares que la anuncian como inminente o ya conseguida.

## Parámetros
tema: modelos
relacionados: red-neuronal, entrenamiento, modelo-de-lenguaje

Los **valores internos que un modelo ajusta durante el entrenamiento**, como los pesos de las conexiones de una red neuronal. Son, en la práctica, lo que el modelo ha «aprendido». Se suele usar su número para describir el tamaño de un modelo, pero más parámetros no garantizan mejores respuestas: también influyen los datos, el entrenamiento y el ajuste posterior.

## Modelo fundacional
tema: modelos
alias: foundation model
relacionados: modelo-de-lenguaje, ajuste-fino, entrenamiento

Modelo grande entrenado con una cantidad enorme de datos variados para que sirva de **base a muchas aplicaciones distintas**. A partir de él, las empresas crean versiones especializadas o lo integran en sus productos. Los modelos que hay detrás de ChatGPT, Gemini o Claude son modelos fundacionales.

## Ajuste fino
tema: modelos
alias: fine-tuning
relacionados: modelo-fundacional, entrenamiento, datos-de-entrenamiento

Entrenamiento adicional que se aplica a un modelo ya entrenado para **especializarlo en una tarea, un estilo o un tipo de datos concreto**, usando muchos menos ejemplos que el entrenamiento original. Sirve, por ejemplo, para que un modelo responda con el tono de una marca o domine la terminología de un sector. Para el uso diario suele bastar con un buen prompt o con instrucciones personalizadas.

## Modelo de razonamiento
tema: modelos
relacionados: modelo-de-lenguaje, inferencia
ver: /mejor-ia-para-programar/

Modelo de lenguaje preparado para **«pensar» paso a paso antes de responder**: divide el problema, prueba caminos y revisa su propio trabajo. Suele dar mejores resultados en matemáticas, programación, lógica y análisis, a cambio de tardar más y, en las API, de consumir más tokens. Para preguntas sencillas, un modelo normal suele ser suficiente y más rápido.

## Modelo abierto
tema: modelos
alias: pesos abiertos, open weights
relacionados: ia-local, parametros, modelo-fundacional

Modelo cuyos **parámetros se publican para que cualquiera pueda descargarlo**, usarlo en su propio equipo o adaptarlo, según las condiciones de su licencia. Se habla de código abierto en sentido estricto cuando también se publican el código y los detalles del entrenamiento; muchos modelos solo publican los pesos. Frente a ellos están los modelos cerrados, a los que solo se accede a través de la web o la API de la empresa.

## Modelo de difusión
tema: modelos
relacionados: texto-a-imagen, ia-generativa
ver: /mejor-ia-para-imagenes/

Técnica con la que funcionan muchos generadores de imágenes y vídeo. El modelo aprende a **partir de una imagen llena de ruido aleatorio y a ir limpiándola paso a paso** hasta obtener una imagen que encaje con la descripción que le has dado. Por eso, con el mismo prompt, cada generación suele dar un resultado distinto.

## Embedding
tema: modelos
alias: incrustación, vector
relacionados: rag, modelo-de-lenguaje
ver: /noticias/embeddinggemma-2-google/

Forma de **convertir un texto, una imagen o un audio en una lista de números** que representa su significado. Textos con significados parecidos dan listas de números parecidas, aunque usen palabras distintas. Los embeddings permiten buscar por significado y no solo por palabras exactas, y son una pieza clave de los sistemas RAG que responden con tus propios documentos.

## Transformer
tema: modelos
relacionados: modelo-de-lenguaje, aprendizaje-profundo, token

Arquitectura de red neuronal presentada por investigadores de Google en 2017 que está en la base de casi todos los modelos de lenguaje actuales (la «T» de GPT viene de *transformer*). Su idea clave es la **atención**: al procesar cada token, el modelo tiene en cuenta los demás tokens del texto (en los modelos que generan texto, los anteriores) y decide cuáles son más importantes para entenderlo.

## Fecha de corte
tema: modelos
alias: fecha de corte de conocimiento, knowledge cutoff
relacionados: entrenamiento, busqueda-con-ia, alucinacion

Fecha hasta la que llegan los datos con los que se entrenó un modelo. Lo que pasó después **no lo conoce**, salvo que la herramienta busque en internet o le des tú la información. Por eso un asistente sin búsqueda puede darte precios, versiones o noticias desactualizados con total seguridad. Si la actualidad importa, comprueba si la respuesta cita fuentes recientes.

## Temperatura
tema: modelos
relacionados: modelo-de-lenguaje, inferencia, api

Ajuste que controla **cuánto se arriesga un modelo al elegir las palabras**. Con temperatura baja, las respuestas son más previsibles y repetibles; con temperatura alta, más variadas y creativas, pero también con más riesgo de errores. En las aplicaciones de chat no suele poder cambiarse directamente; sí en muchas API y en algunas herramientas para desarrolladores.

## IA local
tema: modelos
alias: IA en el dispositivo
relacionados: modelo-abierto, privacidad-de-datos

Modelo de IA que **funciona en tu propio ordenador o móvil**, sin enviar tus datos a un servidor externo. Tiene ventajas de privacidad y funciona sin conexión, pero los modelos que caben en un equipo personal suelen ser más pequeños y menos capaces que los grandes modelos en la nube, y necesitan un equipo con suficiente memoria.

## Instrucciones personalizadas
tema: uso
alias: custom instructions
relacionados: prompt, memoria, asistente-personalizado

Indicaciones que le das a un asistente **una sola vez para que las tenga en cuenta en todas las conversaciones**: quién eres, a qué te dedicas, qué tono prefieres o qué formato quieres en las respuestas. Ahorran repetir el mismo contexto en cada prompt. Internamente, las aplicaciones también usan un «prompt de sistema» que el usuario no ve.

## Ingeniería de prompts
tema: uso
alias: prompt engineering
relacionados: prompt, prompt-con-ejemplos, instrucciones-personalizadas
ver: /guias/mejores-prompts/, /herramientas-radar/generador-de-prompts/

Conjunto de técnicas para **escribir instrucciones que den mejores resultados**: dar contexto, decir el formato que quieres, poner ejemplos, dividir una tarea grande en pasos o pedir al modelo que revise su respuesta. No hace falta saber programar; se aprende probando, comparando resultados y ajustando lo que pides.

## Prompt con ejemplos
tema: uso
alias: few-shot
relacionados: prompt, ingenieria-de-prompts
ejemplo: «Convierte estas frases en titulares. Ejemplo: “Ha llovido mucho en Madrid” → “Madrid, bajo el agua”. Ahora: …».

Técnica que consiste en **incluir en el prompt uno o varios ejemplos** del resultado que esperas antes de pedir la tarea. El modelo imita el formato, el tono y la longitud de los ejemplos, y suele acertar mucho más que si solo describes lo que quieres. Es especialmente útil para clasificar, resumir con un formato fijo o mantener un estilo.

## Búsqueda con IA
tema: uso
alias: buscador con IA, respuestas con fuentes
relacionados: rag, fecha-de-corte, alucinacion
ver: /herramientas/perplexity/

Herramientas o funciones que **buscan en internet y redactan una respuesta resumida con enlaces a las fuentes**, en lugar de mostrar solo una lista de resultados. Permiten consultar información reciente que el modelo no conocía. Las fuentes citadas no garantizan que el resumen sea correcto: conviene abrirlas cuando el dato importa.

## Texto a imagen
tema: uso
relacionados: modelo-de-difusion, ia-generativa, prompt
ver: /mejor-ia-para-imagenes/, /herramientas-radar/prompt-imagenes/

Herramientas que **crean una imagen a partir de una descripción escrita**. Cuanto más concreto seas con el sujeto, el estilo, la luz, el encuadre y los colores, más se parecerá el resultado a lo que imaginas. Muchas permiten además editar partes de una imagen o crear variaciones de una que ya existe.

## Síntesis de voz
tema: uso
alias: texto a voz, TTS
relacionados: ia-multimodal, deepfake, transcripcion
ver: /herramientas/elevenlabs/

Tecnología que **convierte un texto escrito en voz hablada** con entonación natural. Se usa para locuciones, audiolibros, vídeos, accesibilidad o asistentes de voz. Algunas herramientas permiten clonar una voz a partir de grabaciones, algo que solo debe hacerse con la voz propia o con el permiso expreso de quien la tiene.

## Transcripción
tema: uso
alias: voz a texto, speech to text
relacionados: sintesis-de-voz, ia-multimodal
ver: /mejor-ia-para-productividad/

Conversión automática de **audio o vídeo hablado en texto escrito**. Con IA es rápida y bastante precisa, y muchas herramientas añaden quién habla, un resumen o las tareas pendientes de una reunión. La calidad baja con ruido, acentos marcados o varias personas hablando a la vez, así que conviene revisar nombres y cifras.

## Memoria
tema: uso
relacionados: instrucciones-personalizadas, ventana-de-contexto, privacidad-de-datos

Función de algunos asistentes que **guarda datos de tus conversaciones para usarlos en las siguientes**: tus preferencias, tu trabajo o proyectos en curso. Es distinta de la ventana de contexto, que solo abarca la conversación actual. Normalmente puedes ver, borrar o desactivar lo que el asistente recuerda desde sus ajustes.

## Asistente personalizado
tema: uso
alias: GPT personalizado, Gem
relacionados: instrucciones-personalizadas, asistente-de-ia

Versión de un asistente que **configuras para una tarea concreta** con instrucciones, documentos de referencia y, a veces, conexiones con otras herramientas. Por ejemplo, un asistente que corrige textos con el libro de estilo de tu empresa. Cada plataforma les da un nombre distinto y no todas las funciones están disponibles en los planes gratuitos.

## Límite de uso
tema: precios
alias: rate limit, cuota
relacionados: plan-freemium, suscripcion, inferencia
ver: /comparador/

Número máximo de mensajes, imágenes, minutos de audio o tokens que puedes usar **en un periodo de tiempo**, por ejemplo cada pocas horas o al mes. Los planes gratuitos tienen límites más bajos y los de pago los amplían. Los límites cambian con frecuencia y a veces dependen de la demanda, así que consulta siempre la página oficial de la herramienta.

## Plan de empresa
tema: precios
alias: plan Team, plan Business, plan Enterprise
relacionados: suscripcion, privacidad-de-datos
ver: /guias/ia-para-pequenas-empresas/

Planes de pago pensados para **equipos y organizaciones**. Además de más uso, suelen incluir administración centralizada de cuentas, facturación conjunta y condiciones de privacidad más estrictas, como no usar las conversaciones para entrenar modelos por defecto. Si vas a trabajar con datos de clientes, conviene leer las condiciones de cada plan antes de elegir.

## Créditos
tema: precios
relacionados: suscripcion, limite-de-uso
ver: /mejor-ia-para-video/

Unidad que usan algunas herramientas para **medir y cobrar el uso**: cada imagen, segundo de vídeo o canción generada consume una cantidad de créditos. Los planes incluyen un número de créditos al mes y a veces se pueden comprar más. Para comparar precios hay que mirar cuántos créditos gasta cada tarea, no solo cuántos incluye el plan.

## Prueba gratuita
tema: precios
relacionados: plan-freemium, suscripcion

Periodo en el que puedes **usar un plan de pago sin coste**, normalmente durante unos días. Muchas pruebas piden una tarjeta y pasan a cobrarse automáticamente si no cancelas a tiempo. Antes de empezarla, apunta la fecha de fin y comprueba cómo se cancela. No hay que confundirla con un plan freemium, que es gratuito de forma indefinida.

## Privacidad de datos
tema: etica
alias: uso de datos para entrenar
relacionados: rgpd, plan-de-empresa, ia-local, memoria
ver: /guias/privacidad-en-ia/

Lo que una herramienta de IA hace con la información que le das: si guarda tus conversaciones, durante cuánto tiempo, quién puede verlas y si **las usa para entrenar sus modelos**. Muchas herramientas permiten desactivar ese uso en los ajustes. Como norma, no compartas contraseñas, datos bancarios, de salud o datos personales de otras personas.

## RGPD
tema: etica
alias: GDPR, Reglamento General de Protección de Datos
relacionados: privacidad-de-datos, ley-de-ia-de-la-ue
ver: /guias/privacidad-en-ia/

Reglamento General de Protección de Datos de la Unión Europea, aplicable desde 2018. Protege los datos personales de quienes están en la UE y obliga a las empresas, también a las de IA, a explicar **qué datos recogen, para qué y durante cuánto tiempo**, y a respetar derechos como acceder a tus datos o pedir que se borren.

## Ley de IA de la UE
tema: etica
alias: AI Act, Reglamento de IA
relacionados: rgpd, marca-de-agua, deepfake
ver: /noticias/openai-marca-de-agua-textos-ue/

Reglamento europeo que regula la inteligencia artificial según su **nivel de riesgo**: prohíbe algunos usos, impone requisitos estrictos a los sistemas de alto riesgo y exige transparencia a otros, como avisar cuando hablas con una IA o marcar el contenido generado. Entró en vigor en agosto de 2024 y sus obligaciones se aplican de forma escalonada.

## Marca de agua
tema: etica
alias: watermark
relacionados: detector-de-ia, deepfake, ley-de-ia-de-la-ue
ver: /noticias/openai-marca-de-agua-textos-ue/

Señal, visible o invisible, que se añade a un texto, imagen, audio o vídeo **para indicar que lo ha generado una IA**. Las marcas invisibles pueden detectarse con herramientas especiales, pero suelen debilitarse si el contenido se edita, se recorta o se traduce. Que no aparezca la marca no demuestra que lo haya hecho una persona.

## Detector de IA
tema: etica
relacionados: marca-de-agua, alucinacion
ver: /guias/ia-para-estudiar/

Herramienta que intenta **estimar si un texto o una imagen los ha generado una IA**. Sus resultados son probabilidades, no pruebas: pueden marcar como artificial un texto escrito por una persona y dejar pasar otro generado y retocado. Por eso no deberían usarse como única base para acusar a nadie de copiar.

## Deepfake
tema: etica
alias: ultrafalso
relacionados: sintesis-de-voz, marca-de-agua, ia-generativa

Vídeo, imagen o audio **manipulado o creado con IA para que parezca real**, normalmente imitando la cara o la voz de una persona. Se usa en cine y humor, pero también para estafas, desinformación o para dañar la imagen de alguien. Ante un vídeo o audio sorprendente, conviene buscar la fuente original antes de creerlo o compartirlo.

## Derechos de autor
tema: etica
alias: copyright
relacionados: ia-generativa, datos-de-entrenamiento

Cuestiones legales sobre la IA y la propiedad intelectual: si las empresas pueden **entrenar sus modelos con obras protegidas** y quién es dueño de lo que genera una IA. Son debates abiertos que dependen del país y de los tribunales. En la práctica, revisa las condiciones de uso de cada herramienta, sobre todo si vas a usar el resultado con fines comerciales.

## Datos de entrenamiento
tema: etica
relacionados: entrenamiento, sesgo, derechos-de-autor, privacidad-de-datos

Conjunto de textos, imágenes, audios u otros datos con los que **se entrena un modelo**. De ellos depende lo que el modelo sabe, cómo se expresa y también sus errores y sesgos. Las empresas no suelen detallar qué datos han usado, y eso alimenta los debates sobre privacidad y derechos de autor. En la UE, desde agosto de 2025 la Ley de IA obliga a los proveedores de modelos de uso general a publicar un resumen del contenido con el que los entrenan.

## Sesgo
tema: etica
relacionados: datos-de-entrenamiento, algoritmo, alucinacion

Tendencia de un sistema de IA a **dar resultados injustos o desequilibrados** para ciertos grupos o puntos de vista. Suele venir de los datos de entrenamiento: si reflejan estereotipos o están incompletos, el modelo los reproduce. Es especialmente delicado cuando la IA se usa para seleccionar personal, conceder créditos o evaluar a personas.
