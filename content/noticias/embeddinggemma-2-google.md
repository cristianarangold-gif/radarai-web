titulo: Google lanza EmbeddingGemma 2, un modelo abierto que entiende texto, imagen, audio y vídeo
descripcion: EmbeddingGemma 2 es gratuito, de licencia Apache 2.0 y cabe en un móvil. Te contamos qué ofrece, dónde descargarlo y para quién tiene sentido.
fecha: 2026-10-07
empresa: google
herramientas: gemini, huggingface
fuentes: https://deepmind.google/blog/embeddinggemma-2-an-open-lightweight-multimodal-embedding-model/
    https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/

Google ha presentado **EmbeddingGemma 2**, un modelo de código abierto que convierte texto, imágenes, audio y vídeo en representaciones numéricas comparables entre sí. Se anunció el 6 de octubre de 2026 y ya se puede descargar. No es un chatbot ni un asistente: es una pieza técnica que sirve de base para buscadores y sistemas de recuperación de información, y su interés está en que es lo bastante pequeño para funcionar en un móvil.

## Qué ha anunciado Google

Los *embeddings* son la tecnología que permite buscar por significado en lugar de por palabras exactas: por ejemplo, encontrar una foto describiéndola, o localizar el párrafo de un documento que responde a tu pregunta. Según el blog oficial de Google, estas son las claves de la segunda versión:

- **Multimodal:** procesa texto, imágenes, audio y vídeo en un mismo espacio, de modo que se pueden buscar unos contenidos a partir de otros.
- **Tamaño contenido:** el modelo completo tiene 740 millones de parámetros y la parte solo de texto, 270 millones. Está construido sobre la arquitectura de Gemma 4.
- **Más contexto:** admite hasta 8.000 *tokens* de entrada, cuatro veces más que la primera versión.
- **Poca memoria:** Google indica un uso de unos 191 MB de RAM en la versión de texto y unos 567 MB en la multimodal, medidos en un Pixel 11 Pro.
- **Vectores ajustables:** las dimensiones se pueden reducir de 768 hasta 128, lo que según la compañía permite ahorrar hasta seis veces en almacenamiento.
- **Licencia Apache 2.0**, que permite el uso comercial.

Google asegura que ofrece el mejor rendimiento de su categoría de tamaño en pruebas como MTEB y MAEB, que mejora casi diez puntos en tareas de código respecto a su predecesor y que supera a algunos modelos especializados del doble de tamaño. Son cifras publicadas por el propio fabricante y no las hemos verificado de forma independiente.

## Dónde conseguirlo

El modelo está disponible en Hugging Face y en Kaggle, y Google anuncia que llegará próximamente al catálogo Model Garden de su plataforma empresarial. Es compatible con herramientas habituales entre desarrolladores como transformers, sentence-transformers, MLX, vLLM, llama.cpp, Ollama y LM Studio.

## Por qué importa en España y Latinoamérica

La principal ventaja de un modelo así es que puede funcionar **en el propio dispositivo**, sin enviar datos a ningún servidor. Eso tiene un valor práctico claro en nuestro entorno:

- **Privacidad y cumplimiento normativo:** una empresa española o europea que quiera buscar en documentos internos, contratos o historiales sin sacar información de su infraestructura tiene aquí una opción más sencilla de justificar.
- **Coste:** al ser gratuito y ligero, reduce la barrera para startups, pymes y desarrolladores independientes de toda Latinoamérica que no pueden asumir facturas de API por cada consulta.
- **Conexiones irregulares:** un buscador que funciona sin conexión resulta útil en zonas con cobertura limitada.

El anuncio no destaca resultados específicos para español, así que conviene probarlo con textos propios antes de apostar por él.

## Qué cambia en la práctica

- **Si eres usuario final:** de momento, nada directo. No es una aplicación, aunque podrías notarlo en el futuro en buscadores o asistentes que lo integren.
- **Si desarrollas:** puedes descargarlo hoy y probarlo en un sistema de búsqueda semántica o de respuesta sobre documentos, sin pagar licencias.
- **Si ya usas la versión anterior:** merece la pena evaluar el salto, sobre todo por el contexto de 8.000 *tokens* y la compatibilidad con imagen, audio y vídeo.
- **Si trabajas con asistentes como Gemini:** este modelo no sustituye a la familia Gemini; es un componente complementario para tareas de recuperación de información.

## La opinión de Radar IA

Estas noticias no suelen aparecer en portadas, pero son las que más influyen en que las aplicaciones de IA sean rápidas, privadas y baratas. Que Google ofrezca un modelo multimodal con licencia permisiva y con un consumo de memoria tan bajo es una buena noticia para quien quiera construir herramientas propias. Eso sí, las comparativas de rendimiento vienen de la compañía y no sabemos cómo se comportará con textos en español; habrá que esperar a pruebas independientes. Para el usuario no técnico, el efecto será indirecto y llegará a través de las aplicaciones que lo incorporen.

Si quieres saber qué ofrece la familia de modelos de la compañía, consulta nuestra [ficha de Gemini](/herramientas/gemini/); para elegir un asistente de uso diario, tienes la comparativa de [la mejor IA para productividad](/mejor-ia-para-productividad/).
