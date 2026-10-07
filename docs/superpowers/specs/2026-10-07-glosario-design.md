# Radar IA — Glosario de IA

Fecha: 2026-10-07 · Rama: `glosario` · Maqueta: `_preview/maquetas/9-glosario.html` (fuera del repo), opción **A** · Proyecto «Secciones nuevas», parte 2 de 6.

## 1. Objetivo

Una sola página `/glosario/` que explica en español claro unos **50 términos de IA**: qué significan, un ejemplo cuando ayuda y enlaces para seguir aprendiendo.
- Es contenido largo, propio y útil (unas 4.000–5.000 palabras), sin riesgo de «páginas delgadas».
- Cada término tiene su ancla (`/glosario/#token`) para enlazarlo desde artículos, desde «Empieza aquí» y desde el buscador.

**Decisiones del titular:**
- una sola página (A);
- unos 50 términos al empezar; se amplía después;
- más adelante, un término que lo merezca podrá tener página propia con más de 400 palabras (fuera de alcance ahora).

**Criterio de éxito:**
- Todos los enlaces y relacionados existen; si no, el build falla.
- El filtro funciona al momento y la página se lee completa sin JS.
- Se ve bien a 375 y 1440 px.
- Los términos aparecen en el buscador de la web.
- Los tests, el build y `check.py` están en verde.

## 2. Datos: `data/glosario.md`

Es un archivo Markdown fácil de editar a mano. Cada término es un bloque que empieza con `## Término`:

```markdown
## Alucinación
tema: basicos
relacionados: modelo-de-lenguaje, rag
ver: /guias/mejores-prompts/
ejemplo: Le pides la biografía de un autor poco conocido y te atribuye un libro que no existe.

Cuando un asistente de IA se inventa un dato, una cita o una fuente y lo presenta con total seguridad. …
```

- **Cabecera de metadatos** (líneas `clave: valor` hasta la primera línea en blanco):
  - `tema` (obligatorio): uno de 5;

    | id | Etiqueta |
    |---|---|
    | `basicos` | Conceptos básicos |
    | `modelos` | Modelos y tecnología |
    | `uso` | Usar la IA |
    | `precios` | Precios y planes |
    | `etica` | Privacidad y ética |

  - `relacionados` (opcional): slugs de otros términos, separados por comas;
  - `ver` (opcional): hasta 2 URLs internas (guía, comparativa, ficha o utilidad);
  - `alias` (opcional): sinónimos o siglas que el filtro y el buscador también encuentran (por ejemplo, `LLM` para «Modelo de lenguaje»);
  - `ejemplo` (opcional): una frase.
- **Cuerpo:** la definición, de 1 a 3 párrafos de Markdown, entre 25 y 160 palabras.
- **Slug:** se calcula del término, en minúsculas, sin tildes y con guiones (`Alucinación` → `alucinacion`).
- **Orden alfabético español:** sin distinguir tildes, y la Ñ va después de la N.
- **Validación en el build** (`radar/glossary.py`, con un error que nombra el término):
  - términos y slugs únicos;
  - tema válido;
  - los relacionados existen y no apuntan a sí mismos;
  - las URLs de `ver` existen y son indexables (como máximo 2);
  - la definición tiene entre 25 y 160 palabras;
  - no aparece «hemos probado»;
  - no hay claves desconocidas.
- **Contenido:**
  - definiciones generales y comprobables, sin precios ni cifras que caduquen, salvo con fuente y fecha;
  - nunca se afirma haber probado nada;
  - el tono es el de «Tres conceptos para empezar».

## 3. Página `/glosario/`

- **Contenido:** `content/paginas/glosario.md` (tipo página e indexable), con unas 300 palabras propias:
  - para qué sirve el glosario y cómo usarlo;
  - cómo elegimos y escribimos las definiciones;
  - una invitación a sugerir términos (Contacto).
