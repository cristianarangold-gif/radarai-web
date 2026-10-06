# Radar IA — Rediseño para aprobación de AdSense

Fecha: 2026-10-06 · Rama: `rediseno-adsense` · Dominio: https://radarai.es

## 1. Objetivo y criterio de éxito

**Objetivo:** que Google AdSense apruebe radarai.es y que la web pase a ser un medio
profesional en español sobre herramientas y noticias de IA, actualizado de forma continua.

**Motivo del rechazo (AdSense, oct. 2026):** «Contenido de poco valor».

**Diagnóstico medido (texto visible por página, sin menú ni pie):**

| Sección | Páginas | Palabras (media) |
|---|---|---|
| `herramientas/*` | 135 | 54 (plantilla idéntica) |
| `noticias/*` | 7 | 53 (solo enlazan a la fuente) |
| `guias/*` | 6 | 31 |
| Secciones vacías (rankings, reviews, precios, alternativas, cambios, mejor-ia, publicacion, preguntas-frecuentes) | 8 | ~45 |
| `mejor-ia-para-*` | 9 | 200–350 |
| Portada | 1 | 1.865 |

173 de 182 páginas tienen menos de 300 palabras.

**Defectos técnicos detectados:**
- El workflow «Build Radar IA public pages» falla siempre: compara `'<!DOCTYPE html>'` con el texto en mayúsculas.
- Además reescribe el HTML publicado en cada push y hace commit sobre `main`.
- 105 fichas muestran escapes literales (`vídeo`).
- La rama `publicacion-zip-exacta` tiene commits de prueba (`probe`, `foo`, `tmp2`).
- No hay CMP certificado: el banner de cookies es casero.

**Criterio de éxito (cuándo se pide revisión):**
1. Todas las páginas indexables tienen ≥ 800 palabras útiles (fichas ≥ 1.000; guías y comparativas ≥ 1.200). Excepción: las páginas legales y de contacto.
2. Ninguna página indexable es una plantilla casi duplicada.
3. Hay al menos 35 páginas indexables de calidad.
4. Se publican noticias con análisis propio durante ≥ 3 semanas seguidas, con 3–5 por semana.
5. El CMP de Google está activo y el workflow de build está en verde.
6. Search Console no muestra errores de cobertura en el sitemap.

## 2. Principios editoriales (no negociables)

- **Valor propio:** cada página responde a una necesidad concreta del lector hispanohablante: qué herramienta elegir, cuánto cuesta, cómo usarla y qué limitaciones tiene. No basta con describir el producto.
- **Honestidad:** nunca se afirma «lo hemos probado» si no es verdad. El contenido de investigación se marca como tal («según la documentación oficial a fecha X»). Las pruebas propias del autor se añaden en bloques «Nuestra prueba», que **solo el titular rellena**.
- **Fuentes y fechas:** cada ficha, guía y noticia muestra la fecha de actualización y enlaza a sus fuentes. Los precios llevan la fecha de comprobación.
- **Sin copia:** se resume con palabras propias. Las citas literales son de como máximo una frase y van atribuidas.
- **Autor real:** hay una página de autor con nombre, biografía y contacto, que la firma de cada artículo enlaza (E-E-A-T).

Estas reglas se guardan en `content/GUIA_EDITORIAL.md` y las aplican también los borradores automáticos.

## 3. Arquitectura técnica

### 3.1 Generador estático propio (Python)
El HTML escrito a mano, con el CSS duplicado en cada archivo, se sustituye por:

```
content/            # Markdown con front-matter (título, descripción, fecha, autor, fuentes)
  herramientas/     # una ficha por archivo
  mejor-ia/         # comparativas "mejor IA para…"
  guias/
  noticias/
  paginas/          # sobre, metodología, autor, legal
data/
  tools.json        # catálogo completo (los 135 registros actuales, corregidos)
  news_sources.yml  # fuentes RSS de la recogida diaria
  redirects.yml     # URL antigua -> URL nueva
templates/          # Jinja2: base, ficha, comparativa, guía, noticia, portada, listados
static/             # un solo CSS y un JS pequeño (buscador/filtros del catálogo)
scripts/
  build.py          # content + data + templates -> _site/
  check.py          # validaciones (sustituye las del workflow roto)
  news_collect.py   # recogida diaria de candidatas
```

