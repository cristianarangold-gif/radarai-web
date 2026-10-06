# Radar IA — Fase 2: contenido núcleo · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar ~40 páginas indexables de calidad (spec §4.2):
- 9 comparativas;
- 15 fichas;
- 6 guías;
- 9 utilidades con texto explicativo;
- páginas de confianza ya hechas en la fase 1.

Además, saldar la deuda técnica menor de la fase 1.

**Architecture:** el generador de la fase 0 no cambia, salvo un tipo nuevo `utilidad`. Todo lo demás es contenido Markdown en `content/` con metadatos y fuentes verificadas en la web oficial durante la redacción.

**Tech Stack:** Python 3 + Jinja2 + Markdown (sin dependencias nuevas). WebSearch y WebFetch para la investigación.

**Spec:** `docs/superpowers/specs/2026-10-06-radar-ia-adsense-design.md` (§2 principios editoriales y §4.2 contenido).

## Global Constraints

- **Principios editoriales del spec §2 en todo el contenido:**
  - Nunca escribir «lo hemos probado» ni «en nuestras pruebas».
  - El bloque «Nuestra prueba» va como comentario HTML `<!-- NUESTRA PRUEBA: … -->`, invisible, para que Cristian lo rellene.
  - Cada precio indica «(comprobado el D de mes de AAAA)» y procede de la página oficial consultada en esta sesión.
  - Cada página lista sus URLs consultadas en `fuentes`.
- **Mínimos de palabras:**

  | Tipo | Mínimo |
  |---|---|
  | `ficha` | 1000 |
  | `comparativa`, `guia` | 1200 |
  | `utilidad` | 300 |

  `scripts/check.py` los hace cumplir.
- **Texto:** español de España, autor «Cristian Arango», tono cercano y claro.
- **Precios:** en EUR cuando la web oficial los muestra en EUR. Si solo están en USD, se dan en USD y se indica así.
- **Copias:** no copiar frases de las webs oficiales; las citas son de una frase como máximo y van atribuidas.
- **Enlaces internos:** cada comparativa enlaza a las fichas de las herramientas que menciona (`/herramientas/<id>/`) y a 1–2 guías. Cada ficha enlaza a su comparativa principal.
- **Ids de ficha:** coinciden con `data/tools.json`, de modo que el catálogo de la portada enlaza automáticamente a la ficha.

## Review Focus

1. **Afirmaciones de precio o función sin fuente consultada en esta sesión.** Toda cifra tiene que poder rastrearse a una URL de `fuentes`. Se comprueba en cada task de contenido (paso «verificar fuentes»).
2. **Frases que insinúan pruebas propias inexistentes.** Se comprueba con `grep -riE "hemos probado|en nuestras pruebas|probamos"` sobre `content/`, que debe salir vacío. Va en la Task 9.
3. **Ficha cuyo id no existe en `tools.json`.** El enlace del catálogo no aparecería. Test en la Task 1.
4. **Comparativa que enlaza a una ficha inexistente.** Lo detecta `check.py` como enlace roto.
5. **Contenido casi duplicado entre comparativas** (mismo párrafo repetido). Revisión manual en la Task 9 con un script de similitud por párrafos.

---

### Task 1: Deuda técnica de la fase 1 y tipo `utilidad`

**Files:**
- Modify:
  - `radar/content.py` (regex estricta de fecha; `KIND_BY_DIR['utilidades'] = 'utilidad'` con URL `/herramientas-radar/<slug>/`)
  - `radar/models.py` (`noindex` acepta «sí»)
  - `scripts/build.py` (sin canonical en 404; rechaza un `--out` que contenga `scripts/build.py`; listado `/herramientas-radar/`)
  - `templates/base.html` (canonical opcional)
  - `static/css/radar.css` y `static/js/site.js` (menú visible sin JS)
  - `requirements*.txt` (versiones fijadas)
  - `tests/test_build.py` (afirma ambos orígenes)
  - `tests/test_content.py`
  - `tests/test_tools.py`
- Test: los tests nuevos de esta lista.

