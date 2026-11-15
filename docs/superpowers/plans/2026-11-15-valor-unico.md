# Valor único — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mantener vivo el historial de precios con una rutina semanal, ampliar «¿Funciona en España?» a unas 50 funciones y enlazar ambas secciones desde las noticias.

**Architecture:** Generador estático en Python (`scripts/build.py` → `_site`, `scripts/check.py`, `pytest`). Los datos viven en `data/`; las rutinas en la nube (RemoteTrigger) siguen un documento de `docs/` y terminan en una PR que Cristian revisa y fusiona.

**Tech Stack:** Python 3.12 (sin dependencias nuevas), GitHub Actions, rutinas RemoteTrigger.

**Spec:** `docs/superpowers/specs/2026-11-15-valor-unico-design.md`

## Global Constraints

- Nada se publica sin que Cristian lo revise y fusione; se fusiona solo con «Sí, fusiónalo y publícalo» o «ya» y las dos comprobaciones `test` en SUCCESS.
- Una PR por parte; ejecución parte por parte, esperando «Sí, adelante con la parte N».
- Regla 13 de `content/GUIA_EDITORIAL.md`: fuentes oficiales o archive.org, nunca prensa; nada deducido; `sin_confirmar` si la fuente no nombra España, la UE o el EEE; `nota` de 30 palabras como máximo.
- Precios: solo los que ve un visitante español, en euros; si no se pueden leer, se conserva el valor anterior y se dice «no comprobado».
- Las rutinas no fusionan, no hacen push a `main` y no publican.
- Commits con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; cuerpos de PR terminados en `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

## Review Focus

1. Una herramienta cuya página muestra dólares desde la nube: la toma debe conservar el precio anterior y la PR listarla como no comprobada (lo fija el doc de la rutina; test de texto en la Tarea 1).
2. Un precio que cambia en la toma pero no en la ficha: `build.py` falla; el doc obliga a actualizar la ficha (test de texto en la Tarea 1).
3. Un enlace `/funciona-en-espana/#id` con un id que no existe: hoy `check.py` no lo detecta (Tarea 2).
4. Una función nueva de una empresa fuera de `OFICIALES` (por ejemplo Samsung): la validación falla hasta añadir sus dominios (Tarea 3).
5. Una noticia enlazada a una fila que no trata de esa función: revisión manual en la PR de la Tarea 4 (lista noticia → fila en el cuerpo de la PR).

---

### Parte 1 (Tarea 1): Rutina «Precios semanales»

**Files:**
- Create: `docs/rutina-precios.md`
- Test: `tests/test_price_history.py` (añadir)
- Externo: RemoteTrigger nuevo «Radar IA · Precios semanales»

**Interfaces:**
- Consumes: `scripts/fetch_source.py URL`; formato de `data/tomas-precios/AAAA-MM-DD.json` (`nota`, `herramientas.{id}.fuente`, `herramientas.{id}.planes`); `validate_history` en `radar/price_history.py`.
- Produces: PRs semanales en ramas `precios/AAAA-MM-DD`.

- [ ] **Step 1: Test que fija las reglas del doc**

```python
def test_price_routine_doc_keeps_the_safety_rules():
    doc = (ROOT / 'docs/rutina-precios.md').read_text(encoding='utf-8')
    for must in ('scripts/fetch_source.py', 'data/tomas-precios/', 'no comprobad', 'toma anterior',
                 'content/herramientas/', 'precios/AAAA-MM-DD', 'desde España', 'euros',
                 'scripts/build.py', 'scripts/check.py'):
        assert must in doc
    assert 'Tienes prohibido fusionar' in doc
```

- [ ] **Step 2:** `.venv/bin/pytest -q tests/test_price_history.py -k routine` → FAIL (no existe el archivo).
- [ ] **Step 3:** Escribir `docs/rutina-precios.md` con los 8 pasos de la sección 1 del spec. Cuerpo de la PR: tabla `Herramienta | Plan | Antes | Ahora | Página oficial`, cambios primero, lista «No comprobadas (se mantiene el precio de la toma anterior)», y la frase final «Abre cada enlace desde España y confirma los precios en euros antes de fusionar». La `nota` de la toma nombra las comprobadas y las no comprobadas.
- [ ] **Step 4:** Mismo test → PASS; `pytest -q` completo en verde.
- [ ] **Step 5:** Commit, PR, fusión tras aprobación.
- [ ] **Step 6:** Tras la fusión, crear el RemoteTrigger: `CRON_TZ=Europe/Madrid 0 9 * * 1`, entorno `env_01WHmXFpMY3bwy8J66TNZynm`, `claude-sonnet-5-5`, herramientas `Bash, Read, Write, Edit, Glob, Grep`, `clear_mcp_connections: true`; prompt corto: leer y seguir `docs/rutina-precios.md` y `content/GUIA_EDITORIAL.md`, con la lista de prohibiciones. Comunicar la hora de la próxima ejecución y el enlace de la rutina.

