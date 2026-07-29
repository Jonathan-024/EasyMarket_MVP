document.addEventListener('DOMContentLoaded', () => {
  const boutiqueSelect = document.getElementById('boutique-select');
  const checkboxListContainer = document.querySelector('.produits-checkbox-list') || createCheckboxContainer();

  if (boutiqueSelect) {
    boutiqueSelect.addEventListener('change', async (e) => {
      const boutiqueId = e.target.value;
      if (!boutiqueId) return;

      try {
        const response = await fetch(`/api/boutique/${boutiqueId}/produits`);
        const produits = await response.json();

        // Construire dynamiquement les cases à cocher des produits
        let html = '<p class="form-hint">Cochez les produits que vous souhaitez réserver :</p>';
        if (produits.length > 0) {
          produits.forEach(produit => {
            html += `
              <div class="produit-checkbox-item">
                <label>
                  <input type="checkbox" name="produits_ids" value="${produit.id}">
                  <strong>${produit.nom}</strong> — ${produit.prix} ${produit.devise} 
                  <span class="produit-details">(${produit.autres || ''})</span>
                </label>
              </div>
            `;
          });
        } else {
          html = '<p class="empty-state">Aucun produit disponible pour cette boutique.</p>';
        }

        checkboxListContainer.innerHTML = html;
      } catch (error) {
        console.error("Erreur lors du chargement des produits:", error);
      }
    });
  }
});

// Fonction utilitaire si le conteneur n'est pas présent initialement
function createCheckboxContainer() {
  const section = document.querySelector('#produit-input').closest('.form-section');
  const container = document.createElement('div');
  container.className = 'produits-checkbox-list';
  section.appendChild(container);
  return container;
}

// ─── Disponibilité par boutique ───────────────────────────
const indisponibles = {
  'marche-frais': ['mangues', 'avocats'],
  'boucherie-centrale': ['foie de bœuf'],
  'fromagerie': ['camembert', 'brie'],
  'epicerie-coin': [],
  'boulangerie-doree': ['croissants'],
  'poissonnerie-bleue': ['crevettes', 'homard'],
};

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

  // Supprimer le message d'erreur produit si présent
  const inputRow = document.querySelector('.produit-input-row');
  const errMsg = inputRow.nextElementSibling;
  if (errMsg && errMsg.classList.contains('error-msg')) errMsg.remove();

  produits.push(valeur);
  produitInput.value = '';
  produitInput.focus();
  renderProduits();
}

btnAjouter.addEventListener('click', ajouterProduit);

produitInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === 'Tab') {
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
    const inputRow = document.querySelector('.produit-input-row');
    produitInput.classList.add('input-error');
    const existing = inputRow.nextElementSibling;
    if (!existing || !existing.classList.contains('error-msg')) {
      const msg = document.createElement('p');
      msg.classList.add('error-msg');
      msg.textContent = 'Ajoutez au moins un produit.';
      inputRow.insertAdjacentElement('afterend', msg);
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

  // Remplir le modal
  const boutiqueValue = inputBoutique.value;
  const indispoList = indisponibles[boutiqueValue] || [];

  // Avertissement indisponibilités
  const alertBlock = document.getElementById('modal-indispo');
  const alertList = document.getElementById('modal-indispo-list');
  alertList.innerHTML = '';

  if (indispoList.length > 0) {
    indispoList.forEach((produit) => {
      const li = document.createElement('li');
      li.textContent = produit;
      alertList.appendChild(li);
    });
    alertBlock.style.display = 'flex';
  } else {
    alertBlock.style.display = 'none';
  }

  document.getElementById('modal-boutique').textContent = reservation.boutique;
  document.getElementById('modal-nom').textContent = reservation.nom;
  document.getElementById('modal-whatsapp').textContent = reservation.whatsapp;

  const modalProduits = document.getElementById('modal-produits');
  modalProduits.innerHTML = '';
  reservation.produits.forEach((p) => {
    const li = document.createElement('li');
    li.textContent = p;
    modalProduits.appendChild(li);
  });

  document.getElementById('modal-overlay').classList.add('active');
});

// ─── Modal : fermer / confirmer ───────────────────────────
document.getElementById('btn-annuler').addEventListener('click', () => {
  document.getElementById('modal-overlay').classList.remove('active');
});

document.getElementById('btn-confirmer').addEventListener('click', () => {
  const btnConfirmer = document.getElementById('btn-confirmer');
  btnConfirmer.disabled = true;
  btnConfirmer.textContent = 'Envoi en cours...';

  setTimeout(() => {
    btnConfirmer.textContent = 'Confirmé ✓';
    btnConfirmer.style.background = '#27AE60';
    btnConfirmer.style.borderColor = '#27AE60';

    setTimeout(() => {
      document.getElementById('modal-overlay').classList.remove('active');
      form.reset();
      produits = [];
      renderProduits();
      btnConfirmer.disabled = false;
      btnConfirmer.textContent = 'Confirmer';
      btnConfirmer.style.background = '';
      btnConfirmer.style.borderColor = '';
    }, 2000);
  }, 1000);
});

// Fermer au clic sur l'overlay
document.getElementById('modal-overlay').addEventListener('click', (e) => {
  if (e.target === document.getElementById('modal-overlay')) {
    document.getElementById('modal-overlay').classList.remove('active');
  }
});