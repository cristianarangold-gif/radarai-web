// Menú móvil y botón de modo claro/oscuro. El consentimiento de cookies lo gestiona el CMP de Google (AdSense > Privacidad y mensajes).
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('menu-principal');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function () {
    var open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('open', !open);
  });
})();

// Modo claro/oscuro: por defecto sigue al dispositivo; el botón fija la elección y la recuerda (localStorage 'radar-tema').
(function () {
  var btn = document.querySelector('.theme-toggle');
  if (!btn) return;
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function effectiveTheme() {
    var chosen = root.getAttribute('data-theme');
    if (chosen === 'light' || chosen === 'dark') return chosen;
    return media && media.matches ? 'dark' : 'light';
  }
  function paint() {
    var label = effectiveTheme() === 'dark' ? 'Activar modo claro' : 'Activar modo oscuro';
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
  }
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    // La barra del navegador en móvil sigue la elección, no solo el ajuste del sistema.
    document.querySelectorAll('meta[name="theme-color"]').forEach(function (m) {
      m.setAttribute('content', theme === 'dark' ? '#17150f' : '#fbf8f3');
    });
    try { localStorage.setItem('radar-tema', theme); } catch (e) { /* sin almacenamiento: solo para esta página */ }
    paint();
  }
  btn.addEventListener('click', function () {
    applyTheme(effectiveTheme() === 'dark' ? 'light' : 'dark');
  });
  if (media) {
    var onChange = function () { if (!root.hasAttribute('data-theme')) paint(); };
    if (media.addEventListener) media.addEventListener('change', onChange); else if (media.addListener) media.addListener(onChange);
  }
  btn.hidden = false;
  paint();
})();
