Biblioteca de prompts de Radar IA. Cada prompt empieza con «## Título», sigue con sus metadatos
(categoria y para obligatorios; herramientas: 1–2 ids con ficha; consejo opcional) y, tras una línea
en blanco, el prompt en texto plano (15–150 palabras). Los huecos se escriben [nombre] (máximo 4 distintos).
Categorías: escribir, estudiar, trabajo, marketing, imagenes, programar, dia-a-dia, pensar.
Ver docs/superpowers/specs/2026-10-08-biblioteca-prompts-design.md.

## Responder un correo difícil
categoria: escribir
herramientas: chatgpt, claude
para: Contestar una queja o un retraso sin sonar a la defensiva.
consejo: Pega el correo original debajo del prompt, sin datos personales.

Redacta una respuesta breve y cordial a un correo de [quién escribe] que se queja de [problema]. Reconoce el problema sin excusas, explica qué ha pasado en una frase y ofrece [solución]. Tono profesional y cercano, máximo 120 palabras, y termina con una frase que invite a seguir en contacto.

## Mejorar un texto sin cambiar su sentido
categoria: escribir
herramientas: claude, deepl-write
para: Pulir un texto propio para que se lea mejor.

Revisa el texto que pego a continuación para que sea más claro y fluido, pensando en [lector]. No cambies las ideas ni añadas información nueva. Corrige errores, acorta las frases largas y elimina repeticiones. Después, enumera los tres cambios más importantes que has hecho y por qué.

## Que te examine paso a paso
categoria: estudiar
herramientas: notebooklm, chatgpt
para: Aprender preguntando en lugar de releer los apuntes.
consejo: Con Gemini Notebook, sube antes tus apuntes para que las preguntas salgan solo de ellos.

Voy a estudiar [tema] para [curso o examen]. Hazme 10 preguntas de una en una, de menor a mayor dificultad. Espera mi respuesta antes de pasar a la siguiente, corrígela explicando el error si lo hay y, al final, dime qué tres puntos debo repasar.

## Explicar un concepto con un ejemplo cotidiano
categoria: estudiar
herramientas: chatgpt, claude
para: Entender algo que en los apuntes no queda claro.

Explícame [concepto] como si tuviera [edad o nivel]. Usa un ejemplo de la vida cotidiana, evita los tecnicismos y, si tienes que usar alguno, defínelo. Termina con una pregunta corta para comprobar si lo he entendido.

## Preparar una reunión en 10 minutos
categoria: trabajo
herramientas: chatgpt, copilot
para: Llegar a una reunión con objetivos y preguntas claras.

Tengo una reunión de [duración] con [con quién] para hablar de [tema]. Prepárame un orden del día con tiempos, el objetivo principal que debería conseguir, las tres preguntas que conviene hacer y los dos posibles desacuerdos que pueden surgir, con una forma constructiva de plantear cada uno.

## Convertir notas sueltas en un informe
categoria: trabajo
herramientas: claude, notion-ai
para: Ordenar apuntes desordenados en un documento presentable.

Convierte estas notas en un informe breve para [destinatario] con estos apartados: resumen en tres líneas, situación actual, problemas detectados, propuestas y próximos pasos con responsable. Mantén los datos tal como aparecen en las notas y marca con la palabra VERIFICAR cualquier dato que no esté claro. Notas:

## Ideas para una semana de publicaciones
categoria: marketing
herramientas: chatgpt, canva-ai
para: Salir del bloqueo y planificar la semana en redes.

Propón 5 ideas de publicaciones para [red social] de [negocio o marca] dirigidas a [público]. Para cada una indica el formato, un titular de menos de 10 palabras, el mensaje principal y una llamada a la acción. Varía los formatos y evita las ofertas en más de dos publicaciones.

## Describir un producto para la tienda online
categoria: marketing
herramientas: chatgpt, claude
para: Fichas de producto claras que respondan a las dudas del comprador.

