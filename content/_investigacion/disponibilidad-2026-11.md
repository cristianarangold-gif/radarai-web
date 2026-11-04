# Investigación: disponibilidad por región (4 de noviembre de 2026)

Uso interno, no se publica. Páginas oficiales leídas con `scripts/fetch_source.py` o WebFetch. openai.com bloquea la descarga directa: se leyó su copia en archive.org.

## Criterios aplicados

- «Espacio Económico Europeo» o los 27 Estados en una lista oficial cuentan como toda la UE y España.
- Una lista por idiomas no demuestra la situación de toda la UE: `ue: sin_confirmar`.
- `no` solo si la empresa excluye la región o la función se limita a una lista que no la incluye.

## Comprobaciones de lista

Con los 27 Estados de la UE y EE. UU. presentes: aplicación Gemini, Modo IA (lista principal), resúmenes con IA, Google Flow, Antigravity (FAQ), ChatGPT (países admitidos) y Claude (supported-countries, con fecha de efecto 12 de noviembre de 2026).

## Exclusiones expresas leídas

- Apple, Siri AI: «Not available in China mainland and the European Union»; nota: no estará inicialmente en la UE en iOS, iPadOS y watchOS.
- Google: Personal Intelligence, tareas en Gemini e importación de chats, excluidas del Espacio Económico Europeo.
- Google, Gemini 4 Argon en el Modo IA: su lista no incluye ningún Estado de la UE.
- Microsoft, Click to Do en el EEE: «Ask Copilot: Not available».
- OpenAI, dots en Pro: fuera del EEE, Suiza y Reino Unido.

## Correcciones tras la revisión independiente (4 de noviembre de 2026)

Leídas en el navegador, desde España:

- Google, Gemini en Chrome (support.google.com/chrome/answer/16283624): la lista de territorios incluye EE. UU. y Reino Unido y ningún Estado de la UE. Pasa de `sin_confirmar` a `no`.
- Microsoft, Recall: KB5062660, 22 de julio de 2025: «Recall is now available in the European Economic Area (EEA)». Se mantiene `si`, ahora con la fuente que lo afirma.
- Microsoft Copilot: más de 170 mercados sin lista; excepciones «como China». Los precios en euros y el selector de países no afirman disponibilidad. `es` pasa de `si` a `sin_confirmar`.
- Apple, Siri AI: la página de iOS excluye la UE; la de macOS solo excluye China continental, y la nota limita la exclusión a iOS, iPadOS y watchOS. Mac va en fila propia como `sin_confirmar`.
- OpenAI, leído directamente: dots en Pro fuera del EEE, Suiza y Reino Unido; ChatGPT en WhatsApp de vuelta al EEE (13 de julio de 2026), según el prefijo del número; lista de países con España, Francia y EE. UU.; historial del ordenador en el EEE «for Pro users» en macOS (se retira «Enterprise» de la nota).

## Descartadas o pendientes

- Copilot Vision y Copilot Actions: sin página oficial actual por región.
- Deep Research y Gemini Live: la página de ayuda no indica regiones.
- Perplexity, Canva, DeepL, Suno, Runway, ElevenLabs y GitHub Copilot: no revisadas en esta primera tanda.
- Anuncios en ChatGPT: OpenAI habla de «select regions» sin lista.
