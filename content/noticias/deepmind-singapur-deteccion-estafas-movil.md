---
titulo: Google DeepMind crea con Singapur un modelo que detecta estafas en el móvil
descripcion: DeepMind y el Gobierno de Singapur desarrollan un modelo basado en Gemma que avisa de estafas por conversación sin sacar los mensajes del dispositivo.
fecha: 2026-10-14
empresa: google
herramientas: gemini
fuentes: https://deepmind.google/blog/on-device-ai-scam-detection-mddi/
---

Google DeepMind ha presentado este 14 de octubre una colaboración con GovTech Singapur, la agencia tecnológica del Gobierno del país, para construir un modelo de inteligencia artificial que **detecta estafas directamente en el teléfono** y avisa al usuario en tiempo real. La iniciativa se enmarca en la alianza nacional de IA entre Google DeepMind y el Gobierno singapurense y se dio a conocer en la Semana Internacional de la Ciberseguridad de Singapur (SICW 2026).

Es una noticia de alcance local por ahora, pero plantea una idea que afecta a cualquier país con muchas estafas por mensaje: analizar las conversaciones sin enviarlas a ningún servidor.

## Qué ha anunciado Google DeepMind

Según la publicación oficial, el punto de partida es un problema que la propia compañía describe con datos de Singapur: las estafas de inversión, las falsas ofertas de empleo y la suplantación de funcionarios suponen más de la mitad de los delitos denunciados en el país, con pérdidas superiores a 4.000 millones de dólares singapurenses desde 2019. Además, las tácticas han pasado del *phishing* simple a la ingeniería social, en la que el estafador gana confianza durante una conversación antes de pedir dinero. Esas estafas, afirma el texto, concentran hasta el 80 % de las pérdidas.

Para combatirlas, el equipo ha afinado un modelo ligero de la familia **Gemma** (los modelos abiertos de Google) con conversaciones de estafa locales: suplantaciones de instituciones públicas, bancos y personajes conocidos, además de esquemas de moda en la región. El objetivo es que distinga una charla normal de una manipulación real.

El sistema funciona en dos etapas:

1. **Un clasificador muy ligero** revisa los mensajes entrantes con un consumo mínimo de batería y descarta lo que parece inofensivo.
2. **Un modelo Gemma afinado** analiza entonces un fragmento más amplio de la conversación para confirmar la amenaza o descartar la falsa alarma.

Si detecta patrones de manipulación, muestra un aviso en el propio dispositivo que invita a parar y a no compartir datos sensibles ni dinero.

## Privacidad y garantías

El análisis se hace **íntegramente en el dispositivo**, a diferencia de los sistemas que escanean los mensajes en la nube. Google asegura que el modelo solo accede a las conversaciones con el consentimiento del usuario y según las condiciones de la aplicación donde se integre, y que ni el Gobierno de Singapur ni la propia Google pueden leerlas a través de este despliegue.

En cuanto al entrenamiento, la compañía dice que se excluyó información personal y que se usaron conjuntos de datos anonimizados procedentes de denuncias e inteligencia sobre estafas. El ajuste se realizó en un entorno de Google Cloud gestionado por GovTech, aislado de otros datos, y se probó con diálogos sintéticos y corpus locales. Todas estas afirmaciones proceden del fabricante y no hemos podido contrastarlas con una auditoría independiente.

## Por qué importa en España y Latinoamérica

Hay que ser claros: **no hay fecha ni anuncio de llegada a España ni a Latinoamérica**. El texto no menciona aplicaciones concretas, calendario de despliegue ni idiomas compatibles; solo habla de un lanzamiento «por fases» en Singapur y de que Google quiere explorar despliegues similares en otros países.

Aun así, el tema es muy cercano al lector hispanohablante. Las estafas por mensajería, la suplantación de bancos o de organismos públicos y las falsas ofertas de trabajo son habituales a ambos lados del Atlántico. Un detector local que no exige mandar los chats a un servidor es, además, el tipo de enfoque que mejor encaja con las exigencias europeas de protección de datos. Si algún día llega a nuestros mercados, habría que reentrenarlo con estafas locales y en nuestro idioma, como hizo Singapur con las suyas.

## Qué cambia en la práctica

- **Para el usuario de hoy:** nada. No hay ninguna aplicación que puedas instalar a raíz de este anuncio.
- **Para quien se preocupa por la privacidad:** es una señal de que la IA «en el dispositivo» puede servir para proteger sin vigilar. Conviene repasar nuestra [guía de privacidad en IA](/guias/privacidad-en-ia/) para saber qué datos compartes con los asistentes.
- **Para desarrolladores y empresas de seguridad:** Google presenta un patrón de arquitectura (filtro ligero más modelo de confirmación) pensado para ahorrar batería, que puede inspirar soluciones propias.

## La opinión de Radar IA

El enfoque nos parece sensato: avisar en el momento y sin que los mensajes salgan del teléfono es mejor que un filtro en la nube. Pero hoy es una promesa con pocos datos públicos: no se indican tasas de acierto, falsos positivos ni aplicaciones socias, y todo lo que sabemos viene de la propia Google. Lo seguiremos de cerca, sobre todo si se anuncian pruebas en países de habla hispana. Mientras tanto, la mejor defensa sigue siendo desconfiar de cualquiera que te pida dinero con urgencia. Si quieres saber más sobre el ecosistema de Google, tienes la [ficha de Gemini](/herramientas/gemini/).
