// Biblioteca de prompts: filtro, huecos rellenables y botón «Copiar». Sin JS, los prompts se leen enteros.
(function () {
  var controls = document.querySelector('.library-controls');
  if (!controls) return;
  var input = controls.querySelector('.library-filter'), status = controls.querySelector('.library-status'),
    buttons = controls.querySelectorAll('[data-cat]'), empty = document.querySelector('.library-empty'),
    groups = document.querySelectorAll('.library-group'), cat = '', timer = null;
  var live = document.createElement('p');
  live.className = 'sr-only';
  live.setAttribute('aria-live', 'polite');
  document.body.appendChild(live);

  function norm(s) {
    return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\s+/g, ' ').trim();
  }
  function say(msg) {
    live.textContent = '';
    setTimeout(function () { live.textContent = msg; }, 50);
  }
  var cards = Array.prototype.map.call(document.querySelectorAll('.prompt-card'), function (el) {
    var search = norm(el.textContent), text = el.querySelector('.prompt-text'), fill = el.querySelector('.prompt-fill'),
      b = document.createElement('button'), reset = null;
    // Huecos: cada campo rellena todas las apariciones de su hueco.
    if (fill) {
      fill.hidden = false;
      Array.prototype.forEach.call(fill.querySelectorAll('input'), function (f) {
        var name = f.getAttribute('data-slot');
        f.addEventListener('input', function () {
          Array.prototype.forEach.call(text.querySelectorAll('mark.slot'), function (m) {
            if (m.getAttribute('data-slot') !== name) return;
            m.textContent = f.value.trim() || '[' + name + ']';
            m.classList.toggle('filled', !!f.value.trim());
          });
        });
      });
    }
    b.type = 'button';
    b.className = 'copy-prompt';
    b.textContent = 'Copiar';
    b.setAttribute('aria-label', 'Copiar el prompt «' + el.querySelector('h3').textContent + '»');
    function done(msg, spoken) {
      b.textContent = msg;
      say(spoken);
      clearTimeout(reset);
      reset = setTimeout(function () { b.textContent = 'Copiar'; }, 2000);
    }
    function select() {
      var range = document.createRange(), sel = window.getSelection();
      range.selectNodeContents(text);
      sel.removeAllRanges();
      sel.addRange(range);
      done('Seleccionado', 'Prompt seleccionado: cópialo con Ctrl+C o Cmd+C');
    }
    b.addEventListener('click', function () {
      var value = text.textContent.trim();
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(value).then(function () { done('Copiado', 'Prompt copiado'); }, select);
      } else {
        select();
      }
    });
    el.querySelector('.prompt-foot').appendChild(b);
    return { el: el, cat: el.getAttribute('data-cat'), text: search };
  });

  function update() {
    var q = norm(input.value), shown = 0;
    cards.forEach(function (c) {
      var ok = (!cat || c.cat === cat) && (!q || c.text.indexOf(q) >= 0);
      c.el.hidden = !ok;
      if (ok) shown++;
    });
    Array.prototype.forEach.call(groups, function (g) { g.hidden = !g.querySelector('.prompt-card:not([hidden])'); });
    empty.hidden = shown > 0;
    clearTimeout(timer);
    timer = setTimeout(function () { status.textContent = shown === 1 ? '1 prompt' : shown + ' prompts'; }, 300);
  }
  function setCat(value) {
    cat = value;
    Array.prototype.forEach.call(buttons, function (o) {
      o.setAttribute('aria-pressed', String(o.getAttribute('data-cat') === value));
    });
  }
  function reveal() {
    var target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target && target.closest('[hidden]')) {
      input.value = '';
      setCat('');
      update();
      target.scrollIntoView();
    }
  }
  Array.prototype.forEach.call(buttons, function (b) {
    b.addEventListener('click', function () { setCat(b.getAttribute('data-cat')); update(); });
  });
  input.addEventListener('input', update);
  window.addEventListener('hashchange', reveal);
  controls.hidden = false;
})();
