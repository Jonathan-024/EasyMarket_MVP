// ─── Produits ────────────────────────────────────────────
const produitInput = document.getElementById('produit-input');
const btnAjouter = document.getElementById('btn-ajouter');
const produitsList = document.getElementById('produits-list');

let produits = [];

function renderProduits() {
  produitsList.innerHTML = '';
  produits.forEach((produit, index) => {
    const li = document.createElement('li');
    li.classList.add('produit-item');
    li.innerHTML = `
      <span>${produit}</span>
      <button class="produit-remove" data-index="${index}" aria-label="Supprimer">✕</button>
    `;
    produitsList.appendChild(li);
  });

  produitsList.querySelectorAll('.produit-remove').forEach((btn) => {
    btn.addEventListener('click', () => {
      produits.splice(parseInt(btn.dataset.index), 1);
      renderProduits();
    });
  });
}

function ajouterProduit() {
  const valeur = produitInput.value.trim();
  if (!valeur) {
    produitInput.classList.add('input-error');
    produitInput.focus();
    return;
  }
  produitInput.classList.remove('input-error');
  produits.push(valeur);
  produitInput.value = '';
  produitInput.focus();
  renderProduits();
}

btnAjouter.addEventListener('click', ajouterProduit);

produitInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    ajouterProduit();
  }
});

produitInput.addEventListener('input', () => {
  produitInput.classList.remove('input-error');
});

// ─── Validation formulaire ────────────────────────────────
const form = document.getElementById('reserver-form');
const inputNom = document.getElementById('client-nom');
const inputWhatsapp = document.getElementById('client-whatsapp');
const inputBoutique = document.getElementById('boutique-select');

function showError(input, message) {
  input.classList.add('input-error');
  const existing = input.nextElementSibling;
  if (existing && existing.classList.contains('error-msg')) return;
  const msg = document.createElement('p');
  msg.classList.add('error-msg');
  msg.textContent = message;
  input.insertAdjacentElement('afterend', msg);
}

function clearError(input) {
  input.classList.remove('input-error');
  const next = input.nextElementSibling;
  if (next && next.classList.contains('error-msg')) next.remove();
}

[inputNom, inputWhatsapp, inputBoutique].forEach((input) => {
  input.addEventListener('input', () => clearError(input));
  input.addEventListener('change', () => clearError(input));
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  let valid = true;

  if (!inputNom.value.trim()) {
    showError(inputNom, 'Veuillez entrer votre nom.');
    valid = false;
  }

  if (!inputWhatsapp.value.trim()) {
    showError(inputWhatsapp, 'Veuillez entrer votre numéro WhatsApp.');
    valid = false;
  }

  if (produits.length === 0) {
    produitInput.classList.add('input-error');
    const existing = produitInput.nextElementSibling;
    if (!existing || !existing.classList.contains('error-msg')) {
      const msg = document.createElement('p');
      msg.classList.add('error-msg');
      msg.textContent = 'Ajoutez au moins un produit.';
      produitInput.insertAdjacentElement('afterend', msg);
    }
    valid = false;
  }

  if (!inputBoutique.value) {
    showError(inputBoutique, 'Veuillez choisir une boutique.');
    valid = false;
  }

  if (!valid) return;

  // Prêt pour le modal de confirmation — données disponibles :
  const reservation = {
    nom: inputNom.value.trim(),
    whatsapp: inputWhatsapp.value.trim(),
    produits: [...produits],
    boutique: inputBoutique.options[inputBoutique.selectedIndex].text,
  };

  console.log('Réservation prête :', reservation);
  // → ouverture du modal ici à la prochaine étape
});