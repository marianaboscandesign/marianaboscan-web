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
    document.body.appendChild(ul);
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
