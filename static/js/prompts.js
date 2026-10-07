// Botón «Copiar» en cada prompt (cita) de las páginas con prompts. Sin portapapeles, deja el texto seleccionado.
(function () {
  var quotes = document.querySelectorAll('.prompt-page blockquote');
  if (!quotes.length) return;
  var live = document.createElement('p');
  live.className = 'sr-only';
  live.setAttribute('aria-live', 'polite');
  document.body.appendChild(live);

  function select(el) {
    var range = document.createRange(), sel = window.getSelection();
    range.selectNodeContents(el);
    sel.removeAllRanges();
    sel.addRange(range);
  }
  Array.prototype.forEach.call(quotes, function (q) {
    var text = q.textContent.trim(), b = document.createElement('button');
    b.type = 'button';
    b.className = 'copy-prompt';
    b.textContent = 'Copiar';
    b.addEventListener('click', function () {
      function done(msg) {
        b.textContent = msg;
        live.textContent = msg === 'Copiado' ? 'Prompt copiado' : 'Prompt seleccionado: cópialo con Ctrl+C o Cmd+C';
        setTimeout(function () { b.textContent = 'Copiar'; }, 2000);
      }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done('Copiado'); },
          function () { select(q.firstElementChild || q); done('Seleccionado'); });
      } else {
        select(q.firstElementChild || q);
        done('Seleccionado');
      }
    });
    q.classList.add('has-copy');
    q.appendChild(b);
  });
})();
