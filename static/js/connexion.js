const tabs = document.querySelectorAll('.auth-tab');
const forms = document.querySelectorAll('.auth-form');

function switchTab(target) {
  tabs.forEach((tab) => tab.classList.toggle('active', tab.dataset.tab === target));
  forms.forEach((form) => form.classList.toggle('active', form.id === `form-${target}`));
}

const params = new URLSearchParams(window.location.search);
const initialTab = params.get('tab') === 'register' ? 'register' : 'login';
switchTab(initialTab);

tabs.forEach((tab) => {
  tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});