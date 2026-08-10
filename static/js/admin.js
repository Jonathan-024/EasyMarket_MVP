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

document.querySelectorAll('.vendeur-card').forEach((card) => {
  card.addEventListener('click', () => {
    document.querySelectorAll('.vendeur-card').forEach((item) => item.classList.remove('selected'));
    card.classList.add('selected');
  });
});

document.getElementById('btn-gen-code')?.addEventListener('click', async () => {
  const selectedCard = document.querySelector('.vendeur-card.selected');
  const vendeurId = selectedCard ? selectedCard.dataset.id : null;
  const btn = document.getElementById('btn-gen-code');

  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Génération...';
  }

  try {
    const formData = new URLSearchParams();
    if (vendeurId) {
      formData.append('vendeur_id', vendeurId);
    }

    const response = await fetch('/admin/generer-code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData.toString()
    });

    const data = await response.json();
    if (!response.ok || !data.code) {
      throw new Error(data.error || 'Impossible de générer le code.');
    }

    const overlay = document.createElement('div');
    overlay.classList.add('modal-overlay', 'active');
    overlay.innerHTML = `
      <div class="modal">
        <h2 class="modal-title">Code d'accès généré</h2>
        <div class="modal-section">
          <p class="modal-label">Code à transmettre au vendeur</p>
          <div class="code-block" id="code-display">${data.code}</div>
        </div>
        <div class="modal-section">
          <p class="modal-label">Vendeur</p>
          <div class="code-block" id="code-vendeur-display">${data.vendeur_nom || 'Génération libre'}</div>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" id="btn-code-fermer" type="button">Fermer</button>
          <button class="btn primary" id="btn-code-copier" type="button">Copier le code</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#btn-code-fermer').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

    overlay.querySelector('#btn-code-copier').addEventListener('click', async () => {
      const btnCopy = overlay.querySelector('#btn-code-copier');
      try {
        await navigator.clipboard.writeText(data.code);
        btnCopy.textContent = 'Copié ✓';
        btnCopy.style.background = '#27AE60';
        btnCopy.style.borderColor = '#27AE60';
        setTimeout(() => {
          btnCopy.textContent = 'Copier le code';
          btnCopy.style.background = '';
          btnCopy.style.borderColor = '';
        }, 2000);
      } catch (error) {
        btnCopy.textContent = 'Code prêt';
        alert(data.code);
      }
    });
  } catch (error) {
    alert(error.message || 'Erreur lors de la génération du code.');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Générer un code d\'accès';
    }
  }
});