Escribe la descripción de [producto] para una tienda online. Empieza con una frase que explique para quién es y qué problema resuelve, sigue con 4 viñetas con sus características más útiles y termina con un párrafo sobre cuidados o uso. Tono [tono], máximo 150 palabras y sin exageraciones que no pueda demostrar.

## Imagen para una entrada de blog
categoria: imagenes
herramientas: midjourney, canva-ai
para: Una imagen de cabecera coherente con el tema del artículo.

Ilustración de cabecera para un artículo sobre [tema del artículo]. Estilo [estilo visual], paleta de [colores], composición horizontal con espacio libre a la izquierda para un titular, iluminación suave, sin texto ni logotipos dentro de la imagen.

## Explicar un error de programación
categoria: programar
herramientas: cursor, github-copilot
para: Entender un mensaje de error antes de tocar el código.

Tengo este error en un proyecto de [lenguaje o framework]. Explícame en lenguaje sencillo qué significa, cuáles son las tres causas más probables y cómo comprobar cada una antes de cambiar nada. Después propón la corrección mínima y explica por qué funciona. Error y fragmento de código:

## Planificar el menú de la semana
categoria: dia-a-dia
herramientas: chatgpt, gemini
para: Organizar comidas y lista de la compra en un rato.

Planifica las comidas y cenas de una semana para [número de personas] con estas preferencias: [preferencias o alergias]. Usa ingredientes de temporada, repite bases para aprovechar sobras y que ninguna receta lleve más de 30 minutos. Al final, dame la lista de la compra agrupada por secciones del supermercado.

## Ver los dos lados de una decisión
categoria: pensar
herramientas: claude, chatgpt
para: Tomar una decisión con más perspectiva y menos sesgos.

Estoy decidiendo entre [opción A] y [opción B]. Hazme primero 5 preguntas sobre mi situación, de una en una. Con mis respuestas, expón los mejores argumentos a favor de cada opción, los riesgos que estoy pasando por alto y qué información me falta para decidir. No me digas qué elegir.

## Escribir una carta de presentación
categoria: escribir
herramientas: claude, chatgpt
para: Una carta para una oferta de empleo que no suene a plantilla.
consejo: Pega debajo la oferta y tu experiencia resumida; quita teléfono, dirección y DNI.

Escribe una carta de presentación para el puesto de [puesto] en [tipo de empresa]. Relaciona tres requisitos de la oferta con logros concretos de mi experiencia, sin repetir el currículum. Tono seguro pero natural, máximo 250 palabras, y evita frases hechas como «soy una persona proactiva». Oferta y experiencia:

## Resumir un texto largo en tres niveles
categoria: escribir
herramientas: claude, chatgpt
para: Tener la idea clave, el resumen y el detalle de un mismo documento.

Resume el texto que pego en tres niveles: una frase con la idea principal, un párrafo de 80 palabras y una lista con los 7 puntos más importantes. Respeta las cifras y los nombres tal como aparecen y señala si alguna afirmación del texto no está respaldada por datos.

## Cambiar el tono de un mensaje
categoria: escribir
herramientas: chatgpt, deepl-write
para: Adaptar un mismo mensaje a otra persona o situación.

Reescribe este mensaje con un tono [tono deseado] para enviárselo a [destinatario]. Mantén toda la información y la petición principal, ajusta el saludo y la despedida, y dame dos versiones: una breve y otra algo más desarrollada. Mensaje:

## Escribir un discurso corto
categoria: escribir
herramientas: claude, chatgpt
para: Unas palabras para una celebración o una despedida.

Escribe un discurso de [duración] minutos para [ocasión]. Debe incluir una anécdota que yo te contaré, un agradecimiento sincero y un cierre emotivo pero sin dramatismo. Usa frases cortas, fáciles de decir en voz alta, y marca con una barra las pausas. Antes de escribirlo, pregúntame por la anécdota y por las personas que hay que mencionar.

## Revisar ortografía y estilo sin reescribir
categoria: escribir
herramientas: deepl-write, claude
para: Corregir errores respetando tu forma de escribir.

