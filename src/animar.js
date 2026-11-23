/* Efectos de scroll de la home: revelado, palabras que se encienden, galería horizontal, zoom y puntos de navegación. */
(function () {
  var reducir = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  // 1) revelado al entrar en pantalla
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.15 });
    $$('.rev').forEach(function (el) { io.observe(el); });
  } else { $$('.rev').forEach(function (el) { el.classList.add('in'); }); }

  // 2) puntos de navegación
  var secs = $$('[data-nombre]');
  if (secs.length > 1) {
    var ul = document.createElement('ul'); ul.className = 'puntos'; ul.setAttribute('aria-label', 'Secciones');
    secs.forEach(function (s) {
      var li = document.createElement('li'), a = document.createElement('a'), sp = document.createElement('span');
      a.href = '#' + s.id; a.setAttribute('aria-label', s.getAttribute('data-nombre')); sp.textContent = s.getAttribute('data-nombre');
      a.appendChild(sp); li.appendChild(a); ul.appendChild(li); s._dot = a;
    });
    if ('IntersectionObserver' in window) {
      var io2 = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) {
          secs.forEach(function (s) { s._dot.classList.toggle('on', s === e.target); });
          var k = e.target.getAttribute('data-nav') || e.target.id;
          $$('.nav a').forEach(function (a) { if (a.getAttribute('href') === '#' + (k === 'portafolio' ? 'proyectos' : k)) a.setAttribute('aria-current', 'true'); else if (a.getAttribute('href').charAt(0) === '#') a.removeAttribute('aria-current'); });
        } });
      }, { rootMargin: '-45% 0px -45% 0px' });
      secs.forEach(function (s) { io2.observe(s); });
    }
  }
  if (reducir) return;

  // 3) efectos ligados al scroll
  var par = $$('[data-par]'), zoom = $$('[data-zoom]'), pal = $$('.pal');
  var hero = document.querySelector('.hero2'), cartas = $$('.carta'), retr = document.querySelector('.retrato2');
  var exp = document.querySelector('.exp'), filas = $$('.fila-e');
  var enun = document.querySelector('.enunciado'), gal = document.querySelector('.galeria'), pista = gal && gal.querySelector('.pista');
  var movil = matchMedia('(max-width: 699px)');
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var pend = false;

  function progreso(el) { // 0 al empezar a fijarse, 1 al terminar
    var r = el.getBoundingClientRect(), total = el.offsetHeight - innerHeight + 72;
    return total > 0 ? clamp((72 - r.top) / total, 0, 1) : 0;
  }
  function tick() {
    pend = false;
    var y = scrollY, h = innerHeight;
    par.forEach(function (el) { if (y < h * 1.3) el.style.setProperty('--py', (y * parseFloat(el.getAttribute('data-par'))) + 'px'); });
    zoom.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      var p = clamp(1 - (r.bottom - 0) / (h + r.height), 0, 1);
      el.style.setProperty('--z', (1 + p * 0.10).toFixed(3));
    });
    if (enun && pal.length) {
      var p = progreso(enun), n = pal.length, lit = p * (n + 4);
      pal.forEach(function (w, i) { w.style.setProperty('--o', (0.16 + 0.84 * clamp(lit - i, 0, 1)).toFixed(2)); });
    }
    if (hero && cartas.length && matchMedia('(min-width: 900px)').matches) {
      var ph = progreso(hero), nc = cartas.length;
      cartas.forEach(function (c, i) { c.style.setProperty('--a', clamp((ph - (0.05 + i * 0.13)) / 0.14, 0, 1).toFixed(3)); });
      if (retr) retr.style.setProperty('--z', (1 + ph * 0.05).toFixed(3));
    }
    if (exp && filas.length && matchMedia('(min-width: 860px)').matches) {
      var pe = progreso(exp), ne = filas.length, le = pe * (ne + 0.6);
      filas.forEach(function (f, i) { f.style.setProperty('--o', (0.18 + 0.82 * clamp(le - i + 0.3, 0, 1)).toFixed(2)); });
    }
    if (gal && pista && !movil.matches) {
      var q = progreso(gal), rec = Math.max(0, pista.scrollWidth - innerWidth);
      pista.style.setProperty('--tx', (-q * rec).toFixed(1) + 'px');
    }
  }
  function pedir() { if (!pend) { pend = true; requestAnimationFrame(tick); } }
  addEventListener('scroll', pedir, { passive: true });
  addEventListener('resize', pedir);
  tick();
})();

