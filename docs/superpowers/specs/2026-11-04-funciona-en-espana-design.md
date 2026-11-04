# Radar IA — «¿Funciona en España?»

Fecha: 2026-11-04 · Rama: `funciona-en-espana` · Maqueta: `_preview/maquetas/17-funciona-en-espana.html` (fuera del repo), **diseño 1 · Tabla con buscador**.

## 1. Objetivo

Una página donde un lector compruebe rápido si puede usar una función de IA en España, con su estado en EE. UU., la UE y España, la fecha de comprobación y la fuente.

**Decisiones del titular:** tabla con buscador; datos en un archivo revisado; la rutina de noticias propone los cambios por PR y el titular decide con Merge.

**Criterio de éxito:**

- Mínimo de **12 funciones** comprobadas al publicar, con objetivo de 20–25. Solo entra lo que tenga fuente oficial.
- Ningún estado se deduce: si la fuente no lo aclara, es «Sin confirmar».
- Funciona sin JS (tabla completa), en móvil, en claro y en oscuro.
- Tests, build y `check.py` en verde. Sin cambios en precios, anuncios ni menú principal.

**Fuera de alcance:** Latinoamérica (desde España no se puede comprobar bien lo que se ve allí), alertas por correo, lectura automática de webs y entrada en el menú principal mientras AdSense revisa.

## 2. Datos

Archivo `data/disponibilidad.md`, un bloque por función, con el estilo de `data/glosario.md`:

```
## Siri con IA en español
id: siri-ia-espanol
empresa: apple
ficha:
eeuu: si
ue: no
es: no
nota: No disponible en iOS, iPadOS ni watchOS en la UE.
comprobado: 2026-11-04
fuentes: https://www.apple.com/...
noticia: /noticias/siri-ai-espanol-ios-27-2/
```

| Campo | Regla |
|---|---|
| Título (`##`) | Obligatorio y único |
| `id` | Obligatorio, único, en minúsculas con guiones. Es el ancla de la fila |
| `empresa` | Obligatorio; clave de la lista `OFICIALES` de `radar/availability.py` (empresa → dominios oficiales). Una empresa nueva se añade a la lista expresamente |
| `ficha` | Opcional; id de una ficha indexable |
| `eeuu`, `ue`, `es` | Obligatorios; `si`, `parcial`, `no` o `sin_confirmar` |
| `nota` | Máximo 30 palabras. Obligatoria si algún estado es `parcial` |
| `comprobado` | Obligatorio; AAAA-MM-DD, no futura |
| `fuentes` | De 1 a 3 URL `https`, separadas por comas: dominio oficial de la empresa o copia suya en web.archive.org. Prensa no |
| `noticia` | Opcional; URL de una noticia indexable |

**Coherencia que comprueba el build:** si `ue` es `no`, `es` debe ser `no`. Cualquier error de validación detiene el build e indica el bloque.

**Reglas editoriales (las aplica quien redacta y las revisa el titular):**

- `no` solo si la empresa lo dice o la función se limita expresamente a otros países.
- Que algo esté en la UE no significa que esté en España: si la fuente solo habla de «la UE» sin incluirla entera de forma expresa, `es` es `sin_confirmar`.
- Las limitaciones de idioma, plan o dispositivo van en `nota`.

## 3. Módulo

`radar/availability.py`, independiente de otros módulos salvo para leer fichas y URL:

- `parse_availability(text) -> List[Feature]`.
- `validate_availability(features, fichas, site_urls, today) -> None`: lanza `ValueError`.
- `availability_context(features, today) -> dict`: filas ordenadas, recuentos, última fecha de comprobación y filas agrupadas por ficha.

**Orden de las filas:** primero por estado en España (`no`, `parcial`, `sin_confirmar`, `si`) y después por título.

**Antigüedad:** una fila con más de 60 días desde `comprobado` en el momento del build lleva el aviso «Pendiente de revisar». No detiene el build, para no bloquear las noticias diarias, y el build lista esas filas por consola.

`scripts/build.py` carga el módulo cuando existe `content/paginas/funciona-en-espana.md` y falla si falta el archivo de datos, como ya ocurre con el glosario.

