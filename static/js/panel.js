// «Mi panel»: suscripciones de IA, pagos, gasto y copia de seguridad.
// Todo se guarda en localStorage['radar-panel'] de este navegador; nada se envía a ningún servidor.
(function () {
  'use strict';
  var root = document.getElementById('panel');
  if (!root) return;

  var CLAVE = 'radar-panel';
  var VERSION = 1;
  var OTRA = '__otra';
  var MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
    'octubre', 'noviembre', 'diciembre'];
  var euros = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' });
  var precios = { fecha: '', herramientas: {} };
  var editando = null;

  // ---------- Almacenamiento ----------
  function vacio() {
    return { version: VERSION, suscripciones: [], prompts: [], notas: [], proyectos: [] };
  }

  function normalizar(data) {
    var base = vacio();
    if (!data || typeof data !== 'object' || data.version !== VERSION) return null;
    for (var k in base) {
      if (k === 'version') continue;
      if (data[k] === undefined) continue;
      if (!Array.isArray(data[k])) return null;
      base[k] = data[k];
    }
    base.suscripciones = base.suscripciones.filter(valida);
    return base;
  }

  function valida(s) {
    return s && typeof s === 'object' && typeof s.nombre === 'string' && s.nombre &&
      typeof s.euros === 'number' && isFinite(s.euros) && s.euros >= 0 &&
      (s.ciclo === 'mensual' || s.ciclo === 'anual') &&
      Number.isInteger(s.dia) && s.dia >= 1 && s.dia <= 31 &&
      (s.ciclo === 'mensual' || (Number.isInteger(s.mes) && s.mes >= 1 && s.mes <= 12));
  }

  function cargar() {
    try {
      var raw = window.localStorage.getItem(CLAVE);
      return (raw && normalizar(JSON.parse(raw))) || vacio();
    } catch (e) {
      return vacio();
    }
  }

  function guardar(estado) {
    try {
      window.localStorage.setItem(CLAVE, JSON.stringify(estado));
      return true;
    } catch (e) {
      avisoError('Tu navegador no deja guardar datos (quizá estás en modo privado o sin espacio). ' +
        'Lo que hagas ahora solo durará mientras tengas abierta esta página.');
      return false;
    }
  }

  var estado = cargar();
  window.RadarPanel = { cargar: cargar, guardar: guardar };

  function avisoError(texto) {
    var aviso = document.getElementById('panel-aviso');
    aviso.textContent = texto;
    aviso.classList.add('panel-error');
  }

  function nuevoId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  function el(tag, attrs, hijos) {
    var n = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'text') n.textContent = attrs[k];
      else if (k === 'class') n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    }
    (hijos || []).forEach(function (h) { if (h) n.appendChild(typeof h === 'string' ? document.createTextNode(h) : h); });
    return n;
  }

  // ---------- Fechas ----------
  function diasDelMes(anio, mes0) { return new Date(anio, mes0 + 1, 0).getDate(); }

  function fechaCobro(s, anio, mes0) {
    if (s.ciclo === 'anual' && s.mes - 1 !== mes0) return null;
    return new Date(anio, mes0, Math.min(s.dia, diasDelMes(anio, mes0)));
  }

  function hoy() { var d = new Date(); return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }

  function proximoCobro(s) {
    var h = hoy();
    for (var i = 0; i < 25; i++) {
      var anio = h.getFullYear() + Math.floor((h.getMonth() + i) / 12);
      var mes0 = (h.getMonth() + i) % 12;
      var f = fechaCobro(s, anio, mes0);
      if (f && f >= h) return f;
    }
    return h;
  }

  function fechaLarga(iso) {
    var p = (iso || '').split('-');
    if (p.length !== 3) return iso;
    return parseInt(p[2], 10) + ' de ' + MESES[parseInt(p[1], 10) - 1] + ' de ' + p[0];
  }

  // ---------- Formulario «Mis IA» ----------
  var f = {
    form: document.getElementById('form-ia'), herramienta: document.getElementById('ia-herramienta'),
    nombre: document.getElementById('ia-nombre'), campoNombre: document.getElementById('campo-nombre'),
    plan: document.getElementById('ia-plan'), planes: document.getElementById('ia-planes'),
    importe: document.getElementById('ia-importe'), ciclo: document.getElementById('ia-ciclo'),
    dia: document.getElementById('ia-dia'), mes: document.getElementById('ia-mes'),
    campoMes: document.getElementById('campo-mes'), nota: document.getElementById('ia-nota'),
    boton: document.getElementById('ia-guardar'), cancelar: document.getElementById('ia-cancelar')
  };

  MESES.forEach(function (m, i) { f.mes.appendChild(el('option', { value: String(i + 1), text: m })); });
  f.mes.value = String(new Date().getMonth() + 1);

  function rellenarHerramientas() {
    var actual = f.herramienta.value;
    f.herramienta.textContent = '';
    f.herramienta.appendChild(el('option', { value: '', text: 'Elige una herramienta…' }));
    Object.keys(precios.herramientas)
      .sort(function (a, b) { return precios.herramientas[a].nombre.localeCompare(precios.herramientas[b].nombre, 'es'); })
      .forEach(function (id) { f.herramienta.appendChild(el('option', { value: id, text: precios.herramientas[id].nombre })); });
    f.herramienta.appendChild(el('option', { value: OTRA, text: 'Otra IA' }));
    if (actual) f.herramienta.value = actual;
  }

  function planesDe(id) { return (precios.herramientas[id] || {}).planes || {}; }

  function alCambiarHerramienta() {
    var id = f.herramienta.value;
    f.campoNombre.hidden = id !== OTRA;
    f.nombre.required = id === OTRA;
    f.planes.textContent = '';
    Object.keys(planesDe(id)).forEach(function (p) {
      f.planes.appendChild(el('option', { value: p, text: planesDe(id)[p].texto }));
    });
    f.nota.textContent = id && id !== OTRA
      ? 'Escribe o elige el plan: rellenamos el precio con nuestra revisión del ' + fechaLarga(precios.fecha) + '.'
      : '';
  }

  function alCambiarPlan() {
    var info = planesDe(f.herramienta.value)[f.plan.value];
    if (!info) return;
    f.importe.value = info.euros.toFixed(2);
    f.ciclo.value = info.ciclo;
    alCambiarCiclo();
    f.nota.textContent = info.desde
      ? 'Este plan cuesta «' + info.texto + '»: hemos puesto el mínimo. Cambia el importe por el que pagas.'
      : 'Precio según nuestra revisión del ' + fechaLarga(precios.fecha) + ': ' + info.texto + '.';
  }

  function alCambiarCiclo() { f.campoMes.hidden = f.ciclo.value !== 'anual'; }

  function limpiarFormulario() {
    editando = null;
    f.form.reset();
    f.mes.value = String(new Date().getMonth() + 1);
    f.boton.textContent = 'Añadir';
    f.cancelar.hidden = true;
    alCambiarHerramienta();
    alCambiarCiclo();
  }

  f.herramienta.addEventListener('change', alCambiarHerramienta);
  f.plan.addEventListener('change', alCambiarPlan);
  f.plan.addEventListener('input', alCambiarPlan);
  f.ciclo.addEventListener('change', alCambiarCiclo);
  f.cancelar.addEventListener('click', limpiarFormulario);

  f.form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var id = f.herramienta.value;
    var esNuestra = id && id !== OTRA;
    var s = {
      id: editando || nuevoId(),
      herramienta: esNuestra ? id : '',
      nombre: esNuestra ? precios.herramientas[id].nombre : f.nombre.value.trim(),
      plan: f.plan.value.trim(),
      euros: Math.round(parseFloat(String(f.importe.value).replace(',', '.')) * 100) / 100,
      ciclo: f.ciclo.value,
      dia: parseInt(f.dia.value, 10),
      mes: f.ciclo.value === 'anual' ? parseInt(f.mes.value, 10) : null
    };
    if (!valida(s)) {
      f.nota.textContent = 'Revisa los datos: falta el nombre, el importe o el día del cobro (de 1 a 31).';
      return;
    }
    var i = estado.suscripciones.findIndex(function (x) { return x.id === s.id; });
    if (i >= 0) estado.suscripciones[i] = s; else estado.suscripciones.push(s);
    guardar(estado);
    limpiarFormulario();
    pintar();
  });

  function editar(s) {
    editando = s.id;
    f.herramienta.value = s.herramienta && precios.herramientas[s.herramienta] ? s.herramienta : OTRA;
    alCambiarHerramienta();
    f.nombre.value = s.herramienta ? '' : s.nombre;
    f.plan.value = s.plan;
    f.importe.value = s.euros.toFixed(2);
    f.ciclo.value = s.ciclo;
    f.dia.value = s.dia;
    if (s.mes) f.mes.value = String(s.mes);
    alCambiarCiclo();
    f.boton.textContent = 'Guardar cambios';
    f.cancelar.hidden = false;
    f.form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    f.herramienta.focus();
  }

  function borrar(s) {
    if (!window.confirm('¿Borrar ' + s.nombre + (s.plan ? ' (' + s.plan + ')' : '') + '?')) return;
    estado.suscripciones = estado.suscripciones.filter(function (x) { return x.id !== s.id; });
    guardar(estado);
    if (editando === s.id) limpiarFormulario();
    pintar();
  }

  function importeTexto(s) { return euros.format(s.euros) + (s.ciclo === 'anual' ? '/año' : '/mes'); }

  function avisoPrecio(s) {
    var info = s.herramienta && planesDe(s.herramienta)[s.plan];
    if (!info || info.desde || info.ciclo !== s.ciclo || Math.abs(info.euros - s.euros) < 0.005) return null;
    return el('p', { class: 'panel-cambio' }, [
      'Según nuestra revisión del ' + fechaLarga(precios.fecha) + ', ahora cuesta ' + info.texto + '. ',
      el('a', { href: '/historial-de-precios/#precios-' + s.herramienta, text: 'Ver el historial' })
    ]);
  }

  function pintarLista() {
    var ul = document.getElementById('lista-ias');
    ul.textContent = '';
    if (!estado.suscripciones.length) {
      ul.appendChild(el('li', { class: 'panel-vacio', text: 'Aún no has añadido ninguna IA. Empieza con el formulario de arriba.' }));
      return;
    }
    estado.suscripciones.slice().sort(function (a, b) { return a.nombre.localeCompare(b.nombre, 'es'); }).forEach(function (s) {
      var cuando = s.ciclo === 'anual' ? 'cobro el ' + s.dia + ' de ' + MESES[s.mes - 1] : 'cobro el día ' + s.dia;
      var editarBtn = el('button', { type: 'button', class: 'btn secondary', text: 'Editar' });
      var borrarBtn = el('button', { type: 'button', class: 'btn secondary', text: 'Borrar' });
      editarBtn.addEventListener('click', function () { editar(s); });
      borrarBtn.addEventListener('click', function () { borrar(s); });
      ul.appendChild(el('li', { class: 'panel-item' }, [
        el('div', { class: 'panel-item-main' }, [
          el('strong', { text: s.nombre }), s.plan ? el('span', { class: 'panel-plan', text: ' · ' + s.plan }) : null,
          el('p', { class: 'meta', text: importeTexto(s) + ' · ' + cuando }), avisoPrecio(s)
        ]),
        el('div', { class: 'panel-item-actions' }, [editarBtn, borrarBtn])
      ]));
    });
  }

  // ---------- Pagos y gasto ----------
  function gastoMensual(s) { return s.ciclo === 'anual' ? s.euros / 12 : s.euros; }
  function gastoAnual(s) { return s.ciclo === 'anual' ? s.euros : s.euros * 12; }

  function pintarPagos() {
    var subs = estado.suscripciones;
    var mes = subs.reduce(function (t, s) { return t + gastoMensual(s); }, 0);
    var anio = subs.reduce(function (t, s) { return t + gastoAnual(s); }, 0);
    var tot = document.getElementById('totales');
    tot.textContent = '';
    tot.appendChild(el('div', { class: 'panel-total' }, [el('span', { text: 'Al mes' }), el('strong', { text: euros.format(mes) })]));
    tot.appendChild(el('div', { class: 'panel-total' }, [el('span', { text: 'Al año' }), el('strong', { text: euros.format(anio) })]));
    tot.appendChild(el('div', { class: 'panel-total' }, [el('span', { text: 'Suscripciones' }), el('strong', { text: String(subs.length) })]));

    var cobros = document.getElementById('cobros');
    cobros.textContent = '';
    var h = hoy();
    for (var i = 0; i < 2; i++) {
      var anioM = h.getFullYear() + Math.floor((h.getMonth() + i) / 12);
      var mes0 = (h.getMonth() + i) % 12;
      var lista = subs.map(function (s) { return { s: s, f: fechaCobro(s, anioM, mes0) }; })
        .filter(function (x) { return x.f; }).sort(function (a, b) { return a.f - b.f; });
      var total = lista.reduce(function (t, x) { return t + x.s.euros; }, 0);
      var bloque = el('div', { class: 'panel-mes' }, [
        el('h4', { text: MESES[mes0].charAt(0).toUpperCase() + MESES[mes0].slice(1) + ' ' + anioM + ' · ' + euros.format(total) })
      ]);
      var ul = el('ul', { class: 'panel-cobros' });
      if (!lista.length) ul.appendChild(el('li', { class: 'panel-vacio', text: 'Sin cobros.' }));
      lista.forEach(function (x) {
        var pasado = x.f < h;
        ul.appendChild(el('li', { class: pasado ? 'panel-pasado' : '' }, [
          el('time', { datetime: x.f.toISOString().slice(0, 10), text: x.f.getDate() + ' de ' + MESES[x.f.getMonth()] }),
          el('span', { text: x.s.nombre + (x.s.plan ? ' (' + x.s.plan + ')' : '') }),
          el('strong', { text: euros.format(x.s.euros) + (pasado ? ' · cobrado' : '') })
        ]));
      });
      bloque.appendChild(ul);
      cobros.appendChild(bloque);
    }

    var desg = document.getElementById('desglose');
    desg.textContent = '';
    if (!subs.length) { desg.appendChild(el('p', { class: 'panel-vacio', text: 'Añade tus IA en «Mis IA» para ver tu gasto.' })); return; }
    var ul2 = el('ul', { class: 'panel-desglose' });
    subs.slice().sort(function (a, b) { return gastoAnual(b) - gastoAnual(a); }).forEach(function (s) {
      var pct = anio > 0 ? Math.round(gastoAnual(s) / anio * 100) : 0;
      var barra = el('span', { class: 'panel-barra', 'aria-hidden': 'true' });
      barra.style.width = pct + '%';
      ul2.appendChild(el('li', {}, [
        el('span', { text: s.nombre + (s.plan ? ' (' + s.plan + ')' : '') }),
        el('strong', { text: euros.format(gastoAnual(s)) + '/año · ' + pct + ' %' }), barra
      ]));
    });
    desg.appendChild(ul2);
  }

  // ---------- Calendario (.ics, RFC 5545) ----------
  function icsTexto(t) {
    return String(t).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
  }

  // Líneas de 75 bytes como máximo (las tildes ocupan 2 bytes en UTF-8); la continuación empieza por un espacio.
  var codificador = new TextEncoder();
  function plegar(linea) {
    var out = [], actual = '', bytes = 0;
    Array.from(linea).forEach(function (c) {
      var n = codificador.encode(c).length;
      if (bytes + n > 74) { out.push(actual); actual = ' '; bytes = 1; }
      actual += c; bytes += n;
    });
    out.push(actual);
    return out.join('\r\n');
  }

  function dosCifras(n) { return (n < 10 ? '0' : '') + n; }
  function icsFecha(d) { return d.getFullYear() + dosCifras(d.getMonth() + 1) + dosCifras(d.getDate()); }

  function regla(s) {
    var dias = String(s.dia);
    var extra = '';
    if (s.dia >= 29) {
      var lista = [];
      for (var d = 28; d <= s.dia; d++) lista.push(d);
      dias = lista.join(',');
      extra = ';BYSETPOS=-1';
    }
    return s.ciclo === 'anual'
      ? 'RRULE:FREQ=YEARLY;BYMONTH=' + s.mes + ';BYMONTHDAY=' + dias + extra
      : 'RRULE:FREQ=MONTHLY;BYMONTHDAY=' + dias + extra;
  }

  function generarIcs() {
    var ahora = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    var lineas = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Radar IA//Mi panel//ES', 'CALSCALE:GREGORIAN',
      'X-WR-CALNAME:Cobros de IA (Radar IA)'];
    estado.suscripciones.forEach(function (s) {
      var inicio = proximoCobro(s);
      var fin = new Date(inicio.getFullYear(), inicio.getMonth(), inicio.getDate() + 1);
      lineas.push('BEGIN:VEVENT', 'UID:' + s.id + '@radarai.es', 'DTSTAMP:' + ahora,
        'DTSTART;VALUE=DATE:' + icsFecha(inicio), 'DTEND;VALUE=DATE:' + icsFecha(fin), regla(s),
        'SUMMARY:' + icsTexto('Cobro de ' + s.nombre + (s.plan ? ' (' + s.plan + ')' : '')),
        'DESCRIPTION:' + icsTexto('Importe: ' + importeTexto(s) + '. Apuntado en Mi panel de Radar IA: https://radarai.es/mi-panel/'),
        'TRANSP:TRANSPARENT', 'END:VEVENT');
    });
    lineas.push('END:VCALENDAR');
    return lineas.map(plegar).join('\r\n') + '\r\n';
  }

  function descargar(nombre, contenido, tipo) {
    var url = URL.createObjectURL(new Blob([contenido], { type: tipo }));
    var a = el('a', { href: url, download: nombre });
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  document.getElementById('descargar-ics').addEventListener('click', function () {
    if (!estado.suscripciones.length) { window.alert('Añade primero alguna IA en «Mis IA».'); return; }
    descargar('cobros-ia-radar.ics', generarIcs(), 'text/calendar;charset=utf-8');
  });

  // ---------- Copia de seguridad ----------
  var copiaEstado = document.getElementById('copia-estado');

  document.getElementById('exportar').addEventListener('click', function () {
    var copia = JSON.stringify(Object.assign({ app: 'Mi panel de Radar IA', exportado: new Date().toISOString() }, estado), null, 2);
    descargar('radar-panel-' + icsFecha(new Date()).replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') + '.json', copia, 'application/json');
    copiaEstado.textContent = 'Copia descargada. Guárdala en un lugar seguro.';
  });

  document.getElementById('importar').addEventListener('change', function (ev) {
    var archivo = ev.target.files && ev.target.files[0];
    ev.target.value = '';
    if (!archivo) return;
    var lector = new FileReader();
    lector.onload = function () {
      var datos = null;
      try { datos = normalizar(JSON.parse(lector.result)); } catch (e) { datos = null; }
      if (!datos) {
        copiaEstado.textContent = 'Ese archivo no es una copia de «Mi panel» (o es de otra versión). No se ha cambiado nada.';
        return;
      }
      var n = datos.suscripciones.length;
      if (!window.confirm('La copia tiene ' + n + ' suscripción' + (n === 1 ? '' : 'es') +
        '. Sustituirá todo lo que tienes ahora en el panel. ¿Continuar?')) return;
      estado = datos;
      guardar(estado);
      limpiarFormulario();
      pintar();
      copiaEstado.textContent = 'Copia cargada.';
    };
    lector.onerror = function () { copiaEstado.textContent = 'No se ha podido leer el archivo. No se ha cambiado nada.'; };
    lector.readAsText(archivo);
  });

  // ---------- Pestañas ----------
  var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
  function activar(tab, foco) {
    tabs.forEach(function (t) {
      var sel = t === tab;
      t.setAttribute('aria-selected', String(sel));
      t.tabIndex = sel ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !sel;
    });
    if (foco) tab.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { activar(t, false); });
    t.addEventListener('keydown', function (ev) {
      var j = ev.key === 'ArrowRight' ? i + 1 : ev.key === 'ArrowLeft' ? i - 1 : ev.key === 'Home' ? 0 : ev.key === 'End' ? tabs.length - 1 : null;
      if (j === null) return;
      ev.preventDefault();
      activar(tabs[(j + tabs.length) % tabs.length], true);
    });
  });
  var inicial = document.getElementById('tab-' + (location.hash || '').slice(1));
  if (inicial) activar(inicial, false);

  // ---------- Arranque ----------
  function pintar() { pintarLista(); pintarPagos(); }

  rellenarHerramientas();
  limpiarFormulario();
  pintar();
  try { window.localStorage.setItem(CLAVE + '-prueba', '1'); window.localStorage.removeItem(CLAVE + '-prueba'); }
  catch (e) { avisoError('Tu navegador no deja guardar datos (quizá estás en modo privado). Lo que hagas ahora solo durará mientras tengas abierta esta página.'); }

  fetch(root.getAttribute('data-precios'))
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (data) {
      if (!data || !data.herramientas) return;
      precios = data;
      rellenarHerramientas();
      alCambiarHerramienta();
      pintar();
    })
    .catch(function () { /* sin precios: se puede seguir con «Otra IA» */ });
})();