- [ ] Escribir los tests:
  - `test_date_requires_iso_dashes` (`20261001` → ValueError);
  - `test_noindex_accent`;
  - `test_utilidad_url`;
  - `test_404_has_no_canonical`;
  - `test_refuses_out_dir_with_sources`;
  - `test_every_ficha_id_exists_in_catalog`: cada `content/herramientas/*.md` tiene un id en `tools.json`;
  - el test de colisión debe afirmar `content /noticias/buena/` y `redirección`.
- [ ] Verlos fallar, implementar y ver la suite en verde. Después `build` + `check` en OK.
- [ ] Fijar versiones con `pip freeze` de `.venv` (jinja2, markdown, MarkupSafe, pytest).
- [ ] Hacer commit: `Saldar deuda técnica de la fase 1 y añadir tipo utilidad`.

### Task 2: Limpieza del catálogo

- [ ] Eliminar de `data/tools.json` los duplicados (mismo producto con otro id):
  - `copyspace` (Anyword);
  - `gamma-ai`, `gamma-docs` y `gamma-presentations`, que quedan como `gamma`;
  - `otter-transcribe`, que queda como `otter-ai`;
  - `descript-audio`, que queda como `descript`;
  - `jasper-chat`, que queda como `jasper`;
  - `writesonic-seo`, que queda como `writesonic`.

  Las URL antiguas de esos ids redirigen a la categoría del producto que se queda (automático).
- [ ] Ajustar la cifra del test (`len == 127`) y ver la suite en verde.
- [ ] Hacer commit: `Eliminar duplicados del catálogo`.

### Task 3: Investigación de precios y planes (15 herramientas)

**Files:**
- Create: `content/_investigacion/precios-2026-10.md`. No se publica, porque el loader ignora los archivos con `_`.

- [ ] Para cada herramienta de la Task 4, consultar la página oficial de precios y la de funciones con WebFetch y anotar:
  - planes y precio mensual (moneda);
  - límites del plan gratuito;
  - disponibilidad en España/UE;
  - política de uso de datos para entrenamiento;
  - URL y fecha de consulta.
- [ ] Si una página no carga, buscar la fuente oficial alternativa (centro de ayuda o blog) con WebSearch. Nunca rellenar de memoria. Si no hay dato, la ficha lo dice («no publicado»).
- [ ] Hacer commit: `Añadir notas de investigación de precios (octubre 2026)`.

### Task 4: 15 fichas completas

**Ids y su comparativa principal:**

| Id | Comparativa principal |
|---|---|
| chatgpt, claude, gemini, copilot, perplexity | productividad |
| midjourney | imágenes |
| runway | vídeo |
| suno | música |
| elevenlabs | vídeo |
| github-copilot, cursor | programar |
| canva-ai | marketing |
| deepl-write | escribir |
| notion-ai | productividad |
| notebooklm | estudiar |

Si `deepl` no existe en `tools.json`, la ficha usa el id `deepl-write` y cubre DeepL (Translator + Write).

**Estructura de cada ficha (≥ 1000 palabras):**
- **Metadatos:** `titulo` («<Nombre>: qué es, precios y para quién merece la pena»), `descripcion` (≤ 160 caracteres), `fecha`, `fuentes`, `web` (url oficial) y `plataforma`.
- **Secciones:**
  1. Qué es y para quién.
  2. Planes y precios (tabla con fecha de comprobación).
  3. Funciones clave.
  4. Casos de uso con 2–3 prompts o ejemplos concretos.
  5. Limitaciones.
  6. Privacidad y uso de tus datos.
  7. Alternativas, con enlaces a otras fichas o a la comparativa.
  8. Veredicto por perfil.
  9. Preguntas frecuentes (3).
- **Bloque `<!-- NUESTRA PRUEBA -->`** después del veredicto.

**Pasos:**
- [ ] Escribir las fichas en 3 lotes de 5. En cada lote:
  1. Escribir.
  2. Ejecutar `build` + `check`. Esperado: OK, cada ficha indexable y ≥ 1000 palabras.
  3. Verificar que cada cifra está en `content/_investigacion`.
  4. Hacer commit: `Añadir fichas: <ids>`.

