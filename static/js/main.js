const menuToggle = document.getElementById('menu-toggle');
const burgerMenu = document.querySelector('.burger-menu');

document.addEventListener('click', (e) => {
  if (burgerMenu && !burgerMenu.contains(e.target) && menuToggle) {
    menuToggle.checked = false;
  }
});