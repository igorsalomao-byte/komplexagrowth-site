(function () {
  var doc = document.documentElement;
  var hdr = document.querySelector('.hdr');

  function onScroll() {
    if (hdr) hdr.classList.toggle('solid', window.scrollY > 24 || doc.classList.contains('menu-open'));
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = doc.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      onScroll();
    });
    document.querySelectorAll('.mnav a').forEach(function (a) {
      a.addEventListener('click', function () {
        doc.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
        onScroll();
      });
    });
  }

  var alvos = document.querySelectorAll('[data-rv]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    alvos.forEach(function (el) { io.observe(el); });
  } else {
    doc.classList.add('no-anim');
  }
  window.__animReady = true;

  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();
})();
