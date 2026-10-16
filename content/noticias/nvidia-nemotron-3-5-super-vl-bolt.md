titulo: NVIDIA lanza Nemotron 3.5: un modelo abierto de 120.000 millones de parámetros y otro que cabe en 24 GB
descripcion: Super VL para agentes multimodales y Bolt 74B para ejecutar agentes en un PC con GPU. Qué ofrecen, dónde descargarlos y qué falta por confirmar.
fecha: 2026-10-16
empresa: nvidia
herramientas: perplexity
fuentes: https://blogs.nvidia.com/blog/nemotron-3-5-super-vl/

NVIDIA presentó el 15 de octubre de 2026 dos nuevos modelos abiertos de su familia Nemotron: **Nemotron 3.5 Super VL**, pensado para agentes que trabajan con texto e imágenes, y **Nemotron 3.5 Bolt**, una variante comprimida para ejecutar agentes en un ordenador con tarjeta gráfica doméstica. Se suman a Lightning, lanzado en agosto, y a Ultra, la versión para el razonamiento más exigente. Todas las cifras de rendimiento que verás a continuación proceden del fabricante y no han sido contrastadas de forma independiente.

## Qué ha anunciado NVIDIA con Nemotron 3.5

**Super VL.** Es un modelo abierto de 120.000 millones de parámetros orientado a tareas de agentes: seguir instrucciones, usar herramientas, encadenar pasos de un flujo de trabajo empresarial y entender documentos visuales como páginas web, PDF, tablas y gráficos (incluido el reconocimiento de texto en imágenes). Según NVIDIA, su precisión es comparable a la de su modelo de razonamiento más grande con aproximadamente una quinta parte de los parámetros, y llega a ofrecer hasta cinco veces más rendimiento por segundo que el siguiente modelo de su categoría, según el índice de inteligencia de Artificial Analysis. La compañía lo entrenó con unos 26 billones de tokens y lo refinó después con unos 3,8 millones de ejemplos y aprendizaje por refuerzo.

Está disponible desde ya en Hugging Face, en OpenRouter, en la comunidad ModelScope y como microservicio NIM de NVIDIA. Los pesos son abiertos y NVIDIA publica también los conjuntos de datos y las recetas de entrenamiento, lo que facilita adaptarlo. La página oficial no menciona la licencia concreta ni precios, así que conviene leer las condiciones en el repositorio antes de usarlo en un proyecto comercial.

**Bolt 74B-A9B de 24 GB.** Es el modelo para el uso cotidiano en local: investigación en la web, redacción y depuración de código. Está cuantizado de forma nativa a 2 bits, de modo que cabe en 24 GB de memoria y puede convivir con otras aplicaciones abiertas. NVIDIA afirma que es el primer modelo abierto de su clase en el banco de pruebas PinchBench y el segundo en BrowseComp. Se puede descargar ya desde Hugging Face y funciona con herramientas habituales como llama.cpp, Ollama, LM Studio, Unsloth y vLLM.

**Bolt E4B de 4 GB.** Una versión más pequeña, destinada a asistentes de voz locales, personajes interactivos e interfaces integradas en dispositivos. Llegará el 23 de octubre.

NVIDIA cita además a empresas que ya trabajan con la familia, entre ellas Atlassian (búsqueda en Jira y Confluence), CrowdStrike, Dassault Systèmes, Salesforce, Synopsys y Perplexity.

## Por qué importa en España y Latinoamérica

Que un modelo de este tamaño tenga pesos abiertos y se pueda descargar sin pasar por una API tiene una consecuencia práctica para despachos, clínicas, gestorías y pymes de habla hispana: pueden ejecutarlo en sus propios servidores o equipos y mantener los datos dentro de casa. Esto es relevante para quien debe cumplir el RGPD en Europa o las leyes de protección de datos de países como México, Colombia, Chile o Argentina. Si te preocupa qué ocurre con tu información al usar un asistente, tenemos una [guía sobre privacidad en IA](/guias/privacidad-en-ia/).

El segundo punto es el coste. Un modelo que corre en una tarjeta de 24 GB acerca los agentes locales a un público que ya tiene un PC con una GPU de gama alta, sin pagar cuotas mensuales por uso. NVIDIA vincula el lanzamiento de Bolt con los portátiles RTX Spark, que empiezan a llegar a las tiendas el 16 de octubre, y que ya analizamos en [nuestra noticia sobre RTX Spark](/noticias/nvidia-microsoft-rtx-spark-windows/). Recuerda que los precios publicados de esos equipos están en dólares y no hay confirmación de su llegada a España ni a Latinoamérica.

Por último, Super VL entiende bien documentos con tablas y gráficos, una necesidad muy común en administración, contabilidad y logística, donde abundan los PDF y las facturas escaneadas.

## Qué cambia en la práctica

- **Para un usuario sin conocimientos técnicos, casi nada por ahora.** Estos modelos no son una aplicación con botón de instalar: se descargan y se ejecutan con herramientas como Ollama o LM Studio, y exigen un equipo potente. Si buscas un asistente listo para usar, sigue siendo más sencillo recurrir a servicios como [Perplexity](/herramientas/perplexity/).
- **Para desarrolladores y equipos técnicos.** Es una opción abierta para construir agentes que usan herramientas, con datos y recetas de entrenamiento publicados y posibilidad de ajustarlo con NeMo. Super VL está disponible también en OpenRouter, lo que permite probarlo por API sin montar hardware propio.
- **Para empresas.** La combinación de pesos abiertos y despliegue propio reduce la dependencia de un único proveedor, aunque el hardware necesario para el modelo grande es de centro de datos o estaciones profesionales.
- **Cosas que faltan por saber.** NVIDIA no indica precios, la licencia exacta ni el rendimiento en español. Los resultados de PinchBench, BrowseComp y Artificial Analysis son los que cita la compañía; habrá que esperar a evaluaciones independientes, sobre todo en tareas en castellano.

## La opinión de Radar IA

Nos parece una buena noticia que un fabricante de la envergadura de NVIDIA publique no solo los modelos, sino también datos y recetas de entrenamiento: facilita que otros los examinen y los mejoren. Y la apuesta por un modelo de 74.000 millones de parámetros que cabe en 24 GB es una señal clara de hacia dónde va el sector: agentes que funcionan en el propio ordenador.

Dicho esto, conviene mantener los pies en el suelo. Las comparativas son del fabricante, el modelo grande necesita un hardware fuera del alcance del usuario medio y no hay datos sobre su rendimiento en español. Nuestro consejo: si eres desarrollador o responsable técnico de una pyme con datos sensibles, merece la pena seguirlo de cerca y esperar a las primeras evaluaciones independientes; si solo quieres un asistente para el día a día, no hay prisa en cambiar lo que ya usas.

*Fuente consultada: el anuncio oficial en el blog de NVIDIA, publicado el 15 de octubre de 2026. Las cifras de rendimiento proceden del fabricante.*
