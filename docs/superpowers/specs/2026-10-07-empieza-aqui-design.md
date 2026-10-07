# Radar IA — «Empieza aquí»

Fecha: 2026-10-07 · Rama: `empieza-aqui` · Maqueta: `_preview/maquetas/8-empieza-aqui.html` (fuera del repo), **A + B combinadas** · Proyecto «Secciones nuevas», parte 1 de 6 (orden: Empieza aquí → Glosario → X vs Y → Profesiones → Prompts → Historial de precios).

## 1. Objetivo

Una página para quien llega sin saber por dónde empezar. Le lleva a las páginas de Radar IA que le sirven (asistente, comparador, comparativas, guías, utilidades y noticias). Ordena la navegación, aumenta las páginas vistas por visita y es contenido propio con valor (Google y AdSense).

**Decisión del titular:** A + B combinadas:
- arriba, 4 tarjetas «¿Cuál es tu situación?»;
- debajo, la ruta «Tu primera semana con la IA» en 5 pasos.

**Criterio de éxito:**
- Todos los enlaces apuntan a páginas que existen; si no, el build falla.
- Funciona sin JS y se ve bien a 375 y 1440 px.
- La página es indexable y supera las 300 palabras.
- Los tests, el build y `check.py` están en verde.

## 2. Datos editoriales: `data/empieza.json`

```json
{
  "situaciones": [
    {"emoji": "🌱", "titulo": "Nunca he usado la IA", "texto": "Lo básico para empezar con buen pie y sin miedo.",
     "enlaces": [{"texto": "La mejor IA gratis", "url": "/mejor-ia-gratis/"}, ...]},
    ...
  ],
  "pasos": [
    {"titulo": "Elige tu primera herramienta", "texto": "Responde 4 preguntas y te decimos cuál encaja contigo y por qué.",
     "cta": {"texto": "Hacer el test", "url": "/que-ia-necesito/"},
     "extra": [{"texto": "La mejor IA gratis", "url": "/mejor-ia-gratis/"}]},
    ...
  ]
}
```

- **Situaciones:** exactamente 4, cada una con 2–3 enlaces.
- **Pasos:** exactamente 5, cada uno con un `cta` y 0–3 `extra`.
- **Contenido inicial** (como en la maqueta, sin los «próximamente»):
  1. Entiende qué es la IA: guía de privacidad y comparativa gratis.
  2. Elige tu primera herramienta.
  3. Aprende a pedírselo bien: mejores prompts, generador y mejorador.
  4. Úsala en lo tuyo: guías de estudiar, empresas y automatizar.
  5. Compara y mantente al día: comparador y noticias.
- **Secciones futuras:** el glosario, las profesiones y los prompts **se añaden a este archivo cuando existan**, nunca antes.
- **Validación en el build** (`radar/start.py`, con error claro):
  - los recuentos;
  - los campos obligatorios no están vacíos;
  - cada `url` existe en el sitio (en `by_url`, o es una URL de listado como `/noticias/`);
  - sin URLs repetidas dentro de una misma tarjeta o paso.

## 3. Página `/empieza-aqui/`

- **Contenido:** `content/paginas/empieza-aqui.md` (tipo página e indexable), con unas 400 palabras propias:
  - a quién va dirigida Radar IA;
  - cómo usar la web (comparativas, fichas, guías, utilidades y noticias);
  - cómo trabajamos (sin pruebas propias salvo indicación, con fuentes y fecha de comprobación, y un enlace a Metodología);
  - preguntas frecuentes («¿Necesito pagar para usar IA?», «¿Es seguro?», «¿Cuál es la mejor para empezar?»).
- **Plantilla nueva** `start.html` (elegida por la URL en `template_for`):
  - eyebrow «Empieza aquí» y H1 «¿Por dónde *empiezo*?», con la entradilla de la descripción;
  - `section` «¿Cuál es tu situación?»: rejilla de 4 tarjetas (2 columnas, 1 en móvil) con emoji, `h3`, texto y lista de enlaces;
  - `section` «Tu primera semana con la IA»: un `ol` de 5 pasos, con número grande, `h3`, texto, enlaces `extra` y botón `cta`;
  - después, el cuerpo Markdown.
- **Estilos:** sección «16. Empieza aquí» en `radar.css`, con los tokens existentes. No lleva JS.

## 4. Puntos de entrada

- **Menú principal:** «Empieza aquí» como **primer** elemento, resaltado con una píldora de color de acento (`.nav-start`), y con `aria-current` cuando estás en ella. Solo aparece si la página existe en el build, para que las fixtures de test sigan sin enlaces rotos.
- **Portada:** debajo de los botones del hero, `<p class="hero-start">¿Nuevo en la IA? <a href="/empieza-aqui/">Empieza aquí →</a></p>`, también condicionado a que la página exista.
- **Buscador:** la página entra sola en el índice.

## 5. Pruebas

- **Python:**
  - validación: recuentos erróneos, URL inexistente, campo vacío y URL repetida (deben fallar); el archivo real es válido;
  - la página renderiza 4 tarjetas y 5 pasos, y todos sus enlaces son internos y existen;
  - es indexable y supera las 300 palabras;
  - el menú tiene «Empieza aquí» en primer lugar y la portada tiene la línea;
  - en la build de fixtures sin la página, ni el menú ni la portada la enlazan.
- **Navegador** a 375 y 1440 px:
  - el menú móvil sigue funcionando con 6 elementos;
  - sin scroll horizontal ni errores de consola.

## 6. Fuera de alcance

- Personalizar la página según la visita.
- Guardar el progreso de la ruta.
- Incluir secciones que todavía no existen.
