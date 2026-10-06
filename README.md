# Radar IA

Código y contenido de [radarai.es](https://radarai.es). Un generador estático en Python convierte el contenido en Markdown en la web que publica GitHub Pages.

## Estructura

- `content/`: páginas en Markdown con metadatos (`titulo`, `descripcion`, `fecha`, `actualizado`, `fuentes`, `borrador`). Las reglas están en `content/GUIA_EDITORIAL.md`.
- `data/tools.json`: catálogo de herramientas de la portada.
- `data/redirects.yml`: redirecciones de URLs antiguas.
- `templates/` y `static/`: plantillas Jinja2, CSS y JS.
- `radar/`: código del generador.
- `scripts/build.py`: genera la web en `_site/`.
- `scripts/check.py`: valida el resultado antes de publicar.

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
2. **A las 08:30** una rutina programada de Claude sigue `docs/rutina-noticias.md`: elige 1–2 candidatas, lee la fuente original, redacta la noticia y abre un **pull request en borrador**.
3. **Revisión del titular** (nada se publica sin ella):
   - lee el PR en GitHub («Files changed»);
   - edita lo que quieras desde la web de GitHub;
   - pulsa **Ready for review** y después **Merge**;
   - al fusionar, el workflow **Deploy** publica la noticia en unos minutos.

   Si no te convence, cierra el PR.

Para lanzar la recogida a mano: Actions → «Noticias candidatas» → Run workflow.
