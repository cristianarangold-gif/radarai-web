// Menú móvil y aviso de cookies (se sustituye por el CMP de Google en la fase 4).
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('menu-principal');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('open', !open);
    });
  }

  var banner = document.getElementById('cookie-banner');
  if (!banner) return;
  function read() { try { return localStorage.getItem('radar-cookie-choice'); } catch (e) { return 'unavailable'; } }
  function save(v) { try { localStorage.setItem('radar-cookie-choice', v); } catch (e) {} banner.hidden = true; }
  if (!read()) banner.hidden = false;
  document.getElementById('cookie-accept').addEventListener('click', function () { save('all'); });
  document.getElementById('cookie-reject').addEventListener('click', function () { save('necessary'); });
})();
