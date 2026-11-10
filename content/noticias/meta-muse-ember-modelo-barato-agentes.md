titulo: Meta presenta Muse Ember, un modelo de IA muy barato para agentes
descripcion: Meta lanza Muse Ember, su modelo más pequeño: 0,10 dólares por millón de tokens de entrada, entradas multimodales y pensado para agentes de programación.
fecha: 2026-11-10
empresa: meta
fuentes: https://dev.meta.ai/resources/blog/build-with-muse-ember
    https://hipertextual.com/inteligencia-artificial/muse-ember-ia-programar-meta/

Meta presentó el 9 de noviembre de 2026 Muse Ember, el modelo más pequeño y eficiente de su familia Muse. No compite por ser el más listo, sino el más barato para el trabajo repetitivo que hace un agente de IA cuando programa o procesa documentos. Está disponible desde ese mismo día en Muse Code y en la API de modelos de Meta.

## Qué ha anunciado Meta

Según el blog para desarrolladores de la compañía, Muse Ember está pensado para tareas acotadas y repetidas muchas veces: subtareas de programación, llamadas a herramientas, enrutado de peticiones y extracción o resumen de documentos. Admite como entrada texto, imágenes, audio y vídeo, de modo que un agente puede leer capturas de pantalla, documentos escaneados o grabaciones sin recurrir a otro modelo. Hipertextual añade que acepta hasta un millón de tokens de entrada y puede generar hasta 512.000, dato que no hemos podido contrastar en la página oficial que hemos leído.

Meta lo posiciona como complemento de los modelos grandes de la familia. La idea es que Muse Wonder o Muse Spark planifiquen y supervisen, y que Ember ejecute las partes sencillas en paralelo. Como ejemplo, la empresa describe una migración de 16 analizadores léxicos de la librería Pygments de Python a Rust con varios agentes pequeños coordinados por un modelo grande.

El precio es el gran reclamo: 0,10 dólares por millón de tokens de entrada y 0,50 por millón de salida para peticiones de hasta 200.000 tokens de entrada; por encima de ese tamaño, 0,30 y 1,50. Además, está incluido en todos los planes de suscripción de Muse Code.

En rendimiento, Meta compara Ember con Claude Haiku 5.5 y GPT-6 Luna. Según sus propias cifras, obtiene 40,9 puntos en Terminal-Bench 4.0 frente a 39,2 de Haiku y 16,4 de Luna, y 37,8 en AutomationBench-AA frente a 13,9 y 20,2. Sin embargo, en FrontierCode 2.0-AA queda por debajo de Haiku (27,2 frente a 34,9). Todas las cifras proceden del fabricante y los resultados varían según la prueba, así que conviene leerlas como orientativas y no como un veredicto general.

## Por qué importa en España y Latinoamérica

Los modelos pequeños y baratos son los que hacen viables los agentes en proyectos con presupuesto ajustado: una pyme, una startup o un desarrollador independiente de cualquier país de habla hispana puede lanzar cientos de llamadas por tarea sin que la factura se dispare. Por eso la guerra de precios en este segmento importa más que otro récord en un benchmark.

Pero hay incógnitas que afectan a nuestro público. En el blog oficial que hemos leído no consta si Muse Code y la API de Meta están disponibles en la UE o en cada país de Latinoamérica, ni cómo se tratan los datos que se envían, ni hay precios en euros. Tampoco conocemos el rendimiento del modelo en español. Hasta que Meta lo aclare, conviene comprobarlo antes de integrarlo en un producto con clientes europeos.

## Qué cambia en la práctica

- **Para desarrolladores:** hay una nueva opción económica para subagentes. Conviene medir coste y calidad en tu propio caso antes de sustituir un modelo que ya uses; en [la mejor IA para programar](/mejor-ia-para-programar/) tienes las alternativas actuales.
- **Para equipos con agentes:** el esquema «un modelo grande planifica, uno pequeño ejecuta» abarata flujos largos, aunque exige definir bien qué recibe y devuelve cada tarea. Nuestra guía para [automatizar tareas](/guias/automatizar-tareas/) ayuda a decidir qué delegar.
- **Para el usuario de a pie:** no hay un cambio directo; Ember es un modelo para desarrolladores, no una nueva app.
- **Para quien se preocupa por los datos:** revisa las condiciones de la API y repasa la [guía de privacidad en IA](/guias/privacidad-en-ia/) antes de enviar documentos con información sensible.

## La opinión de Radar IA

El movimiento tiene sentido: la parte del trabajo de un agente que más se repite es también la que menos necesita un modelo gigante, y ahí es donde el precio manda. Que Meta publique una comparación que incluye un resultado desfavorable (FrontierCode) hace la información algo más creíble que la típica tabla donde todo sale a favor.

Aun así, es una comparativa hecha por la propia empresa, con configuraciones de máximo esfuerzo y pruebas de su elección. Nuestra recomendación es esperar a evaluaciones independientes y, si te interesa, probarlo con una tarea real y acotada. Y, como siempre con servicios de terceros, comprueba disponibilidad en tu país y tratamiento de datos antes de apostar por él en producción.

Este artículo se basa en el blog oficial de Meta para desarrolladores y en la cobertura de Hipertextual a fecha de 10 de noviembre de 2026. Las cifras de precio y rendimiento proceden del fabricante.
