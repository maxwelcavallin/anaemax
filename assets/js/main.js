// ============================================================
// Ana Flávia & Maxwel · Save the Date
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

  /* ---- Nav: solid background on scroll ---- */
  var nav = document.getElementById("siteNav");
  function updateNav() {
    if (window.scrollY > 40) {
      nav.classList.add("scrolled");
    } else {
      nav.classList.remove("scrolled");
    }
  }
  updateNav();
  window.addEventListener("scroll", updateNav, { passive: true });

  /* ---- Mobile menu toggle ---- */
  var toggle = document.getElementById("navToggle");
  var links = document.getElementById("navLinks");

  function closeMenu() {
    links.classList.remove("open");
    toggle.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }

  toggle.addEventListener("click", function () {
    var isOpen = links.classList.toggle("open");
    toggle.classList.toggle("open", isOpen);
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  links.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", closeMenu);
  });

  // Tocar fora fecha. O clique no proprio botao e ignorado aqui, senao ele
  // abriria e fecharia no mesmo toque, quando o evento sobe ate o documento.
  document.addEventListener("click", function (event) {
    if (!links.classList.contains("open")) return;
    if (links.contains(event.target) || toggle.contains(event.target)) return;
    closeMenu();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" || event.key === "Esc") closeMenu();
  });

  /* ---- Countdown ---- */
  // Data do casamento: 22 de agosto de 2027, horário de Brasília (UTC-3)
  var weddingDate = new Date("2027-08-22T16:00:00-03:00").getTime();

  var elDias = document.getElementById("cd-dias");
  var elHoras = document.getElementById("cd-horas");
  var elMin = document.getElementById("cd-min");
  var elSeg = document.getElementById("cd-seg");

  function pad(n, len) {
    len = len || 2;
    n = String(Math.max(0, n));
    while (n.length < len) n = "0" + n;
    return n;
  }

  function tick() {
    var now = new Date().getTime();
    var diff = weddingDate - now;

    if (diff <= 0) {
      elDias.textContent = "000";
      elHoras.textContent = "00";
      elMin.textContent = "00";
      elSeg.textContent = "00";
      return;
    }

    var dias = Math.floor(diff / (1000 * 60 * 60 * 24));
    var horas = Math.floor((diff / (1000 * 60 * 60)) % 24);
    var min = Math.floor((diff / (1000 * 60)) % 60);
    var seg = Math.floor((diff / 1000) % 60);

    elDias.textContent = pad(dias, 3);
    elHoras.textContent = pad(horas);
    elMin.textContent = pad(min);
    elSeg.textContent = pad(seg);
  }

  tick();
  setInterval(tick, 1000);

});
