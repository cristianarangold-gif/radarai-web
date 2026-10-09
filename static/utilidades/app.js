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
    'todo todos toda todas tu tus un una unas uno unos y ya yo vez puede pueden hacer hace sido estar otros otras mucha muchos muchas ' +
    'solo mismo misma mismos mismas aunque ahora siempre').split(' '));
  const ARTICLES = new Set(['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas']);
  const words = (s) => s.match(WORD) || [];
  const isStop = (w) => STOP.has(deaccent(w.toLowerCase()));

  const fields = {
'generador-de-prompts':[['objetivo','Objetivo','Qué quieres conseguir','ta'],['contexto','Contexto','Datos y antecedentes','ta'],['audiencia','Audiencia','Para quién es','text'],['formato','Formato','Tabla, pasos, guion, JSON…','text'],['tono','Tono','Profesional, cercano, técnico…','text'],['restricciones','Restricciones','Límites y requisitos','ta']],
'mejorador-de-prompts':[['objetivo','Prompt actual','Pega el prompt que quieres mejorar','ta'],['contexto','Contexto adicional','Información útil','ta'],['audiencia','Audiencia','Destinatario','text'],['modelo','Uso o modelo','Chat, imagen, vídeo, código…','text'],['formato','Formato deseado','Cómo debe responder','text']],
'generador-de-titulos':[['tema','Tema o contenido','Describe el contenido','ta'],['plataforma','Plataforma','YouTube, TikTok, blog…','text'],['audiencia','Audiencia','A quién quieres atraer','text'],['palabras','Palabras clave','Separadas por comas','text'],['tono','Tono','Curioso, experto, emocional…','text']],
'generador-de-ideas':[['tema','Tema o nicho','Ej.: IA, fitness, educación…','ta'],['objetivo','Objetivo','Educar, vender, entretener…','text'],['plataforma','Plataforma','TikTok, YouTube, blog…','text'],['audiencia','Audiencia','Perfil del público','text'],['cantidad','Cantidad','5–16','number']],
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
  const countText = (raw) => {
    const x = raw.normalize('NFC');
    const w = words(x);
    // Frases: se corta tras . ! ? … seguidos de espacio y en cada salto de línea (sin lookbehind, que falla en Safari antiguo).
    const sentences = x.replace(/([.!?…])\s+/g, '$1\u0001').replace(/\n+/g, '\u0001').split('\u0001').filter((s) => words(s).length);
    const f = sentences.length;
    const p = x.split(/\n\s*\n/).filter((s) => s.trim()).length;
    const long = sentences.filter((s) => words(s).length > 30).length;
    const freq = new Map();
    for (const word of w) {
      const k = word.toLowerCase();
      if (k.length >= 4 && /\p{L}/u.test(k) && !isStop(k)) freq.set(k, (freq.get(k) || 0) + 1);
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
    // Quita tildes y signos pero conserva la ñ (año ≠ ano).
    const plain = deaccent(w.replace(/ñ/g, '\u0002').replace(/Ñ/g, '\u0003')).replace(/\u0002/g, 'ñ').replace(/\u0003/g, 'Ñ').replace(/[^A-Za-z0-9ñÑ]/g, '');
    if (plain.length <= 5 && plain === plain.toUpperCase() && /[A-ZÑ]/.test(plain)) return plain;
    return /[a-zñ][A-ZÑ]/.test(plain) ? cap(plain) : cap(plain.toLowerCase()); // NotebookLM, ChatGPT
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

  // Rellena {T} (inicio de frase) y {t} (dentro de la frase) y aplica las contracciones «del» y «al».
  const fill = (tpl, tema) => {
    const lower = /^\p{Lu}{2,}/u.test(tema) ? tema : tema.charAt(0).toLowerCase() + tema.slice(1);
    return cap(tpl.replace('{T}', cap(tema)).replace('{t}', lower).replace(/\bde el\b/g, 'del').replace(/\ba el\b/g, 'al'));
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

  // Descripción de vídeo: estructura según la plataforma; hashtags solo de tus palabras clave.
  const platformOf = (s) => {
    const t = deaccent(s.toLowerCase());
    if (/short|reel|tiktok|instagram/.test(t)) return 'corto';
    if (/youtube/.test(t)) return 'youtube';
    if (/linkedin/.test(t)) return 'linkedin';
    return 'general';
  };
  const PLATFORM_LABEL = { youtube: 'YouTube', corto: 'vídeo corto (TikTok, Reels, Shorts)', linkedin: 'LinkedIn', general: 'general' };
  const videoDescription = (tema) => {
    const kind = platformOf(v('plataforma'));
    const kws = [...new Set(list(v('keywords')))];
    const tags = [...new Set(kws.slice(0, 5).map((k) => toTag(words(k))).filter((x) => x.length > 2))].join(' ');
    const audiencia = v('audiencia');
    const cta = v('cta');
    const intro = fill(`Un vídeo${v('tono') ? ' ' + v('tono').toLowerCase() : ''} sobre {t}${audiencia ? ', pensado para ' + audiencia : ''}.`, tema);
    if (kind === 'youtube') {
      return block([cap(tema), '',
        intro, '',
        'LO QUE VERÁS', ...(kws.length ? kws.map((k) => '• ' + k) : ['• [añade los puntos clave del vídeo]']), '',
        'MARCAS DE TIEMPO', '00:00 Introducción', '[00:00] [siguiente sección]', '',
        '👉 ' + (cta || 'Suscríbete y cuéntame tu opinión en los comentarios.'),
        !!tags && '', !!tags && tags]);
    }
    if (kind === 'corto') {
      return block([cap(tema), !!audiencia && `Para ${audiencia}.`, '👉 ' + (cta || 'Guárdalo para verlo después.'), !!tags && '', !!tags && tags]);
    }
    if (kind === 'linkedin') {
      return block([cap(tema), '',
        intro,
        kws.length > 0 && 'Puntos clave: ' + kws.join(', ') + '.', '',
        '¿Qué opinas? Te leo en los comentarios.', !!cta && cta,
        !!tags && '', !!tags && tags]);
    }
    return block([cap(tema), '',
      intro, '',
      '👉 ' + (cta || 'Suscríbete y comparte tu opinión.'),
      kws.length > 0 && '', kws.length > 0 && 'PALABRAS CLAVE\n' + kws.join(' · '), !!tags && '', !!tags && tags]);
  };

  // Ideas: títulos distintos, con formato según la plataforma y cierre según el objetivo.
  const IDEAS = ['Los 3 errores más comunes con {t} (y cómo evitarlos)', 'Mitos sobre {t}: qué es cierto y qué no',
    'Tutorial: {t} paso a paso para empezar hoy', 'Comparativa: dos formas de abordar {t} y cuándo elegir cada una',
    'Caso práctico: {t} en una situación real', 'La pregunta incómoda sobre {t} que pocos responden',
    'Antes y después de {t}: qué cambia de verdad', 'Lista de comprobación de {t}: lo imprescindible en 5 puntos',
    'Reto de 7 días relacionado con {t}', 'Respuestas a las 5 dudas más frecuentes sobre {t}',
    'Novedades sobre {t}: qué ha cambiado y a quién le afecta', 'Una semana con {t}: qué pasa y qué aprendes',
    'Opinión argumentada sobre {t}: a favor y en contra', '{T} para principiantes: lo que necesitas saber el primer día',
    '{T} a nivel avanzado: detalles que marcan la diferencia', 'Serie de contenidos: {t} en 4 entregas'];
  const formatOf = (s) => {
    const t = deaccent(s.toLowerCase());
    if (/short|reel|tiktok/.test(t)) return 'Vídeo corto';
    if (/youtube/.test(t)) return 'Vídeo';
    if (/instagram/.test(t)) return 'Carrusel';
    if (/linkedin/.test(t)) return 'Publicación';
    if (/newsletter|boletin|correo|email/.test(t)) return 'Correo';
    if (/podcast/.test(t)) return 'Episodio';
    if (/blog|web/.test(t)) return 'Artículo';
    return 'Contenido';
  };
  const closingOf = (s) => {
    const t = deaccent(s.toLowerCase());
    if (/educ|ensen|explic/.test(t)) return 'Cierra con un resumen en 3 puntos.';
    if (/vend|venta|client|conver/.test(t)) return 'Cierra explicando cómo ayuda tu producto o servicio, sin exagerar.';
    if (/entreten|divert|humor/.test(t)) return 'Cierra con una pregunta divertida para los comentarios.';
    if (/comunidad|fideli|seguidor/.test(t)) return 'Cierra invitando a contar su experiencia.';
    if (/visib|alcance|viral|crec/.test(t)) return 'Cierra invitando a guardar o compartir.';
    return 'Cierra con una acción útil para tu audiencia.';
  };

  // Mejorador de prompts: diagnóstico calculado sobre tu texto, no fijo.
  const diagnose = (p) => {
    const n = words(p).length;
    const has = (re) => re.test(p);
    return [
      [n >= 15, `Tiene detalle suficiente (${n} palabras).`, `Es muy corto (${n} palabras): explica qué quieres conseguir y con qué datos.`],
      [!!v('contexto') || has(/\b(contexto|soy|trabajo en|tengo|es para|lo necesito para|para (una|un|mi|mis)|mi (empresa|negocio|clase|proyecto|equipo))\b/i), 'Da contexto (quién eres, para qué es, datos de partida).', 'No da contexto: di quién eres, para qué es y de qué datos partes.'],
      [!!v('audiencia') || has(/\b(p[úu]blicos?|audiencia|lector(es|as)?|clientes?|alumn[oa]s|estudiantes|dirigid[oa]s?|destinad[oa]s?)\b/i), 'Dice a quién va dirigido el resultado.', 'No dice a quién va dirigido el resultado.'],
      [!!v('formato') || has(/\b(tablas?|listas?|vi[ñn]etas|pasos|p[áa]rrafos?|json|esquemas?|guion|correo|puntos?|\d+ (palabras|caracteres|l[íi]neas|frases))\b/i), 'Pide un formato concreto.', 'No pide un formato (tabla, lista, pasos, extensión…).'],
      [has(/\b(por ejemplo|ejemplos?|como este)\b/i), 'Incluye un ejemplo de lo que esperas.', 'No incluye un ejemplo (es opcional, pero ayuda mucho).'],
      [has(/\b(m[áa]xim[oa]s?|m[íi]nim[oa]s?|no inventes|no uses|no incluyas|evit\w*|l[íi]mites?|\d+ (palabras|caracteres|l[íi]neas|frases))\b/i), 'Pone límites.', 'No pone límites (extensión, qué evitar, «no inventes»).'],
    ];
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
      const checks = diagnose(v('objetivo'));
      const ok = (i) => checks[i][0];
      const score = checks.filter(([pass]) => pass).length;
      t = block([
        'DIAGNÓSTICO',
        ...checks.map(([pass, good, bad]) => (pass ? '✓ ' + good : '✗ ' + bad)),
        `Puntuación: ${score} de 6`,
        score === 6 && 'Tu prompt ya está bien planteado: la versión de abajo solo lo ordena por bloques.',
        '',
        'PROMPT MEJORADO',
        'Actúa como experto en la tarea que te describo.',
        '',
        'TAREA\n' + v('objetivo'),
        '',
        'CONTEXTO\n' + (v('contexto') || (ok(1) ? 'El indicado en la tarea.' : '[completa: quién eres, para qué es y datos de partida]')),
        '',
        'AUDIENCIA\n' + (v('audiencia') || (ok(2) ? 'La indicada en la tarea.' : '[completa: para quién es el resultado]')),
        '',
        'FORMATO\n' + (v('formato') || (ok(3) ? 'El indicado en la tarea.' : '[completa: tabla, lista, pasos, extensión…]')),
        !ok(4) && '',
        !ok(4) && 'EJEMPLO\n[opcional: pega un ejemplo del resultado que esperas]',
        '',
        'LÍMITES\nNo inventes datos: si falta información, pregúntamela antes de responder.' + (ok(5) ? '' : '\n[completa: extensión máxima u otros límites]'),
        !!v('modelo') && '',
        !!v('modelo') && 'USO\n' + v('modelo'),
      ]);
      m = `${score} de 6 puntos · analizado en tu navegador`;
    } else if (tool === 'generador-de-titulos') {
      if (!tema) return set('Escribe un tema.');
      const tone = toneOf(v('tono'));
      const kws = list(v('palabras'));
      const titles = TITLES[tone].map((x) => fill(x, tema));
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
      const asked = parseInt(v('cantidad'), 10);
      const n = clamp(asked, 5, IDEAS.length, 10);
      const format = formatOf(v('plataforma'));
      const closing = closingOf(v('objetivo'));
      t = block([
        'PLAN DE IDEAS',
        format !== 'Contenido' && 'Formato: ' + format + ` (para ${v('plataforma')})`,
        !!v('objetivo') && 'Objetivo: ' + v('objetivo'),
        !!v('audiencia') && 'Audiencia: ' + v('audiencia'),
        'Cierre recomendado: ' + closing.replace(/^Cierra /, ''),
        Number.isFinite(asked) && asked !== n && `La cantidad va de 5 a ${IDEAS.length}: usamos ${n}.`,
        '',
        ...IDEAS.slice(0, n).map((x, i) => `${i + 1}. ${format === 'Contenido' ? '' : `[${format}] `}${fill(x, tema)}`),
      ]);
      m = `${n} ideas · generado en tu navegador`;
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
      t = videoDescription(tema);
      m = `${t.length} caracteres · formato ${PLATFORM_LABEL[platformOf(v('plataforma'))]}`;
    } else if (tool === 'prompt-imagenes') {
      if (!v('sujeto')) return set('Describe el sujeto o escena.');
      t = `${v('sujeto')}. ${cap(v('estilo') || 'estilo cinematográfico')}, ${v('composicion') || 'composición equilibrada'}, ${v('camara') || 'profundidad de campo natural'}, ${v('luz') || 'iluminación cuidada'}, ${v('ambiente') || 'atmósfera envolvente'}, formato ${v('formato') || '16:9'}.\n\nNEGATIVE PROMPT\n${v('negativos') || 'texto, marcas de agua, baja resolución, deformaciones, anatomía incorrecta'}`;
    }
    set(t, m);
  };

  const SAMPLES = {
    'contador-de-palabras': { texto: 'La inteligencia artificial está cambiando la forma de crear, aprender y trabajar. La inteligencia artificial ayuda a resumir textos largos. Pero conviene revisar siempre lo que escribe la inteligencia artificial.' },
    'prompt-imagenes': { sujeto: 'Una ciudad futurista bajo la lluvia' },
    'generador-de-hashtags': { tema: 'receta de bizcocho sin gluten', nicho: 'repostería saludable, cocina sin gluten', audiencia: 'personas celíacas', cantidad: '10' },
    'descripcion-video': { tema: 'cómo organizar tus apuntes con IA', plataforma: 'YouTube', audiencia: 'estudiantes universitarios', keywords: 'apuntes, NotebookLM, resúmenes', tono: 'cercano' },
    'generador-de-ideas': { tema: 'la IA para estudiar', objetivo: 'educar', plataforma: 'Instagram', audiencia: 'estudiantes de bachillerato', cantidad: '6' },
    'mejorador-de-prompts': { objetivo: 'Hazme un resumen de este tema' },
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
