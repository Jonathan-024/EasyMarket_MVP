// ─── Nav latérale active au scroll ───────────────────────
const sections = [
  { id: 'section-boutique', link: document.querySelector('a[href="#section-boutique"]') },
  { id: 'section-produits', link: document.querySelector('a[href="#section-produits"]') },
  { id: 'section-clients',  link: document.querySelector('a[href="#section-clients"]') },
];

window.addEventListener('scroll', () => {
  let current = sections[0].id;

  sections.forEach(({ id }) => {
    const el = document.getElementById(id);
    if (!el) return;
    const rect = el.getBoundingClientRect();
    if (rect.top <= window.innerHeight / 2) current = id;
  });

  sections.forEach(({ id, link }) => {
    link.classList.toggle('active', id === current);
  });
});

// ─── Formulaire boutique ──────────────────────────────────
const formBoutique = document.getElementById('form-boutique');

formBoutique.addEventListener('submit', (e) => {
  e.preventDefault();

  const nom = document.getElementById('boutique-nom').value.trim();
  const vendeur = document.getElementById('vendeur-nom').value.trim();

  if (!nom || !vendeur) {
    if (!nom) showError(document.getElementById('boutique-nom'), 'Champ requis.');
    if (!vendeur) showError(document.getElementById('vendeur-nom'), 'Champ requis.');
    return;
  }

  const btn = formBoutique.querySelector('.btn.primary');
  btn.textContent = 'Enregistré ✓';
  btn.style.background = '#27AE60';
  btn.style.borderColor = '#27AE60';

  setTimeout(() => {
    btn.textContent = 'Enregistrer';
    btn.style.background = '';
    btn.style.borderColor = '';
  }, 2000);
});

// ─── Utilitaires erreurs ──────────────────────────────────
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

document.querySelectorAll('.form-input').forEach((input) => {
  input.addEventListener('input', () => clearError(input));
});

// ─── Produits ────────────────────────────────────────────
let produits = [];
let categories = [];
let produitIdCounter = 1;
let filtreActif = '';

const produitsList = document.getElementById('produits-list');
const categoriesList = document.getElementById('categories-list');

function generateId() {
  return `PRD-${String(produitIdCounter++).padStart(4, '0')}`;
}

function renderFiltres() {
  const filtreContainer = document.getElementById('produits-filtres');
  if (!filtreContainer) return;

  filtreContainer.innerHTML = '';

  const btnTous = document.createElement('button');
  btnTous.classList.add('filtre-btn');
  if (!filtreActif) btnTous.classList.add('active');
  btnTous.textContent = 'Tous';
  btnTous.addEventListener('click', () => { filtreActif = ''; renderFiltres(); renderProduits(); });
  filtreContainer.appendChild(btnTous);

  categories.forEach((cat) => {
    const btn = document.createElement('button');
    btn.classList.add('filtre-btn');
    if (filtreActif === cat) btn.classList.add('active');
    btn.textContent = cat;
    btn.addEventListener('click', () => { filtreActif = cat; renderFiltres(); renderProduits(); });
    filtreContainer.appendChild(btn);
  });
}

function renderProduits() {
  produitsList.innerHTML = '';

  const filtered = filtreActif
    ? produits.filter((p) => p.type === filtreActif)
    : [...produits];

  const sorted = filtered.sort((a, b) => a.nom.localeCompare(b.nom));

  if (sorted.length === 0) {
    produitsList.innerHTML = '<p class="empty-state">Aucun produit dans cette catégorie.</p>';
    return;
  }

  sorted.forEach((produit) => {
    const card = document.createElement('div');
    card.classList.add('produit-card');
    card.innerHTML = `
      <div class="produit-card-top">
        <div class="produit-main">
          <span class="produit-id">${produit.id}</span>
          <span class="produit-nom">${produit.nom}</span>
        </div>
        <span class="produit-statut ${produit.disponible ? 'statut--dispo' : 'statut--indispo'}">
          ${produit.disponible ? 'Disponible' : 'Indisponible'}
        </span>
      </div>
      <div class="produit-card-body">
        <span class="produit-meta">
          <span class="meta-label">Catégorie</span>
          <select class="meta-select" data-id="${produit.id}">
            <option value="">— Aucune —</option>
            ${categories.map((c) => `<option value="${c}" ${produit.type === c ? 'selected' : ''}>${c}</option>`).join('')}
          </select>
        </span>
        <span class="produit-meta">
          <span class="meta-label">Prix</span>
          <span>${produit.prix ? produit.prix + ' ' + produit.devise : '—'}</span>
        </span>
        ${produit.autres ? `<span class="produit-meta produit-meta--full"><span class="meta-label">Autres</span><span>${produit.autres}</span></span>` : ''}
      </div>
      <div class="produit-card-actions">
        <button class="btn-toggle-dispo" data-id="${produit.id}">
          ${produit.disponible ? 'Marquer indisponible' : 'Marquer disponible'}
        </button>
        <button class="btn-delete-produit" data-id="${produit.id}">Supprimer</button>
      </div>
    `;
    produitsList.appendChild(card);
  });

  produitsList.querySelectorAll('.btn-toggle-dispo').forEach((btn) => {
    btn.addEventListener('click', () => {
      const p = produits.find((p) => p.id === btn.dataset.id);
      if (p) { p.disponible = !p.disponible; renderProduits(); renderCategories(); }
    });
  });

  produitsList.querySelectorAll('.btn-delete-produit').forEach((btn) => {
    btn.addEventListener('click', () => {
      produits = produits.filter((p) => p.id !== btn.dataset.id);
      if (filtreActif && !produits.find((p) => p.type === filtreActif)) filtreActif = '';
      renderProduits();
      renderCategories();
      renderFiltres();
    });
  });

  produitsList.querySelectorAll('.meta-select').forEach((select) => {
    select.addEventListener('change', () => {
      const p = produits.find((p) => p.id === select.dataset.id);
      if (p) {
        p.type = select.value;
        renderCategories();
        renderFiltres();
      }
    });
  });
}