// nav transparente sobre el hero + portafolio en arco
(function () {
  var barra = document.querySelector('.barra.foto'), hc = document.querySelector('.hc');
  var arco = document.querySelector('.arco');
  var reducido = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cards = arco ? Array.prototype.slice.call(arco.querySelectorAll('.tarj')) : [];
  var act = arco && arco.querySelector('.arco-act'), activo = -1, pend = false;
  var paso = arco ? parseFloat(arco.getAttribute('data-paso')) : 13, k0 = arco ? parseFloat(arco.getAttribute('data-k0')) : 3;
  function pinta(k) {
    var i = Math.round(k); if (i === activo) return; activo = i;
    cards.forEach(function (c, n) { c.classList.toggle('on', n === i); });
    var a = cards[i] && cards[i].querySelector('a'); if (!a || !act) return;
    act.href = a.href; act.target = a.target || ''; act.querySelector('.n').textContent = ('0' + (i + 1)).slice(-2);
    act.querySelector('.m').textContent = a.getAttribute('data-nom'); act.querySelector('.d').textContent = a.getAttribute('data-desc');
    act.classList.remove('cambia'); void act.offsetWidth; act.classList.add('cambia');
  }
  function tick() {
    pend = false;
    if (barra && hc) barra.classList.toggle('solido', hc.getBoundingClientRect().bottom < 110);
    if (arco && matchMedia('(min-width: 900px)').matches && !reducido) {
      var r = arco.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, -r.top / Math.max(1, r.height - innerHeight)));
      var k = k0 + p * (cards.length - 1 - 1 - k0);
      arco.style.setProperty('--rot', (-k * paso).toFixed(2) + 'deg'); pinta(k);
    }
  }
  function pedir() { if (!pend) { pend = true; requestAnimationFrame(tick); } }
  addEventListener('scroll', pedir, { passive: true }); addEventListener('resize', pedir);
  if (arco) {
    if (reducido || !('IntersectionObserver' in window)) arco.classList.add('in');
    else new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting) { arco.classList.add('in'); o.disconnect(); } }); }, { threshold: .2 }).observe(arco);
    arco.style.setProperty('--rot', (-k0 * paso) + 'deg'); pinta(k0);
  }
  tick();
})();