## 4. Página

URL `/funciona-en-espana/`, con `content/paginas/funciona-en-espana.md` y plantilla `templates/availability.html`.

- **Cabecera:** como en la maqueta, con el texto «Última comprobación: …» y el número de funciones.
- **Controles:** buscador y filtros Todas, No disponibles, Parciales, Sin confirmar y Disponibles, referidos al estado en España. Llevan `hidden` en el HTML y `static/js/availability.js` los muestra. El script solo muestra u oculta filas, sin `innerHTML`, y anuncia con `aria-live` cuántas filas quedan o que no hay resultados.
- **Tabla:** función, empresa y nota; EE. UU.; UE; España; comprobado y fuente. Con `caption` y `scope`. En móvil, cada fila pasa a ficha apilada, como en la maqueta.
- **Estados:** texto más icono, nunca solo color. Disponible (✓), Parcial (◐), No disponible (✕), Sin confirmar (?). Cada fila tiene `id` para enlazarla, y su enlace a ficha o noticia si existe.
- **Texto propio** bajo la tabla: qué significa cada estado, cómo comprobamos los datos, por qué algo llega antes a otros países, y preguntas frecuentes. Debe superar el mínimo de palabras de `check.py`. Sin consejos legales.
- **Colores:** tokens nuevos `--avail-{si,parcial,no,duda}-{bg,fg}` en los dos bloques oscuros de `static/css/radar.css`, con contraste AA en `tests/test_theme.py`.
- **Anuncios:** la página sigue las reglas generales; no añade huecos propios.

## 5. Entradas

- **Portada:** una línea enlazada.
- **Empieza aquí:** un enlace en `data/empieza.json`.
- **Fichas:** recuadro «Disponibilidad en España» en `templates/tool.html`, con hasta 3 funciones de esa ficha, solo si tiene alguna.
- **Noticias:** el redactor enlaza la fila cuando la noticia trate de disponibilidad.
- **Buscador del sitio:** cada función entra en el índice con el tipo «Disponibilidad» y la URL `/funciona-en-espana/#id`.
- **Sitemap:** automático, como las demás páginas.

## 6. Mantenimiento

- **`docs/rutina-noticias.md` y el resumen de la rutina en la nube:** si la noticia confirma un cambio de disponibilidad de una función del archivo, o de una función nueva con fuente oficial, actualizar o añadir el bloque en el mismo PR, con la nueva fecha, y decirlo en el cuerpo del PR. Si no hay confirmación oficial, no se toca.
- **`content/GUIA_EDITORIAL.md`:** regla 13 con las reglas de la sección 2.
- La rutina nunca fusiona: el titular decide con Merge.

## 7. Tests

`tests/test_availability.py`:

- Lectura de bloques y cada error de validación: campo ausente, estado desconocido, `id` o título repetido, empresa o ficha desconocidas, fecha futura, dominio no oficial, prensa como fuente, copia archivada de otra web, nota ausente con `parcial`, nota demasiado larga, noticia inexistente y `ue: no` con `es` distinto de `no`.
- Orden de las filas y aviso a los 60 días, justo en el límite.
- En los datos reales: al menos 12 funciones.
- En el sitio construido: la página existe con tabla completa sin JS, controles `hidden`, anclas de fila, función en el índice de búsqueda, recuadro en una ficha con datos y ausente en una sin datos, enlace en portada y en Empieza aquí.
- `availability.js` no usa `innerHTML`.

**Navegador:** buscador, filtros, sin resultados, móvil y 1280 px, claro y oscuro.

## 8. Partes

1. **Datos y validador:** investigación de fuentes oficiales, `data/disponibilidad.md`, `radar/availability.py` y sus tests. Tabla de lo encontrado para revisar.
2. **Página:** plantilla, CSS, JS y texto propio. Vista previa.
3. **Entradas y mantenimiento:** portada, Empieza aquí, fichas, búsqueda, guía y rutina.
4. **Cierre:** revisión independiente (opus), correcciones y PR. Se fusiona solo con el OK del titular, y entonces se actualiza la rutina en la nube.