function renderCategories() {
  categoriesList.innerHTML = '';

  if (categories.length === 0) {
    categoriesList.innerHTML = '<p class="empty-state">Aucune catégorie ajoutée.</p>';
    renderFiltres();
    return;
  }

  categories.forEach((cat) => {
    const produitsDeCat = produits.filter((p) => p.type === cat);
    const bloc = document.createElement('div');
    bloc.classList.add('categorie-bloc');
    bloc.innerHTML = `
      <div class="categorie-header">
        <span class="categorie-nom">${cat}</span>
        <span class="categorie-count">${produitsDeCat.length} produit${produitsDeCat.length !== 1 ? 's' : ''}</span>
        <button class="btn-assign-produits" data-cat="${cat}">Gérer</button>
        <button class="btn-delete-cat" data-cat="${cat}">✕</button>
      </div>
      <div class="categorie-produits">
        ${produitsDeCat.length === 0
          ? '<p class="empty-state">Aucun produit dans cette catégorie.</p>'
          : produitsDeCat.map((p) => `
            <div class="categorie-produit-item">
              <span>${p.nom}</span>
              <span class="produit-statut ${p.disponible ? 'statut--dispo' : 'statut--indispo'}">
                ${p.disponible ? 'Disponible' : 'Indisponible'}
              </span>
            </div>
          `).join('')
        }
      </div>
    `;
    categoriesList.appendChild(bloc);
  });

  categoriesList.querySelectorAll('.btn-assign-produits').forEach((btn) => {
    btn.addEventListener('click', () => openAssignModal(btn.dataset.cat));
  });

  categoriesList.querySelectorAll('.btn-delete-cat').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (filtreActif === btn.dataset.cat) filtreActif = '';
      categories = categories.filter((c) => c !== btn.dataset.cat);
      produits.forEach((p) => { if (p.type === btn.dataset.cat) p.type = ''; });
      renderCategories();
      renderFiltres();
      renderProduits();
    });
  });

  renderFiltres();
}

// ─── Modal générique ──────────────────────────────────────
function openModal(content) {
  const overlay = document.createElement('div');
  overlay.classList.add('modal-overlay', 'active');
  overlay.innerHTML = `<div class="modal">${content}</div>`;
  document.body.appendChild(overlay);

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.remove();
  });

  return overlay;
}

