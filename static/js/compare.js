// Comparador: tabla lado a lado de 2–3 herramientas con ficha. Datos incrustados por el build; solo DOM y textContent.
(function () {
  var form = document.getElementById('comparador'), out = document.getElementById('comparador-resultado'),
    src = document.getElementById('comparador-datos');
  if (!form || !out || !src) return;
  var MAX = 3, byId = {}, chosen = [], status = form.querySelector('.compare-status'),
    duels = document.getElementById('comparador-duelos');
  duels = duels ? JSON.parse(duels.textContent) : {};
  JSON.parse(src.textContent).forEach(function (t) { byId[t.id] = t; });
  var boxes = Array.prototype.slice.call(form.querySelectorAll('input[name="h"]'));
  var ROWS = [['Precio desde', 'desde'], ['Plan de pago', 'pago'], ['Ideal para', 'ideal'],
    ['Plataformas', 'plataformas'], ['Categoría', 'cat'], ['Veredicto', 'veredicto']];

  function make(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function box(id) { return form.querySelector('input[name="h"][value="' + id + '"]'); }
  // El logotipo ya está pintado en la casilla: se clona para la cabecera de la tabla.
  function logo(id) {
    var l = box(id).parentNode.querySelector('.logo');
    return l ? l.cloneNode(true) : make('span');
  }

  function render() {
    while (out.firstChild) out.removeChild(out.firstChild);
    boxes.forEach(function (b) { b.disabled = !b.checked && chosen.length >= MAX; });
    if (chosen.length < 2) {
      status.textContent = chosen.length ? 'Elige al menos 2 herramientas (llevas 1).' : 'Elige al menos 2 herramientas.';
      return;
    }
    status.textContent = chosen.length + ' de ' + MAX + ' elegidas' +
      (chosen.length >= MAX ? '. Desmarca una para elegir otra.' : '.');
    var tools = chosen.map(function (id) { return byId[id]; }), wrap = make('div', 'table-scroll compare-scroll'),
      table = make('table', 'compare-table'), thead = make('thead'), head = make('tr'), body = make('tbody');
    var names = tools.map(function (t) { return t.n; });
    table.appendChild(make('caption', 'sr-only', 'Comparación de ' + names.slice(0, -1).join(', ') + ' y ' + names[names.length - 1]));
    head.appendChild(make('td'));
    tools.forEach(function (t) {
      var th = make('th');
      th.setAttribute('scope', 'col');
      th.appendChild(logo(t.id));
      th.appendChild(make('span', null, t.n));
      head.appendChild(th);
    });
    thead.appendChild(head);
    table.appendChild(thead);
    ROWS.forEach(function (r) {
      var tr = make('tr'), th = make('th', null, r[0]);
      th.setAttribute('scope', 'row');
      tr.appendChild(th);
      tools.forEach(function (t) { tr.appendChild(make('td', r[1] === 'veredicto' ? 'compare-verdict' : null, t[r[1]])); });
      body.appendChild(tr);
    });
    var links = make('tr'), lth = make('th', null, 'Más información');
    lth.setAttribute('scope', 'row');
    links.appendChild(lth);
    tools.forEach(function (t) {
      var td = make('td', 'compare-links'), ficha = make('a', null, 'Leer la ficha →');
      ficha.href = t.u;
      td.appendChild(ficha);
      if (t.w) {
        var web = make('a', null, 'Web oficial ↗');
        web.href = t.w;
        web.target = '_blank';
        web.rel = 'noopener nofollow';
        td.appendChild(web);
      }
      links.appendChild(td);
    });
    body.appendChild(links);
    table.appendChild(body);
    wrap.appendChild(table);
    out.appendChild(wrap);
    // Si las dos elegidas tienen un «Cara a cara», se sugiere (en cualquier orden).
    var duel = chosen.length === 2 && duels[chosen.slice().sort().join(',')];
    if (duel) {
      var p = make('p', 'compare-duel'), a = make('a', null, 'Lee nuestro análisis ' + duel.label + '\u00a0'),
        arrow = make('span', null, '→');
      arrow.setAttribute('aria-hidden', 'true');
      a.appendChild(arrow);
      a.href = duel.u;
      p.appendChild(a);
      out.appendChild(p);
    }
  }

  function sync() {
    history.replaceState(null, '', chosen.length ? '?h=' + chosen.join(',') : location.pathname);
    render();
  }

  boxes.forEach(function (b) {
    b.addEventListener('change', function () {
      var i = chosen.indexOf(b.value);
      if (b.checked && i < 0 && chosen.length < MAX) chosen.push(b.value);
      else if (!b.checked && i >= 0) chosen.splice(i, 1);
      b.checked = chosen.indexOf(b.value) >= 0;
      sync();
    });
  });
  form.addEventListener('submit', function (ev) { ev.preventDefault(); });

  // Selección compartida: ids válidos, sin repetir y como máximo 3, en el orden de la URL.
  var raw = new URLSearchParams(location.search).get('h') || '';
  raw.split(',').forEach(function (id) {
    id = id.trim();
    if (byId[id] && box(id) && chosen.indexOf(id) < 0 && chosen.length < MAX) {
      chosen.push(id);
      box(id).checked = true;
    }
  });
  boxes.forEach(function (b) { if (b.checked && chosen.indexOf(b.value) < 0) b.checked = false; });
  if (chosen.join(',') !== raw) sync(); // deja en la barra solo los ids válidos
  else render();
})();
