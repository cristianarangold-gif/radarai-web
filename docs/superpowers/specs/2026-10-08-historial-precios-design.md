# Radar IA — Historial de precios

Fecha: 2026-10-08 · Rama: `historial-precios` · Maqueta: `_preview/maquetas/13-historial-precios.html` (fuera del repo), opción **A** · Proyecto «Secciones nuevas», parte 6 de 6.

## 1. Objetivo

Una página `/historial-de-precios/` que cuenta **cómo han cambiado los precios de los planes individuales** de las 15 herramientas con ficha desde enero de 2023: subidas, bajadas, planes nuevos, planes retirados y cambios de condiciones. Cada cambio lleva fecha y fuente.

**Decisiones del titular:**
- **A + B:** tomas propias fechadas desde ahora, más los cambios pasados investigados.
- **Fuentes:** oficial, copia archivada de la web oficial (web.archive.org) o prensa reconocida. Nunca webs comerciales de seguimiento de precios.
- **Alcance:** planes individuales (gratis y de pago para una persona), sin planes de empresa, desde enero de 2023.
- **Formato A:** línea de tiempo «Últimos cambios», un bloque por herramienta con gráfico y un recuadro en cada ficha.

**Criterio de éxito:**
- **Cobertura:** las 15 fichas tienen bloque, con precio actual y cambios. Si no hay cambios verificables, se dice claramente.
- **Trazabilidad:** cada cambio tiene fecha y una fuente de un dominio permitido. El build falla si no.
- **Coherencia:** los precios de la última toma coinciden con las fichas. El build falla si no.
- **Revisiones futuras:** una toma nueva con precios distintos añade sola los cambios a la línea de tiempo.
- **Sin JS:** la página funciona sin JS (gráficos SVG generados en el build) y se ve bien a 375 y 1440 px.
- **Verde:** pasan los tests, el build y `check.py`.

## 2. Datos

### 2.1 Cambios pasados: `data/historial-precios.md`

Las líneas con `|` son cambios; el resto (comentarios, líneas en blanco) se ignora. Una línea por cambio, con siete campos:

```
fecha | herramienta | tipo | plan | precio | frase | fuente
2025-11 | chatgpt | nuevo | Go | 9,99 €/mes | ChatGPT Go llega a España. | https://www.xataka…
2026-08 | chatgpt | baja | Go | 9,99 €/mes → 8 €/mes | Go baja de precio en España. | https://web.archive.org/web/2026…/https://chatgpt.com/es-ES/pricing/
2025-06-16 | cursor | condiciones | Pro | 20 $/mes | Mismo precio, pero pasa de 500 peticiones rápidas a 20 $ de uso. | https://cursor.com/blog/june-2025-pricing
```

- **fecha:** `AAAA-MM` o `AAAA-MM-DD`, entre `2023-01` y la fecha del build.
- **herramienta:** id de una ficha indexable.
- **tipo:**

  | tipo | Etiqueta | precio |
  |---|---|---|
  | `sube` | ↑ Subida | obligatorio, `antes → después` |
  | `baja` | ↓ Bajada | obligatorio, `antes → después` |
  | `nuevo` | ＋ Plan nuevo | obligatorio, un valor |
  | `retirado` | − Plan retirado | opcional, un valor |
  | `condiciones` | ≈ Condiciones | opcional, un valor |

- **Valor de precio:** `[desde ]N[,NN] €|$[/mes|/año]`, por ejemplo `8 €/mes`, `desde 103 €/mes` o `110 €/año`.
  - En `sube` y `baja`, si las dos cifras tienen la misma moneda y periodo, el sentido debe cuadrar: «sube» exige después > antes.