- **Dependencias:** `jinja2` y `markdown`, nada más.
- **Salida:** `_site/`, sin versionar en git.
- **Despliegue:** workflow `deploy.yml`: en push a `main` ejecuta build, luego check, y publica con `actions/deploy-pages`. El workflow nunca hace commits.
- **Cambio en GitHub Pages:** el origen pasa de «rama main /» a «GitHub Actions». Es un ajuste del repositorio y se hace con la confirmación del titular.
- **Workflows eliminados:** `site-refresh.yml` y `sitemap-cleanup.yml`. Su trabajo pasa a `build.py`.

### 3.2 Lo que genera `build.py`
- **Por página:** canonical, `<meta description>` propia, Open Graph y JSON-LD (`Article`/`NewsArticle` con autor y fechas; `SoftwareApplication` en fichas; `BreadcrumbList`).
- **Sitemap:** `sitemap.xml` solo con páginas indexables, con `lastmod` real.
- **Feed:** `rss.xml` de noticias.
- **Redirecciones:** las URL retiradas se convierten en páginas de redirección (`meta refresh` + canonical al destino + `noindex`), ya que GitHub Pages no admite 301.
- **Fichas no completadas:** de las 135 herramientas solo se genera página para las que tienen ficha completa en `content/herramientas/`. El resto aparece en el catálogo de la portada con enlace a su web oficial, sin página propia.

### 3.3 `check.py` (bloquea el despliegue si falla)
- Cada página tiene DOCTYPE (comprobación correcta), title, description única, canonical y `lang="es"`.
- No hay enlaces internos rotos.
- No aparecen secuencias `\uXXXX` literales en el texto.
- Las páginas indexables cumplen el mínimo de palabras del §1. Si no llegan, deben marcarse `noindex` explícitamente.
- No hay títulos ni descripciones duplicados.
- El sitemap solo incluye páginas indexables.

## 4. Contenido

### 4.1 Recorte (fase 1)
| Actual | Destino |
|---|---|
| 135 fichas plantilla | Se retiran; quedan las 15 completas del §4.2. Las demás URL redirigen a la categoría correspondiente |
| rankings, reviews, precios, alternativas, cambios, mejor-ia, publicacion, preguntas-frecuentes | Se fusionan: «mejor-ia» pasa a ser el índice de comparativas y las FAQ van a la portada. El resto redirige a la portada o al índice más cercano |
| 6 guías de ~31 palabras | Se reescriben (§4.2) o se retiran |
| 7 noticias sin cuerpo | Se reescriben con análisis o se retiran |
| `herramientas-radar/*` (9) | Se revisan una a una: se fusionan con la comparativa equivalente o se retiran |

### 4.2 Contenido núcleo (fase 2)
- **Comparativas «Mejor IA para…» (9):** escribir, estudiar, imágenes, marketing, productividad, programar, vídeo, gratis y crear música. Cada una con 1.200–1.800 palabras, que incluyen:
  - criterios de elección y tabla comparativa con precio y fecha;
  - opción recomendada por perfil (estudiante, autónomo, empresa);
  - limitaciones, privacidad y alternativas gratuitas;
  - preguntas frecuentes, fuentes y bloque «Nuestra prueba».
- **Fichas completas (15):** ChatGPT, Claude, Gemini, Microsoft Copilot, Perplexity, Midjourney, Runway, Suno, ElevenLabs, GitHub Copilot, Cursor, Canva IA, DeepL, Notion AI y NotebookLM. Cada una con ≥ 1.000 palabras:
  - qué es y para quién es;
  - planes y precios en EUR con fecha;
  - funciones clave, casos de uso con ejemplos de prompts y límites;
  - privacidad y uso de datos;
  - alternativas y veredicto.
- **Guías prácticas (6):** cómo escribir buenos prompts, automatizar tareas, crear presentaciones, IA para estudiar sin plagiar, IA en la pequeña empresa y privacidad al usar IA. Cada una ≥ 1.200 palabras.
- **Páginas de confianza:**
  - Sobre Radar IA.
  - Metodología: cómo se evalúa y la diferencia entre investigación y prueba propia.
  - Autor.
  - Política editorial y de correcciones.
  - Contacto.
  - Legales actualizadas.
- Los datos (precios, planes, funciones) se investigan en fuentes oficiales en el momento de escribir. Nada se toma de memoria.

**Total en el lanzamiento:** unas 40 páginas indexables más las noticias.

### 4.3 Portada
- Se reescribe con propuesta de valor clara, últimas noticias, comparativas destacadas y catálogo filtrable (datos de `tools.json`). El JS de favoritos, comparador y valoraciones locales solo se mantiene si funciona y aporta valor.
- Se elimina el contenido «de relleno» y los textos del tipo «FASE X».