Revisa la ortografía, la gramática y la puntuación de este texto. No cambies mi estilo ni mis palabras salvo que sean incorrectas. Devuélveme el texto corregido y, debajo, una lista con cada corrección y la regla que se aplica, para que pueda aprender de los errores. Texto:

## Ordenar unos apuntes desordenados
categoria: estudiar
herramientas: notebooklm, claude
para: Convertir apuntes de clase en un esquema claro para repasar.

Ordena estos apuntes de [asignatura] en un esquema jerárquico con títulos, subtítulos y viñetas. No añadas información que no esté en los apuntes, pero señala con la palabra REVISAR los puntos que parezcan incompletos o contradictorios. Al final, propón tres preguntas de examen basadas solo en este contenido.

## Crear tarjetas de memoria
categoria: estudiar
herramientas: chatgpt, notebooklm
para: Repasar definiciones y datos con la técnica de las tarjetas.

Crea 20 tarjetas de memoria sobre [tema] con el formato pregunta en una línea y respuesta en la siguiente. Las preguntas deben ser concretas y tener una sola respuesta correcta. Ordénalas de lo básico a lo avanzado y marca con un asterisco las 5 más importantes para un examen de [nivel].

## Plan de estudio hasta el examen
categoria: estudiar
herramientas: chatgpt, gemini
para: Repartir el temario en los días que quedan.

Tengo el examen de [asignatura] dentro de [días] días y puedo estudiar [horas] horas al día. Reparte estos temas en un calendario realista, deja dos días al final para repasar y un día libre a la semana, y alterna temas difíciles y fáciles. Temas y dificultad de cada uno:

## Corregir una redacción en otro idioma
categoria: estudiar
herramientas: deepl-write, chatgpt
para: Aprender de los errores al escribir en un idioma que estudias.

Corrige esta redacción en [idioma] escrita por un estudiante de nivel [nivel]. Marca cada error, explica en español por qué es incorrecto y propone la forma correcta. No reescribas el texto entero: quiero aprender de mis fallos. Al final, dame tres consejos para mejorar en mi próxima redacción.

## Comprobar si has entendido un texto
categoria: estudiar
herramientas: notebooklm, claude
para: Saber si de verdad has comprendido una lectura.

Acabo de leer este texto sobre [tema]. Hazme 5 preguntas de comprensión que no se puedan responder copiando una frase literal: tienen que obligarme a relacionar ideas. Espera mis respuestas, valóralas y explícame lo que no haya entendido bien, citando el fragmento del texto en el que se apoya cada explicación.

## Preparar una exposición oral
categoria: estudiar
herramientas: chatgpt, canva-ai
para: Organizar una presentación de clase y ensayarla.

Tengo que exponer [tema] durante [minutos] minutos ante [público]. Propón una estructura con introducción que enganche, tres ideas principales con un ejemplo cada una y un cierre. Después, hazme las cuatro preguntas difíciles que me podría hacer el público para que practique las respuestas.

## Redactar un correo para pedir algo
categoria: trabajo
herramientas: chatgpt, copilot
para: Pedir un favor, un plazo o una aprobación de forma clara.

Escribe un correo para pedir a [destinatario] que [petición]. Explica el motivo en dos frases, indica qué necesito exactamente y para cuándo, y facilita que pueda decir que sí con una respuesta corta. Tono [tono] y máximo 120 palabras. Propón también un asunto claro de menos de 8 palabras.

## Priorizar la lista de tareas
categoria: trabajo
herramientas: chatgpt, notion-ai
para: Decidir por dónde empezar cuando todo parece urgente.

Esta es mi lista de tareas pendientes con sus plazos. Clasifícalas en urgentes e importantes, importantes no urgentes, urgentes no importantes y prescindibles. Propón el orden para hoy teniendo en cuenta que dispongo de [horas] horas, y dime qué podría delegar o aplazar sin consecuencias. Lista:

## Preparar una entrevista de trabajo
categoria: trabajo
herramientas: claude, chatgpt
para: Practicar las preguntas más probables antes de una entrevista.