### Parte 2 (Tarea 2): Comprobar enlaces a filas de «¿Funciona en España?»

**Files:**
- Modify: `radar/check.py` (`_anchor_missing`)
- Test: `tests/test_check.py`

**Interfaces:**
- Produces: `check_site` informa de `/funciona-en-espana/#id` inexistentes. Lo usan las Partes 3 y 4.

- [ ] **Step 1: Test**

```python
def test_link_to_missing_availability_anchor(tmp_path):
    page(tmp_path, 'index.html', '/', body='<a href="/funciona-en-espana/#uno">u</a> '
                                           '<a href="/funciona-en-espana/#nada">n</a>')
    page(tmp_path, 'funciona-en-espana/index.html', '/funciona-en-espana/', title='F',
         body='<tr id="uno"></tr>')
    sitemap(tmp_path, '/', '/funciona-en-espana/')
    errors = check_site(tmp_path)
    assert any('/funciona-en-espana/#nada' in e for e in errors) and not any('#uno' in e for e in errors)
```

- [ ] **Step 2:** `pytest -q tests/test_check.py -k availability_anchor` → FAIL.
- [ ] **Step 3:** Añadir `'/funciona-en-espana/#'` a los prefijos de `_anchor_missing` y a su docstring.
- [ ] **Step 4:** Test → PASS; `pytest -q`, `build.py` y `check.py --site _site` en verde (si `check.py` encuentra enlaces rotos ya existentes, se corrigen en esta misma parte).
- [ ] **Step 5:** Commit y PR.

### Partes 3a, 3b y 3c (Tarea 3): Funciones nuevas en «¿Funciona en España?»

**Files:**
- Modify: `data/disponibilidad.md`; `radar/availability.py` (`OFICIALES`, solo si entra una empresa nueva)
- Test: la validación de `build.py` y `tests/test_availability.py` existentes

- [ ] **Step 1:** Elegir unas 8 funciones por parte (criterio del spec, sin repetir las 26 actuales) y leer cada fuente oficial con `scripts/fetch_source.py`.
- [ ] **Step 2:** Si entra una empresa nueva, añadir antes un test en `tests/test_availability.py` que valide un bloque de esa empresa (FAIL), luego sus dominios a `OFICIALES` (PASS).
- [ ] **Step 3:** Añadir los bloques con `id`, `empresa`, `eeuu`, `ue`, `es`, `nota`, `comprobado` (fecha del día), `fuentes`, y `ficha`/`noticia` si existen.
- [ ] **Step 4:** `build.py`, `check.py --site _site` y `pytest -q` en verde.
- [ ] **Step 5:** PR con una tabla función → estado EE. UU./UE/España → fuente, para revisión.

### Parte 4 (Tarea 4): Enlaces desde las noticias

**Files:**
- Modify: `content/noticias/*.md` (solo las que tratan de una función con fila o de un precio); `docs/rutina-noticias.md`

- [ ] **Step 1:** Cruzar las noticias con los ids de `data/disponibilidad.md` y con las herramientas del historial; lista noticia → enlace.
- [ ] **Step 2:** Añadir una frase o enlace por noticia a `/funciona-en-espana/#id` o `/historial-de-precios/#precios-<herramienta>`, sin tocar el resto del texto; si la fila no tiene `noticia:` y esa noticia es la suya, añadirla.
- [ ] **Step 3:** En `docs/rutina-noticias.md`, punto 48: «toda» noticia sobre una función con fila o sobre un precio enlaza a ella.
- [ ] **Step 4:** `build.py`, `check.py --site _site` (ya detecta anclas rotas, Parte 2) y `pytest -q` en verde.
- [ ] **Step 5:** PR con la lista noticia → enlace.
