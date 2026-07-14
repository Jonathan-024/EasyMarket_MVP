// ─── Toggle tabs ──────────────────────────────────────────
const tabs = document.querySelectorAll('.auth-tab');
const forms = document.querySelectorAll('.auth-form');
const switchLinks = document.querySelectorAll('.auth-switch-link');

function switchTab(target) {
  tabs.forEach((tab) => tab.classList.toggle('active', tab.dataset.tab === target));
  forms.forEach((form) => form.classList.toggle('active', form.id === `form-${target}`));
}

tabs.forEach((tab) => {
  tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});

switchLinks.forEach((link) => {
  link.addEventListener('click', () => switchTab(link.dataset.tab));
});

// ─── Validation login ─────────────────────────────────────
const formLogin = document.getElementById('form-login');

formLogin.addEventListener('submit', (e) => {
  e.preventDefault();
  const whatsapp = document.getElementById('login-whatsapp');
  const code = document.getElementById('login-code');

  let valid = true;
  if (!whatsapp.value.trim()) { showError(whatsapp, 'Numéro requis.'); valid = false; }
  if (!code.value.trim()) { showError(code, 'Code requis.'); valid = false; }
  if (!valid) return;

  const btn = formLogin.querySelector('.auth-submit');
  btn.textContent = 'Connexion...';
  setTimeout(() => {
    window.location.href = 'dashboard.html';
  }, 800);
});

// ─── Validation register ──────────────────────────────────
const formRegister = document.getElementById('form-register');

formRegister.addEventListener('submit', (e) => {
  e.preventDefault();
  const fields = [
    document.getElementById('register-boutique'),
    document.getElementById('register-nom'),
    document.getElementById('register-whatsapp'),
    document.getElementById('register-code'),
  ];

  let valid = true;
  fields.forEach((f) => {
    if (!f.value.trim()) { showError(f, 'Champ requis.'); valid = false; }
  });
  if (!valid) return;

  const btn = formRegister.querySelector('.auth-submit');
  btn.textContent = 'Création...';
  setTimeout(() => {
    window.location.href = 'boutique.html';
  }, 800);
});

// ─── Utilitaires erreurs ──────────────────────────────────
function showError(input, message) {
  input.classList.add('input-error');
  const existing = input.nextElementSibling;
  if (existing && existing.classList.contains('error-msg')) return;
  const msg = document.createElement('p');
  msg.classList.add('error-msg');
  msg.textContent = message;
  input.insertAdjacentElement('afterend', msg);
}

document.querySelectorAll('.form-input').forEach((input) => {
  input.addEventListener('input', () => {
    input.classList.remove('input-error');
    const next = input.nextElementSibling;
    if (next && next.classList.contains('error-msg')) next.remove();
  });
});