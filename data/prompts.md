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
