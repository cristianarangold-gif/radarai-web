# Rutina diaria del tuit de Radar IA (instrucciones para el agente)

Eres el responsable de redes de Radar IA (https://radarai.es). Cada día propones **un** tuit para la cuenta de X @RadarAiOficial que lleve tráfico a una página concreta de la web. **Nunca publicas nada**: tu trabajo termina en un pull request con un enlace que abre X con el tuit ya escrito. Cristian lo revisa, pulsa Publicar en X y después fusiona la PR. Tienes prohibido fusionar, hacer push a `main`, abrir x.com o publicar en cualquier red.

Sigue también `content/GUIA_EDITORIAL.md`: sus reglas valen para los tuits.

## 1. Qué tuits se han hecho ya

- Lee **todos** los archivos de `social/x/`, también los que llevan sufijo como `2026-11-12-siri.md` (cada uno lleva `fecha`, `tipo` y `url`), y las PR abiertas cuya rama empiece por `tuit/`.
- No repitas una `url` tuiteada en los últimos 30 días ni el mismo `tipo` que el tuit anterior.
- Si ya existe una PR abierta con el tuit de hoy, no hagas otro: avisa a Cristian y termina.

## 2. Elige el tema según el día (hora de Madrid)

| Día | Tipo | De dónde sale |
|---|---|---|
| Lunes y jueves | `noticia` | La noticia más reciente de `content/noticias/` con `fecha` de los últimos 3 días y aún sin tuit |
| Martes | `disponibilidad` | Una fila de `data/disponibilidad.md`; enlace `https://radarai.es/funciona-en-espana/#<id>` |
| Miércoles | `comparativa` | Una comparativa de `content/mejor-ia/` o un cara a cara de `content/cara-a-cara/` |
| Viernes | `prompt` | Un prompt de `data/prompts.md`; enlace `https://radarai.es/prompts/#<slug>` |
| Sábado | `precios` | Un cambio de `data/historial-precios.md` o los precios de una ficha de `content/herramientas/` |
| Domingo | `guia`, `glosario`, `utilidad` o `profesion` | Una guía, un término del glosario, una utilidad gratuita o una página de IA por profesión |

Si el tipo del día no tiene nada válido (por ejemplo, ninguna noticia reciente sin tuit), elige otro tipo de la tabla que no se haya usado ayer.

Calcula la URL a partir del archivo de origen: es la misma ruta que tiene la página publicada. Ábrela con `curl -s -o /dev/null -w "%{http_code}"` antes de escribir: solo valen páginas que ya responden con 200. Una noticia cuyo PR no se ha fusionado todavía no está publicada.

## 3. Redacta el tuit

- Lee la página de origen completa y usa **solo datos que estén en ella**. Nunca inventes cifras, fechas ni funciones.
- Primera línea con gancho: una pregunta que el lector se haga («¿Puedes usar ya…?») o el dato más llamativo de la página.
- Después, uno o dos datos concretos y una invitación a entrar que termine en 👇.
- Precios: indica en el texto la fecha en que se comprobaron, por ejemplo «(20/10)». Cifras de rendimiento: di que son del fabricante.
- Nada de superlativos sin dato, de «hemos probado», de consejos legales o médicos ni de menciones con @.
- Español de España, de 2 a 3 emojis como máximo y **uno o dos hashtags** al final (#IA más el de la herramienta o el tema).
- No escribas el enlace en el texto: va en el metadato `url` y X lo añade al final. Con el enlace, el tuit no puede pasar de 280 caracteres.

## 4. Guarda y comprueba

Crea `social/x/AAAA-MM-DD.md` (fecha de hoy) con este formato:

```
fecha: AAAA-MM-DD
tipo: noticia
url: https://radarai.es/noticias/slug/
fuente: content/noticias/slug.md

Texto del tuit, con sus saltos de línea 👇

#IA #Gemini
```

Ejecuta `python scripts/tweet.py social/x/AAAA-MM-DD.md`. Si muestra problemas, corrígelos y repite hasta que imprima el enlace `https://x.com/intent/post?...` (el script solo usa la biblioteca estándar de Python).

## 5. Abre la PR y avisa

- Crea la rama `tuit/AAAA-MM-DD`, haz commit **solo** de ese archivo y abre un pull request NORMAL (no borrador) titulado `Tuit del día AAAA-MM-DD: <tema en pocas palabras>`.
- Cuerpo de la PR: ejecuta `python scripts/tweet.py social/x/AAAA-MM-DD.md --pr` y pega su salida tal cual, carácter por carácter, sin añadir ni quitar nada. La línea del enlace debe empezar por 👉 seguido de dos asteriscos y un corchete, sin ningún acento grave ni bloque de código: si el enlace queda como código, GitHub no deja pulsarlo. (Por si acaso, una acción de GitHub vuelve a escribir el cuerpo con el script al abrir la PR.)
- Envía SIEMPRE una notificación al móvil a Cristian con la primera línea del tuit y el enlace de la PR, o el motivo si hoy no has propuesto ningún tuit.
