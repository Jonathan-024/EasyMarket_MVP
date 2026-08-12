document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('reserver-form');
  const boutiqueSelect = document.getElementById('select-boutique') || document.getElementById('boutique-select');
  const customInput = document.getElementById('produit-input');
  const addBtn = document.getElementById('btn-ajouter');
  const openConfirmBtn = document.getElementById('btn-ouvrir-confirmation');
  const confirmBtn = document.getElementById('btn-confirmer');
  const cancelBtn = document.getElementById('btn-annuler');
  const modal = document.getElementById('modal-overlay');
  const produitsList = document.getElementById('modal-produits');
  const boutiqueLabel = document.getElementById('modal-boutique');
  const nomLabel = document.getElementById('modal-nom');
  const whatsappLabel = document.getElementById('modal-whatsapp');

  if (boutiqueSelect) {
    boutiqueSelect.addEventListener('change', (event) => {
      const value = event.target.value;
      if (!value) return;
      window.location.href = `/reserver?boutique=${encodeURIComponent(value)}`;
    });
  }

  document.querySelectorAll('.btn-choisir-boutique').forEach((button) => {
    button.addEventListener('click', () => {
      const boutiqueId = button.dataset.id;
      if (!boutiqueId) return;
      window.location.href = `/boutique/${encodeURIComponent(boutiqueId)}`;
    });
  });

  if (addBtn && customInput && form) {
    addBtn.addEventListener('click', () => {
      const value = customInput.value.trim();
      if (!value) {
        alert('Renseignez le nom du produit à ajouter.');
        return;
      }

      const field = document.createElement('input');
      field.type = 'hidden';
      field.name = 'produits_custom';
      field.value = value;
      form.appendChild(field);

      const item = document.createElement('div');
      item.className = 'produit-checkbox-item';
      item.innerHTML = `
        <label>
          <input type="checkbox" checked name="produits_ids" value="custom:${Date.now()}" data-nom="${value}" data-prix="0 CDF" data-disponible="true">
          <strong>${value}</strong>
        </label>
      `;
      const list = form.querySelector('.produits-checkbox-list');
      if (list) {
        list.appendChild(item);
      }

      customInput.value = '';
    });
  }

  if (openConfirmBtn && form && modal) {
    openConfirmBtn.addEventListener('click', () => {
      const nom = document.getElementById('client-nom')?.value.trim() || '';
      const whatsapp = document.getElementById('client-whatsapp')?.value.trim() || '';
      const selected = form.querySelectorAll('input[name="produits_ids"]:checked');

      if (!nom || !whatsapp) {
        alert('Veuillez remplir votre nom et votre numéro WhatsApp.');
        return;
      }

      if (selected.length === 0) {
        alert('Veuillez sélectionner au moins un produit.');
        return;
      }

      produitsList.innerHTML = '';
      selected.forEach((checkbox) => {
        const li = document.createElement('li');
        li.textContent = `${checkbox.dataset.nom || 'Produit'} — ${checkbox.dataset.prix || '0 CDF'}`;
        produitsList.appendChild(li);
      });

      if (boutiqueLabel) {
        const selectedBoutique = boutiqueSelect?.options[boutiqueSelect.selectedIndex];
        boutiqueLabel.textContent = selectedBoutique ? selectedBoutique.textContent.replace(' — ', ' · ') : 'Boutique sélectionnée';
      }
      if (nomLabel) nomLabel.textContent = nom;
      if (whatsappLabel) whatsappLabel.textContent = whatsapp;

      modal.style.display = 'flex';
    });
  }

  if (confirmBtn && form) {
    confirmBtn.addEventListener('click', () => {
      form.submit();
    });
  }

  if (cancelBtn && modal) {
    cancelBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }
});