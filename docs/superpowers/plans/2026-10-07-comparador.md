# Comparador — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Construir `/comparador/` para comparar 2–3 herramientas con ficha, con selección por logotipos, una URL compartible, una tabla resumen estática y puntos de entrada desde las fichas, `/herramientas/` y el asistente.

**Architecture:**
- `radar/compare.py` genera la lista de herramientas comparables a partir de las fichas indexables.
- La plantilla `compare.html` pinta las casillas, la tabla resumen estática y el JSON incrustado.
- `static/js/compare.js` construye la tabla de comparación con DOM.

**Spec:** `docs/superpowers/specs/2026-10-07-comparador-design.md`

## Global Constraints

- **Herramientas:** solo fichas indexables, ordenadas por nombre; un campo vacío se muestra como «—».
- **Límite:** como máximo 3 herramientas; con 3 marcadas, el resto queda `disabled`.
- **URL:** `?h=a,b,c`; los ids inválidos se ignoran y se recorta a 3.
- **Textos fijos:**
  - eyebrow «Comparador»;
  - H1 «Compara herramientas de IA»;
  - legend «Elige hasta 3 herramientas»;
  - botón en la ficha «Comparar <nombre> con… →»;
  - botón en `/herramientas/` «⇄ Comparar herramientas»;
  - enlace en el asistente «Comparar con las alternativas →».
- **Sin «más barato»:** no se marca ninguna herramienta como la más barata.
- **Seguridad y tamaño:** nada de `innerHTML` con datos, y `compare.js` ≤ 5 KB comprimido.
- **Commits** en la rama `comparador` con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. La PR no se fusiona sin el OK de Cristian.

## Review Focus

1. **URL con más de 3 ids o con ids repetidos:** se marcan como máximo 3 distintos. *Task 2.*
2. **Ficha sin `plan_pago` o sin `plataforma`:** se muestra «—» y el resto de la tabla sigue bien. *Test en la Task 1.*
3. **Una sola herramienta marcada:** no aparece la tabla, sino el aviso «Elige al menos 2». *Task 2.*
4. **Tabla de 3 columnas a 375 px:** no desborda la página; solo se desplaza la tabla, con la primera columna fija. *Task 2.*
5. **Enlace del asistente cuando las alternativas no tienen ficha:** el enlace no aparece si quedan menos de 2 herramientas con ficha. *Task 3.*

---

### Task 1: Datos y página

- **Archivos:**
  - nuevos: `radar/compare.py`, `content/paginas/comparador.md` (unas 350 palabras), `templates/compare.html` y `tests/test_compare.py`;
  - cambian: `scripts/build.py` (`compare_payload` en el contexto) y `radar/render.py` (plantilla por URL y paso del payload).
- **Interfaz:** `compare_payload(fichas: Dict[str, Page], tools, brands, categories) -> List[dict]`, con los campos `{id, n, c, m, u, w, desde, pago, ideal, plataformas, veredicto, cat}`.
- **TDD:**
  - orden y «—» en los campos vacíos;
  - la página tiene una casilla por ficha, el JSON es válido y la tabla estática lista todas las fichas;
  - la página es indexable y supera las 300 palabras.

### Task 2: `compare.js` y estilos

- **Archivos:** `static/js/compare.js`, `static/css/radar.css` (sección «15. Comparador») y tests.
- **TDD:**
  - test estático: sin `innerHTML`, con `replaceState` y `scope`, y ≤ 5 KB comprimido;
  - verificación en el navegador de los puntos 1, 3 y 4 del Review Focus.

### Task 3: Puntos de entrada, revisión y PR

- **Archivos:**
  - `templates/tool.html`: botón en el lateral;
  - `templates/listing.html`: botón en `/herramientas/`;
  - `static/js/assistant.js`: enlace en el resultado;
  - `README.md` y tests.
- **TDD:** los enlaces existen y el enlace del asistente se oculta si hay menos de 2 herramientas con ficha.
- **Después:** revisión independiente (opus), correcciones RED→GREEN y PR.
