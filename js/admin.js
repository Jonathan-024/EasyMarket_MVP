// ─── Nav latérale active au scroll ───────────────────────
const sections = [
  { id: 'section-overview',   link: document.querySelector('a[href="#section-overview"]') },
  { id: 'section-vendeurs',   link: document.querySelector('a[href="#section-vendeurs"]') },
  { id: 'section-clients',    link: document.querySelector('a[href="#section-clients"]') },
  { id: 'section-historique', link: document.querySelector('a[href="#section-historique"]') },
];

window.addEventListener('scroll', () => {
  let current = sections[0].id;
  sections.forEach(({ id }) => {
    const el = document.getElementById(id);
    if (el && el.getBoundingClientRect().top <= window.innerHeight / 2) current = id;
  });
  sections.forEach(({ id, link }) => {
    link.classList.toggle('active', id === current);
  });
});

// ─── Génération code d'accès ──────────────────────────────
document.getElementById('btn-gen-code').addEventListener('click', () => {
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

// ─── Actions vendeurs ─────────────────────────────────────
document.querySelectorAll('.vendeur-card').forEach((card) => {
  const statut = card.dataset.statut;
  const badge = card.querySelector('.badge-statut');

  card.querySelector('.action-btn--delete')?.addEventListener('click', () => {
    card.style.transition = 'opacity 0.3s ease';
    card.style.opacity = '0';
    setTimeout(() => card.remove(), 300);
  });

  card.querySelector('.action-btn--suspend')?.addEventListener('click', () => {
    card.dataset.statut = 'suspendu';
    badge.className = 'badge-statut statut--suspendu';
    badge.textContent = 'Suspendu';
  });

  card.querySelector('.action-btn--confirm')?.addEventListener('click', () => {
    card.dataset.statut = 'actif';
    badge.className = 'badge-statut statut--actif';
    badge.textContent = 'Actif';
  });

  card.querySelector('.action-btn--warn')?.addEventListener('click', () => {
    const overlay = document.createElement('div');
    overlay.classList.add('modal-overlay', 'active');
    overlay.innerHTML = `
      <div class="modal">
        <h2 class="modal-title">Envoyer un avertissement</h2>
        <div class="modal-section">
          <p class="modal-label">Message</p>
          <textarea class="form-input" id="warn-message" rows="4" placeholder="Motif de l'avertissement..."></textarea>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" id="btn-warn-annuler">Annuler</button>
          <button class="btn primary" id="btn-warn-envoyer">Envoyer</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#btn-warn-annuler').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

    overlay.querySelector('#btn-warn-envoyer').addEventListener('click', () => {
      const btn = overlay.querySelector('#btn-warn-envoyer');
      btn.textContent = 'Envoyé ✓';
      btn.style.background = '#27AE60';
      btn.style.borderColor = '#27AE60';
      setTimeout(() => overlay.remove(), 1500);
    });
  });
});

// ─── Filtre clients ───────────────────────────────────────
document.querySelectorAll('.clients-filtres .filtre-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.clients-filtres .filtre-btn').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');

    const filtre = btn.textContent.trim();
    document.querySelectorAll('.admin-client-card').forEach((card) => {
      const badge = card.querySelector('.badge');
      if (filtre === 'Tous') {
        card.style.display = '';
      } else if (filtre === 'Nouveaux') {
        card.style.display = badge?.classList.contains('badge-new') ? '' : 'none';
      } else if (filtre === 'Habitués') {
        card.style.display = badge?.classList.contains('badge-old') ? '' : 'none';
      }
    });
  });
});