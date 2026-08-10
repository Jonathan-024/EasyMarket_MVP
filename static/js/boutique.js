document.addEventListener('DOMContentLoaded', () => {
  const addProduitBtn = document.getElementById('btn-add-produit');
  const addCategorieBtn = document.getElementById('btn-add-categorie');
  const formProduit = document.getElementById('form-add-produit');
  const formCategorie = document.getElementById('form-add-categorie');

  if (addProduitBtn && formProduit) {
    addProduitBtn.addEventListener('click', () => {
      formProduit.style.display = formProduit.style.display === 'none' ? 'flex' : 'none';
      if (formCategorie) formCategorie.style.display = 'none';
    });
  }

  if (addCategorieBtn && formCategorie) {
    addCategorieBtn.addEventListener('click', () => {
      formCategorie.style.display = formCategorie.style.display === 'none' ? 'flex' : 'none';
      if (formProduit) formProduit.style.display = 'none';
    });
  }
});