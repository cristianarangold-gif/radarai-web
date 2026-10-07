titulo: IA para abogados: herramientas, prompts y deontología
descripcion: Cómo usar la IA en un despacho: analizar documentación, preparar borradores y traducir, con lo que exige el Código Deontológico y el secreto profesional.
fecha: 2026-10-07
profesion: abogados y despachos
emoji: ⚖️
kit: claude = Analizar y resumir documentación extensa | notebooklm = Trabajar solo con tus expedientes y normativa | deepl-write = Traducir documentos sin que se usen para entrenar = Individual 7,49 €/mes
fuentes: https://abogaciavasca.net/cgae-circular-interpretativa-3-2026_deontologia/
    https://www.aepd.es/guias/recomendaciones-ia-aepd.pdf

En un despacho, buena parte del tiempo se va en leer, resumir, ordenar y redactar. La inteligencia artificial generativa puede acelerar esas tareas, y el propio Consejo General de la Abogacía Española lo reconoce: en su **Circular interpretativa 3/2026** considera que usarla para elaborar borradores o textos jurídicos es **«una práctica lícita y admisible»**. Pero añade una condición clara: la IA es una función auxiliar, sujeta a supervisión humana, y delegar en ella de forma acrítica es incompatible con la deontología. En esta página reunimos las tareas en las que más ayuda, con qué herramienta hacerlas según nuestras fichas y lo que hay que vigilar.

## Tareas en las que te ayuda

### Resumir documentación extensa

Contratos, actas, informes periciales o expedientes largos son el terreno de [Claude](/herramientas/claude/), que permite subir varios archivos y pedir resúmenes, comparaciones o extracción de datos concretos. Trabaja siempre con **documentos anonimizados** (más abajo explicamos por qué) y comprueba cada referencia en el original.

> Prepara una tabla con las obligaciones de cada parte, los plazos y las penalizaciones de este contrato, con el número de cláusula en cada fila. Añade una segunda tabla con las cláusulas que se aparten de lo que suele pactarse en este tipo de contrato y el motivo, para que yo las revise.

### Preparar un primer borrador

Un correo a un cliente, una carta de requerimiento o la estructura de un escrito pueden partir de un borrador de la IA, siempre que el contenido jurídico lo revises tú. La Circular 3/2026 recuerda que estos sistemas pueden producir **contenidos incorrectos con apariencia de excelencia técnica**.

> Redacta un primer borrador de carta de requerimiento de pago amistoso para un cliente ficticio: deuda de una factura de servicios vencida hace 60 días, tono firme pero cordial, plazo de 10 días para pagar antes de iniciar acciones. Deja entre corchetes los datos que debo completar.

### Trabajar solo con tus propias fuentes

Cuando necesitas respuestas basadas exclusivamente en un conjunto de documentos (la normativa aplicable, la jurisprudencia que ya has seleccionado o la documentación de un asunto), [Gemini Notebook (antes NotebookLM)](/herramientas/notebooklm/) responde **solo con las fuentes que subes** y cita el fragmento exacto de cada respuesta. Eso no elimina los errores, pero facilita comprobar de dónde sale cada afirmación.

> Con las fuentes de este cuaderno, elabora un esquema de los requisitos que exige la normativa para este tipo de procedimiento. Para cada requisito, cita el artículo y el fragmento exacto de la fuente en el que se basa.

### Preparar una cronología de hechos

En asuntos con mucha documentación, ordenar los hechos por fecha ahorra horas. Pide a la IA una cronología a partir de los documentos (anonimizados) y contrástala con los originales.

> A partir de estos documentos, elabora una cronología de los hechos en formato tabla: fecha, hecho, documento en el que aparece y página. Si una fecha es dudosa o no aparece de forma explícita, indícalo en una columna aparte.

### Traducir documentos

Para documentos en otros idiomas, [DeepL](/herramientas/deepl-write/) mantiene el diseño original y permite fijar terminología con glosarios. Un punto importante para un despacho: según su página oficial, en los planes de pago **los datos no se emplean nunca para entrenar sus modelos** y se eliminan tras prestar el servicio. Aun así, DeepL no sustituye a un traductor profesional en textos legales de alto impacto, como reconoce nuestra ficha.

> Traduce este documento al inglés manteniendo la terminología jurídica. Al final, añade una lista con los términos que no tengan una equivalencia exacta en el derecho anglosajón y una breve explicación de cada uno.

### Preparar la explicación para el cliente

