titulo: NVIDIA y Microsoft presentan RTX Spark: portátiles Windows para ejecutar IA y agentes en local
descripcion: Surface Laptop Ultra y otros portátiles con el chip RTX Spark llegan en octubre. Qué ofrecen, cuánto cuestan (en dólares) y qué son los Execution Containers de Windows 11.
fecha: 2026-10-08
empresa: nvidia
herramientas: copilot, github-copilot
fuentes: https://blogs.nvidia.com/blog/local-ai-rtx-spark-microsoft-windows-event/
    https://techcrunch.com/2026/10/07/microsoft-releases-new-nvidia-chip-ai-pcs-with-revamped-windows-11/

NVIDIA y Microsoft presentaron el 7 de octubre de 2026, en un evento en San Francisco, una nueva generación de ordenadores Windows pensados para ejecutar modelos de IA y agentes **en el propio equipo**, sin depender de la nube. La pieza central es **RTX Spark**, un chip de NVIDIA que combina GPU y CPU, y que fabricantes como Acer, ASUS, Dell, HP, Lenovo, MSI, Gigabyte y la propia Microsoft llevarán a portátiles y sobremesas compactos.

## Qué ha anunciado NVIDIA y Microsoft

**El chip y los equipos.** Según NVIDIA, RTX Spark une una GPU Blackwell RTX de hasta 6.144 núcleos con una CPU Grace de hasta 20 núcleos, conectadas entre sí a 600 GB/s. Ofrece hasta 128 GB de memoria unificada y, siempre según la compañía, hasta un petaflop de rendimiento de IA en FP4. Son cifras del fabricante que no hemos podido contrastar de forma independiente.

**Calendario.** Las reservas de portátiles se abrieron el 7 de octubre y los equipos llegarán el 16 de octubre. Los sobremesas compactos, diseñados para funcionar las 24 horas como sistema de IA dedicado, saldrán en noviembre.

**Surface Laptop Ultra.** Es el portátil de Microsoft construido sobre RTX Spark. Según TechCrunch, hay dos modelos base: uno desde 2.600 dólares y otro, con un chip más potente, desde 3.700 dólares. Con más memoria y almacenamiento el precio sube hasta 5.900 dólares. Microsoft también presentó una estación de trabajo, la Surface RTX Spark Dev Box, desde 6.000 dólares, con herramientas como VS Code, GitHub Copilot CLI, WSL y PowerShell 7. Dell, por su parte, ofrece el XPS 16 Creator Edition en reserva por 3.800 dólares en Estados Unidos.

**DGX Station para Windows.** NVIDIA presentó en versión preliminar una máquina de sobremesa con 748 GB de memoria coherente y hasta 20 petaflops de IA en FP4, pensada para empresas que quieran ajustar y ejecutar modelos enormes en local. No se han dado precio ni fecha.

**Execution Containers.** Microsoft anunció la disponibilidad general de estos contenedores, una capa del sistema operativo para que los agentes de IA se ejecuten en segundo plano de forma aislada, observable y controlada. Satya Nadella aseguró que estará disponible para todos los usuarios de Windows 11, no solo para los de los equipos nuevos.

## Por qué importa en España y Latinoamérica

Para quien trabaja con IA en Europa y Latinoamérica, la gran promesa de ejecutar modelos en local es la **privacidad**: los datos no salen del ordenador, algo relevante para despachos, clínicas o pymes sujetas al RGPD o a leyes locales de protección de datos. NVIDIA añade que el uso local no tiene cuotas por consulta, aunque el equipo hay que pagarlo por adelantado. Si te interesa el tema, tenemos una [guía sobre privacidad en IA](/guias/privacidad-en-ia/).

Hay un matiz importante: **ni NVIDIA ni TechCrunch indican en qué países se venderán estos equipos**, y todos los precios publicados están en dólares. No sabemos todavía si llegarán a España ni a qué precio en euros, ni si habrá distribución oficial en Latinoamérica. Conviene esperar a que los fabricantes confirmen disponibilidad y tarifas locales antes de planificar una compra.

## Qué cambia en la práctica

- **Para el usuario normal, casi nada de momento.** Son equipos de gama muy alta, con precios que parten de unos 2.600 dólares, y orientados a desarrolladores, creadores y entusiastas.
- **Para desarrolladores.** El entorno CUDA completo y la compatibilidad con WSL permiten, según NVIDIA, mover modelos y flujos de trabajo hacia estaciones DGX sin reescribirlos. Quienes ya usen [GitHub Copilot](/herramientas/github-copilot/) encontrarán su versión de línea de comandos preinstalada en la Dev Box.
- **Para todos los usuarios de Windows 11.** Los Execution Containers pueden ser lo más relevante a medio plazo: si los desarrolladores los adoptan, los agentes que actúen sobre tu ordenador lo harán con más aislamiento. Microsoft también dice que abrirá a aplicaciones de terceros la orquestación y la memoria de agentes, no solo a las suyas, algo que afecta a asistentes como [Microsoft Copilot](/herramientas/copilot/).
- **Rendimiento.** NVIDIA afirma que un modelo local de 125.000 millones de parámetros «iguala la inteligencia de muchos modelos en la nube» y que los juegos AAA corren a más de 100 fps en 1440p con DLSS 5. Son afirmaciones del fabricante; faltan análisis independientes.

## La opinión de Radar IA

La idea de un ordenador capaz de ejecutar modelos grandes sin conexión es atractiva, pero hoy es una propuesta cara y todavía sin precio ni fecha para el mercado hispanohablante. Lo que sí parece un cambio real es el apartado de seguridad: dar a los agentes un espacio aislado dentro de Windows es una condición casi imprescindible si vamos a dejarles actuar por nosotros.

Nuestro consejo: no compres nada hasta ver reseñas independientes y precios en euros. Si ya tienes un buen equipo, los Execution Containers deberían llegarte sin cambiar de hardware; y para la mayoría de las tareas diarias, un asistente en la nube sigue siendo más barato que un portátil de más de 2.500 dólares.

*Fuentes consultadas: el blog de NVIDIA y la cobertura de TechCrunch, ambos del 7 de octubre de 2026. Las cifras de rendimiento y los precios proceden de ellas y no los hemos verificado de forma independiente.*
