// Utilidades de Radar IA: todo se calcula en el navegador; no se envía ni se guarda nada.
(() => {
  const $ = (s) => document.querySelector(s);
  const tool = document.body.dataset.tool || document.querySelector('[data-tool]')?.dataset.tool || '';
  const form = $('#radar-form');
  const out = $('#radar-output');
  const meta = $('#radar-meta');
  const v = (id) => (document.querySelector('#' + id)?.value || '').trim();
  const lines = (a) => a.filter(Boolean).join('\n');
  // Como lines(), pero conserva las líneas vacías ('') para separar bloques; omite false, null y undefined.
  const block = (a) => a.filter((x) => x !== false && x != null).join('\n');
  const list = (s) => s.split(/[,;\n]/).map((x) => x.trim()).filter(Boolean);
  const set = (t, m = '') => { if (out) out.textContent = t; if (meta) meta.textContent = m; };
  const clamp = (n, min, max, def) => Math.min(max, Math.max(min, Number.isFinite(n) ? n : def));
  const deaccent = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
  const WORD = /[\p{L}\p{N}][\p{L}\p{N}’'-]*/gu;
  // Palabras vacías del español: no cuentan como «repetidas» ni como hashtags amplios.
  const STOP = new Set(('a al algo algun alguna algunas alguno algunos ante antes aqui asi aun bajo bien cada como con contra cual ' +
    'cuales cuando de del desde donde dos el ella ellas ellos en entre era eran es esa esas ese eso esos esta estaba estan estas ' +
    'este esto estos fue fueron ha han hasta hay la las le les lo los mas me mi mis mucho muy nada ni no nos nuestra nuestro o os ' +
    'otra otro para pero poco por porque que quien se sea segun ser si sin sobre son su sus tambien tan tanto te tiene tienen ' +
    'todo todos tu tus un una unas uno unos y ya yo vez puede pueden hacer hace sido estar').split(' '));
  const ARTICLES = new Set(['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas']);
  const words = (s) => s.match(WORD) || [];
  const isStop = (w) => STOP.has(deaccent(w.toLowerCase()));

  const fields = {
'generador-de-prompts':[['objetivo','Objetivo','Qué quieres conseguir','ta'],['contexto','Contexto','Datos y antecedentes','ta'],['audiencia','Audiencia','Para quién es','text'],['formato','Formato','Tabla, pasos, guion, JSON…','text'],['tono','Tono','Profesional, cercano, técnico…','text'],['restricciones','Restricciones','Límites y requisitos','ta']],
'mejorador-de-prompts':[['objetivo','Prompt actual','Pega el prompt que quieres mejorar','ta'],['contexto','Contexto adicional','Información útil','ta'],['audiencia','Audiencia','Destinatario','text'],['modelo','Uso o modelo','Chat, imagen, vídeo, código…','text'],['formato','Formato deseado','Cómo debe responder','text']],
'generador-de-titulos':[['tema','Tema o contenido','Describe el contenido','ta'],['plataforma','Plataforma','YouTube, TikTok, blog…','text'],['audiencia','Audiencia','A quién quieres atraer','text'],['palabras','Palabras clave','Separadas por comas','text'],['tono','Tono','Curioso, experto, emocional…','text']],
'generador-de-ideas':[['tema','Tema o nicho','Ej.: IA, fitness, educación…','ta'],['objetivo','Objetivo','Educar, vender, entretener…','text'],['plataforma','Plataforma','TikTok, YouTube, blog…','text'],['audiencia','Audiencia','Perfil del público','text'],['cantidad','Cantidad','5–20','number']],
'generador-de-hashtags':[['tema','Tema','Ej.: receta de bizcocho sin gluten','text'],['nicho','Nicho','Comunidad o subtema, separados por comas','text'],['audiencia','Audiencia','Público objetivo','text'],['cantidad','Cantidad','5–30','number']],
'contador-de-palabras':[['texto','Texto','Pega el texto','ta']],
'descripcion-video':[['tema','Tema o título','Qué contiene el vídeo','ta'],['plataforma','Plataforma','YouTube, TikTok…','text'],['audiencia','Audiencia','Público objetivo','text'],['keywords','Palabras clave','Separadas por comas','text'],['cta','Llamada a la acción','Suscríbete, comenta…','text'],['tono','Tono','Educativo, cercano…','text']],
'prompt-imagenes':[['sujeto','Sujeto o escena','Qué debe aparecer','ta'],['estilo','Estilo visual','3D, fotografía, ilustración…','text'],['composicion','Composición','Primer plano, plano general…','text'],['camara','Cámara','35mm, 85mm, profundidad…','text'],['luz','Iluminación','Neón, estudio, hora dorada…','text'],['ambiente','Ambiente','Emoción, clima, colores…','text'],['formato','Formato','9:16, 16:9, 1:1…','text'],['negativos','Evitar','Texto, deformaciones…','text']],
  };
  const cfg = fields[tool] || [];
  if (form) {
    for (const [id, label, ph, type] of cfg) {
      const box = document.createElement('div');
      box.className = 'field' + (type === 'ta' ? ' field-wide' : '');
      const lab = document.createElement('label');
      lab.htmlFor = id;
      lab.textContent = label;
      const input = document.createElement(type === 'ta' ? 'textarea' : 'input');
      input.id = id;
      input.placeholder = ph;
      if (type !== 'ta') input.type = type === 'number' ? 'number' : 'text';
      box.append(lab, input);
      form.append(box);
    }
  }

  // Contador de palabras: cifras, palabras repetidas y frases largas.
  const countText = (x) => {
    const w = words(x);
    const sentences = x.split(/(?<=[.!?…])\s+/).filter((s) => words(s).length);
    const f = sentences.length;
    const p = x.split(/\n\s*\n/).filter((s) => s.trim()).length;
    const long = sentences.filter((s) => words(s).length > 30).length;
    const freq = new Map();
    for (const word of w) {
      const k = word.toLowerCase();
      if (k.length >= 4 && !isStop(k)) freq.set(k, (freq.get(k) || 0) + 1);
    }
    const rep = [...freq].filter(([, n]) => n >= 2).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'es')).slice(0, 8);
    return block([
      `PALABRAS: ${w.length}`,
      `CARACTERES: ${x.length}`,
      `SIN ESPACIOS: ${x.replace(/\s/g, '').length}`,
      `FRASES: ${f}`,
      `PÁRRAFOS: ${p}`,
      `MEDIA POR FRASE: ${f ? (Math.round(w.length / f * 10) / 10).toLocaleString('es-ES') + ' palabras' : '—'}`,
      `FRASES DE MÁS DE 30 PALABRAS: ${long}`,
      `LECTURA: ${Math.max(1, Math.ceil(w.length / 200))} min`,
      `LOCUCIÓN: ${Math.max(1, Math.ceil(w.length / 130))} min`,
      '',
      'PALABRAS MÁS REPETIDAS',
      rep.length ? rep.map(([k, n]) => `${k} (×${n})`).join(' · ') : 'Ninguna palabra se repite 2 o más veces.',
    ]);
  };

  // Hashtags: frases de tus campos (específicos) y palabras sueltas (amplios), sin etiquetas fijas.
  // Las siglas en mayúsculas (IA, SEO, PYME) se respetan; el resto va con mayúscula inicial.
  const tagWord = (w) => {
    const plain = deaccent(w).replace(/[^A-Za-z0-9]/g, '');
    return plain.length <= 5 && plain === plain.toUpperCase() && /[A-Z]/.test(plain) ? plain : cap(plain.toLowerCase());
  };
  const toTag = (ws) => '#' + ws.map(tagWord).join('');
  const hashtags = () => {
    const phrases = [v('tema'), ...list(v('nicho')), ...list(v('audiencia'))].filter(Boolean);
    const specific = [];
    const broad = [];
    const seen = new Set();
    const add = (bucket, tag) => {
      const k = tag.toLowerCase();
      if (tag.length > 2 && !seen.has(k)) { seen.add(k); bucket.push(tag); }
    };
    for (const ph of phrases) {
      const ws = words(ph).filter((w) => !ARTICLES.has(w.toLowerCase()));
      const meaningful = ws.filter((w) => !isStop(w));
      if (meaningful.length >= 2 && ws.length <= 4) add(specific, toTag(ws));
      else if (ws.length > 4) {
        // Frase larga: trozos de 3 y 2 palabras que empiezan y acaban en palabra con significado.
        for (const size of [3, 2]) {
          for (let i = 0; i + size <= ws.length; i++) {
            const part = ws.slice(i, i + size);
            if (!isStop(part[0]) && !isStop(part[size - 1])) add(specific, toTag(part));
          }
        }
      }
      for (const w of meaningful) if (w.length >= 3 || /^\p{Lu}{2}$/u.test(w)) add(broad, toTag([w]));
    }
    return { specific, broad };
  };

  // Títulos: plantillas según el tono, sin afirmar pruebas propias.
  const TITLES = {
    general: ['Cómo empezar con {t}: guía paso a paso', '{T}: 7 claves que conviene conocer', 'Los errores más comunes con {t} (y cómo evitarlos)',
      '{T}: ¿merece la pena? Lo que debes saber antes', '{T}: explicación sencilla y sin tecnicismos', '5 ideas sobre {t} que puedes aplicar hoy',
      'Antes de empezar con {t}, lee esto', '{T}: preguntas frecuentes y respuestas claras'],
    curioso: ['Lo que casi nadie te cuenta sobre {t}', '{T}: 5 datos que quizá no conocías', '¿Qué pasa realmente con {t}?',
      'El detalle de {t} que lo cambia todo', '{T}, más allá de lo básico', 'La pregunta sobre {t} que todos se hacen'],
    experto: ['{T}: guía completa para profesionales', 'Cómo optimizar {t}: método en 5 pasos', '{T}: errores técnicos y cómo corregirlos',
      'Buenas prácticas de {t}, con ejemplos', '{T} a fondo: lo que marca la diferencia', 'Lista de comprobación de {t} para no dejarte nada'],
    emocional: ['{T}: el cambio que estabas buscando', '{T}: la forma de ponerte las cosas más fáciles', 'Deja de complicarte con {t}: empieza aquí',
      '{T} sin miedo: tu primer paso', '{T}: por fin, una explicación clara para ti', 'Lo que conviene saber antes de empezar con {t}'],
  };
  const toneOf = (s) => {
    const t = deaccent(s.toLowerCase());
    if (/curios|intrig|sorpre/.test(t)) return 'curioso';
    if (/expert|profes|tecnic|serio/.test(t)) return 'experto';
    if (/emoc|inspir|motiv/.test(t)) return 'emocional';
    return 'general';
  };

  const run = () => {
    let t = '';
    let m = 'Generado en tu navegador';
    const tema = v('tema');
    if (tool === 'generador-de-prompts') {
      if (!v('objetivo')) return set('Escribe un objetivo para crear un prompt útil.');
      t = lines(['ROL\nActúa como un especialista experto en la tarea solicitada.', 'OBJETIVO\n' + v('objetivo'),
        'CONTEXTO\n' + (v('contexto') || 'No inventes información; identifica los datos que falten.'),
        'AUDIENCIA\n' + (v('audiencia') || 'Adapta el nivel al lector.'),
        'INSTRUCCIONES\nAnaliza la petición. Divide el trabajo en pasos cuando ayude. Explica supuestos. Da ejemplos concretos.',
        'FORMATO\n' + (v('formato') || 'Respuesta clara, estructurada y reutilizable.'), 'TONO\n' + (v('tono') || 'Claro y profesional.'),
        'RESTRICCIONES\n' + (v('restricciones') || 'No inventes datos. Señala incertidumbres.'),
        'CONTROL DE CALIDAD\nComprueba objetivo, formato, precisión y restricciones antes de responder.']);
    } else if (tool === 'mejorador-de-prompts') {
      if (!v('objetivo')) return set('Pega un prompt para mejorarlo.');
      t = lines(['PROMPT MEJORADO', 'Actúa como experto en transformar instrucciones ambiguas en resultados precisos.', 'TAREA\n' + v('objetivo'),
        'CONTEXTO\n' + (v('contexto') || 'Usa solo datos proporcionados y separa hechos de supuestos.'),
        'AUDIENCIA\n' + (v('audiencia') || 'Adapta la respuesta al destinatario.'), 'USO\n' + (v('modelo') || 'IA general'),
        'FORMATO\n' + (v('formato') || 'Usa encabezados, pasos y ejemplos cuando aporten claridad.'),
        'CRITERIOS\nDefine el resultado, elimina ambigüedades, añade requisitos verificables y revisa el cumplimiento.',
        'DIAGNÓSTICO\n✓ Objetivo definido\n✓ Contexto separado\n✓ Audiencia y formato contemplados\n✓ Control de calidad añadido']);
    } else if (tool === 'generador-de-titulos') {
      if (!tema) return set('Escribe un tema.');
      const tone = toneOf(v('tono'));
      const kws = list(v('palabras'));
      const titles = TITLES[tone].map((x) => cap(x.replace('{T}', cap(tema)).replace('{t}', tema)));
      t = block([
        'TÍTULOS' + (v('plataforma') ? ' PARA ' + v('plataforma').toUpperCase() : ''),
        !!v('audiencia') && 'Audiencia: ' + v('audiencia'),
        'Tono: ' + (tone !== 'general' ? tone : v('tono') ? v('tono') + ' (plantillas generales)' : 'general'),
        kws.length > 0 && 'Palabras clave para incluir si encajan: ' + kws.join(', '),
        '',
        ...titles.map((x, i) => `${i + 1}. ${x} (${x.length} caracteres)`),
      ]);
      m = `${titles.length} títulos · generado en tu navegador`;
    } else if (tool === 'generador-de-ideas') {
      if (!tema) return set('Escribe un tema o nicho.');
      const n = clamp(parseInt(v('cantidad'), 10), 5, 30, 10);
      const angles = ['error común', 'mito', 'tutorial', 'comparativa', 'caso práctico', 'pregunta polémica', 'antes y después', 'checklist', 'reto',
        'preguntas frecuentes', 'tendencia', 'experimento', 'opinión argumentada', 'guía para principiantes', 'nivel avanzado', 'serie de contenidos'];
      t = 'PLAN DE IDEAS\nObjetivo: ' + (v('objetivo') || 'aportar valor') + '\nPlataforma: ' + (v('plataforma') || 'redes') + '\nAudiencia: ' +
        (v('audiencia') || 'público interesado') + '\n\n' + Array.from({ length: n }, (_, i) =>
        (i + 1) + '. ' + angles[i % angles.length] + ': ' + tema + '. Desarrolla el ángulo con un ejemplo y termina con una acción útil.').join('\n');
    } else if (tool === 'generador-de-hashtags') {
      if (!tema) return set('Escribe un tema.');
      const asked = parseInt(v('cantidad'), 10);
      const n = clamp(asked, 5, 30, 10);
      const { specific, broad } = hashtags();
      const takeS = specific.slice(0, n);
      const takeB = broad.slice(0, n - takeS.length);
      const got = takeS.length + takeB.length;
      t = block([
        takeS.length > 0 && 'ESPECÍFICOS\n' + takeS.join(' ') + '\n',
        takeB.length > 0 && 'AMPLIOS\n' + takeB.join(' ') + '\n',
        Number.isFinite(asked) && asked !== n && `La cantidad va de 5 a 30: usamos ${n}.\n`,
        got === 0 && 'No sale ningún hashtag con significado de lo que has escrito. Describe el tema con palabras concretas (por ejemplo, «receta de bizcocho sin gluten») y añade el nicho o la audiencia.\n',
        got > 0 && got < n && `${got === 1 ? 'Solo sale 1 hashtag' : `Solo salen ${got} hashtags`} de lo que has escrito (pediste ${n}). Añade más detalle en el nicho o la audiencia para obtener más: no rellenamos con etiquetas que no tengan que ver.\n`,
        got > 0 && 'Revisa cada uno en la propia red antes de usarlo y quita los que no encajen con tu publicación.',
      ]);
      m = `${got} ${got === 1 ? 'hashtag' : 'hashtags'} · generado en tu navegador`;
    } else if (tool === 'contador-de-palabras') {
      const x = v('texto');
      if (!x) return set('Pega un texto.');
      t = countText(x);
      m = 'Analizado en tu navegador';
    } else if (tool === 'descripcion-video') {
      if (!tema) return set('Describe el vídeo.');
      t = `${tema}\n\nEn este vídeo descubrirás los puntos clave de ${tema}, explicado de forma ${v('tono') || 'clara'} para ${v('audiencia') || 'personas interesadas en el tema'}. Encontrarás ideas, ejemplos y pasos aplicables desde hoy.\n\n👉 ${v('cta') || 'Suscríbete y comparte tu opinión'}.\n\nPALABRAS CLAVE\n${list(v('keywords')).join(' · ') || 'Añade palabras clave específicas'}\n\n#IA #Tecnologia #Aprendizaje`;
    } else if (tool === 'prompt-imagenes') {
      if (!v('sujeto')) return set('Describe el sujeto o escena.');
      t = `${v('sujeto')}. ${v('estilo') || 'estilo cinematográfico'}, ${v('composicion') || 'composición equilibrada'}, ${v('camara') || 'profundidad de campo natural'}, ${v('luz') || 'iluminación cuidada'}, ${v('ambiente') || 'atmósfera envolvente'}, formato ${v('formato') || '16:9'}.\n\nNEGATIVE PROMPT\n${v('negativos') || 'texto, marcas de agua, baja resolución, deformaciones, anatomía incorrecta'}`;
    }
    set(t, m);
  };

  const SAMPLES = {
    'contador-de-palabras': { texto: 'La inteligencia artificial está cambiando la forma de crear, aprender y trabajar. La inteligencia artificial ayuda a resumir textos largos. Pero conviene revisar siempre lo que escribe la inteligencia artificial.' },
    'prompt-imagenes': { sujeto: 'Una ciudad futurista bajo la lluvia' },
    'generador-de-hashtags': { tema: 'receta de bizcocho sin gluten', nicho: 'repostería saludable, cocina sin gluten', audiencia: 'personas celíacas', cantidad: '10' },
    'generador-de-titulos': { tema: 'usar la IA para estudiar', audiencia: 'estudiantes de bachillerato', palabras: 'IA, estudiar, exámenes', tono: 'curioso' },
  };
  $('#run-tool')?.addEventListener('click', run);
  $('#sample-tool')?.addEventListener('click', () => {
    const sample = SAMPLES[tool] || (cfg[0] ? { [cfg[0][0]]: 'Crear contenido útil sobre inteligencia artificial' } : {});
    for (const [id, value] of Object.entries(sample)) { const el = $('#' + id); if (el) el.value = value; }
    run();
  });
  $('#clear-tool')?.addEventListener('click', () => { form?.reset(); set('Aquí aparecerá tu resultado.', 'Listo para empezar.'); });
  $('#copy-output')?.addEventListener('click', () => navigator.clipboard?.writeText(out?.textContent || ''));
})();