- **Plantilla nueva** `glossary.html` (elegida por la URL):
  - eyebrow «Glosario» y H1 «Glosario de *inteligencia artificial*», con la entradilla;
  - **controles**: un campo de filtro (`input type="search"`, con etiqueta), los chips de tema (`button` con `aria-pressed`) y una línea `aria-live` («12 términos»). Llevan `hidden` y los muestra el JS;
  - **saltos por letra**: A–Z más Ñ; las letras sin términos se pintan desactivadas (`span`), y las demás son enlaces `#letra-a`;
  - **por cada letra:** `h2` con la letra e `id="letra-x"`, y una `dl`;
  - **por cada término:** `div.term` con `id="<slug>"` y `data-tema`, que contiene:
    - `dt` con el término y la etiqueta del tema;
    - `dd` con la definición, el ejemplo («Ejemplo: …») y la línea «Relacionado: …» (anclas a otros términos y títulos de las páginas de `ver`);
  - después, el cuerpo Markdown.
- **`static/js/glossary.js`** (sin librerías, ≤ 2 KB comprimido):
  - filtra por texto (término, alias y definición; sin tildes ni mayúsculas) y por tema;
  - oculta las letras sin resultados y actualiza el recuento;
  - si no hay resultados: «Ningún término coincide. Prueba con otra palabra o sugiérenos uno.».
- **Datos estructurados:** JSON-LD `DefinedTermSet` con cada `DefinedTerm` (`name`, `description` en texto plano y `url` con ancla), además de la miga de pan habitual.
- **Estilos:** sección «17. Glosario» en `radar.css`. En móvil, término y definición van en una columna; en escritorio, en dos (220 px + resto).

## 4. Buscador y enlaces

- **Buscador:** cada término entra en `search-index.json` con:
  - `t`: el término;
  - `u`: `/glosario/#slug`;
  - `k`: «Glosario»;
  - `d`: el inicio de la definición;
  - `x`: los alias y el tema;
  - símbolo «G» en color tinta.

  `check.py` ya valida las URLs del índice; se amplía para comprobar que el ancla existe en la página.
- **«Empieza aquí»:**
  - el paso 1 añade el enlace extra «Glosario de IA»;
  - la sección «Tres conceptos para empezar» termina con «Más términos en el glosario».
- **Pie de página:** en la columna «Radar IA», el enlace «Glosario de IA», solo si la página existe en el build.
- **Enlaces desde otras páginas:**
  - la ficha y la guía de prompts no se tocan;
  - en la página «Sobre Radar IA», la lista «Qué publicamos» añade el glosario.

## 5. Pruebas

- **Python:**
  - el parser lee las cabeceras y el cuerpo y calcula el slug;
  - el orden español: tildes y Ñ (por ejemplo, «Ñ» después de «N» y «Árbol» junto a la A);
  - la validación falla con: tema inválido, relacionado inexistente o a sí mismo, URL de `ver` inexistente, definición demasiado corta o larga, «hemos probado», término duplicado o clave desconocida;
  - el archivo real es válido y tiene al menos 45 términos;
  - la página renderiza un `div.term` por término con su `id`, las letras vacías desactivadas, el JSON-LD `DefinedTermSet` válido, y es indexable con más de 300 palabras;
  - el índice de búsqueda contiene los términos con ancla;
  - `check.py` detecta un ancla de glosario inexistente;
  - `glossary.js` no usa `innerHTML` y pesa ≤ 2 KB comprimido;
  - «Empieza aquí» enlaza el glosario.
- **Navegador** a 375 y 1440 px:
  - filtrar por texto, con tilde y sin ella, y por alias («LLM»);
  - chips de tema;
  - sin resultados;
  - saltos por letra;
  - abrir `/glosario/#token` desde el buscador;
  - sin scroll horizontal ni errores de consola.

## 6. Fuera de alcance

- Páginas individuales por término.
- Enlazar automáticamente los términos dentro de los artículos (tooltips).
- Traducciones.
- Un enlace en el menú principal (ya tiene 6 elementos; se llega por «Empieza aquí», el buscador y el pie).
