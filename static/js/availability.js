// ¿Funciona en España?: buscador y filtros sobre la tabla. Sin JS, la tabla se ve entera.
(function () {
  var controls = document.querySelector('.avail-controls');
  if (!controls) return;
  var input = controls.querySelector('[data-avail-search]'), buttons = controls.querySelectorAll('[data-avail-filter]'),
    rows = document.querySelectorAll('.avail-table tbody tr'), count = document.querySelector('[data-avail-count]'),
    empty = document.querySelector('[data-avail-empty]'), table = document.querySelector('.avail-table'),
    filter = 'todas';

  function fold(s) {
    return s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
  }
  var texts = Array.prototype.map.call(rows, function (r) { return fold(r.textContent); });

  function apply() {
    var words = fold(input.value).trim().split(/\s+/).filter(Boolean), visible = 0;
    Array.prototype.forEach.call(rows, function (row, i) {
      var show = (filter === 'todas' || row.getAttribute('data-es') === filter) &&
        words.every(function (w) { return texts[i].indexOf(w) !== -1; });
      row.hidden = !show;
      if (show) visible++;
    });
    count.textContent = visible === 1 ? '1 función' : visible + ' funciones';
    empty.hidden = visible !== 0;
    table.hidden = visible === 0;
  }

  Array.prototype.forEach.call(buttons, function (b) {
    b.addEventListener('click', function () {
      filter = b.getAttribute('data-avail-filter');
      Array.prototype.forEach.call(buttons, function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      apply();
    });
  });
  input.addEventListener('input', apply);
  controls.addEventListener('submit', function (e) { e.preventDefault(); });
  controls.hidden = false;
})();
