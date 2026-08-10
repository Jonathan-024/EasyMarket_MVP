document.addEventListener('DOMContentLoaded', () => {
  const notifyButtons = document.querySelectorAll('.notify-btn');

  notifyButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const card = button.closest('.reservation-card');
      const clientName = card?.querySelector('.client-name')?.textContent?.trim() || 'client';

      button.disabled = true;
      button.textContent = 'Notifié ✓';
      button.classList.add('is-sent');

      alert(`Notification envoyée à ${clientName}.`);
    });
  });

  const navLinks = document.querySelectorAll('.side-nav-link');
  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.forEach((item) => item.classList.remove('active'));
      link.classList.add('active');
    });
  });
});
