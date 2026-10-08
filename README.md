# Radar IA

Código y contenido de [radarai.es](https://radarai.es). Un generador estático en Python convierte el contenido en Markdown en la web que publica GitHub Pages.

## Estructura

- `content/`: páginas en Markdown con metadatos (`titulo`, `descripcion`, `fecha`, `actualizado`, `fuentes`, `borrador`). Las reglas están en `content/GUIA_EDITORIAL.md`.
- `data/tools.json`: catálogo de herramientas (se muestra en `/herramientas/`).
- `data/redirects.yml`: redirecciones de URLs antiguas.
- `templates/` y `static/`: plantillas Jinja2, CSS y JS.
- `radar/`: código del generador.
- `scripts/build.py`: genera la web en `_site/`.
- `scripts/check.py`: valida el resultado antes de publicar.

## Diseño

- **Estilo:** «Editorial claro» (crema, tinta y naranja). Colores y componentes en `static/css/radar.css`; fuentes Fraunces e Inter alojadas en `static/fonts/` (licencia OFL), sin Google Fonts.
- **Marcas y logotipos:** `data/brands.json` guarda el color, el icono y la inicial de cada herramienta o empresa. Los iconos (Simple Icons, CC0) se descargan una sola vez con `python scripts/fetch_logos.py` a `static/logos/`. Si una marca no tiene icono, se usa su inicial.
- **Radar de la portada:** muestra las herramientas del metadato `herramientas:` de las 6 noticias más recientes y se completa con ChatGPT, Claude, Gemini, Midjourney y Perplexity. Solo aparecen herramientas con ficha.
- **Imprescindibles:** `data/imprescindibles.txt`, una URL por línea (máximo 4).
- **Metadatos nuevos:**
  - noticias: `empresa` (id de `brands.json`) y `herramientas` (ids de `tools.json`, separados por comas);
  - fichas: `precio_desde`, `plan_pago`, `ideal_para` y `veredicto` (una frase), siempre tomados del propio texto de la ficha.
- **Imágenes de portada:** se generan solas en cada build (SVG en la página y PNG 1200×630 en `_site/og/` para compartir en redes). No se guardan en git.
- **Buscador:** el build genera `search-index.json` (artículos indexables y herramientas del catálogo sin ficha) y lo enlaza versionado en `<body data-search-index>`. `static/js/search.js` abre la ventana desde «Buscar» o la tecla «/» y da servicio a la página `/buscar/` (noindex). Si ningún resultado contiene todas las palabras, muestra los que contienen alguna, con un aviso.
- **«¿Qué IA necesito?»** (`/que-ia-necesito/`): 27 recomendaciones editoriales en `data/asistente.json` (tarea × presupuesto, con cambios opcionales `si_avanzado` y `si_equipo`). Cada «porque» debe salir de nuestras comparativas o fichas. El build las valida (herramientas existentes, principal con ficha y gratis si el presupuesto es «gratis») y añade alternativas automáticas del catálogo; `static/js/assistant.js` pinta el resultado.
- **Comparador** (`/comparador/`): compara 2–3 herramientas con ficha usando los metadatos de las fichas (`radar/compare.py` → JSON incrustado → `static/js/compare.js`). Incluye una tabla resumen estática de todas las fichas. Se enlaza desde cada ficha, desde `/herramientas/` y desde el resultado del asistente (solo si existe `content/paginas/comparador.md`).
- **Empieza aquí** (`/empieza-aqui/`): 4 tarjetas «¿Cuál es tu situación?» y una ruta de 5 pasos, definidas en `data/empieza.json` y validadas por `radar/start.py` (el build falla si un enlace apunta a una página que no existe). Se enlaza como primer elemento del menú y desde la portada, solo si existen el archivo de datos y `content/paginas/empieza-aqui.md`. Las secciones nuevas (glosario, profesiones, prompts) se añaden a ese JSON cuando se publiquen.
- **Glosario** (`/glosario/`): una sola página con los términos de `data/glosario.md` (bloques `## Término` + metadatos `tema`, `relacionados`, `ver`, `alias`, `ejemplo` + definición de 25–160 palabras), validados por `radar/glossary.py` y ordenados en orden alfabético español. Filtro por texto y tema en `static/js/glossary.js`, JSON-LD `DefinedTermSet`, y cada término entra en el buscador como `/glosario/#slug` (`check.py` valida esas anclas). Se enlaza desde «Empieza aquí», el pie y «Sobre».
- **Cara a cara** (`/a-vs-b/`): duelos entre dos herramientas con ficha, en `content/cara-a-cara/` (tipo `duelo`, mínimo 1.000 palabras). Metadatos `herramientas`, `respuesta`, `elige_1`, `elige_2` y `fuentes`, validados por `radar/duels.py` (sin «hemos probado», sin pares repetidos). La tabla de datos sale de las fichas vía `compare_payload`, y la portada lleva las dos marcas (`CoverSpec.brand2`). Se enlazan desde `/mejor-ia/` (sección «Cara a cara»), el lateral de cada ficha, el comparador (cuando las 2 elegidas forman un duelo) y el buscador. Reglas editoriales en `content/GUIA_EDITORIAL.md` (regla 10).
- **IA por profesión** (`/ia-para-<slug>/` + índice `/ia-por-profesion/`): páginas en `content/profesiones/` (tipo `profesion`, mínimo 1.000 palabras) con metadatos `profesion`, `emoji`, `kit` (2–4 `id = para qué`, con ficha) y `fuentes` oficiales, validadas por `radar/professions.py` (secciones obligatorias, 5–7 tareas, al menos 5 prompts, precios presentes en las fichas, sin «hemos probado»). El kit toma los datos de las fichas; cada cita del cuerpo es un prompt con botón «Copiar» (`static/js/prompts.js`, reutilizable). Se enlazan desde «Empieza aquí», el lateral de las fichas («Recomendada para»), la guía de pequeñas empresas y el buscador. Reglas editoriales en `content/GUIA_EDITORIAL.md` (regla 11).
- **Biblioteca de prompts** (`/prompts/`): una sola página con los prompts de `data/prompts.md` (bloques `## Título` + `categoria`, `herramientas` con ficha, `para`, `consejo` opcional + prompt en texto plano con huecos `[nombre]`, 15–150 palabras, máx. 4 huecos), validados por `radar/prompt_library.py`. `static/js/library.js` filtra por texto y categoría, rellena los huecos en la tarjeta y copia el prompt completo. Cada prompt entra en el buscador como `/prompts/#slug` (`check.py` valida esas anclas). Se enlaza desde «Empieza aquí», la guía de prompts y el pie.
- **Historial de precios** (`/historial-de-precios/`): cambios de precio de los planes individuales desde 2023 en `data/historial-precios.md` (una línea por cambio, con fuente oficial, copia archivada de la web oficial o prensa reconocida) y tomas fechadas en `data/tomas-precios/AAAA-MM-DD.json`, validados por `radar/price_history.py`: los precios de la última toma deben figurar en las fichas y los cambios entre tomas se añaden solos. Gráfico SVG por herramienta generado en el build, recuadro en el lateral de cada ficha, entradas «Precios» en el buscador (`/historial-de-precios/#precios-<id>`, validadas por `check.py`), enlace en el pie, «Empieza aquí» y la comparativa de herramientas gratis. Regla 12 de `content/GUIA_EDITORIAL.md`.
- **Validaciones:** el build falla si una noticia cita una herramienta o empresa inexistente, si `imprescindibles.txt` apunta a una página que no existe o si una ficha no tiene ningún dato de resumen. `check.py` falla si una página indexable no tiene imagen para compartir o si un enlace apunta a una categoría del catálogo (`#cat-…`) que no existe.

## Uso local

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest -q
.venv/bin/python scripts/build.py && .venv/bin/python scripts/check.py
.venv/bin/python -m http.server -d _site 8000
```

## Publicación (importante)

La web se publica con `.github/workflows/deploy.yml` (GitHub Actions) en cada push a `main`. **Antes de la primera fusión de este generador en `main`:**

1. En *Settings → Pages → Build and deployment → Source*, elegir **GitHub Actions**. Si no se cambia, Pages seguiría publicando la raíz de `main`, que ya no contiene la web, y radarai.es dejaría de funcionar.
2. Fusionar en `main` y comprobar que el workflow **Deploy** termina en verde.
3. En *Settings → Pages*, confirmar que el dominio personalizado sigue siendo `radarai.es` y que **Enforce HTTPS** está activo. Con GitHub Actions, el archivo `CNAME` no basta: el dominio lo fija esa configuración.

## Noticias semiautomáticas

1. **Cada mañana (07:00, hora de Madrid)** el workflow `Noticias candidatas` lee las fuentes de `data/news_sources.txt` y abre una issue con la etiqueta `noticias` y las novedades de las últimas 26 horas.
2. **A las 08:30** una rutina programada de Claude sigue `docs/rutina-noticias.md`: elige 1–2 candidatas, lee la fuente original, redacta la noticia, abre un **pull request** y te avisa al móvil con el enlace.
3. **Revisión del titular** (nada se publica sin ella):
   - lee el PR en GitHub («Files changed»);
   - edita lo que quieras desde la web de GitHub;
   - pulsa **Merge** (también desde la app de GitHub en el móvil);
   - al fusionar, el workflow **Deploy** publica la noticia en unos minutos.

   Si no te convence, cierra el PR.

Para lanzar la recogida a mano: Actions → «Noticias candidatas» → Run workflow.
