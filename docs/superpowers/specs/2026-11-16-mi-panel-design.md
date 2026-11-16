# «Mi panel»: herramientas personales sin cuenta

Fecha: 2026-11-16 · Estado: pendiente de aprobación del titular

## Por qué

Cristian quiere un servicio para los visitantes: controlar las IA que pagan, ver un calendario de
cobros, guardar prompts y apuntar notas, ideas y proyectos. Se descartaron las cuentas de usuario
(Google no ve lo que hay tras un inicio de sesión, obligaciones legales por guardar datos personales,
la web es estática y hoy el tráfico es bajo). Se eligió una versión **sin cuenta**: los datos viven en
el navegador del visitante. Además suma «valor único» para AdSense: herramientas públicas y útiles.

## Objetivos

1. Página pública e indexable `/mi-panel/` con texto que explica cómo usarla.
2. **Mis IA:** lista de suscripciones (herramienta, plan, precio, ciclo mensual o anual, día de cobro).
   Se puede elegir una herramienta de nuestras fichas y el plan y precio se rellenan con la última toma
   de precios; también se puede escribir una IA que no tengamos.
3. **Aviso de cambio de precio:** si el precio guardado de una herramienta nuestra no coincide con el de
   la última toma, se avisa («Según nuestra revisión del 16 de noviembre de 2026 ahora cuesta X») con
   enlace a `/historial-de-precios/#precios-<id>`. Nunca cambia el dato del usuario por su cuenta.
4. **Calendario de pagos:** cobros del mes en curso y del siguiente, y un botón «Añadir a mi calendario»
   que descarga un archivo `.ics` con un evento repetido por suscripción (vale para Google Calendar,
   el calendario del iPhone y Outlook).
5. **Calculadora de gasto:** total al mes y al año, y desglose por herramienta.
6. **Prompts guardados:** botón «Guardar en mi panel» en el generador de prompts, el mejorador de prompts
   (y el resto de utilidades que generan prompts) y en cada prompt de `/prompts/`. En el panel se pueden
   editar, copiar y borrar.
7. **Notas, ideas y proyectos:** notas con título y texto, agrupadas por proyecto.
8. **Copia de seguridad:** exportar todo a un archivo `.json` e importarlo (para no perderlo o pasarlo a
   otro dispositivo). Aviso visible: si se borran los datos del navegador sin copia, se pierden.
9. Enlace a `/que-ia-necesito/` (el test «¿qué IA me conviene?» ya existe; no se duplica).

## No objetivos

- Cuentas de usuario, sincronización entre dispositivos, boletín por correo, recordatorios por correo
  o notificaciones del navegador.
- Rediseñar la web o el menú mientras AdSense esté en revisión: solo se añaden una página y enlaces.

## Antiobjetivos

- Enviar a cualquier servidor (ni al nuestro ni a terceros) lo que el visitante escribe.
- Perder datos por un error: los datos se guardan con un número de versión y la importación valida
  el archivo antes de sustituir nada (y pide confirmación).
- Precios inventados: el autocompletado solo usa la última toma de `data/tomas-precios/`.

## Enfoques considerados

- **A. Panel en el navegador, sin cuenta** — elegido por Cristian.
- **B. Cuentas con usuario y contraseña** — descartado por ahora (coste legal, seguridad, poco tráfico).
- **C. Solo boletín** — descartado por ahora; el boletín queda para más adelante.

## Diseño

- **Página:** `content/paginas/mi-panel.md` (texto explicativo indexable) + plantilla
  `templates/panel.html` (el panel arriba, con pestañas: Mis IA · Pagos y gasto · Prompts · Notas ·
  Copia de seguridad) + `static/js/panel.js`, sin librerías externas.
- **Datos de precios:** `scripts/build.py` genera `/mi-panel/precios.json` desde la última toma:
  `{fecha, herramientas: {id: {nombre, ficha, planes: {plan: {texto, euros, ciclo}}}}}`. Solo planes con
  importe en euros; «desde X» se ofrece con su importe mínimo y se indica.
- **Almacenamiento:** `localStorage`, clave `radar-panel`, objeto `{version: 1, suscripciones, prompts,
  notas, proyectos}`; todo dentro de `try/catch`: si el navegador no deja guardar, la página lo dice y
  sigue funcionando en esa visita.
- **Botones «Guardar en mi panel»:** en `static/utilidades/app.js` (utilidades que generan prompts) y en
  la biblioteca de prompts (`static/js/library.js` o `prompts.js`). Guardan y muestran «Guardado ✓» con
  enlace al panel.
- **Archivo `.ics`:** generado en el navegador; un `VEVENT` por suscripción con `RRULE` mensual o anual,
  título «Cobro de <IA> (<plan>)» e importe en la descripción.
- **Privacidad:** párrafo nuevo en la política de privacidad: «Mi panel» guarda los datos solo en el
  navegador del visitante; Radar IA no los recibe. Cristian revisa ese texto.
- **Enlaces:** desde el generador y el mejorador de prompts, `/prompts/`, `/historial-de-precios/`,
  la página de utilidades y el pie de página.

## Pruebas

- Python (`pytest`): la página existe y es indexable; `precios.json` sale de la última toma y solo trae
  importes en euros; las utilidades y la biblioteca cargan el botón de guardar; la política de privacidad
  menciona «Mi panel».
- Navegador (vista previa local): añadir y borrar una suscripción, aviso de cambio de precio, total
  mensual y anual, descargar el `.ics`, guardar un prompt desde el generador y desde `/prompts/`, notas
  por proyecto, exportar e importar, móvil y modo oscuro.

## Lo que decide quien lo construya

- Diseño visual dentro del estilo actual, textos de la página y orden exacto de las pestañas.

## Orden (partes con su PR)

1. Página, almacenamiento, Mis IA, aviso de precio, pagos y calculadora, `.ics`, copia de seguridad.
2. Prompts guardados (botones en utilidades y biblioteca) y notas por proyecto.
3. Enlaces desde otras páginas y párrafo de privacidad.
