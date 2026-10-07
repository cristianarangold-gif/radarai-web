// Glosario: filtro por texto (sin tildes, también por siglas o alias) y por tema. Sin JS, el glosario se lee entero.
(function () {
  var controls = document.querySelector('.glossary-controls');
  if (!controls) return;
  var input = controls.querySelector('.glossary-filter'), status = controls.querySelector('.glossary-status'),
    buttons = controls.querySelectorAll('.glossary-tema'), empty = document.querySelector('.glossary-empty'),
    groups = document.querySelectorAll('.glossary-group'), tema = '';
  function norm(s) {
    return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, ' ').trim();
  }
  var terms = Array.prototype.map.call(document.querySelectorAll('.term'), function (el) {
    var dt = el.querySelector('dt'), dd = el.querySelector('dd');
    return { el: el, tema: el.getAttribute('data-tema'),
      name: norm(dt.firstChild.textContent + ' ' + (el.getAttribute('data-alias') || '')),
      text: norm(dd.textContent) };
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
    status.textContent = shown === 1 ? '1 término' : shown + ' términos';
    empty.hidden = shown > 0;
  }

  Array.prototype.forEach.call(buttons, function (b) {
    b.addEventListener('click', function () {
      tema = b.getAttribute('data-tema');
      Array.prototype.forEach.call(buttons, function (o) { o.setAttribute('aria-pressed', String(o === b)); });
      update();
    });
  });
  input.addEventListener('input', update);
  controls.hidden = false;
})();
