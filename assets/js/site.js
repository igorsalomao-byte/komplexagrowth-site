(function () {
  var doc = document.documentElement;
  var hdr = document.querySelector('.hdr');
  var reduz = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

  // revelação das seções e gatilho das animações dos cases (.in)
  var alvos = document.querySelectorAll('[data-rv]');
  var temIO = 'IntersectionObserver' in window;
  if (temIO) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    alvos.forEach(function (el) { io.observe(el); });
  } else {
    doc.classList.add('no-anim');
    alvos.forEach(function (el) { el.classList.add('in'); });
  }
  window.__animReady = true;

  // números que contam: o HTML já tem o valor final; aqui ele volta ao início e sobe quando aparece
  function fmt(n, dec) {
    return n.toLocaleString('pt-BR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }
  function texto(el, v) {
    var dec = parseInt(el.dataset.dec || '0', 10);
    el.textContent = (el.dataset.pre || '') + fmt(v, dec) + (el.dataset.suf || '');
  }
  function conta(el) {
    var de = parseFloat(el.dataset.from || '0'), ate = parseFloat(el.dataset.to);
    var dur = ate >= 1000 ? 1900 : 1300, t0 = null;
    function passo(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      texto(el, de + (ate - de) * e);
      if (p < 1) requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
  }
  var nums = document.querySelectorAll('.cnt');
  if (temIO && !reduz) {
    var ion = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { conta(e.target); ion.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    nums.forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight) texto(el, parseFloat(el.dataset.from || '0'));
      ion.observe(el);
    });
  }

  // método: a linha avança com a rolagem e cada etapa acende quando a linha chega nela
  var met = document.querySelector('.metodo');
  if (met && !reduz) {
    var passos = met.querySelectorAll('.passo');
    var pedido = false;
    var tick = function () {
      pedido = false;
      var r = met.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh * 0.82 - r.top) / (vh * 0.5)));
      met.style.setProperty('--p', p.toFixed(3));
      passos.forEach(function (el, i) {
        el.classList.toggle('ok', p >= i / Math.max(1, passos.length - 1) - 0.001);
      });
    };
    window.addEventListener('scroll', function () {
      if (!pedido) { pedido = true; requestAnimationFrame(tick); }
    }, { passive: true });
    window.addEventListener('resize', tick);
    tick();
  }

  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();
})();
