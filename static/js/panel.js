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
    base.prompts = base.prompts.filter(validaPrompt);
    base.notas = base.notas.filter(validaNota);
    base.proyectos = base.proyectos.filter(function (p, i, l) {
      return typeof p === 'string' && p.trim() && l.indexOf(p) === i;
    });
    return base;
  }

  function texto(x) { return typeof x === 'string'; }
  function validaPrompt(p) { return p && typeof p === 'object' && texto(p.id) && texto(p.titulo) && texto(p.texto) && p.texto; }
  function validaNota(n) {
    return n && typeof n === 'object' && texto(n.id) && texto(n.titulo) && n.titulo && texto(n.texto) &&
      (n.proyecto === undefined || texto(n.proyecto));
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

  // ---------- Prompts ----------
  function copiarTexto(valor, boton) {
    var original = boton.textContent;
    function hecho(msg) { boton.textContent = msg; setTimeout(function () { boton.textContent = original; }, 2000); }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(valor).then(function () { hecho('Copiado'); }, function () { hecho('No se pudo copiar'); });
    } else {
      hecho('No se pudo copiar');
    }
  }

  function fechaCorta(iso) { return iso ? fechaLarga(iso) : ''; }

  function pintarPrompts() {
    var ul = document.getElementById('lista-prompts');
    ul.textContent = '';
    if (!estado.prompts.length) {
      ul.appendChild(el('li', { class: 'panel-vacio', text: 'Aún no has guardado ningún prompt.' }));
      return;
    }
    estado.prompts.forEach(function (p) {
      var li = el('li', { class: 'panel-item panel-prompt' });
      var meta = [p.fecha ? 'Guardado el ' + fechaCorta(p.fecha) : ''];
      var cuerpo = el('div', { class: 'panel-item-main' }, [
        el('strong', { text: p.titulo || 'Prompt sin título' }),
        el('p', { class: 'meta' }, [meta[0], p.origen && p.origen.charAt(0) === '/' ? (meta[0] ? ' · ' : '') : '',
          p.origen && p.origen.charAt(0) === '/' ? el('a', { href: p.origen, text: 'Ver de dónde viene' }) : null]),
        el('pre', { class: 'panel-texto', text: p.texto })
      ]);
      var copiarBtn = el('button', { type: 'button', class: 'btn secondary', text: 'Copiar' });
      var editarBtn = el('button', { type: 'button', class: 'btn secondary', text: 'Editar' });
      var borrarBtn = el('button', { type: 'button', class: 'btn secondary', text: 'Borrar' });
      copiarBtn.addEventListener('click', function () { copiarTexto(p.texto, copiarBtn); });
      editarBtn.addEventListener('click', function () { editarPrompt(p, li); });
      borrarBtn.addEventListener('click', function () {
        if (!window.confirm('¿Borrar el prompt «' + (p.titulo || 'sin título') + '»?')) return;
        estado.prompts = estado.prompts.filter(function (x) { return x.id !== p.id; });
        guardar(estado);
        pintarPrompts();
      });
      li.appendChild(cuerpo);
      li.appendChild(el('div', { class: 'panel-item-actions' }, [copiarBtn, editarBtn, borrarBtn]));
      ul.appendChild(li);
    });
  }

  function editarPrompt(p, li) {
    var idT = 'pt-' + p.id, idX = 'px-' + p.id;
    var titulo = el('input', { id: idT, maxlength: '120', value: p.titulo });
    var area = el('textarea', { id: idX, rows: '8' });
    area.value = p.texto;
    var ok = el('button', { type: 'submit', class: 'btn primary', text: 'Guardar cambios' });
    var no = el('button', { type: 'button', class: 'btn secondary', text: 'Cancelar' });
    var form = el('form', { class: 'panel-form utility-app panel-editor' }, [
      el('div', { class: 'field' }, [el('label', { for: idT, text: 'Título' }), titulo]),
      el('div', { class: 'field' }, [el('label', { for: idX, text: 'Prompt' }), area]),
      el('div', { class: 'actions' }, [ok, no])
    ]);
    no.addEventListener('click', pintarPrompts);
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!area.value.trim()) { area.focus(); return; }
      p.titulo = titulo.value.trim();
      p.texto = area.value.trim();
      guardar(estado);
      pintarPrompts();
    });
    li.textContent = '';
    li.appendChild(form);
    titulo.focus();
  }

  // ---------- Notas por proyecto ----------
  var n = {
    form: document.getElementById('form-nota'), proyecto: document.getElementById('nota-proyecto'),
    titulo: document.getElementById('nota-titulo'), texto: document.getElementById('nota-texto'),
    aviso: document.getElementById('nota-aviso'), boton: document.getElementById('nota-guardar'),
    cancelar: document.getElementById('nota-cancelar'), filtro: document.getElementById('filtro-proyecto'),
    borrarProyecto: document.getElementById('borrar-proyecto'), formProyecto: document.getElementById('form-proyecto'),
    nuevoProyecto: document.getElementById('proyecto-nombre')
  };
  var TODAS = '__todas';
  var editandoNota = null;

  function opciones(select, lista, actual) {
    select.textContent = '';
    lista.forEach(function (o) { select.appendChild(el('option', { value: o[0], text: o[1] })); });
    select.value = lista.some(function (o) { return o[0] === actual; }) ? actual : lista[0][0];
  }

  function proyectosOrdenados() { return estado.proyectos.slice().sort(function (a, b) { return a.localeCompare(b, 'es'); }); }

  function pintarSelectores() {
    var ps = proyectosOrdenados().map(function (p) { return [p, p]; });
    opciones(n.proyecto, [['', 'Sin proyecto']].concat(ps), n.proyecto.value);
    opciones(n.filtro, [[TODAS, 'Todas las notas'], ['', 'Sin proyecto']].concat(ps), n.filtro.value || TODAS);
    n.borrarProyecto.hidden = n.filtro.value === TODAS || n.filtro.value === '';
  }

  function limpiarNota() {
    editandoNota = null;
    n.titulo.value = '';
    n.texto.value = '';
    n.aviso.textContent = '';
    n.boton.textContent = 'Añadir nota';
    n.cancelar.hidden = true;
  }

  function pintarNotas() {
    pintarSelectores();
    var ul = document.getElementById('lista-notas');
    ul.textContent = '';
    var filtro = n.filtro.value;
    var lista = estado.notas.filter(function (x) { return filtro === TODAS || (x.proyecto || '') === filtro; });
    if (!lista.length) {
      ul.appendChild(el('li', { class: 'panel-vacio', text: estado.notas.length ? 'No hay notas en este proyecto.' : 'Aún no tienes notas.' }));
      return;
    }
    lista.forEach(function (x) {
      var editarBtn = el('button', { type: 'button', class: 'btn secondary', text: 'Editar' });
      var borrarBtn = el('button', { type: 'button', class: 'btn secondary', text: 'Borrar' });
      editarBtn.addEventListener('click', function () {
        editandoNota = x.id;
        n.proyecto.value = x.proyecto || '';
        n.titulo.value = x.titulo;
        n.texto.value = x.texto;
        n.boton.textContent = 'Guardar cambios';
        n.cancelar.hidden = false;
        n.form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        n.titulo.focus();
      });
      borrarBtn.addEventListener('click', function () {
        if (!window.confirm('¿Borrar la nota «' + x.titulo + '»?')) return;
        estado.notas = estado.notas.filter(function (y) { return y.id !== x.id; });
        guardar(estado);
        if (editandoNota === x.id) limpiarNota();
        pintarNotas();
      });
      ul.appendChild(el('li', { class: 'panel-item' }, [
        el('div', { class: 'panel-item-main' }, [
          el('strong', { text: x.titulo }),
          el('p', { class: 'meta', text: (x.proyecto || 'Sin proyecto') + (x.fecha ? ' · ' + fechaCorta(x.fecha) : '') }),
          x.texto ? el('p', { class: 'panel-texto', text: x.texto }) : null
        ]),
        el('div', { class: 'panel-item-actions' }, [editarBtn, borrarBtn])
      ]));
    });
  }

  n.formProyecto.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var nombre = n.nuevoProyecto.value.trim().slice(0, 60);
    if (!nombre) return;
    if (estado.proyectos.indexOf(nombre) < 0) estado.proyectos.push(nombre);
    guardar(estado);
    n.nuevoProyecto.value = '';
    n.proyecto.value = nombre;
    pintarSelectores();
    n.proyecto.value = nombre;
    n.filtro.value = nombre;
    pintarNotas();
  });

  n.form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var titulo = n.titulo.value.trim();
    if (!titulo) { n.aviso.textContent = 'Ponle un título a la nota.'; n.titulo.focus(); return; }
    var previa = estado.notas.filter(function (x) { return x.id === editandoNota; })[0];
    var nota = {
      id: editandoNota || nuevoId(), proyecto: n.proyecto.value, titulo: titulo.slice(0, 120),
      texto: n.texto.value.trim().slice(0, 5000), fecha: previa ? previa.fecha : new Date().toISOString().slice(0, 10)
    };
    if (previa) estado.notas[estado.notas.indexOf(previa)] = nota; else estado.notas.unshift(nota);
    guardar(estado);
    limpiarNota();
    pintarNotas();
  });

  n.cancelar.addEventListener('click', limpiarNota);
  n.filtro.addEventListener('change', pintarNotas);

  n.borrarProyecto.addEventListener('click', function () {
    var p = n.filtro.value;
    var cuantas = estado.notas.filter(function (x) { return x.proyecto === p; }).length;
    if (!window.confirm('¿Borrar el proyecto «' + p + '»?' + (cuantas ? ' Sus ' + cuantas + ' nota' + (cuantas === 1 ? '' : 's') +
      ' no se borran: pasan a «Sin proyecto».' : ''))) return;
    estado.proyectos = estado.proyectos.filter(function (x) { return x !== p; });
    estado.notas.forEach(function (x) { if (x.proyecto === p) x.proyecto = ''; });
    guardar(estado);
    n.filtro.value = TODAS;
    pintarNotas();
  });

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
      function cuenta(k, uno, varios) { var c = datos[k].length; return c + ' ' + (c === 1 ? uno : varios); }
      if (!window.confirm('La copia tiene ' + cuenta('suscripciones', 'suscripción', 'suscripciones') + ', ' +
        cuenta('prompts', 'prompt', 'prompts') + ' y ' + cuenta('notas', 'nota', 'notas') +
        '. Sustituirá todo lo que tienes ahora en el panel. ¿Continuar?')) return;
      estado = datos;
      guardar(estado);
      limpiarFormulario();
      limpiarNota();
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
  function desdeAncla() {
    var t = document.getElementById('tab-' + (location.hash || '').slice(1));
    if (t && tabs.indexOf(t) >= 0) activar(t, false);
  }
  desdeAncla();
  window.addEventListener('hashchange', desdeAncla);

  // ---------- Arranque ----------
  function pintar() { pintarLista(); pintarPagos(); pintarPrompts(); pintarNotas(); }

  // Si guardas un prompt en otra pestaña, el panel abierto se actualiza.
  window.addEventListener('storage', function (ev) {
    if (ev.key !== CLAVE) return;
    estado = cargar();
    pintar();
  });

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
