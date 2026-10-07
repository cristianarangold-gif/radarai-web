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
