# Valor único: «¿Funciona en España?» y el historial de precios vivos

Fecha: 2026-11-15 · Estado: pendiente de aprobación del titular

## Por qué

AdSense volvió a rechazar radarai.es el 14/11/2026 por «contenido de poco valor». Google pide
información auténtica, **mantenimiento continuo** e **interés de los usuarios**. Las dos secciones que
ninguna otra web en español tiene son «¿Funciona en España?» (26 funciones) y el historial de precios
(dos tomas, 6 y 20 de octubre; nadie lo actualiza desde entonces). Solo 2 de 35 noticias enlazan a ellas.

## Objetivos

1. Que el historial de precios se revise **cada semana** y se note («comprobado el …» reciente).
2. Pasar «¿Funciona en España?» de 26 a unas 50 funciones con fuentes oficiales.
3. Que las noticias enlacen a la fila o a la herramienta correspondiente, también las ya publicadas.

## No objetivos

- Páginas nuevas por herramienta (opción B) o la página «Cuánto cuesta la IA en España» (opción C): más adelante.
- Cambios de diseño o de estructura de la web mientras AdSense esté pendiente.

## Antiobjetivos (sería un fracaso aunque funcione)

- Publicar un precio que no es el que ve un visitante español (dólares, otro país, sin IVA).
- Una toma que diga «revisado» de una herramienta que la rutina no pudo leer.
- Rellenar «¿Funciona en España?» con estados deducidos o con prensa como fuente (regla 13).
- Que algo se publique sin que Cristian lo revise y fusione.

## Enfoques considerados

- **A. Mantenerlas vivas y ampliarlas** — elegido por Cristian. Rutina semanal de precios + tanda de
  funciones nuevas + enlaces desde las noticias. Poco riesgo y refuerza lo que ya existe.
- **B. Una página por herramienta** — descartado: muchas páginas parecidas, riesgo de «poco valor».
- **C. Página «Cuánto cuesta la IA en España»** — aplazado: se puede sumar a A después.

Para la revisión de precios se eligió la **rutina en la nube** (funciona con el Mac apagado) frente a
una tarea en el Mac. Coste aceptado: como la nube puede ver precios de otro país, **Cristian confirma
en cada PR, desde España, los precios en euros antes de fusionar**.

## Diseño

### 1. Rutina «Radar IA · Precios semanales»

- RemoteTrigger en la nube, **lunes 9:00 Madrid** (`CRON_TZ=Europe/Madrid 0 9 * * 1`), mismo entorno
  que la rutina de tuits (`env_01WHmXFpMY3bwy8J66TNZynm`), claude-sonnet-5-5, sin conectores.
- Instrucciones en `docs/rutina-precios.md` (el prompt de la rutina solo dice «lee y sigue ese archivo
  y la guía editorial»).
- Pasos:
  1. Lee la última toma de `data/tomas-precios/` y, para cada herramienta, su `fuente` oficial.
  2. Lee cada fuente con `python scripts/fetch_source.py URL` (y WebFetch si hace falta).
  3. Si la página muestra precios **en euros** para los planes individuales, los apunta.
     Si muestra otra moneda, no se puede leer o no se ven los planes, **no inventa**: copia el valor
     de la toma anterior y la marca como **no comprobada**.
  4. Escribe `data/tomas-precios/AAAA-MM-DD.json` (fecha del lunes) con todas las herramientas
     (la validación lo exige). La `nota` dice cuáles se comprobaron y cuáles **no** y conservan el
     valor anterior.
  5. Si un precio cambia, actualiza también el precio y la fecha de comprobación en la ficha de
     `content/herramientas/` (la validación exige que el precio de la última toma aparezca en la ficha).
  6. `scripts/build.py` y `scripts/check.py` deben pasar.
  7. Rama `precios/AAAA-MM-DD`, PR normal «Precios semana AAAA-MM-DD: N cambios» con una tabla
     *herramienta · plan · antes · ahora · enlace oficial*, los cambios primero, y la lista de las no
     comprobadas. Termina con: «Abre cada enlace desde España y confirma los precios en euros antes de fusionar».
  8. Notificación al móvil con el número de cambios y el enlace de la PR.
- Aunque no cambie nada, abre la PR: la toma nueva actualiza la fecha de revisión visible.
- Prohibido fusionar, hacer push a `main` o publicar.

### 2. Tanda de funciones nuevas en «¿Funciona en España?»

- La hago yo en esta sesión, en **3 PR de unas 8 funciones**, siguiendo la regla 13 (fuentes oficiales
  o archive.org, estados sin deducir, `sin_confirmar` si la fuente no nombra España/UE/EEE).
- Criterio de elección: funciones de IA de consumo que la gente busca en España (asistentes de los
  móviles, funciones de Gemini/ChatGPT/Copilot/Meta, Galaxy AI, Pixel, herramientas de imagen y vídeo),
  priorizando las que ya salen en noticias o fichas de la web. La lista exacta va en cada PR.

### 3. Enlaces desde las noticias

- Una PR que añade a las noticias ya publicadas, donde corresponda, un enlace a su fila
  (`/funciona-en-espana/#id`) o al historial de la herramienta (`/historial-de-precios/`), solo cuando la
  noticia trata justo de esa función o de ese precio. Sin cambiar el resto del texto.
- `docs/rutina-noticias.md`: reforzar que **toda** noticia sobre una función con fila, o sobre precios,
  enlace a ella.

## Lo que decide quien lo construya

- Redacción exacta de `docs/rutina-precios.md` y del prompt de la rutina.
- Qué funciones entran en cada tanda y en qué orden.
- En qué frase de cada noticia va el enlace.

## Orden

1. Rutina de precios (doc + rutina) — una PR.
2. Funciones nuevas — tres PR.
3. Enlaces en noticias y refuerzo de la rutina de noticias — una PR.
