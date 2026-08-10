document.addEventListener('DOMContentLoaded', () => {
  const boutiqueSelect = document.getElementById('select-boutique') || document.getElementById('boutique-select');

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
});
