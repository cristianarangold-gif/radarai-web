// «Guardar en mi panel»: guarda prompts de las utilidades y de la biblioteca en localStorage['radar-panel'].
// Mismo formato que static/js/panel.js. Nada se envía a ningún servidor.
(function () {
  'use strict';
  var CLAVE = 'radar-panel';
  var VERSION = 1;
  var MAX = 20000;

  function leer(raw) {
    if (!raw) return { version: VERSION, suscripciones: [], prompts: [], notas: [], proyectos: [] };
    var data = JSON.parse(raw);
    if (!data || data.version !== VERSION) throw new Error('version');
    ['suscripciones', 'prompts', 'notas', 'proyectos'].forEach(function (k) {
      if (data[k] === undefined) data[k] = [];
      if (!Array.isArray(data[k])) throw new Error('formato');
    });
    return data;
  }

  // Devuelve 'nuevo', 'repetido', 'incompatible' o 'error'. Si los datos guardados no se entienden, no se tocan.
  function guardarPrompt(titulo, texto, origen) {
    var raw, estado;
    try { raw = window.localStorage.getItem(CLAVE); } catch (e) { return 'error'; }
    try { estado = leer(raw); } catch (e) { return 'incompatible'; }
    try {
      if (estado.prompts.some(function (p) { return p && p.texto === texto; })) return 'repetido';
      estado.prompts.unshift({
        id: Date.now().toString(36) + Math.random().toString(36).slice(2, 8),
        titulo: titulo.slice(0, 120), texto: texto.slice(0, MAX), origen: origen,
        fecha: new Date().toISOString().slice(0, 10)
      });
      window.localStorage.setItem(CLAVE, JSON.stringify(estado));
      return 'nuevo';
    } catch (e) {
      return 'error';
    }
  }

  function crearBoton(clase, etiqueta) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = clase;
    b.textContent = 'Guardar en mi panel';
    b.setAttribute('aria-label', etiqueta);
    var estado = document.createElement('span');
    estado.className = 'guardado-estado';
    estado.setAttribute('role', 'status');
    return { boton: b, estado: estado };
  }

  function mostrar(estado, resultado) {
    estado.textContent = '';
    if (resultado === 'incompatible') {
      estado.appendChild(document.createTextNode('No se ha guardado: los datos de tu panel no se pueden leer. '));
      var enlace = document.createElement('a');
      enlace.href = '/mi-panel/#copia';
      enlace.textContent = 'Revisa tu panel';
      estado.appendChild(enlace);
      return;
    }
    if (resultado === 'error') {
      estado.textContent = 'Tu navegador no deja guardar datos (quizá estás en modo privado).';
      return;
    }
    estado.appendChild(document.createTextNode(resultado === 'repetido' ? 'Ya estaba guardado ✓ · ' : 'Guardado ✓ · '));
    var a = document.createElement('a');
    a.href = '/mi-panel/#prompts';
    a.textContent = 'Ver mi panel';
    estado.appendChild(a);
  }

  // Utilidades: botón junto a «Copiar»; guarda el resultado si ya hay uno.
  var salida = document.getElementById('radar-output'), copiar = document.getElementById('copy-output');
  if (salida && copiar) {
    var ejemplo = salida.textContent.trim();
    var h1 = document.querySelector('h1');
    var u = crearBoton('btn secondary', 'Guardar el resultado en mi panel');
    copiar.insertAdjacentElement('afterend', u.boton);
    u.boton.insertAdjacentElement('afterend', u.estado);
    u.boton.addEventListener('click', function () {
      var texto = salida.textContent.trim();
      if (!texto || texto === ejemplo) {
        u.estado.textContent = 'Primero genera un resultado.';
        return;
      }
      var titulo = (h1 ? h1.textContent.trim() : 'Utilidad') + ' · ' +
        new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'long' });
      mostrar(u.estado, guardarPrompt(titulo, texto, location.pathname));
    });
  }

  // Biblioteca de prompts: un botón en cada tarjeta; guarda el prompt con los huecos que hayas rellenado.
  Array.prototype.forEach.call(document.querySelectorAll('.prompt-card'), function (card) {
    var texto = card.querySelector('.prompt-text'), h3 = card.querySelector('h3'), pie = card.querySelector('.prompt-foot');
    if (!texto || !h3 || !pie) return;
    var c = crearBoton('copy-prompt', 'Guardar el prompt «' + h3.textContent.trim() + '» en mi panel');
    pie.appendChild(c.boton);
    pie.appendChild(c.estado);
    c.boton.addEventListener('click', function () {
      mostrar(c.estado, guardarPrompt(h3.textContent.trim(), texto.textContent.trim(), location.pathname + '#' + card.id));
    });
  });
})();
