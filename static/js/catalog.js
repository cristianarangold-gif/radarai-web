// Buscador del catálogo de /herramientas/: filtra tarjetas y abre los grupos con resultados.
(function () {
  function openFromHash() {
    var group = location.hash.indexOf('#cat-') === 0 && document.getElementById(location.hash.slice(1));
    if (group && group.tagName === 'DETAILS') {
      group.open = true;
      group.scrollIntoView({ behavior: 'instant', block: 'start' });
    }
  }
  openFromHash();
  // Repetir cuando terminan de cargar las fuentes (cambian la altura de lo que hay encima),
  // pero solo si el lector no se ha movido desde el primer salto.
  var firstY = window.scrollY;
  window.addEventListener('load', function () {
    setTimeout(function () { if (Math.abs(window.scrollY - firstY) < 2) openFromHash(); }, 0);
  });
  window.addEventListener('hashchange', openFromHash);

  var input = document.getElementById('catalog-search');
  if (!input) return;
  var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
  var cards = Array.prototype.slice.call(document.querySelectorAll('.tool-card'));
  cards.forEach(function (c) { c.dataset.norm = norm(c.dataset.search || ''); });
  input.addEventListener('input', function () {
    var q = norm(input.value.trim());
    document.querySelectorAll('.catalog-group').forEach(function (group) {
      var visible = 0;
      group.querySelectorAll('.tool-card').forEach(function (c) {
        var match = !q || c.dataset.norm.indexOf(q) !== -1;
        c.hidden = !match;
        if (match) visible++;
      });
      group.hidden = visible === 0;
      if (q) group.open = visible > 0;
    });
  });
})();
