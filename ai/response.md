### FILE: templates/home.html [PATCH]
### REPLACE
      <form class="contact-form" action="https://api.web3forms.com/submit" method="POST" data-ajax="true">
        <input type="hidden" name="access_key" value="TA_CLE_ICI">
        <input type="text" name="name" class="form-input" placeholder="Votre nom" required>
        <input type="email" name="email" class="form-input" placeholder="Votre email" required>
        <textarea name="message" class="form-input" rows="4" placeholder="Votre message" required></textarea>
        <button type="submit" class="btn primary form-input">Envoyer</button>
      </form>
### WITH
      <form class="contact-form" action="https://api.web3forms.com/submit" method="POST" data-ajax="true">
        <input type="hidden" name="access_key" value="b7efc4b7-4e6c-416b-bcca-b030337d97f4">
        <input type="text" name="name" class="form-input" placeholder="Votre nom" required>
        <input type="email" name="email" class="form-input" placeholder="Votre email" required>
        <textarea name="message" class="form-input" rows="4" placeholder="Votre message" required></textarea>
        <button type="submit" class="btn primary form-input">Envoyer</button>
      </form>
### END FILE

### FILE: static/js/home.js [PATCH]
### REPLACE
const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', (event) => {
### WITH
function showFormMessage(text, type) {
  const existing = document.querySelector('.form-message');
  if (existing) existing.remove();

  const msg = document.createElement('p');
  msg.className = `form-message form-message--${type}`;
  msg.textContent = text;
  form.appendChild(msg);

  setTimeout(() => msg.remove(), 4000);
}

const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', (event) => {
### END FILE

### FILE: static/js/home.js [PATCH]
### REPLACE
      .then(() => {
        form.reset();
      })
      .catch(() => {
        console.warn('Le formulaire de contact n’a pas de traitement backend configuré.');
      });
### WITH
      .then(() => {
        form.reset();
        showFormMessage('Message envoyé, merci !', 'success');
      })
      .catch(() => {
        showFormMessage('Erreur lors de l’envoi, réessaie plus tard.', 'error');
      });
### END FILE

### FILE: static/scss/home.scss [PATCH]
### REPLACE
  .contact-form {
### WITH
  .form-message {
    margin-top: 0.5rem;
    font-size: 0.9rem;

    &--success { color: #2e7d32; }
    &--error { color: #c62828; }
  }

  .contact-form {
### END FILE