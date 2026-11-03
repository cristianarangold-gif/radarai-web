---
titulo: Android activará un modo de protección reforzada contra estafas en Mensajes con Gemini
descripcion: Google Mensajes sumará un modo opcional que analiza estafas en la nube con Gemini, además de avisos al compartir pantalla y al desviar llamadas. Qué cambia y cuándo.
fecha: 2026-11-03
empresa: google
herramientas: gemini
fuentes: https://blog.google/security/new-android-scam-protections/, https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-october-2026/
---

Google ha detallado un conjunto de nuevas defensas de Android contra las estafas por móvil, que presentó el 14 de octubre de 2026 y que ha vuelto a destacar en su repaso mensual de novedades de IA publicado el 2 de noviembre. La pieza central es el **modo de protección reforzada de Google Mensajes**, un ajuste opcional que recurre a los modelos Gemini más capaces de la nube para detectar timos que se desarrollan poco a poco en una conversación.

## Qué ha anunciado Google

Según el blog oficial de seguridad de Android, el paquete incluye varias medidas:

- **Protección reforzada en Google Mensajes.** Es un ajuste que el usuario tiene que activar y que llegará «en las próximas semanas». Con él, la detección de estafas puede usar Gemini en la nube, dentro de lo que Google llama *Private AI Compute*, un espacio cifrado donde, según la compañía, los datos quedan inaccesibles incluso para ella.
- **Comprobación de enlaces con Gemini Nano.** El modelo que se ejecuta en el propio teléfono evalúa enlaces desconocidos con señales de la web en tiempo real, para pillar sitios recién creados que aún no figuran en ninguna lista negra.
- **Avisos antes de tocar un enlace** enviado desde un número que no tienes guardado, con más contexto y tiempo para pensarlo.
- **Alertas de estafa en las notificaciones de chat**, que ya existen en los Pixel y que Google quiere llevar a «cientos de millones» de móviles más gracias a acuerdos con fabricantes como Motorola, Xiaomi, OPPO, OnePlus, realme o vivo, a lo largo de este año.
- **Privacidad al compartir pantalla.** Chrome y las vistas web de Android ocultarán automáticamente los campos de contraseña y de pago durante una sesión de pantalla compartida. Se despliega este mes en Android 15 o superior.
- **Protección del desvío de llamadas.** Android impedirá que una aplicación active un desvío en segundo plano y avisará si alguien te convence de marcar un código de desvío a mano. Estará disponible desde principios de diciembre en los Pixel y otros móviles seleccionados.

Google añade que su detección de estafas en Teléfono y Mensajes ya marca más de cinco millones de llamadas y mensajes sospechosos al mes. Esa cifra, igual que las comparativas con iPhone que aparecen en el artículo (basadas en un estudio encargado por la propia Google), procede del fabricante y no hemos podido contrastarla de forma independiente.

## Por qué importa en España y Latinoamérica

Las estafas por SMS, WhatsApp y llamadas suplantando a un banco o a una empresa de mensajería son un problema cotidiano en el mundo hispanohablante. El caso más citado en el anuncio es el de Brasil, donde Google dice haber bloqueado más de tres millones de llamadas falsas de dos bancos desde junio con su sistema de «llamadas financieras verificadas». Ese sistema ya funciona con otras entidades, como Revolut. Google no menciona por ahora bancos de España ni de otros países de habla hispana, aunque invita a las entidades interesadas a sumarse mediante su documentación para desarrolladores.

Otro detalle relevante es la privacidad: la protección reforzada envía a la nube parte del análisis de los mensajes. Google asegura que se procesa de forma cifrada y aislada, pero el usuario debe saber que ese es el precio de una detección más fina, y por eso es una opción que se elige.

## Qué cambia en la práctica

- **Hay que activarlo.** Nada cambia solo: la protección reforzada es opcional y aparecerá de forma escalonada. Conviene revisar los ajustes de Mensajes cuando llegue.
- **Depende del móvil.** La parte de Gemini en la nube está pensada para Pixel 6 o posteriores, Galaxy S24 o posteriores y otros dispositivos con AICore; la comprobación de enlaces con Gemini Nano, para Pixel 10, Galaxy S26 y modelos seleccionados. Google advierte además de que algunas funciones pueden no estar disponibles en todos los países, y no ha concretado el calendario para España o Latinoamérica.
- **Lo más inmediato** es la privacidad al compartir pantalla, en Android 15 o superior, y el aviso de desvío de llamadas, desde diciembre.
- **No es sustituto del sentido común.** Nunca facilites códigos de un solo uso ni cambies datos bancarios por una llamada que no has iniciado tú.

Si te interesa saber qué pasa con tus datos cuando una IA analiza tus mensajes, tenemos una [guía de privacidad en IA](/guias/privacidad-en-ia/). Para conocer la herramienta que hay detrás, consulta la [ficha de Gemini](/herramientas/gemini/). Y si te interesa el enfoque de detección en el propio dispositivo, repasa la [noticia sobre el modelo de DeepMind y Singapur](/noticias/deepmind-singapur-deteccion-estafas-movil/).

## La opinión de Radar IA

La idea de combinar un modelo ligero en el móvil con otro más potente en la nube, solo si el usuario lo permite, nos parece un enfoque razonable: ofrece una opción real entre privacidad máxima y protección máxima. Lo que echamos en falta es concreción para nuestro mercado. El anuncio habla mucho de Brasil y de Estados Unidos, pero no dice cuándo llegarán las llamadas bancarias verificadas a España, México, Argentina o Colombia, ni si la detección de conversaciones funciona igual de bien en español. Tampoco hay datos independientes sobre cuántos timos detecta realmente el modo reforzado.

Mientras tanto, el consejo es el de siempre: activa las opciones de seguridad cuando lleguen, mantén el sistema actualizado y desconfía de cualquier mensaje que te meta prisa. La IA ayuda, pero la última barrera sigue siendo tu criterio.
