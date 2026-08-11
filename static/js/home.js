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
      })
      .catch(() => {
        console.warn('Le formulaire de contact n’a pas de traitement backend configuré.');
      });
  });
}