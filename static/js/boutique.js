let produits = [];
let categories = [];
let produitIdCounter = 1;
let filtreActif = '';

const produitsList = document.getElementById('produits-list');
const categoriesList = document.getElementById('categories-list');

function generateId() {
  return `PRD-${String(produitIdCounter++).padStart(4, '0')}`;
}

function renderProduits() {
  if (!produitsList) return;
  produitsList.innerHTML = '';
  const filtered = filtreActif ? produits.filter((p) => p.type === filtreActif) : [...produits];
  if (filtered.length === 0) {
    produitsList.innerHTML = '<p class="empty-state">Aucun produit dans cette catégorie.</p>';
    return;
  }
}

renderProduits();