### Task 5: 9 comparativas «Mejor IA para…»

**Slugs:** los 8 existentes más `mejor-ia-para-crear-musica`. Se reescriben con `borrador` eliminado.

**Estructura (≥ 1200 palabras):**
1. Respuesta rápida (las 3 mejores, cada una en una línea).
2. Cómo hemos elegido (criterios; sin afirmar pruebas propias).
3. Tabla comparativa (herramienta, para qué destaca, plan gratuito, precio desde y fecha).
4. Análisis de 5–7 herramientas (2–3 párrafos cada una, enlazando a su ficha si existe).
5. Recomendación por perfil (estudiante, autónomo, empresa).
6. Alternativas gratuitas.
7. Privacidad.
8. Preguntas frecuentes (3–4).

- Los precios de herramientas que no están en las 15 fichas también se consultan en su web oficial y se añaden a `content/_investigacion`.

**Pasos:**
- [ ] 3 lotes de 3. En cada lote: `build` + `check` en OK y commit: `Reescribir comparativas: <slugs>`.

### Task 6: 6 guías prácticas

**Slugs y contenido:**

| Slug | Estado | Tema |
|---|---|---|
| `mejores-prompts` | reescritura | Cómo escribir buenos prompts |
| `automatizar-tareas` | reescritura | Automatizar tareas |
| `crear-presentaciones-con-ia` | nueva | Crear presentaciones |
| `ia-para-estudiar` | reescritura | IA para estudiar sin plagiar |
| `ia-para-pequenas-empresas` | nueva | IA en la pequeña empresa |
| `privacidad-en-ia` | reescritura | Privacidad al usar IA |

- **Se retiran con redirección:** `como-elegir-una-ia` → `/mejor-ia/` y `chatbot-buscador-generador` → `/guias/`.
- **Contenido de cada guía:** ≥ 1200 palabras, con pasos numerados, ejemplos reales de prompts, errores habituales y FAQ.

**Pasos:**
- [ ] 2 lotes de 3. En cada lote: `build` + `check` en OK y commit.

### Task 7: Utilidades integradas en las plantillas

- [ ] Mover cada utilidad de `static/utilidades/<slug>/index.html` a `content/utilidades/<slug>.md`:
  1. Conservar el formulario HTML dentro de `<div markdown="0">`.
  2. Añadir `<script src="/herramientas-radar/app.js" defer>` a la plantilla mediante el metadato `script`.
  3. Escribir ≥ 300 palabras explicativas: para qué sirve, cómo usarla paso a paso, ejemplo y relación con las guías.
- [ ] Mantener `static/utilidades/app.js`. Escribir el índice `/herramientas-radar/` como listado.
- [ ] Comprobar en el navegador que cada utilidad funciona (rellenar campos y obtener resultado), a 375 px y en escritorio.
- [ ] Hacer commit: `Integrar utilidades en las plantillas con texto explicativo`.

### Task 8: Portada e interenlazado

- [ ] Añadir a la portada:
  - el bloque «Comparativas destacadas» (6), generado del listado;
  - el bloque «Guías» (3);
  - el bloque «Utilidades gratuitas».
- [ ] Quitar de `inicio.md` las afirmaciones que aún no se cumplan.
- [ ] Ejecutar `build` + `check` en OK y hacer commit.

### Task 9: Control de calidad editorial

- [ ] `grep -riE "hemos probado|en nuestras pruebas|probamos|nuestro equipo ha probado" content/ --include=*.md`. Esperado: sin resultados.
- [ ] Script de similitud: ningún párrafo de más de 25 palabras aparece igual en dos páginas.
- [ ] Revisión en el navegador de 1 ficha, 1 comparativa y 1 guía en móvil y escritorio.
- [ ] Ejecutar `build` + `check`. Esperado: sitemap con ≥ 38 URLs.
- [ ] Hacer commit y push. CI en verde.