- **plan:** nombre del plan tal como lo usa la empresa (Go, Plus, Pro…), sin planes de empresa (Business, Team, Enterprise). Se rechaza un plan que contenga esas palabras.
- **frase:** 30 palabras como máximo, sin las frases de `FORBIDDEN`.
- **fuente:** URL `https://` de un dominio permitido:
  - **oficial:** el dominio de `web` o de `fuentes` de la ficha (y sus subdominios), más `OFFICIAL_EXTRA`, por ejemplo `chatgpt: openai.com`, `claude: anthropic.com`, `gemini: blog.google`;
  - **archivo:** `web.archive.org`, y la URL archivada debe ser de un dominio oficial de esa herramienta;
  - **prensa:** lista cerrada `PRESS` en el código (xataka.com y sus variantes, genbeta.com, techcrunch.com, theverge.com, ocu.org, elpais.com, eldiario.es, reuters.com, arstechnica.com, engadget.com).

  Ampliar las listas `OFFICIAL_EXTRA` y `PRESS` es un cambio de código revisable, no un dato.
- **Duplicados:** se rechazan las líneas con los mismos fecha, herramienta, plan y tipo.

### 2.2 Tomas propias: `data/tomas-precios/AAAA-MM-DD.json`

```json
{"herramientas": {
  "chatgpt": {"fuente": "https://chatgpt.com/es-ES/pricing/",
              "planes": {"Gratis": "0 €", "Go": "8 €/mes", "Plus": "23 €/mes", "Pro": "desde 103 €/mes"}}
}}
```

- **Nombre del archivo:** la fecha de la revisión.
- **Primera toma:** `2026-10-06.json`, a partir de `content/_investigacion/precios-2026-10.md` y las fichas.
- **Última toma** (la de fecha mayor):
  - cubre todas las fichas indexables;
  - cada importe (`prices_in`) aparece en el texto de su ficha (`ficha_text`). El error nombra la herramienta y el precio.
- **Todas las tomas:** valores con el formato de 2.1, fuente oficial y planes individuales.

### 2.3 Cambios automáticos entre tomas

Para cada par de tomas consecutivas, y para cada herramienta y plan:

| Situación | Cambio |
|---|---|
| El plan aparece | `nuevo` |
| El plan desaparece | `retirado` |
| Otro precio, misma moneda y periodo | `sube` o `baja` |
| Otra moneda o periodo | `condiciones` («pasa de X a Y») |

- **Fecha:** la de la toma nueva.
- **Frase:** «Detectado en nuestra revisión del 6 de enero de 2027».
- **Fuente:** la de la toma nueva.
- **Sin duplicar:** si el archivo de cambios ya tiene ese cambio (misma herramienta, plan y tipo, y la fecha en el mismo mes), no se duplica.

### 2.4 Módulo `radar/price_history.py`

- `parse_history(text) -> List[Change]` y `load_snapshots(dir) -> List[Snapshot]`
- `validate_history(changes, snapshots, fichas, today)`: los errores empiezan por `historial-precios.md:` o `tomas-precios/<archivo>:` y nombran la línea o la herramienta.
- `auto_changes(snapshots) -> List[Change]`
- `history_context(changes, snapshots, compare_by_id) -> dict`:
  - `latest` (fecha);
  - `count`;
  - `recent`: los 10 cambios más recientes;
  - `tools`: en el orden del catálogo, con `id`, `nombre`, `url`, `planes` actuales, `changes` (más recientes primero) y `chart`;
  - `by_tool`: para el recuadro de las fichas.
- **Gráfico** (`chart`): el plan con más puntos de precio distintos, con al menos 2 puntos en la misma moneda y periodo; si empatan, el primero de la última toma.
  - **Puntos:** los precios de `nuevo`, `sube` y `baja` y de las tomas.
  - **Dibujo:** escalones, eje de enero de 2023 a la fecha de la última toma, años marcados y etiqueta en cada punto.
  - Se genera como datos (coordenadas ya calculadas) y la plantilla pinta el SVG.
  - Sin 2 puntos válidos, no hay gráfico.

## 3. Página `/historial-de-precios/`

- **Contenido:** `content/paginas/historial-de-precios.md` (título, descripción y unas 300 palabras propias):
  - cómo recogemos los datos;
  - qué fuentes aceptamos;
  - por qué hay precios en € y en $ (la empresa factura en dólares);
  - el precio final puede variar con impuestos y país;
  - cómo avisarnos de un cambio, en contacto.