## 5. Noticias semiautomáticas (opción A)

1. **Recogida automática diaria:** workflow `news-collect.yml`, todos los días a las 07:00 (hora de Madrid).
   - `news_collect.py` lee las fuentes de `data/news_sources.yml`: blogs oficiales de OpenAI, Anthropic, Google/DeepMind, Meta AI, Microsoft, Mistral, Hugging Face, Apple ML, NVIDIA y medios de referencia en inglés y español.
   - Descarta duplicados con `data/news_seen.json`.
   - Abre una issue «Candidatas AAAA-MM-DD» con 5–10 candidatas: título, fuente, enlace y motivo de interés.
2. **Redacción asistida:** una rutina programada de Claude (o una sesión a demanda) elige 1–2 candidatas, investiga la fuente original y redacta la noticia en `content/noticias/`. La noticia sigue la `GUIA_EDITORIAL`, con 500–900 palabras:
   - qué ha pasado;
   - por qué importa a un usuario hispanohablante;
   - qué cambia en la práctica (precio, disponibilidad en España o la UE);
   - opinión de Radar IA y fuentes.

   El resultado se entrega como **pull request** en borrador.
3. **Revisión humana:** el titular lee el PR, añade su opinión si quiere y hace merge. El merge publica la noticia (deploy automático).
4. **Lo que nunca se hace:** publicar sin revisión, ni copiar o traducir artículos enteros.

## 6. Cumplimiento AdSense y anuncios

- **CMP:** el titular activa en AdSense > Privacidad y mensajes el mensaje de consentimiento del RGPD de Google (CMP certificado por el IAB TCF). Después se retira el banner de cookies casero para no mostrar dos.
- **Políticas:** la política de cookies y la de privacidad se actualizan para nombrar a Google como proveedor publicitario y el CMP.
- **Antes de la aprobación:** solo se mantiene el script de verificación de AdSense en el `<head>` de las páginas de contenido. No hay unidades de anuncio.
- **Después de la aprobación:** anuncios manuales mediante un componente de plantilla:
  - como máximo 3 por artículo: tras el 2.º o 3.er párrafo, a mitad y al final;
  - 1 en la barra lateral en escritorio;
  - nunca en páginas legales, de contacto ni 404;
  - espacio reservado para evitar saltos de diseño (CLS).

  Auto ads queda desactivado inicialmente.
- **`ads.txt`:** se mantiene tal cual (ya es correcto).
- **Search Console:** el titular verifica la propiedad del dominio, envía `sitemap.xml` y solicita la indexación de las páginas nuevas.

## 7. Fases y orden de ejecución

| Fase | Contenido | Resultado visible |
|---|---|---|
| 0 | Generador, plantillas, CSS único, `check.py`, `deploy.yml`, corrección de escapes, migración de los legales | La web se ve igual o mejor; workflow en verde |
| 1 | Recorte y redirecciones; sitemap solo con páginas indexables | Desaparecen las páginas vacías |
| 2 | Contenido núcleo (§4.2): 9 comparativas, 15 fichas, 6 guías y páginas de confianza | Unas 40 páginas sólidas |
| 3 | Recogida de noticias, rutina de redacción y 6–8 noticias iniciales con análisis | Sección de noticias viva |
| 4 | CMP, legales, Search Console y componente de anuncios desactivado | Web lista para la revisión |
| 5 | Rodaje de ≥ 3 semanas publicando y después solicitud de revisión en AdSense | Solicitud enviada |

Cada fase se entrega como PR desde `rediseno-adsense` (o sub-ramas). No se publica en `main` sin el visto bueno del titular.

## 8. Acciones que solo puede hacer el titular

- Aportar los datos del autor: nombre público, foto opcional, biografía breve y experiencia con IA.
- Rellenar los bloques «Nuestra prueba» con pruebas reales (opcional, pero mejora mucho la calidad percibida).
- Cambiar el origen de GitHub Pages a «GitHub Actions», o autorizar que se haga vía `gh`.
- Activar el CMP en AdSense y verificar Search Console.
- Revisar y fusionar los PR de contenido y noticias.
- Pulsar «Solicitar revisión» en AdSense al final de la fase 5.

## 9. Fuera de alcance (por ahora)

Newsletter real, valoraciones globales de usuarios, Google Analytics, versión en inglés y monetización por afiliación. Se reconsideran después de la aprobación de AdSense.
