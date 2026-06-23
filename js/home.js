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

// ─── Formulaire contact ───────────────────────────────────
const form = document.querySelector('.contact-form');
const inputNom = form.querySelector('input[type="text"]');
const inputEmail = form.querySelector('input[type="email"]');
const inputMessage = form.querySelector('textarea');
const btnEnvoyer = form.querySelector('.btn.primary');

function showError(input, message) {
  input.classList.add('input-error');
  const existing = input.nextElementSibling;
  if (existing && existing.classList.contains('error-msg')) return;
  const msg = document.createElement('p');
  msg.classList.add('error-msg');
  msg.textContent = message;
  input.insertAdjacentElement('afterend', msg);
}

function clearError(input) {
  input.classList.remove('input-error');
  const next = input.nextElementSibling;
  if (next && next.classList.contains('error-msg')) next.remove();
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Effacer l'erreur dès que l'utilisateur retape
[inputNom, inputEmail, inputMessage].forEach((input) => {
  input.addEventListener('input', () => clearError(input));
});

btnEnvoyer.addEventListener('click', () => {
  let valid = true;

  if (!inputNom.value.trim()) {
    showError(inputNom, 'Veuillez entrer votre nom.');
    valid = false;
  }

  if (!inputEmail.value.trim()) {
    showError(inputEmail, 'Veuillez entrer votre email.');
    valid = false;
  } else if (!isValidEmail(inputEmail.value.trim())) {
    showError(inputEmail, 'Format d\'email invalide.');
    valid = false;
  }

  if (!inputMessage.value.trim()) {
    showError(inputMessage, 'Veuillez entrer votre message.');
    valid = false;
  }

  if (!valid) return;

  // Feedback envoi
  btnEnvoyer.disabled = true;
  btnEnvoyer.textContent = 'Envoi en cours...';

  setTimeout(() => {
    btnEnvoyer.textContent = 'Envoyé ✓';
    btnEnvoyer.style.background = '#27AE60';
    btnEnvoyer.style.borderColor = '#27AE60';

    setTimeout(() => {
      inputNom.value = '';
      inputEmail.value = '';
      inputMessage.value = '';
      btnEnvoyer.disabled = false;
      btnEnvoyer.textContent = 'Envoyer';
      btnEnvoyer.style.background = '';
      btnEnvoyer.style.borderColor = '';
    }, 2000);
  }, 1000);
});