Voy a una entrevista para [puesto] en [sector]. Hazme 8 preguntas de entrevista, incluidas dos sobre situaciones difíciles, de una en una. Espera mi respuesta, valórala del 1 al 5 con una explicación y propón cómo mejorarla con un ejemplo concreto. Al final, dime qué tres preguntas debería hacer yo a la empresa.

## Dar una mala noticia al equipo
categoria: trabajo
herramientas: claude, chatgpt
para: Comunicar un cambio difícil con claridad y respeto.

Ayúdame a comunicar a mi equipo que [mala noticia]. Prepara un mensaje que explique el motivo con honestidad, lo que cambia para cada persona, lo que no cambia y los próximos pasos. Evita los eufemismos y las promesas que no pueda cumplir. Después, anticipa las cuatro preguntas que probablemente me harán y propón una respuesta para cada una.

## Escribir un procedimiento paso a paso
categoria: trabajo
herramientas: notion-ai, claude
para: Documentar una tarea para que otra persona pueda hacerla.

Convierte esta explicación de cómo hago [tarea] en un procedimiento numerado que pueda seguir alguien nuevo en el puesto. Incluye qué se necesita antes de empezar, los pasos con verbos en imperativo, los errores habituales y qué hacer si algo falla. Marca con la palabra PREGUNTAR cualquier paso que no quede claro en mi explicación.

## Preparar una negociación
categoria: trabajo
herramientas: claude, chatgpt
para: Llegar a una negociación con argumentos y límites claros.

Voy a negociar [qué se negocia] con [la otra parte]. Ayúdame a preparar mi objetivo ideal, el mínimo aceptable, tres argumentos ordenados de más a menos fuertes, lo que probablemente pedirá la otra parte y dos concesiones que podría ofrecer sin perder mucho. Después, simula la conversación haciendo tú de la otra parte.

## Asuntos de correo para una newsletter
categoria: marketing
herramientas: chatgpt, claude
para: Encontrar el asunto que invite a abrir el correo.

Propón 10 asuntos para una newsletter de [marca] sobre [tema del envío], dirigida a [público]. Máximo 45 caracteres, sin mayúsculas sostenidas ni promesas exageradas. Agrúpalos en informativos, de curiosidad y de beneficio, y añade un texto de vista previa de una línea para los tres que consideres más claros.

## Responder una reseña negativa
categoria: marketing
herramientas: chatgpt, claude
para: Contestar una mala reseña pública con profesionalidad.

Escribe una respuesta pública a esta reseña negativa de [negocio]. Agradece el comentario, reconoce lo que haya podido fallar sin culpar al cliente, explica brevemente qué se va a hacer y ofrece un canal privado para resolverlo. Máximo 80 palabras, sin copiar frases de la reseña ni incluir datos personales. Reseña:

## Analizar a la competencia
categoria: marketing
herramientas: perplexity, chatgpt
para: Entender cómo se presentan tus competidores antes de diferenciarte.

Investiga cómo se presentan en internet tres negocios de [sector] en [zona]: su propuesta principal, a quién se dirigen, sus precios si los publican y el tono de su comunicación. Cita la fuente de cada dato. Después, propón tres formas en las que [mi negocio] podría diferenciarse sin copiar a ninguno.

## Guion para un vídeo corto de producto
categoria: marketing
herramientas: chatgpt, runway
para: Un vídeo vertical que explique un producto en pocos segundos.

Escribe un guion de 20 segundos para un vídeo vertical sobre [producto]. Primer plano con un gancho visual, después el problema que resuelve, una demostración en dos planos y un cierre con llamada a la acción. Indica para cada plano qué se ve, el texto en pantalla y la locución, si la hay.

## Encuesta para conocer a tus clientes
categoria: marketing
herramientas: chatgpt, gemini
para: Preguntar a tus clientes sin cansarles.

Diseña una encuesta de máximo 7 preguntas para clientes de [negocio] con el objetivo de [objetivo]. Mezcla preguntas cerradas y una abierta, evita las preguntas que sugieran la respuesta y ordénalas de la más sencilla a la más personal. Añade un texto de introducción de dos frases que explique para qué se usarán las respuestas.

