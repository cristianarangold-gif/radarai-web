titulo: Anthropic lanza OSS Scanner, un servicio gratuito que busca fallos de seguridad en proyectos de código abierto
descripcion: Anthropic estrena su Cyber Mission con OSS Scanner, un escáner gratuito y opcional para proyectos de código abierto. Qué ofrece, qué límites tiene y a quién afecta.
fecha: 2026-10-09
empresa: anthropic
herramientas: claude
fuentes: https://www.anthropic.com/news/anthropic-cyber-mission
    https://www.anthropic.com/news/cyber-verification-program
    https://www.theverge.com/ai-artificial-intelligence/1008521/anthropic-open-source-oss-scanner

Anthropic ha presentado esta semana la **Anthropic Cyber Mission**, un programa a largo plazo para ayudar a quienes defienden software y sistemas con herramientas, investigación y recursos. Se anunció el 8 de octubre de 2026 y su pieza más llamativa para el público general es **OSS Scanner**, un servicio gratuito que revisa proyectos de código abierto en busca de vulnerabilidades. La apuesta de la compañía es que los atacantes ya disponen de modelos muy capaces y que los defensores necesitan acceso a herramientas equivalentes.

## Qué ha anunciado Anthropic

Según la publicación oficial de la compañía, la iniciativa se centra por ahora en dos frentes:

- **OSS Scanner:** es un servicio opcional y gratuito. Los responsables de un proyecto de código abierto se inscriben y, de forma periódica, Anthropic analiza el código con sus modelos más potentes. Cada informe incluye una prueba de concepto, una explicación del problema y, a veces, una propuesta de corrección.
- **Critical Infrastructure Defense Program (CIDP):** da a proveedores de seguridad de confianza acceso a los modelos más avanzados de Claude, ingenieros desplazados in situ e investigación sobre amenazas, para proteger sistemas industriales como redes eléctricas, agua o transporte. Entre los socios fundadores figuran Accenture, Booz Allen, CrowdStrike, Deloitte, Palo Alto Networks, PwC y Rockwell Automation. Arranca con un grupo reducido de proveedores.

Anthropic advierte de un límite importante: los informes de OSS Scanner se envían **sin revisión humana**, así que algunos pueden ser incorrectos. La propia empresa dice esperar una tasa de aciertos superior al 90 %, una cifra que procede del fabricante y que no hemos podido contrastar de forma independiente.

Además, el Project Glasswing se integra en un Cyber Verification Program ampliado. Según una segunda publicación de Anthropic, este programa ofrece tres niveles de acceso para profesionales de seguridad verificados (defensa, equipos rojos y acceso especializado), todos con retención de datos para vigilar usos indebidos. Anthropic afirma que sus propios escaneos de código abierto han encontrado 5.500 vulnerabilidades más entre abril y octubre de 2026 y reconoce que probablemente es una cifra por debajo de la real.

## Por qué importa en España y Latinoamérica

Buena parte del software que usamos a diario, desde administraciones hasta pymes, depende de librerías de código abierto mantenidas por equipos pequeños o por voluntarios. Si esas librerías tienen fallos, el problema llega a todo el que las use, esté donde esté.

- **Mantenedores y desarrolladores hispanohablantes:** pueden inscribir sus proyectos sin coste, lo que supone una revisión de seguridad que antes solo estaba al alcance de quien pudiera pagar una auditoría.
- **Empresas y administraciones:** se benefician de forma indirecta si las dependencias que utilizan se revisan y corrigen antes.
- **Sector de la ciberseguridad:** los programas para proveedores y equipos de defensa interesan a consultoras y empresas de seguridad con presencia en España y América Latina, aunque los socios que cita Anthropic son sobre todo estadounidenses.

El anuncio no menciona condiciones específicas por país ni de idioma, de modo que conviene revisar los requisitos de inscripción antes de contar con ello.

## Qué cambia en la práctica

- **Si mantienes un proyecto de código abierto:** puedes inscribirlo en OSS Scanner. Recibirás informes con prueba de concepto; tendrás que verificarlos tú, porque pueden contener falsos positivos.
- **Si eres usuario final:** no cambia nada directo. El efecto, si lo hay, será que algunas aplicaciones y librerías reciban correcciones de seguridad antes.
- **Si trabajas en ciberseguridad:** puedes solicitar acceso al Cyber Verification Program. Los niveles con más capacidades exigen revisión de la organización y pueden tardar semanas.
- **Si necesitas privacidad estricta:** todos los niveles del programa requieren conservar datos para detectar abusos. Anthropic ha dicho que más adelante este otoño lanzará salvaguardas para empresas que permitirán guardar los datos en infraestructura propia.

## La opinión de Radar IA

Que un escáner de este tipo sea gratuito para proyectos abiertos es una buena noticia, porque el código abierto es una de las partes más frágiles de la seguridad informática. También nos parece sensato que Anthropic avise de que los informes pueden fallar: un aviso erróneo cuesta tiempo a un mantenedor que ya va justo. Lo que está por ver es cuánto trabajo adicional supondrá filtrar los informes y si las correcciones propuestas son fiables en la práctica. Las cifras de aciertos y de vulnerabilidades halladas son de la propia compañía, así que conviene tomarlas con cautela hasta que haya análisis independientes.

Si te interesa ver cómo encaja Claude entre otras herramientas, consulta su [ficha de Claude](/herramientas/claude/) y nuestra comparativa de [la mejor IA para programar](/mejor-ia-para-programar/). Y si te preocupa qué ocurre con tu información al usar asistentes, la [guía de privacidad en IA](/guias/privacidad-en-ia/) te ayudará a decidir qué compartir.
