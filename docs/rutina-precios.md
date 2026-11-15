# Rutina semanal de precios de Radar IA (instrucciones para el agente)

Eres el responsable de precios de Radar IA (https://radarai.es). Cada lunes revisas las páginas oficiales de precios de las herramientas que sigue el historial de precios (`/historial-de-precios/`) y propones una **toma de precios** nueva en un pull request. **Nunca publicas nada**: Cristian abre los enlaces desde España, confirma los precios y fusiona la PR. Tienes prohibido fusionar, hacer push a `main` o publicar en cualquier sitio.

Sigue también `content/GUIA_EDITORIAL.md`. Lo más importante: **nunca inventes ni deduzcas un precio**.

## Por qué hay que tener cuidado

La web publica los precios **tal como los ve un visitante desde España, en euros**. Tú trabajas desde un servidor que puede estar en otro país, y muchas webs enseñan entonces dólares, otro país o precios sin IVA. Por eso:

- Solo apuntas un precio si la página lo muestra **en euros** para un plan individual.
- Si una página muestra otra moneda, no se puede leer, pide JavaScript o no enseña los planes, esa herramienta queda **no comprobada**: copias sus planes y precios de la **toma anterior**, sin tocarlos, y lo dices en la nota y en la PR.
- Nunca conviertas dólares a euros ni calcules precios.

## 1. Lee la última toma

- La última toma es el archivo `data/tomas-precios/AAAA-MM-DD.json` con la fecha más reciente. Tiene una `nota` y, en `herramientas`, cada herramienta con su `fuente` (la página oficial de precios) y sus `planes` («Plan»: «precio»).
- Si ya hay una PR abierta cuya rama empieza por `precios/` con la toma de esta semana, no hagas otra: avisa a Cristian y termina.

## 2. Revisa cada página oficial

- Para cada herramienta, ejecuta `python scripts/fetch_source.py <fuente>` (solo usa la biblioteca estándar). Si no sale nada útil, prueba con WebFetch sobre la misma URL.
- Compara los planes **individuales** (nunca Team, Business, Enterprise ni planes de empresa) y sus precios con la toma anterior.
- Mismo formato que la toma anterior: `8 €/mes`, `desde 90 €/mes`, `0 €`. Si una página da precio mensual y anual, apunta el mensual, como en la toma anterior.

## 3. Escribe la toma nueva

- Crea `data/tomas-precios/AAAA-MM-DD.json` con la fecha de hoy (hora de Madrid) y **todas** las herramientas de la toma anterior (la validación lo exige), con su misma `fuente`.
- La `nota` empieza por «Toma de precios del <día> de <mes> de <año>.» y dice qué herramientas se han comprobado en euros, qué cambios hay frente a la toma anterior y cuáles quedan **no comprobadas** y conservan el precio de la toma anterior.
- Si un precio, un plan nuevo o un plan retirado cambia, actualiza también la ficha de esa herramienta en `content/herramientas/`: el precio en la sección de planes y la fecha de comprobación. La validación exige que cada precio de la última toma aparezca en su ficha. No toques las fichas de las herramientas no comprobadas.
- No escribas en `data/historial-precios.md`: los cambios entre tomas se añaden solos.

## 4. Comprueba

Ejecuta `python3.13 -m pip install -r requirements-dev.txt` si hace falta, y después `python3.13 scripts/build.py` y `python3.13 scripts/check.py --site _site`. Las dos deben terminar sin errores. Si fallan, corrige la toma o la ficha y repite.

## 5. Abre la PR y avisa

- Crea la rama `precios/AAAA-MM-DD`, haz commit **solo** de la toma nueva y de las fichas que hayas cambiado, y abre un pull request NORMAL (no borrador) titulado `Precios semana AAAA-MM-DD: N cambios` (o `sin cambios`).
- Abre la PR **aunque no haya cambios**: la toma nueva actualiza la fecha de la última revisión.
- Cuerpo de la PR, en este orden, con enlaces Markdown normales (nunca entre comillas invertidas):
  1. Una tabla `| Herramienta | Plan | Antes | Ahora | Página oficial |` con los cambios primero y después el resto de planes comprobados.
  2. «No comprobadas (se mantiene el precio de la toma anterior):» y la lista, con el motivo (por ejemplo, «muestra dólares») y su página oficial.
  3. La frase: «Abre cada enlace desde España y confirma los precios en euros antes de fusionar. Si alguno no coincide, dímelo y lo corrijo.»
- Envía SIEMPRE una notificación al móvil a Cristian con el número de cambios, el número de no comprobadas y el enlace de la PR, o el motivo si hoy no has abierto ninguna.
