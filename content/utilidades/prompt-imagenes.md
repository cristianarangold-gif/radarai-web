titulo: Generador de prompts para imágenes con IA
descripcion: Crea prompts visuales detallados para Midjourney, ChatGPT, Gemini o Firefly: sujeto, estilo, composición, cámara, iluminación, ambiente, formato y elementos a evitar.
script: /herramientas-radar/app.js

Los generadores de imágenes responden mejor a descripciones visuales completas. Esta utilidad te guía campo a campo para construir un prompt de imagen detallado.

<div class="utility-app" data-tool="prompt-imagenes" markdown="0">
<form id="radar-form" class="utility-grid"></form>
<div class="actions"><button id="run-tool" class="btn primary" type="button">✦ Crear prompt visual</button><button id="sample-tool" class="btn secondary" type="button">Probar ejemplo</button><button id="clear-tool" class="btn secondary" type="button">Limpiar</button></div><div class="result"><div class="result-head"><h2>Prompt visual</h2><div id="radar-meta" class="meta">Listo para empezar.</div><button id="copy-output" class="btn secondary" type="button">Copiar</button></div><pre id="radar-output">Aquí aparecerá tu prompt y negative prompt.</pre></div>
</div>

## Para qué sirve

Pedir «una imagen bonita de una playa» deja casi todo al azar. Los mejores resultados en herramientas como [Midjourney](/herramientas/midjourney/), [ChatGPT](/herramientas/chatgpt/), [Gemini](/herramientas/gemini/) o Adobe Firefly llegan cuando describes la escena como lo haría un fotógrafo o un director de arte. Este generador estructura tu idea en los elementos que más influyen en el resultado.

## Cómo usarlo paso a paso

1. **Sujeto o escena**: qué aparece y qué está ocurriendo.
2. **Estilo visual**: fotografía documental, acuarela, ilustración plana, 3D…
3. **Composición**: primer plano, plano general, vista cenital, regla de los tercios.
4. **Cámara**: tipo de objetivo o efecto (gran angular, desenfoque de fondo).
5. **Iluminación**: luz natural de mañana, atardecer, estudio, neón.
6. **Ambiente**: tranquilo, enérgico, nostálgico, misterioso.
7. **Formato**: horizontal, vertical o cuadrado, según dónde vayas a usar la imagen.
8. **Evitar**: elementos que no quieres que aparezcan (texto, personas, marcas de agua).

Pulsa **Crear prompt visual** y copia el prompt en tu herramienta. Si el resultado no encaja, cambia un solo campo cada vez para entender qué afecta a la imagen. Solo el sujeto es obligatorio.

## Qué genera

El resultado tiene dos partes:

1. **El prompt**: una frase con el sujeto seguida de los detalles visuales separados por comas, en este orden: estilo, composición, cámara, iluminación, ambiente y formato.
2. **NEGATIVE PROMPT**: la lista de lo que quieres evitar.

Si dejas un campo vacío, se rellena con un valor neutro para que el prompt quede completo:

| Campo vacío | Valor que se usa |
|---|---|
| Estilo visual | estilo cinematográfico |
| Composición | composición equilibrada |
| Cámara | profundidad de campo natural |
| Iluminación | iluminación cuidada |
| Ambiente | atmósfera envolvente |
| Formato | 16:9 |
| Evitar | texto, marcas de agua, baja resolución, deformaciones, anatomía incorrecta |

## Ejemplo

Con el sujeto «Una ciudad futurista bajo la lluvia», estilo «fotografía nocturna», iluminación «neón reflejado en el asfalto mojado» y formato «9:16», obtienes un prompt como: «Una ciudad futurista bajo la lluvia. Fotografía nocturna, composición equilibrada, profundidad de campo natural, neón reflejado en el asfalto mojado, atmósfera envolvente, formato 9:16», seguido de la lista de elementos a evitar.

## Cómo usar la parte «Evitar» en cada herramienta

No todas las herramientas tratan igual lo que no quieres en la imagen:

- **Midjourney**: tiene un parámetro propio para excluir elementos, `--no`, que se añade al final del prompt (por ejemplo, `--no texto, marcas de agua`). Escribe los elementos sin la palabra «sin».
- **ChatGPT, Gemini y otros asistentes conversacionales**: no tienen un campo aparte. Copia el prompt y añade al final una frase como «Evita: texto, marcas de agua…».
- **Herramientas con un campo «negativo»**: algunas aplicaciones de generación de imágenes tienen una casilla específica; pega ahí la lista.

El formato funciona de forma parecida: en Midjourney se indica con el parámetro `--ar` (por ejemplo, `--ar 9:16`), y en los asistentes conversacionales basta con pedir «formato vertical 9:16».

## Consejos

- **Sé concreto con la luz y el encuadre**: suelen ser de los elementos que más cambian el resultado.
- **No pidas demasiadas cosas en una sola escena**: dos o tres elementos principales suelen funcionar mejor que diez.
- **Describe, no ordenes**: «una taza de café humeante sobre una mesa de madera» funciona mejor que «haz una foto de café».
- **El texto dentro de la imagen puede salir con errores**: si necesitas un cartel o un título exacto, es más seguro añadirlo después con un editor como Canva.
- **Respeta los derechos**: evita imitar a artistas concretos, marcas o personas reales.

Compara herramientas en [la mejor IA para crear imágenes](/mejor-ia-para-imagenes/) y aprende más técnicas en la guía de [cómo escribir buenos prompts](/guias/mejores-prompts/).

La utilidad funciona por completo en tu navegador y no guarda lo que escribes.

## Preguntas frecuentes

### ¿En qué idioma escribo el prompt de imagen?

Los principales generadores entienden el español. Si una herramienta no interpreta bien algún término, prueba a escribir solo ese detalle en inglés.

### ¿Tengo que registrarme o pagar?

No. La utilidad es gratuita, no requiere cuenta y funciona directamente en tu navegador.
