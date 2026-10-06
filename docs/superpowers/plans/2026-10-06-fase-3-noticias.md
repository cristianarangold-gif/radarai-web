# Radar IA — Fase 3: noticias semiautomáticas · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar la opción A del spec §5:
1. Recogida diaria automática de noticias candidatas en una issue de GitHub.
2. Redacción asistida de borradores como pull request.
3. Publicación tras la revisión del titular.

Además, publicar 6 noticias iniciales con análisis propio.

**Architecture:**
- `scripts/news_collect.py` usa solo la librería estándar: `urllib` y `xml.etree`. Lee las fuentes de `data/news_sources.txt`, filtra lo publicado en las últimas 26 h, prioriza las fuentes oficiales y genera el cuerpo de la issue.
- El workflow `news-collect.yml` lo ejecuta cada día y crea la issue con `gh`.
- No hay estado persistente: la ventana de 26 h con ejecución diaria evita duplicados, y así se evitan commits automáticos en `main`.
- La redacción la hace una rutina programada de Claude (skill `schedule`) que abre un PR en borrador por noticia.

**Tech Stack:** Python 3 (stdlib), GitHub Actions y GitHub CLI.

**Spec:** `docs/superpowers/specs/2026-10-06-radar-ia-adsense-design.md` §5.

## Global Constraints

- Nunca se publica sin revisión humana: la rutina abre PR en **borrador** y no los fusiona.
- Cada noticia sigue `content/GUIA_EDITORIAL.md`:
  - 500–900 palabras;
  - estructura: qué ha pasado · por qué importa · qué cambia en la práctica en España/UE · opinión de Radar IA · fuentes;
  - sin copiar ni traducir artículos enteros, con citas de una frase como máximo;
  - metadatos `fecha` y `fuentes` obligatorios.
- Las fuentes oficiales tienen prioridad sobre los medios.
- Los workflows nunca hacen commits en `main`.

## Review Focus

1. **Feed caído o con XML inválido.** La recogida sigue con las demás fuentes y lista los fallos al final de la issue (`test_broken_feed_does_not_abort`).
2. **Fechas en RFC 822 (RSS) e ISO 8601 (Atom), con y sin zona horaria.** Todas se interpretan (`test_parses_rss_and_atom_dates`).
3. **Ningún candidato en la ventana.** No se crea una issue vacía; el workflow termina sin error (`test_no_candidates_returns_none`).
4. **Títulos con entidades HTML o CDATA.** Se muestran limpios en la issue (`test_titles_unescaped`).
5. **La misma noticia en varias fuentes** (misma URL). Aparece una sola vez (`test_dedupes_by_url`).

---

### Task 1: Recogida de candidatas (TDD)

**Files:**
- Create: `scripts/news_collect.py`, `data/news_sources.txt`, `tests/test_news_collect.py`, `tests/fixtures/rss.xml`, `tests/fixtures/atom.xml`

**Interfaces:**
- `parse_feed(xml_text: str, source: str, official: bool) -> list[Item]`, donde `Item` es una namedtuple con `title`, `url`, `published` (datetime en UTC), `source` y `official`.
- `load_sources(path) -> list[tuple[name, url, official]]`. Formato de cada línea: `oficial|medio · Nombre · URL`.
- `select_candidates(items, now, hours=26, limit=10) -> list[Item]`: dentro de la ventana, sin URLs duplicadas, oficiales primero y después por fecha descendente.
- `render_issue(items, failures, today) -> str | None`. Devuelve `None` si no hay candidatas.
- `main()` escribe el cuerpo en stdout y sale con código 0. Si no hay candidatas, no escribe nada.

**Pasos:**
- [ ] Escribir los tests de Review Focus y además `test_select_orders_official_first`.
- [ ] Verlos fallar, implementar y ver la suite en verde.
- [ ] Ejecutar en local contra las fuentes reales: `python scripts/news_collect.py`.
- [ ] Hacer commit.

### Task 2: Workflow diario

- [ ] Crear `.github/workflows/news-collect.yml`:
  - `schedule: cron '0 5 * * *'` (07:00 en Madrid en horario de verano) y `workflow_dispatch`;
  - `permissions: issues: write, contents: read`;
  - ejecuta el script y, si genera salida, `gh issue create --title "Noticias candidatas AAAA-MM-DD" --label noticias --body-file`;
  - crea la etiqueta `noticias` si no existe.
- [ ] Probarlo con `gh workflow run` tras fusionarlo. Antes no se puede: los workflows programados solo corren desde `main`.
- [ ] Hacer commit.

### Task 3: Seis noticias iniciales

- [ ] Elegir 6 noticias de IA relevantes de las últimas 2–3 semanas, a partir de las candidatas reales y de WebSearch.
- [ ] Para cada una:
  1. Leer la fuente primaria.
  2. Redactar según la guía editorial.
  3. Escribir `content/noticias/<slug>.md` con `fecha` igual a la fecha de publicación en Radar IA y `fuentes`.
- [ ] Retirar los 6 borradores antiguos de septiembre, con redirección de sus URL a `/noticias/`.
- [ ] Ejecutar `build` + `check` en OK y hacer commit.

### Task 4: Rutina de redacción asistida

- [ ] Crear con la skill `schedule` una rutina diaria a las 08:30 (hora de Madrid). Debe:
  1. Leer la issue «Noticias candidatas» del día.
  2. Elegir 1–2 candidatas con más interés para España y Latinoamérica.
  3. Investigar la fuente primaria.
  4. Redactar según `content/GUIA_EDITORIAL.md`.
  5. Comprobar con `scripts/build.py` y `scripts/check.py`.
  6. Abrir un PR en **borrador** por noticia, enlazando la issue.
  7. Comentar en la issue lo que ha hecho.
- [ ] Documentar en `README.md` el flujo de revisión del titular: leer el PR, editarlo si quiere, marcarlo como «Ready» y hacer merge, que publica.
