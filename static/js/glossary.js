// Glosario: filtro por texto (sin tildes, también por siglas o alias) y por tema. Sin JS, el glosario se lee entero.
(function () {
  var controls = document.querySelector('.glossary-controls');
  if (!controls) return;
  var input = controls.querySelector('.glossary-filter'), status = controls.querySelector('.glossary-status'),
    buttons = controls.querySelectorAll('.glossary-tema'), empty = document.querySelector('.glossary-empty'),
    groups = document.querySelectorAll('.glossary-group'), letters = document.querySelectorAll('.glossary-letters a'),
    tema = '', timer = null;
  function norm(s) {
    return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\s+/g, ' ').trim();
  }
  var terms = Array.prototype.map.call(document.querySelectorAll('.term'), function (el) {
    return { el: el, tema: el.getAttribute('data-tema'),
      name: norm(el.getAttribute('data-name') + ' ' + (el.getAttribute('data-alias') || '')),
      text: norm(el.querySelector('dd').textContent) };
  });

  function update() {
    var q = norm(input.value), shown = 0;
    terms.forEach(function (t) {
      // Primero se busca en el término y sus alias; con 3 letras o más, también en la definición.
      var ok = (!tema || t.tema === tema) &&
        (!q || t.name.indexOf(q) >= 0 || (q.length >= 3 && t.text.indexOf(q) >= 0));
      t.el.hidden = !ok;
      if (ok) shown++;
    });
    Array.prototype.forEach.call(groups, function (g) { g.hidden = !g.querySelector('.term:not([hidden])'); });
    // Las letras sin resultados se ocultan para no saltar a una sección vacía.
    Array.prototype.forEach.call(letters, function (a) {
      a.hidden = document.getElementById(a.getAttribute('href').slice(1)).parentNode.hidden;
    });
    empty.hidden = shown > 0;
    // El recuento se anuncia (aria-live) cuando se deja de escribir, no en cada tecla.
    clearTimeout(timer);
    timer = setTimeout(function () { status.textContent = shown === 1 ? '1 término' : shown + ' términos'; }, 300);
  }
  function setTema(value) {
    tema = value;
    Array.prototype.forEach.call(buttons, function (o) {
      o.setAttribute('aria-pressed', String(o.getAttribute('data-tema') === value));
    });
  }
  // Si el enlace apunta a un término oculto por el filtro, se quita el filtro y se muestra.
  function reveal() {
    var target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target && target.closest('[hidden]')) {
      input.value = '';
      setTema('');
      update();
      target.scrollIntoView();
    }
  }

  Array.prototype.forEach.call(buttons, function (b) {
    b.addEventListener('click', function () { setTema(b.getAttribute('data-tema')); update(); });
  });
  input.addEventListener('input', update);
  window.addEventListener('hashchange', reveal);
  controls.hidden = false;
})();