## Ilustración para un cuento infantil
categoria: imagenes
herramientas: midjourney, canva-ai
para: Una ilustración amable y coherente para una historia.

Ilustración para un cuento infantil: [escena]. Estilo acuarela suave con contornos finos, colores cálidos y luminosos, personajes de rasgos redondeados y expresivos, fondo sencillo que no distraiga, formato vertical y sin texto dentro de la imagen.

## Fotografía de producto sobre fondo neutro
categoria: imagenes
herramientas: midjourney, canva-ai
para: Una imagen limpia para una ficha de producto o un catálogo.

Fotografía de estudio de [producto] sobre fondo [color] liso, iluminación suave lateral, sombra natural bajo el objeto, encuadre centrado con espacio alrededor, enfoque nítido en los detalles de [material], estilo de catálogo profesional y sin elementos decorativos.

## Cartel para un evento
categoria: imagenes
herramientas: canva-ai, midjourney
para: Un cartel legible para anunciar un evento.

Diseña un cartel para [evento] que se celebra en [lugar y fecha]. Jerarquía clara: nombre del evento muy grande, fecha y lugar en segundo nivel y una línea con lo que el público encontrará. Estilo [estilo], dos colores principales, mucho contraste para que se lea de lejos y un espacio libre abajo para los logotipos.

## Icono para una aplicación
categoria: imagenes
herramientas: midjourney, chatgpt
para: Explorar ideas de icono para una app o un servicio.

Icono de aplicación para [tipo de app], estilo plano y minimalista, una sola forma reconocible que represente [concepto], esquinas redondeadas, dos colores con buen contraste, fondo liso y legible incluso en tamaño pequeño. Muestra cuatro variaciones distintas de la idea.

## Retrato ilustrado para un perfil
categoria: imagenes
herramientas: midjourney, chatgpt
para: Un avatar ilustrado sin usar una foto real de nadie.
consejo: No subas fotos de otras personas para generar su retrato sin su permiso.

Retrato ilustrado ficticio de una persona [descripción general] para usar como avatar, estilo [estilo de ilustración], encuadre de hombros hacia arriba, fondo de color liso, expresión amable y colores armoniosos. Sin parecido con personas reales ni texto en la imagen.

## Escena para una presentación
categoria: imagenes
herramientas: canva-ai, midjourney
para: Una imagen de apoyo que refuerce una idea en una diapositiva.

Imagen conceptual para una diapositiva que explica [idea]. Una metáfora visual sencilla, estilo [estilo], fondo con espacio libre a la derecha para texto, paleta de [colores] y composición limpia con un solo punto de atención. Sin texto, sin logotipos y sin personas reconocibles.

## Revisar un fragmento de código
categoria: programar
herramientas: github-copilot, cursor
para: Una segunda opinión sobre legibilidad y posibles errores.

Revisa este código de [lenguaje] como lo haría un compañero con experiencia. Señala errores, casos límite sin cubrir, problemas de seguridad y partes difíciles de leer, ordenados de más a menos graves. Para cada punto, explica el riesgo y propón el cambio mínimo. No reescribas todo el código. Código:

## Escribir pruebas para una función
categoria: programar
herramientas: cursor, github-copilot
para: Cubrir una función con pruebas antes de tocarla.

Escribe pruebas unitarias en [framework de pruebas] para esta función. Cubre el caso normal, los valores límite, las entradas inválidas y cualquier comportamiento que te parezca ambiguo, que me señalarás como pregunta en lugar de suponerlo. Usa nombres de prueba que describan el comportamiento esperado. Función:

## Explicar un código que no es tuyo
categoria: programar
herramientas: claude, cursor
para: Entender un archivo heredado antes de modificarlo.

Explícame este código de [lenguaje] como si me incorporara hoy al proyecto. Primero, qué hace en dos frases; después, el flujo paso a paso, las dependencias externas y las partes frágiles o con efectos secundarios. Termina con las tres preguntas que debería hacer a quien lo escribió. Código:

