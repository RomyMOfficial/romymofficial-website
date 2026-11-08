(function () {
  // Mobile navigation
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('nav-open', open);
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        links.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('nav-open');
      }
    });
  }

  // Waitlist form (Kit form 9611831)
  var form = document.getElementById('wl-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      fetch(form.action, { method: 'POST', body: data, mode: 'no-cors' }).catch(function () {});
      var box = document.getElementById('waitlist');
      box.innerHTML = '<div class="wl-label">You’re on the list</div>' +
        '<p class="wl-note"><span class="nw">You’ll hear from</span> me when enrolment opens for the 1 December <span class="nw">2026 intake.</span></p>';
    });
  }

  // FAQ accordion
  var faqs = document.querySelectorAll('.faq-btn');
  faqs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      faqs.forEach(function (b) {
        b.setAttribute('aria-expanded', 'false');
        b.querySelector('.faq-sign').textContent = '+';
        document.getElementById(b.getAttribute('aria-controls')).classList.remove('open');
      });
      if (!open) {
        btn.setAttribute('aria-expanded', 'true');
        btn.querySelector('.faq-sign').textContent = '−';
        document.getElementById(btn.getAttribute('aria-controls')).classList.add('open');
      }
    });
  });

  // Testimonial carousel (Feedspace widget, same as the live site)
  var slot = document.querySelector('.feedspace-embed');
  if (slot) {
    var loadFs = function () {
      var t = document.createElement('script');
      t.src = 'https://js.feedspace.io/v1/embed/embed.min.js';
      t.async = true;
      document.head.appendChild(t);
    };
    if ('IntersectionObserver' in window) {
      var fio = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { fio.disconnect(); loadFs(); }
      }, { rootMargin: '400px' });
      fio.observe(slot);
    } else { loadFs(); }
  }

  // Before / After tabs on the homepage case studies
  document.querySelectorAll('.ba-tabs').forEach(function (tabs) {
    var card = tabs.parentElement;
    tabs.querySelectorAll('[role="tab"]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var which = btn.getAttribute('data-panel');
        tabs.querySelectorAll('[role="tab"]').forEach(function (b) { b.setAttribute('aria-selected', b === btn ? 'true' : 'false'); });
        card.querySelectorAll('.ba-panel').forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== which; });
      });
    });
  });

  // Scroll reveal
  var els = document.querySelectorAll('section h2, section h3, section p, section figure, .offer, .stat, .pw-card, .pw-case, .ex, .ba, .cs-item-head, .res-grid > div, .photo-strip, .taste, .testi, .faq, .first-win');
  var list = [];
  els.forEach(function (el) {
    if (el.closest('.hero') || el.closest('.cs-hero') || el.closest('.reveal')) return;
    el.classList.add('reveal');
    list.push(el);
  });
  if (!('IntersectionObserver' in window)) {
    list.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  list.forEach(function (el) { io.observe(el); });
})();