// motion por sección: titulares palabra a palabra, cascadas, telón en la foto, contadores y paralaje
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var d = document, $ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  d.documentElement.classList.add('mo');
  function split(el) {
    var i = 0;
    (function walk(n) {
      Array.prototype.slice.call(n.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var f = d.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (t) {
            if (!t) return;
            if (/^\s+$/.test(t)) f.appendChild(d.createTextNode(t));
            else { var w = d.createElement('span'), s = d.createElement('span'); w.className = 'sw'; s.textContent = t; s.style.setProperty('--wi', i++); w.appendChild(s); f.appendChild(w); }
          });
          c.parentNode.replaceChild(f, c);
        } else if (c.nodeType === 1) walk(c);
      });
    })(el);
  }
  $('#sobre h2, #experiencia h2, #formacion h2, .cta-final h2, .arco-centro h2').forEach(split);
  // índices para las cascadas
  [['.stats li'], ['.sobre>p,.sobre>h2'], ['.apps li']].forEach(function (g) {
    $(g[0]).forEach(function (el, i) { el.style.setProperty('--k', i); el.classList.remove('rev'); });
  });
  $('.sobre-foto, .sobre').forEach(function (el) { el.classList.remove('rev'); });
  // visibilidad por sección
  var secs = $('.stats, #sobre, #experiencia, #formacion, #contacto');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); if (e.target.classList.contains('stats')) cuenta(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.18 });
    secs.forEach(function (s) { io.observe(s); });
  } else secs.forEach(function (s) { s.classList.add('vis'); });
  // contadores
  function cuenta(sec) {
    $('b', sec).forEach(function (b) {
      var m = /^(\d+)(\+?)$/.exec(b.textContent.trim()); if (!m) return;
      var fin = +m[1], suf = m[2], t0 = null;
      (function paso(t) { if (t0 === null) t0 = t; var p = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - p, 3); b.textContent = Math.round(fin * e) + suf; if (p < 1) requestAnimationFrame(paso); })(performance.now());
    });
  }
  // paralaje suave en la foto de About
  var foto = $('.sobre-foto img')[0], pend = false;
  function par() { pend = false; var r = foto.parentNode.getBoundingClientRect(), p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight; foto.style.setProperty('--py', (Math.max(-1, Math.min(1, p)) * -28).toFixed(1) + 'px'); }
  if (foto) { addEventListener('scroll', function () { if (!pend) { pend = true; requestAnimationFrame(par); } }, { passive: true }); par(); }
})();

// timeline de experiencia: horizontal en escritorio (avanza con el scroll), vertical en móvil
(function () {
  var sec = document.querySelector('.exph'), tl = document.querySelector('.tl'); if (!sec || !tl) return;
  var its = Array.prototype.slice.call(tl.querySelectorAll('.tl-it')), pend = false, root = document.documentElement;
  var reducir = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mq = matchMedia('(min-width: 900px)');
  function horizontal() { return mq.matches && !reducir; }
  function layout() {
    var h = horizontal();
    root.classList.toggle('tlh', h);
    var pin = sec.querySelector('.tl-pin');
    if (h) {
      sec.style.height = ''; pin.style.top = '0px';
      var max = Math.max(0, tl.scrollWidth - innerWidth), ph = pin.offsetHeight;
      pin.style.top = Math.max(72, Math.round((innerHeight - ph) / 2)) + 'px';
      sec.style.height = Math.round(ph + max * 0.9) + 'px';
    } else { sec.style.height = ''; if (pin) pin.style.top = ''; tl.style.transform = ''; tl.style.removeProperty('--fw'); }
    tick();
  }
  function tick() {
    pend = false;
    if (horizontal()) {
      var r = sec.getBoundingClientRect(), pt = parseFloat(sec.querySelector('.tl-pin').style.top) || 0, total = sec.offsetHeight - sec.querySelector('.tl-pin').offsetHeight, p = total > 0 ? Math.max(0, Math.min(1, (pt - r.top) / total)) : 0;
      var max = Math.max(0, tl.scrollWidth - innerWidth), x = p * max, fw = x + innerWidth * (0.3 + 0.55 * p);
      tl.style.transform = 'translate3d(' + (-x).toFixed(1) + 'px,0,0)'; tl.style.setProperty('--fw', fw.toFixed(1) + 'px');
      its.forEach(function (li) { li.classList.toggle('on', li.offsetLeft + 10 < fw); });
    } else {
      var q = tl.getBoundingClientRect(), y = innerHeight * 0.62, pp = Math.max(0, Math.min(1, (y - q.top) / q.height));
      tl.style.setProperty('--p', pp.toFixed(4));
      its.forEach(function (li) { var d = li.querySelector('.tl-dot').getBoundingClientRect(); li.classList.toggle('on', d.top + 10 < y); });
    }
  }
  function pedir() { if (!pend) { pend = true; requestAnimationFrame(tick); } }
  addEventListener('scroll', pedir, { passive: true }); addEventListener('resize', layout); addEventListener('load', layout); layout();
})();