## Escribir una consulta SQL
categoria: programar
herramientas: chatgpt, github-copilot
para: Obtener datos de una base de datos sin dominar SQL.

Escribe una consulta SQL para [motor de base de datos] que devuelva [qué datos necesito]. Estas son las tablas y columnas disponibles. Explica cada parte de la consulta, avisa si puede ser lenta con muchos datos y propón un índice si hace falta. No uses columnas que no aparezcan en la descripción. Tablas:

## Documentar una función
categoria: programar
herramientas: github-copilot, claude
para: Comentarios y documentación útiles, no obvios.

Escribe la documentación de esta función en el formato habitual de [lenguaje]: qué hace, parámetros con sus tipos, valor devuelto, errores que puede lanzar y un ejemplo de uso. No describas línea a línea lo que ya se lee en el código; explica el porqué de las decisiones que no sean evidentes. Función:

## Automatizar una tarea repetitiva con un script
categoria: programar
herramientas: chatgpt, cursor
para: Un pequeño script para ahorrar clics cada semana.

Quiero automatizar esta tarea que hago a mano: [tarea]. Escribe un script en [lenguaje] sencillo y comentado, que avise de lo que va haciendo y no borre ni sobrescriba nada sin pedir confirmación. Explícame cómo ejecutarlo paso a paso y cómo probarlo primero con una copia de los archivos.

## Organizar un viaje
categoria: dia-a-dia
herramientas: perplexity, gemini
para: Un itinerario realista sin pasarte horas buscando.

Organiza un viaje de [días] días a [destino] en [época del año] para [quiénes viajan]. Propón un itinerario por días con un máximo de tres actividades diarias, tiempos de desplazamiento realistas y un plan alternativo para un día de lluvia. Cita las fuentes de horarios y precios para que pueda comprobarlos, porque pueden haber cambiado.

## Escribir una reclamación
categoria: dia-a-dia
herramientas: chatgpt, claude
para: Reclamar a una empresa de forma clara y documentada.

Redacta una reclamación a [empresa] por [problema]. Incluye un resumen de los hechos con fechas, lo que solicito exactamente, el plazo razonable de respuesta y una referencia a los justificantes que adjunto. Tono firme y educado, sin amenazas. No cites leyes concretas a menos que te las indique yo.

## Presupuesto mensual del hogar
categoria: dia-a-dia
herramientas: chatgpt, gemini
para: Ordenar gastos e ingresos y ver dónde ahorrar.

Ayúdame a hacer un presupuesto mensual con estos ingresos y gastos aproximados. Agrúpalos en fijos, variables y prescindibles, calcula qué porcentaje supone cada grupo y propón tres ajustes realistas para ahorrar [cantidad o porcentaje] al mes sin eliminar lo que considero imprescindible: [imprescindibles]. Datos:

## Entender una factura o un contrato
categoria: dia-a-dia
herramientas: claude, notebooklm
para: Saber qué estás pagando o firmando, en lenguaje claro.
consejo: Tapa tu nombre, dirección y número de cliente antes de subir el documento.

Explícame en lenguaje sencillo esta [factura o contrato]. Dime qué conceptos estoy pagando o aceptando, cuáles son los plazos y las condiciones para cancelar, y qué puntos conviene preguntar a la empresa antes de firmar o pagar. Señala cualquier cosa que no se entienda bien en el documento en lugar de suponerla.

## Ideas para un regalo
categoria: dia-a-dia
herramientas: chatgpt, gemini
para: Encontrar un regalo personal sin caer en lo de siempre.

Dame 10 ideas de regalo para [persona y relación conmigo] que disfruta con [aficiones]. Presupuesto aproximado: [presupuesto]. Mezcla objetos, experiencias y algo hecho a mano, explica en una frase por qué encajaría cada idea y evita los regalos genéricos como perfumes o tazas.

## Ordenar la casa por zonas
categoria: dia-a-dia
herramientas: chatgpt, notion-ai
para: Un plan de orden y limpieza que se pueda cumplir.

