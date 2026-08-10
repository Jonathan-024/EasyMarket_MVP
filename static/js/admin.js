const sections = [
  { id: 'section-overview',   link: document.querySelector('a[href="#section-overview"]') },
  { id: 'section-vendeurs',   link: document.querySelector('a[href="#section-vendeurs"]') },
  { id: 'section-clients',    link: document.querySelector('a[href="#section-clients"]') },
  { id: 'section-historique', link: document.querySelector('a[href="#section-historique"]') },
  { id: 'section-commission', link: document.querySelector('a[href="#section-commission"]') },
];

window.addEventListener('scroll', () => {
  let current = sections[0].id;
  sections.forEach(({ id }) => {
    const el = document.getElementById(id);
    if (el && el.getBoundingClientRect().top <= window.innerHeight / 2) current = id;
  });
  sections.forEach(({ id, link }) => {
    if (link) link.classList.toggle('active', id === current);
  });
});

document.getElementById('btn-gen-code')?.addEventListener('click', () => {
  const code = 'EM-' + Math.random().toString(36).substring(2, 8).toUpperCase();
  const overlay = document.createElement('div');
  overlay.classList.add('modal-overlay', 'active');
  overlay.innerHTML = `
    <div class="modal">
      <h2 class="modal-title">Code d'accès généré</h2>
      <div class="modal-section">
        <p class="modal-label">Code à transmettre au vendeur</p>
        <div class="code-block" id="code-display">${code}</div>
      </div>
      <div class="modal-section">
        <p class="modal-label">Nom du vendeur (optionnel)</p>
        <input type="text" class="form-input" id="code-vendeur" placeholder="Ex : Boulangerie Dorée">
      </div>
      <div class="modal-actions">
        <button class="btn secondary" id="btn-code-fermer">Fermer</button>
        <button class="btn primary" id="btn-code-copier">Copier le code</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  overlay.querySelector('#btn-code-fermer').addEventListener('click', () => overlay.remove());
  overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

  overlay.querySelector('#btn-code-copier').addEventListener('click', () => {
    navigator.clipboard.writeText(code).then(() => {
      const btn = overlay.querySelector('#btn-code-copier');
      btn.textContent = 'Copié ✓';
      btn.style.background = '#27AE60';
      btn.style.borderColor = '#27AE60';
      setTimeout(() => {
        btn.textContent = 'Copier le code';
        btn.style.background = '';
        btn.style.borderColor = '';
      }, 2000);
    });
  });
});