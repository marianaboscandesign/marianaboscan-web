/* Movimiento de las páginas internas: titular palabra a palabra, cascadas y revelado al hacer scroll. */
(function () {
  var d = document, $ = function (s) { return Array.prototype.slice.call(d.querySelectorAll(s)); };
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
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
  $('.cab-int h1, .cta-final h2').forEach(split);
  $('.rejilla > li, .pila > *, .pager > *').forEach(function (el, i) { el.style.setProperty('--k', el.parentNode.classList.contains('rejilla') ? i % 3 : 0); });
  $('.rev').forEach(function (el) { el.classList.remove('rev'); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  // las piezas muy altas (páginas largas cortadas en tramos) nunca llegan al 12 % visible: se revelan en cuanto asoman
  var ioAlto = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); ioAlto.unobserve(e.target); } });
  }, { threshold: 0, rootMargin: '0px 0px -6% 0px' });
  $('.cab-int, .rejilla > li, .pila > *, .pager, .hoja, #contacto').forEach(function (el) {
    (el.offsetHeight > innerHeight * 3 ? ioAlto : io).observe(el);
  });
})();