Crea un plan semanal para ordenar y limpiar una casa de [tamaño] en la que viven [personas]. Reparte las tareas por días con un máximo de 30 minutos diarios, asigna tareas sencillas a cada persona y deja una tarea mensual de limpieza a fondo por semana. Preséntalo como una tabla fácil de imprimir.

## Aprender una habilidad nueva en 30 días
categoria: dia-a-dia
herramientas: chatgpt, claude
para: Un plan para empezar algo nuevo sin abandonar a la semana.

Quiero aprender [habilidad] desde cero en 30 días con [minutos] minutos al día. Diseña un plan por semanas con un objetivo semanal medible, ejercicios diarios cortos, recursos gratuitos para cada fase y una pequeña prueba al final de cada semana para comprobar mi progreso.

## Encontrar los puntos débiles de una idea
categoria: pensar
herramientas: claude, chatgpt
para: Poner a prueba una idea antes de invertir tiempo o dinero.

Actúa como un crítico exigente pero justo. Esta es mi idea: [idea]. Enumera los cinco motivos más probables por los que podría fallar, ordenados por gravedad, y para cada uno propón una forma barata de comprobar si es un problema real antes de seguir adelante. No suavices las críticas.

## Explicar algo complejo con una analogía
categoria: pensar
herramientas: claude, chatgpt
para: Aclarar tus propias ideas explicándolas de otra forma.

Explícame [concepto complejo] mediante tres analogías distintas de la vida cotidiana. Para cada una, indica en qué se parece al concepto y en qué falla la comparación, para no quedarme con una idea equivocada. Termina con la analogía que te parezca más fiel y por qué.

## Preparar los argumentos del otro lado
categoria: pensar
herramientas: claude, perplexity
para: Entender la postura contraria antes de debatir.

Sobre el tema [tema], yo defiendo que [mi postura]. Expón los tres mejores argumentos de quien piensa lo contrario, en su versión más sólida y sin caricaturizarlos, con los datos o fuentes en que suelen apoyarse. Después, dime qué parte de mi postura es más débil frente a esos argumentos.

## Detectar sesgos en un razonamiento
categoria: pensar
herramientas: claude, chatgpt
para: Revisar si una conclusión está bien fundamentada.

Analiza este razonamiento y señala posibles sesgos cognitivos, saltos lógicos o generalizaciones. Para cada problema, cita la frase concreta, explica el sesgo en lenguaje sencillo y propón cómo reformular la idea de forma más rigurosa. Si el razonamiento es sólido en algún punto, dilo también. Razonamiento:

## Resolver un problema con preguntas
categoria: pensar
herramientas: chatgpt, claude
para: Desbloquearte cuando no sabes por dónde atacar un problema.

Tengo este problema: [problema]. No me des la solución todavía. Hazme preguntas de una en una, como un buen mentor, para ayudarme a entender la causa de fondo. Cuando creas que lo tengo claro, resume lo que hemos descubierto y propón tres caminos posibles con sus ventajas e inconvenientes.

## Hacer una retrospectiva de un proyecto
categoria: pensar
herramientas: notion-ai, claude
para: Aprender de lo que salió bien y mal en un proyecto terminado.

Guíame en una retrospectiva del proyecto [proyecto]. Hazme preguntas sobre qué salió bien, qué salió mal y qué haríamos distinto, de una en una. Con mis respuestas, redacta un resumen con tres aprendizajes concretos y una acción para el próximo proyecto, con responsable y fecha.

## Escribir una biografía breve
categoria: escribir
herramientas: claude, chatgpt
para: Una presentación profesional para una web, un perfil o un evento.

Escribe tres versiones de una biografía profesional sobre mí para [dónde se publicará]: una de 30 palabras, otra de 80 y otra de 150, en tercera persona. Destaca [dos o tres logros] y mi especialidad en [especialidad], con un tono cercano y sin adjetivos grandilocuentes. Antes de escribirlas, pregúntame lo que necesites saber.