- **Plantilla:** `templates/price_history.html`, con `template_for` en `radar/render.py`. El build exige los datos si existe la página, como `/prompts/`.
- **Cabecera:** eyebrow «Historial de precios», h1 «Cómo han cambiado los precios *de la IA*», entradilla y línea con la fecha de la última revisión, las herramientas y los cambios registrados.
- **«Últimos cambios»:** `ol` en línea de tiempo con los 10 más recientes. Cada cambio muestra:
  - la fecha en palabras («noviembre de 2025» o «3 de noviembre de 2025»);
  - la etiqueta de color;
  - el logo y el nombre de la herramienta;
  - el plan y el precio;
  - la frase;
  - «Fuente: dominio» (enlace `rel="nofollow noopener"`; para archive, «copia archivada de dominio»).
- **«Por herramienta»:** una `section` por herramienta con `id="precios-<id>"` y `h3`. Contiene:
  - una línea «Hoy: Gratis 0 € · Go 8 €/mes…»;
  - el SVG con `role="img"` y `aria-label` («Precio del plan Go por fecha: 9,99 €/mes en noviembre de 2025, 8 €/mes en agosto de 2026»);
  - la lista de todos sus cambios, o «Sin cambios de precio verificables desde enero de 2023»;
  - «Ficha de X →».
- **Texto de la página:** al final, en `.prose`.
- **CSS:** sección «21. Historial de precios» en `radar.css`. Etiquetas de color con contraste AA y el texto de la etiqueta siempre visible (no solo color).

## 4. Enlaces y buscador

- **Ficha** (`templates/tool.html`, columna lateral): recuadro «Historial de precios» con los 2 cambios más recientes y «Ver todos los cambios →» (a `/historial-de-precios/#precios-<id>`). Si no hay cambios: «Sin cambios registrados desde 2023».
- **Buscador:**
  - una entrada por herramienta: `k='Precios'`, título «Historial de precios de X», `u=/historial-de-precios/#precios-<id>`, `d` con el precio actual y `x` con los planes y las frases;
  - filtro «Precios» en `search.js`.
- **Pie de página:** «Historial de precios», solo si existe la página.
- **`data/empieza.json`:** extra del paso 5 («Compara antes de pagar…»).
- **Comparativa** `mejor-ia-gratis.md`: un párrafo con enlace.
- **`check.py`:** `_anchor_missing` cubre `/historial-de-precios/#`.
- **`GUIA_EDITORIAL.md`:** regla 12, «cuando cambie un precio en una ficha, añade una toma nueva en `data/tomas-precios/` con la fecha de la revisión y su fuente».

## 5. Investigación (parte 2)

- **Qué se busca:** los cambios de los planes individuales de las 15 herramientas, de 2023 a hoy, en las fuentes permitidas.
- **Cada cambio:** se comprueba abriendo la fuente. Para copias archivadas, se enlaza la captura concreta.
- **Lo dudoso o contradictorio no entra.**
- **Revisión del titular:** la lista se enseña antes de pasar a la parte 3.

## 6. Tests

`tests/test_price_history.py`:
- **Lectura:** parseo de líneas y comentarios.
- **Errores**, cada uno con su `needle`:
  - fecha mala, fecha futura o anterior a 2023;
  - herramienta sin ficha;
  - tipo desconocido;
  - precio con formato malo;
  - `sube` con importe menor;
  - `sube` sin flecha;
  - plan de empresa;
  - frase larga o con «hemos probado»;
  - fuente de dominio no permitido;
  - archive de otro dominio;
  - duplicado;
  - toma sin una ficha;
  - precio de la toma que no está en la ficha.
- **Cambios automáticos:** sube, baja, nuevo, retirado, moneda distinta y sin duplicar.
- **Gráfico:** solo con 2 o más puntos, con la misma moneda y el orden por fecha.
- **Build real:** 15 secciones, ids, recuadro en las fichas, entradas del buscador, pie y empieza.
- **Datos reales:** validación del contenido real, la página indexable y al menos 250 palabras.

## 7. Partes

1. **Datos y validación:** módulo, formato, primera toma, tests de reglas.
2. **Investigación:** `data/historial-precios.md` con fuentes, y revisión del titular.
3. **Página:** plantilla, gráfico, CSS y texto.
4. **Enlaces:** ficha, buscador, pie, empieza, comparativa, `check.py` y guía editorial. Después, revisión independiente y PR.
