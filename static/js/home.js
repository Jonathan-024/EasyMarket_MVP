function showFormMessage(text, type) {
  const existing = document.querySelector('.form-message');
  if (existing) existing.remove();

  const msg = document.createElement('p');
  msg.className = `form-message form-message--${type}`;
  msg.textContent = text;
  form.appendChild(msg);

  setTimeout(() => msg.remove(), 4000);
}

function showFormMessage(text, type) {
  const existing = document.querySelector('.form-message');
  if (existing) existing.remove();

  const msg = document.createElement('p');
  msg.className = `form-message form-message--${type}`;
  msg.textContent = text;
  form.appendChild(msg);

  setTimeout(() => msg.remove(), 4000);
}

function showFormMessage(text, type) {
  const existing = document.querySelector('.form-message');
  if (existing) existing.remove();

  const msg = document.createElement('p');
  msg.className = `form-message form-message--${type}`;
  msg.textContent = text;
  form.appendChild(msg);

  setTimeout(() => msg.remove(), 4000);
}

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
    const isAjax = form.dataset.ajax === 'true';

    if (!isAjax) {
      return;
    }

    event.preventDefault();

    fetch(form.action || window.location.href, {
      method: form.method || 'POST',
      body: new FormData(form),
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Erreur lors de l’envoi du formulaire.');
        }
        return response.text();
      })
      .then(() => {
        form.reset();
        showFormMessage('Message envoyé, merci !', 'success');
      })
      .catch(() => {
        showFormMessage('Erreur lors de l’envoi, réessaie plus tard.', 'error');
      });
  });
}