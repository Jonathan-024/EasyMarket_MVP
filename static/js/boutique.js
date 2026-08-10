document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('reserver-form') || document.getElementById('form-reservation');
  const btnOuvrir = document.getElementById('btn-ouvrir-confirmation');
  const btnAnnuler = document.getElementById('btn-annuler-modal');
  const btnValiderFinal = document.getElementById('btn-valider-final');
  const modal = document.getElementById('modal-confirmation');
  const recapContainer = document.getElementById('recap-produits-container');

  if (!btnOuvrir || !form || !modal || !recapContainer) return;

  btnOuvrir.addEventListener('click', () => {
    const nomEl = document.getElementById('client-nom') || document.getElementById('nom_client');
    const whatsappEl = document.getElementById('client-whatsapp') || document.getElementById('whatsapp_client');
    const nom = nomEl ? nomEl.value.trim() : '';
    const whatsapp = whatsappEl ? whatsappEl.value.trim() : '';
    const checkboxes = form.querySelectorAll('input[name="produits_ids"]:checked');

    if (!nom || !whatsapp) {
      alert('Veuillez remplir votre nom et votre numéro WhatsApp.');
      return;
    }

    if (checkboxes.length === 0) {
      alert('Veuillez sélectionner au moins un produit.');
      return;
    }

    recapContainer.innerHTML = '';
    
    checkboxes.forEach((cb) => {
      const nomProduit = cb.dataset.nom || 'Produit';
      const prixProduit = cb.dataset.prix || '';
      const disponible = cb.dataset.disponible === 'true';

      const itemDiv = document.createElement('div');
      itemDiv.style.display = 'flex';
      itemDiv.style.justifyContent = 'space-between';
      itemDiv.style.alignItems = 'center';
      itemDiv.style.padding = '8px 0';
      itemDiv.style.borderBottom = '1px solid #eee';

      itemDiv.innerHTML = `
        <div>
          <strong>${nomProduit}</strong> (${prixProduit})
          ${!disponible ? '<br><small style="color: #e32d2d;">⚠️ Produit actuellement indisponible</small>' : ''}
        </div>
        <button type="button" class="btn-retirer" data-id="${cb.value}" style="background: #FFF5F5; border: 1px solid #FCCACA; color: #e32d2d; padding: 4px 8px; border-radius: 4px; cursor: pointer;">
          Retirer
        </button>
      `;

      recapContainer.appendChild(itemDiv);
    });

    recapContainer.querySelectorAll('.btn-retirer').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const prodId = e.currentTarget.dataset.id;
        const cbOriginal = form.querySelector(`input[name="produits_ids"][value="${prodId}"]`);
        if (cbOriginal) {
          cbOriginal.checked = false;
        }
        e.currentTarget.parentElement.remove();

        if (recapContainer.children.length === 0) {
          recapContainer.innerHTML = '<p style="color: #777;">Aucun produit sélectionné.</p>';
        }
      });
    });

    modal.style.display = 'block';
  });

  if (btnAnnuler) {
    btnAnnuler.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }

  if (btnValiderFinal) {
    btnValiderFinal.addEventListener('click', () => {
      const checkboxesRestantes = form.querySelectorAll('input[name="produits_ids"]:checked');
      if (checkboxesRestantes.length === 0) {
        alert('Votre liste est vide. Sélectionnez au moins un produit.');
        modal.style.display = 'none';
        return;
      }
      form.submit();
    });
  }
});