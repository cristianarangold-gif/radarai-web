// Índice lateral de fichas y artículos: resalta la sección que se está leyendo y avanza la barra de lectura.
(function () {
  var box = document.querySelector('.toc-box');
  if (!box) return;
  if (window.matchMedia('(max-width: 960px)').matches) box.open = false;

  var links = Array.prototype.slice.call(box.querySelectorAll('.toc a'));
  var heads = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var bar = box.querySelector('.progress i');
  var main = document.querySelector('.article-main');
  var current = -1;

  function update() {
    // Sección activa: el último título que ya ha pasado del 30 % superior de la pantalla.
    var line = window.innerHeight * 0.3, active = -1;
    heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top <= line) active = i; });
    if (active !== current) {
      links.forEach(function (a, i) {
        a.classList.toggle('on', i === active);
        if (i === active) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
      current = active;
    }
    if (bar && main) {
      var r = main.getBoundingClientRect(), total = r.height - window.innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      bar.style.width = (p * 100).toFixed(1) + '%';
    }
  }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
