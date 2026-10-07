// Botón «Copiar» en cada prompt (cita) de las páginas con prompts. Sin portapapeles, deja el texto seleccionado.
(function () {
  var quotes = document.querySelectorAll('.prompt-page blockquote');
  if (!quotes.length) return;
  var live = document.createElement('p');
  live.className = 'sr-only';
  live.setAttribute('aria-live', 'polite');
  document.body.appendChild(live);

  function say(msg) {
    live.textContent = '';
    setTimeout(function () { live.textContent = msg; }, 50);
  }
  Array.prototype.forEach.call(quotes, function (q, i) {
    var text = q.textContent.trim(), b = document.createElement('button'), timer = null;
    b.type = 'button';
    b.className = 'copy-prompt';
    b.textContent = 'Copiar';
    b.setAttribute('aria-label', 'Copiar prompt ' + (i + 1));
    function done(msg, spoken) {
      b.textContent = msg;
      say(spoken);
      clearTimeout(timer);
      timer = setTimeout(function () { b.textContent = 'Copiar'; }, 2000);
    }
    function select() {
      var range = document.createRange(), sel = window.getSelection();
      range.setStart(q, 0);
      range.setEndBefore(b);
      sel.removeAllRanges();
      sel.addRange(range);
      done('Seleccionado', 'Prompt seleccionado: cópialo con Ctrl+C o Cmd+C');
    }
    b.addEventListener('click', function () {
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done('Copiado', 'Prompt ' + (i + 1) + ' copiado'); },
          select);
      } else {
        select();
      }
    });
    q.classList.add('has-copy');
    q.appendChild(b);
  });
})();