Explicar a un cliente, en lenguaje claro, en qué punto está su asunto o qué implica una cláusula es una tarea donde la IA ayuda a simplificar el texto. El contenido y las recomendaciones siguen siendo tuyos.

> Reescribe esta explicación técnica para un cliente sin formación jurídica: máximo 200 palabras, frases cortas, sin latinismos y con un ejemplo práctico. Mantén todas las condiciones y plazos que aparecen en el original.

## Precauciones en tu profesión

**Verificar siempre: es un deber deontológico.** La [Circular interpretativa 3/2026 del Consejo General de la Abogacía Española](https://abogaciavasca.net/cgae-circular-interpretativa-3-2026_deontologia/) interpreta los artículos 4.1, 10.2.e, 12.A.8 y 21.2 del Código Deontológico en relación con los escritos elaborados con IA generativa. Señala que **la falta de comprobación de un escrito confeccionado por la IA** supone una omisión del deber de diligencia, y recuerda que el artículo 21.2 exige un uso «responsable y diligente» de la tecnología. En la práctica: comprueba cada cita de normativa y jurisprudencia en la fuente oficial, porque los modelos pueden inventarlas (lo que se conoce como [alucinación](/glosario/#alucinacion)).

**Cuidado con lo que introduces.** La misma circular pide **«extremar el cuidado al decidir qué datos se le introducen»** y anuncia otra circular específica sobre confidencialidad y secreto profesional. Mientras tanto, la recomendación general de la Agencia Española de Protección de Datos es clara: su [decálogo sobre el uso de la IA](https://www.aepd.es/guias/recomendaciones-ia-aepd.pdf) aconseja no compartir datos personales ni información confidencial de la entidad, de su personal o de sus clientes, y describir un caso ficticio cuando sea posible. Anonimiza los documentos antes de subirlos.

**Las buenas prácticas de la Circular.** Además, recomienda cinco buenas prácticas que, aunque no son obligaciones deontológicas en sí, pueden ser relevantes para apreciar tu diligencia: conocer cabalmente las herramientas que usas; no utilizar nunca resultados de IA sin una lectura crítica completa; contrastar siempre con fuentes jurídicas externas fiables; usar la IA solo en materias que domines; y conservar una trazabilidad interna de cuándo y para qué la has usado.

**Elige bien el plan y la herramienta.** Las condiciones de privacidad cambian mucho entre planes. Por ejemplo, en los planes de consumo de Claude el uso de las conversaciones para entrenar depende de un ajuste que eliges tú, y en los planes de pago de DeepL los textos no se usan para entrenar. Para el despacho, valora los planes para equipos o empresas, que añaden controles de administración. Lo resumimos en la guía de [privacidad al usar IA](/guias/privacidad-en-ia/).

## Qué no conviene delegar en la IA

- **La estrategia y el consejo jurídico.** La herramienta puede ordenar información, pero no conoce al cliente ni asume responsabilidad.
- **La firma de cualquier escrito sin revisión completa**, incluidas todas las citas.
- **La valoración de pruebas y riesgos** de un asunto concreto.
- **La relación con el cliente** en decisiones importantes.

Nada de lo anterior es asesoramiento jurídico: resume lo que dicen las fuentes citadas. Ante dudas deontológicas, consulta a tu colegio profesional.

## Preguntas frecuentes

### ¿Puedo usar ChatGPT o Claude en mi despacho?

El Consejo General de la Abogacía Española considera «lícita y admisible» la IA generativa para elaborar borradores o textos jurídicos, siempre que se verifique el resultado y no se delegue de forma acrítica. La Circular 3/2026 no aborda la confidencialidad ni el secreto profesional, que deja para otra circular; mientras tanto, extrema la prudencia con los datos de clientes y consulta a tu colegio ante cualquier duda.

### ¿Puedo subir documentos de un cliente?

Con mucha prudencia. La AEPD aconseja no compartir con la IA información confidencial de clientes, y el secreto profesional te obliga. Lo más seguro es anonimizar los documentos y elegir planes con garantías de privacidad adecuadas.

### ¿Qué pasa si presento un escrito con una cita inventada por la IA?

Según la Circular 3/2026, la falta de verificación de un escrito elaborado con IA puede constituir una infracción del deber de diligencia del Código Deontológico. Comprueba siempre cada referencia en la fuente oficial.

### ¿Qué herramienta usar para analizar expedientes?

Para documentos extensos, Claude permite subir varios archivos y compararlos; para trabajar solo con un conjunto cerrado de fuentes y con citas al fragmento exacto, Gemini Notebook. Puedes compararlas en el [comparador](/comparador/?h=claude,notebooklm).
