// ─── Burger menu ─────────────────────────────────────────
const menuToggle = document.getElementById('menu-toggle');
const burgerMenu = document.querySelector('.burger-menu');

// Fermer au clic extérieur
document.addEventListener('click', (e) => {
  if (!burgerMenu.contains(e.target)) {
    menuToggle.checked = false;
  }
});

// Fermer au clic sur un lien
document.querySelectorAll('.menu-link').forEach((link) => {
  link.addEventListener('click', () => {
    menuToggle.checked = false;
  });
});