// Asistente «¿Qué IA necesito?»: pinta la recomendación con los datos que el build incrusta en la página.
// Toda la lógica de negocio (reglas y alternativas del catálogo) viene resuelta del build; aquí solo se elige y se pinta.
(function () {
  var form = document.getElementById('asistente'), out = document.getElementById('asistente-resultado'),
    src = document.getElementById('asistente-datos');
  if (!form || !out || !src) return;
  var data = JSON.parse(src.textContent), NAMES = ['tarea', 'presupuesto', 'nivel', 'para'], shown = false;
  var NIVEL = { principiante: 'Fácil', intermedio: 'Intermedio', avanzado: 'Avanzado' };

  function make(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function link(href, text, cls, external) {
    var a = make('a', cls, text);
    a.href = href;
    if (external) { a.target = '_blank'; a.rel = 'noopener nofollow'; }
    return a;
  }
  function logo(t, cls) {
    var s = make('span', cls, t.m);
    s.style.background = t.c;
    s.setAttribute('aria-hidden', 'true');
    return s;
  }
  function values() {
    var v = {};
    NAMES.forEach(function (n) {
      var c = form.querySelector('input[name="' + n + '"]:checked');
      v[n] = c ? c.value : '';
    });
    return v;
  }
  // Igual que radar.assistant.pick_rule: el equipo gana al nivel avanzado.
  function pick(rule, v) {
    if (v.para === 'equipo' && rule.si_equipo) return rule.si_equipo;
    if (v.nivel === 'avanzado' && rule.si_avanzado) return rule.si_avanzado;
    return rule;
  }
  function toolItem(id, motivo) {
    var t = data.tools[id];
    if (!t) return null;
    var a = link(t.u, null, 'assistant-alt'), text = make('span');
    a.appendChild(logo(t, 'assistant-logo-sm'));
    text.appendChild(make('strong', null, t.n));
    text.appendChild(make('small', null, (motivo || t.i) + (t.p ? ' · Desde ' + t.p : '')));
    a.appendChild(text);
    return a;
  }
  function group(title, items) {
    items = items.filter(Boolean);
    if (!items.length) return null;
    var box = make('section', 'assistant-group');
    box.appendChild(make('h3', null, title));
    items.forEach(function (i) { box.appendChild(i); });
    return box;
  }

  function render(v) {
    var rule = pick(data.reglas[v.tarea + '/' + v.presupuesto], v), task = data.tareas[v.tarea],
      t = data.tools[rule.principal], card = make('article', 'assistant-card'), head = make('div', 'assistant-head'),
      titles = make('div'), why = make('div', 'assistant-why'), list = make('ul'), facts = make('dl', 'summary'),
      cta = make('div', 'assistant-cta');
    while (out.firstChild) out.removeChild(out.firstChild);

    head.appendChild(logo(t, 'assistant-logo'));
    titles.appendChild(make('p', 'kicker', 'Te recomendamos'));
    titles.appendChild(make('h2', null, t.n));
    head.appendChild(titles);
    card.appendChild(head);

    why.appendChild(make('h3', null, 'Por qué encaja contigo'));
    rule.porque.forEach(function (p) { list.appendChild(make('li', null, p)); });
    why.appendChild(list);
    card.appendChild(why);

    [['Precio desde', t.p], ['Ideal para', t.i], ['Nivel', NIVEL[t.nivel] || '']].forEach(function (f) {
      if (!f[1]) return;
      var d = make('div');
      d.appendChild(make('dt', null, f[0]));
      d.appendChild(make('dd', null, f[1]));
      facts.appendChild(d);
    });
    card.appendChild(facts);

    cta.appendChild(link(t.u, 'Leer el análisis →', 'btn'));
    cta.appendChild(link(t.w, 'Probar ' + t.n + ' ↗', 'btn assistant-try', true));
    card.appendChild(cta);
    out.appendChild(card);

    var alts = group('También encajan', (rule.alternativas || []).map(function (a) { return toolItem(a.id, a.motivo); }));
    var auto = group('Otras opciones del catálogo',
      (data.auto[v.tarea + '/' + v.presupuesto + '/' + v.nivel] || []).map(function (id) { return toolItem(id); }));
    if (alts) out.appendChild(alts);
    if (auto) out.appendChild(auto);

    var more = make('p', 'assistant-more');
    more.appendChild(link(task.comparativa, 'Ver la comparativa completa: ' + task.etiqueta.toLowerCase() + ' →'));
    more.appendChild(document.createTextNode(' · '));
    more.appendChild(link(task.guia, 'Leer la guía relacionada →'));
    out.appendChild(more);

    // En el móvil el resultado queda debajo de las preguntas: se acerca a la vista la primera vez.
    if (!shown && window.innerWidth < 760) {
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      out.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }
    shown = true;
  }

  function update() {
    var v = values(), params = new URLSearchParams();
    NAMES.forEach(function (n) { if (v[n]) params.set(n, v[n]); });
    var qs = params.toString();
    history.replaceState(null, '', qs ? '?' + qs : location.pathname);
    if (NAMES.every(function (n) { return v[n]; })) {
      render(v);
    } else if (shown) {
      while (out.firstChild) out.removeChild(out.firstChild);
      out.appendChild(make('p', 'assistant-hint', 'Responde las 4 preguntas para ver la recomendación.'));
    }
  }

  // Respuestas compartidas en la URL: solo se aceptan valores que existen en el formulario.
  var params = new URLSearchParams(location.search);
  NAMES.forEach(function (n) {
    var wanted = params.get(n);
    Array.prototype.forEach.call(form.querySelectorAll('input[name="' + n + '"]'), function (r) {
      if (r.value === wanted) r.checked = true;
    });
  });
  form.addEventListener('change', update);
  form.addEventListener('submit', function (ev) { ev.preventDefault(); });
  if (NAMES.every(function (n) { return form.querySelector('input[name="' + n + '"]:checked'); })) {
    shown = true; // al llegar desde un enlace compartido no se desplaza la página
    render(values());
  }
})();
