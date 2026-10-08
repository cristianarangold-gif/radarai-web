// Buscador de Radar IA: ventana desde la cabecera y página /buscar/. Sin librerías.
// Los resultados se pintan siempre con nodos DOM y textContent (nunca HTML del índice).
(function () {
  var body = document.body, indexUrl = body.getAttribute('data-search-index');
  if (!indexUrl || !window.fetch) return;
  var SUGGEST = ['ChatGPT', 'imágenes', 'gratis', 'estudiar', 'programar'];
  var MAX_DIALOG = 8, cache = null;
  var STOP = ['a', 'al', 'con', 'de', 'del', 'el', 'en', 'la', 'las', 'lo', 'los', 'para', 'por', 'que', 'un', 'una', 'y'];

  function norm(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function make(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); }

  // Descarga el índice una vez; si falla, se reintenta en la siguiente búsqueda.
  function loadIndex() {
    if (!cache) {
      cache = fetch(indexUrl).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      }).then(function (list) {
        list.forEach(function (e) { e.nt = norm(e.t); e.nx = norm(e.x); e.nd = norm(e.d); e.nk = norm(e.k); });
        return list;
      }).catch(function (err) { cache = null; throw err; });
    }
    return cache;
  }

  // 2 = al principio de una palabra; 1 = dentro de una palabra (términos de 3 letras o más).
  function hit(text, w) {
    if ((' ' + text).indexOf(' ' + w) >= 0) return 2;
    return w.length >= 3 && text.indexOf(w) >= 0 ? 1 : 0;
  }
  // Devuelve las entradas que contienen todas las palabras; si no hay ninguna, las que contienen
  // alguna (ordenadas por cuántas coinciden) y marca la lista con .partial = true.
  function search(list, query) {
    var q = norm(query), terms = significant(q), out = [], full = 0;
    if (!terms.length) return out;
    list.forEach(function (e) {
      var score = 0, n = 0;
      for (var i = 0; i < terms.length; i++) {
        var w = terms[i], t = hit(e.nt, w), s = t === 2 ? (e.nt.indexOf(w) === 0 ? 12 : 8) : t ? 5 : 0;
        if (hit(e.nx, w)) s += 4;
        if (hit(e.nd, w)) s += 2;
        if (hit(e.nk, w)) s += 1;
        if (s) { score += s; n++; }
      }
      if (!n) return;
      if (e.k === 'Ficha' || e.k === 'Comparativa' || e.k === 'Cara a cara') score += 3;
      if (e.nt.indexOf(q) >= 0) score += 2;
      if (n === terms.length) full++;
      out.push({ e: e, s: score, n: n });
    });
    if (full) out = out.filter(function (r) { return r.n === terms.length; });
    var res = out.sort(function (a, b) { return b.n - a.n || b.s - a.s || a.e.t.localeCompare(b.e.t, 'es'); })
      .map(function (r) { return r.e; });
    res.partial = !full && res.length > 0;
    return res;
  }
  var PARTIAL = 'Sin coincidencias con todas las palabras; se muestran resultados con alguna de ellas.';

  // Resalta los términos en el título sin usar HTML: se cortan trozos de texto y se envuelven en <mark>.
  function highlight(node, text, terms) {
    var low = '', marks = [], pos = 0, i;
    for (i = 0; i < text.length; i++) {
      var c = norm(text[i]);
      low += c.length === 1 ? c : ' ';
    }
    terms.forEach(function (w) {
      for (var p = low.indexOf(w); p >= 0; p = low.indexOf(w, p + 1)) marks.push([p, p + w.length]);
    });
    marks.sort(function (a, b) { return a[0] - b[0]; }).forEach(function (m) {
      if (m[0] < pos) return;
      node.appendChild(document.createTextNode(text.slice(pos, m[0])));
      node.appendChild(make('mark', null, text.slice(m[0], m[1])));
      pos = m[1];
    });
    node.appendChild(document.createTextNode(text.slice(pos)));
  }
  function isLight(hex) {
    var n = parseInt(hex.slice(1), 16);
    return (0.2126 * (n >> 16) + 0.7152 * (n >> 8 & 255) + 0.0722 * (n & 255)) / 255 > 0.6;
  }
  function item(e, terms, id) {
    var a = make('a', 'search-hit'), icon = make('span', 'search-ic', e.m), text = make('span', 'search-tx'),
      title = make('strong');
    a.href = e.u;
    if (id) { a.id = id; a.setAttribute('role', 'option'); a.setAttribute('aria-selected', 'false'); }
    icon.style.background = e.c;
    if (isLight(e.c)) icon.style.color = '#151515';
    icon.setAttribute('aria-hidden', 'true');
    highlight(title, e.t, terms);
    text.appendChild(title);
    text.appendChild(make('small', null, e.k + ' · ' + (e.f || (e.p ? 'Desde ' + e.p : e.d))));
    a.appendChild(icon);
    a.appendChild(text);
    return a;
  }
  // Quita palabras vacías («la», «para»…) salvo que la consulta solo tenga esas.
  function significant(q) {
    var all = q ? q.split(' ') : [], rest = all.filter(function (w) { return STOP.indexOf(w) < 0; });
    return rest.length ? rest : all;
  }
  function terms(query) { return significant(norm(query)); }

  // Mensajes: sugerencias, sin resultados o error de carga.
  function message(box, input, kind, query) {
    clear(box);
    if (kind === 'error') {
      box.appendChild(make('p', null, 'No se ha podido cargar el buscador. Inténtalo de nuevo.'));
      return;
    }
    if (kind === 'empty') {
      box.appendChild(make('p', null, 'No hay resultados para «' + query + '».'));
      [['Ver comparativas', '/mejor-ia/'], ['Ver el catálogo de herramientas', '/herramientas/']].forEach(function (l) {
        var a = make('a', 'search-chip', l[0]);
        a.href = l[1];
        box.appendChild(a);
      });
      return;
    }
    box.appendChild(make('p', null, 'Prueba con:'));
    SUGGEST.forEach(function (s) {
      var b = make('button', 'search-chip', s);
      b.type = 'button';
      b.addEventListener('click', function () { input.value = s; input.dispatchEvent(new Event('input')); input.focus(); });
      box.appendChild(b);
    });
  }
  function count(n) { return n === 1 ? '1 resultado' : n + ' resultados'; }

  // --- Ventana de búsqueda -------------------------------------------------
  var dlg = document.getElementById('search-dialog');
  if (dlg) {
    var input = document.getElementById('search-input'), list = document.getElementById('search-results'),
      msg = dlg.querySelector('.search-msg'), status = dlg.querySelector('.search-status'),
      all = dlg.querySelector('.search-all'), opener = null, active = -1;

    var setActive = function (i) {
      var opts = list.querySelectorAll('[role=option]');
      if (!opts.length) return;
      active = (i + opts.length) % opts.length;
      for (var k = 0; k < opts.length; k++) {
        opts[k].classList.toggle('on', k === active);
        opts[k].setAttribute('aria-selected', String(k === active));
      }
      input.setAttribute('aria-activedescendant', opts[active].id);
      opts[active].scrollIntoView({ block: 'nearest' });
    };
    var run = function () {
      var query = input.value;
      loadIndex().then(function (index) {
        if (input.value !== query) return;
        var found = search(index, query), shown = found.slice(0, MAX_DIALOG), t = terms(query), n = 0;
        clear(list);
        active = -1;
        input.removeAttribute('aria-activedescendant');
        if (!t.length) { message(msg, input, 'suggest'); } else if (!found.length) { message(msg, input, 'empty', query); } else { clear(msg); }
        [['Artículos', function (e) { return e.k !== 'Catálogo'; }],
          ['Herramientas del catálogo', function (e) { return e.k === 'Catálogo'; }]].forEach(function (g) {
          var group = shown.filter(g[1]);
          if (!group.length) return;
          var head = make('div', 'search-group', g[0]);
          head.setAttribute('role', 'presentation');
          list.appendChild(head);
          group.forEach(function (e) { list.appendChild(item(e, t, 'sr-' + n++)); });
        });
        input.setAttribute('aria-expanded', String(shown.length > 0));
        status.textContent = t.length ? (found.partial ? PARTIAL + ' ' : '') + count(found.length) : '';
        all.hidden = !found.length;
        all.href = '/buscar/?q=' + encodeURIComponent(query);
        all.textContent = 'Ver todos (' + found.length + ')';
      }).catch(function () { clear(list); message(msg, input, 'error'); status.textContent = ''; });
    };
    var openDialog = function (ev) {
      if (ev) ev.preventDefault();
      opener = document.activeElement;
      dlg.hidden = false;
      body.classList.add('search-lock');
      input.value = '';
      input.focus();
      run();
    };
    var closeDialog = function () {
      if (dlg.hidden) return;
      dlg.hidden = true;
      body.classList.remove('search-lock');
      input.setAttribute('aria-expanded', 'false');
      if (opener && opener.focus) opener.focus();
    };

    Array.prototype.forEach.call(document.querySelectorAll('.search-open'), function (b) {
      b.addEventListener('click', openDialog);
      ['mouseenter', 'focus'].forEach(function (t) { b.addEventListener(t, function () { loadIndex().catch(function () {}); }); });
    });
    input.addEventListener('input', run);
    input.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
        ev.preventDefault();
        setActive(active + (ev.key === 'ArrowDown' ? 1 : -1));
      } else if (ev.key === 'Enter') {
        ev.preventDefault();
        var opts = list.querySelectorAll('[role=option]');
        if (active >= 0 && opts[active]) opts[active].click();
        else if (terms(input.value).length) location.href = '/buscar/?q=' + encodeURIComponent(input.value);
      }
    });
    dlg.querySelector('.search-close').addEventListener('click', closeDialog);
    dlg.addEventListener('click', function (ev) {
      if (ev.target === dlg) closeDialog();
      else if (ev.target.closest && ev.target.closest('.search-hit, .search-all')) closeDialog();
    });
    document.addEventListener('keydown', function (ev) {
      if (!dlg.hidden) {
        if (ev.key === 'Escape') { ev.preventDefault(); closeDialog(); }
        if (ev.key === 'Tab') {
          var f = Array.prototype.filter.call(dlg.querySelectorAll('input, button, a[href]'),
            function (n) { return !n.hidden && n.offsetParent !== null; });
          var first = f[0], last = f[f.length - 1];
          if (!dlg.contains(document.activeElement)) { ev.preventDefault(); first.focus(); }
          else if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
          else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
        }
        return;
      }
      var t = ev.target, typing = t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName);
      if (ev.key === '/' && !typing && !ev.ctrlKey && !ev.metaKey && !ev.altKey) openDialog(ev);
    });
  }

  // --- Página /buscar/ -------------------------------------------------------
  var pageInput = document.getElementById('search-page-input');
  if (!pageInput || !body.hasAttribute('data-search-page')) return;
  var results = document.getElementById('search-page-results'), filters = document.querySelector('.search-filters'),
    pageStatus = document.querySelector('.search-page-wrap .search-status'), pageMsg = make('div', 'search-msg'),
    kind = 'Todo', refocus = false;
  filters.parentNode.insertBefore(pageMsg, filters);

  var renderPage = function () {
    var query = pageInput.value;
    history.replaceState(null, '', terms(query).length ? '?q=' + encodeURIComponent(query) : location.pathname);
    loadIndex().then(function (index) {
      var found = search(index, query), t = terms(query), counts = { Todo: found.length };
      found.forEach(function (e) { counts[e.k] = (counts[e.k] || 0) + 1; });
      if (!counts[kind]) kind = 'Todo';
      clear(results);
      clear(filters);
      if (!t.length) message(pageMsg, pageInput, 'suggest');
      else if (!found.length) message(pageMsg, pageInput, 'empty', query);
      else clear(pageMsg);
      if (found.length) {
        ['Todo', 'Ficha', 'Comparativa', 'Cara a cara', 'Profesión', 'Guía', 'Noticia', 'Utilidad', 'Página', 'Glosario', 'Prompt', 'Catálogo'].forEach(function (k) {
          if (!counts[k]) return;
          var b = make('button', 'search-chip', k + ' (' + counts[k] + ')');
          b.type = 'button';
          b.setAttribute('aria-pressed', String(k === kind));
          b.addEventListener('click', function () { kind = k; refocus = true; renderPage(); });
          filters.appendChild(b);
        });
      }
      found.filter(function (e) { return kind === 'Todo' || e.k === kind; }).forEach(function (e) {
        var li = make('li');
        li.appendChild(item(e, t));
        results.appendChild(li);
      });
      pageStatus.textContent = t.length ? (found.partial ? PARTIAL + ' ' : '') + count(found.length) : '';
      if (refocus) {
        refocus = false;
        var pressed = filters.querySelector('[aria-pressed="true"]');
        if (pressed) pressed.focus();
      }
    }).catch(function () { clear(results); pageStatus.textContent = ''; message(pageMsg, pageInput, 'error'); });
  };
  pageInput.value = new URLSearchParams(location.search).get('q') || '';
  pageInput.addEventListener('input', renderPage);
  pageInput.form.addEventListener('submit', function (ev) { ev.preventDefault(); renderPage(); });
  renderPage();
})();