// ─── Modal ajouter produit ────────────────────────────────
document.getElementById('btn-add-produit').addEventListener('click', () => {
  const catOptions = categories.map((c) => `<option value="${c}">${c}</option>`).join('');

  const overlay = openModal(`
    <h2 class="modal-title">Ajouter un produit</h2>
    <div class="modal-section">
      <p class="modal-label">Nom du produit</p>
      <input type="text" class="form-input" id="new-produit-nom" placeholder="Ex : Tomates fraîches">
    </div>
    <div class="modal-section">
      <p class="modal-label">Type / Catégorie</p>
      <select class="form-input" id="new-produit-type">
        <option value="">— Aucune catégorie —</option>
        ${catOptions}
      </select>
    </div>
    <div class="modal-section">
      <p class="modal-label">Prix</p>
      <div class="amount-group">
        <input type="text" class="form-input amount-input" id="new-produit-prix" placeholder="Ex : 5000">
        <select class="form-input amount-select" id="new-produit-devise">
          <option value="CDF">CDF</option>
          <option value="USD">USD</option>
        </select>
      </div>
    </div>
    <div class="modal-section">
      <p class="modal-label">Statut</p>
      <select class="form-input" id="new-produit-statut">
        <option value="true">Disponible</option>
        <option value="false">Indisponible</option>
      </select>
    </div>
    <div class="modal-section">
      <p class="modal-label">Autres informations</p>
      <input type="text" class="form-input" id="new-produit-autres" placeholder="Ex : Bio, importé, en promotion...">
    </div>
    <div class="modal-actions">
      <button class="btn secondary" id="btn-modal-annuler">Annuler</button>
      <button class="btn primary" id="btn-modal-confirmer">Ajouter</button>
    </div>
  `);

  overlay.querySelector('#btn-modal-annuler').addEventListener('click', () => overlay.remove());

  overlay.querySelector('#btn-modal-confirmer').addEventListener('click', () => {
    const nomInput = overlay.querySelector('#new-produit-nom');
    const nom = nomInput.value.trim();
    if (!nom) { showError(nomInput, 'Nom requis.'); return; }

    produits.push({
      id: generateId(),
      nom,
      type: overlay.querySelector('#new-produit-type').value,
      prix: overlay.querySelector('#new-produit-prix').value.trim(),
      devise: overlay.querySelector('#new-produit-devise').value,
      disponible: overlay.querySelector('#new-produit-statut').value === 'true',
      autres: overlay.querySelector('#new-produit-autres').value.trim(),
    });

    renderProduits();
    renderCategories();
    overlay.remove();
  });
});

// ─── Modal assigner produit à catégorie ───────────────────
function openAssignModal(cat) {
  const produitsDispos = produits.map((p) => `
    <label class="jour-label">
      <input type="checkbox" value="${p.id}" ${p.type === cat ? 'checked' : ''}>
      ${p.nom}
    </label>
  `).join('');

  const overlay = openModal(`
    <h2 class="modal-title">Produits — ${cat}</h2>
    <div class="modal-section">
      <p class="modal-label">Cochez les produits à inclure</p>
      <div class="jours-grid" style="margin-top:8px;">
        ${produitsDispos.length ? produitsDispos : '<p class="empty-state">Aucun produit existant.</p>'}
      </div>
    </div>
    <div class="modal-actions">
      <button class="btn secondary" id="btn-assign-annuler">Annuler</button>
      <button class="btn primary" id="btn-assign-confirmer">Enregistrer</button>
    </div>
  `);

  overlay.querySelector('#btn-assign-annuler').addEventListener('click', () => overlay.remove());

  overlay.querySelector('#btn-assign-confirmer').addEventListener('click', () => {
    const checked = overlay.querySelectorAll('input[type="checkbox"]:checked');
    const checkedIds = Array.from(checked).map((cb) => cb.value);

    produits.forEach((p) => {
      if (checkedIds.includes(p.id)) p.type = cat;
      else if (p.type === cat) p.type = '';
    });

    renderProduits();
    renderCategories();
    overlay.remove();
  });
}

// ─── Modal ajouter catégorie ──────────────────────────────
document.getElementById('btn-add-categorie').addEventListener('click', () => {
  const overlay = openModal(`
    <h2 class="modal-title">Ajouter une catégorie</h2>
    <div class="modal-section">
      <p class="modal-label">Nom de la catégorie</p>
      <input type="text" class="form-input" id="new-cat-nom" placeholder="Ex : Fruits & Légumes">
    </div>
    <div class="modal-actions">
      <button class="btn secondary" id="btn-cat-annuler">Annuler</button>
      <button class="btn primary" id="btn-cat-confirmer">Ajouter</button>
    </div>
  `);

  overlay.querySelector('#btn-cat-annuler').addEventListener('click', () => overlay.remove());

  overlay.querySelector('#btn-cat-confirmer').addEventListener('click', () => {
    const nom = overlay.querySelector('#new-cat-nom').value.trim();
    if (!nom) {
      showError(overlay.querySelector('#new-cat-nom'), 'Nom requis.');
      return;
    }
    if (categories.includes(nom)) {
      showError(overlay.querySelector('#new-cat-nom'), 'Catégorie déjà existante.');
      return;
    }
    categories.push(nom);
    renderCategories();
    overlay.remove();
  });
});

// ─── Init ─────────────────────────────────────────────────
renderProduits();
renderCategories();