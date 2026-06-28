// ─── Compteurs ───────────────────────────────────────────
const countPrets = document.getElementById('count-prets');
const countServis = document.getElementById('count-servis');
const pretsList = document.getElementById('prets-list');
const servisList = document.getElementById('servis-list');
const emptyPrets = document.getElementById('empty-prets');
const emptyServis = document.getElementById('empty-servis');

let prets = [
  { client: 'Fatou D.', montant: '32 000', devise: 'CDF' },
  { client: 'Patrick M.', montant: '18 500', devise: 'CDF' },
];

let servis = [
  { client: 'Grace K.', montant: '27 000', devise: 'CDF' },
  { client: 'Samuel T.', montant: '45', devise: 'USD' },
];

function updateCounts() {
  const countAttente = document.getElementById('count-attente');
  const sideAttente = document.getElementById('side-count-attente');
  const sidePrets = document.getElementById('side-count-prets');
  const sideServis = document.getElementById('side-count-servis');

  const attenteCount = document.querySelectorAll('.reservation-card').length;
  if (countAttente) countAttente.textContent = attenteCount;
  if (sideAttente) sideAttente.textContent = attenteCount;
  if (sidePrets) sidePrets.textContent = prets.length;
  if (sideServis) sideServis.textContent = servis.length;

  countPrets.textContent = prets.length;
  countServis.textContent = servis.length;
}

function renderPrets() {
  pretsList.innerHTML = '';
  if (prets.length === 0) {
    pretsList.appendChild(emptyPrets);
    return;
  }
  prets.forEach((item, index) => {
    const card = document.createElement('div');
    card.classList.add('pret-card');
    card.innerHTML = `
      <div class="pret-info">
        <span class="pret-client">${item.client}</span>
        <span class="pret-montant">${item.montant} ${item.devise}</span>
      </div>
      <button class="btn-servir" data-index="${index}">Marquer comme servi</button>
    `;
    pretsList.appendChild(card);
  });

  pretsList.querySelectorAll('.btn-servir').forEach((btn) => {
    btn.addEventListener('click', () => {
      const index = parseInt(btn.dataset.index);
      servis.unshift(prets.splice(index, 1)[0]);
      renderPrets();
      renderServis();
      updateCounts();
    });
  });
}

function renderServis() {
  servisList.innerHTML = '';
  if (servis.length === 0) {
    servisList.appendChild(emptyServis);
    return;
  }
  servis.forEach((item, index) => {
    const card = document.createElement('div');
    card.classList.add('servi-card');
    card.innerHTML = `
      <div class="servi-info">
        <span class="servi-client">${item.client}</span>
        <span class="servi-montant">${item.montant} ${item.devise}</span>
      </div>
      <button class="btn-annuler-servi" data-index="${index}">Annuler</button>
    `;
    servisList.appendChild(card);
  });

  servisList.querySelectorAll('.btn-annuler-servi').forEach((btn) => {
    btn.addEventListener('click', () => {
      const index = parseInt(btn.dataset.index);
      prets.unshift(servis.splice(index, 1)[0]);
      renderPrets();
      renderServis();
      updateCounts();
    });
  });
}

// ─── Bouton Notifier ──────────────────────────────────────
document.querySelectorAll('.notify-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const card = btn.closest('.reservation-card');
    const client = card.querySelector('.client-name').textContent;
    const contact = card.querySelector('.client-contact').textContent.trim();
    const montant = card.querySelector('.amount-input').value.trim();
    const devise = card.querySelector('.amount-select').value.toUpperCase();

    if (!montant) {
      card.querySelector('.amount-input').classList.add('input-error');
      card.querySelector('.amount-input').focus();
      return;
    }

    card.querySelector('.amount-input').classList.remove('input-error');

    // Produits non cochés = indisponibles
    const items = card.querySelectorAll('.reservation-items li');
    const indispos = [];
    items.forEach((li) => {
      const checkbox = li.querySelector('input[type="checkbox"]');
      const label = li.querySelector('label').textContent.trim();
      if (!checkbox.checked) indispos.push(label);
    });

    // Construction du message WhatsApp
    const boutique = document.querySelector('.page-title').textContent.replace('Tableau de bord — ', '');

    let message = `🛍️ *EasyMarket* — _Le marché facile, pour tous !_\n`;
    message += `🏪 *${boutique}*\n`;
    message += `─────────────────────\n\n`;
    message += `Bonjour *${client}* 👋,\n\n`;
    message += `✅ Vos produits sont prêts à être récupérés !\n\n`;
    message += `💰 *Montant à régler :* ${montant} ${devise}\n`;

    if (indispos.length > 0) {
      message += `\n⚠️ *Produits non disponibles :*\n`;
      indispos.forEach((p) => { message += `  • ${p}\n`; });
    }

    message += `\n─────────────────────\n`;
    message += `🕗 La boutique ferme à *20h00*.\n`;
    message += `📍 Vous pouvez dès à présent passer récupérer votre commande.\n\n`;
    message += `Merci pour votre confiance ! 🙏\n`;
    message += `_À tout à l'heure !_`;

    // Numéro WhatsApp — retire espaces et +
    const numero = contact.replace(/[\s+]/g, '');
    const url = `https://wa.me/${numero}?text=${encodeURIComponent(message)}`;

    // Feedback bouton
    btn.disabled = true;
    btn.textContent = 'Envoyé ✓';
    btn.style.background = '#27AE60';
    btn.style.borderColor = '#27AE60';

    // Ouvrir WhatsApp
    window.open(url, '_blank');

    // Ajouter dans prêts non servis
    prets.push({ client, montant, devise });
    renderPrets();
    updateCounts();

    // Retirer la card
    setTimeout(() => {
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      card.style.opacity = '0';
      card.style.transform = 'translateY(-8px)';
      setTimeout(() => card.remove(), 400);
    }, 1000);
  });
});

// ─── Nav latérale active au scroll ───────────────────────
const sections = [
  { id: 'section-attente', link: document.querySelector('a[href="#section-attente"]') },
  { id: 'section-prets',   link: document.querySelector('a[href="#section-prets"]') },
  { id: 'section-servis',  link: document.querySelector('a[href="#section-servis"]') },
];

window.addEventListener('scroll', () => {
  let current = sections[0].id;
  sections.forEach(({ id }) => {
    const el = document.getElementById(id);
    if (el && el.getBoundingClientRect().top <= 120) current = id;
  });
  sections.forEach(({ id, link }) => {
    link.classList.toggle('active', id === current);
  });
});

// ─── Init ─────────────────────────────────────────────────
renderPrets();
renderServis();
updateCounts();