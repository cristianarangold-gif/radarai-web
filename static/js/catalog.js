// Buscador del catálogo de la portada: filtra tarjetas y abre los grupos con resultados.
(function () {
  function openFromHash() {
    var group = location.hash.indexOf('#cat-') === 0 && document.getElementById(location.hash.slice(1));
    if (group && group.tagName === 'DETAILS') {
      group.open = true;
      // Tras cargar fuentes y estilos, para que el salto no se pierda.
      window.requestAnimationFrame(function () { setTimeout(function () { group.scrollIntoView({ behavior: 'instant', block: 'start' }); }, 50); });
    }
  }
  openFromHash();
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
