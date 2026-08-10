import os

FILES_DATA = {
    ".env": """SECRET_KEY=dev-key-a-changer-en-production
DATABASE_URL=sqlite:///instance/easymarket.db
FLASK_ENV=development

ADMIN_WHATSAPP=+243849912381
ADMIN_CODE=ADMIN-2026-SECURE""",

    ".gitignore": """__pycache__/
*.pyc
.env
instance/
venv/
.vscode/
.DS_Store

# Ignorer le script de génération et le fichier de code compilé
generate_code_md.py
code.md""",

    "app.py": """import os
from flask import Flask
from config import Config
from models.db_models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # --- SOLUTION : S'assurer que le dossier instance existe physiquement ---
    instance_path = app.instance_path
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
    # ------------------------------------------------------------------------

    print("Avant init :", app.config["SQLALCHEMY_DATABASE_URI"])
    
    # Initialisation de SQLAlchemy
    db.init_app(app)
    print("Après init :", app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        from models.db_models import Vendeur, Boutique, Produit, Categorie, Client, Reservation, LigneReservation
        db.create_all()

    from routes.main import main
    from routes.auth import auth_bp
    from routes.vendeur import vendeur_bp
    from routes.admin import admin_bp

    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(vendeur_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)""",

    "config.py": """import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-a-changer-en-production')
    # Fichier stocké directement à la racine du projet
    SQLALCHEMY_DATABASE_URI = 'sqlite:///easymarket.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False""",

    "generate_code_md.py": """import os

# Extensions de fichiers à inclure
EXTENSIONS = {".py", ".html", ".scss", ".js", ".txt", ".env"}
# Fichiers spécifiques sans extension autorisés
SPECIAL_FILES = {".gitignore", ".env"}
# Dossiers à ignorer
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", "venv", ".venv"}

OUTPUT_FILE = "code.md"

def should_process(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXTENSIONS:
        return True
    if filename in SPECIAL_FILES:
        return True
    return False

def generate_markdown():
    markdown_content = "# Code Source du Projet\\n\\nCe fichier regroupe l'ensemble du code source du projet par fichier.\\n\\n"
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in sorted(files):
            if should_process(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.normpath(file_path)
                if relative_path.startswith("./") or relative_path.startswith(".\\\\"):
                    relative_path = relative_path[2:]
                
                ext = os.path.splitext(file)[1].lower()
                lang_map = {
                    ".py": "python",
                    ".html": "html",
                    ".scss": "scss",
                    ".js": "javascript",
                    ".env": "env",
                    ".gitignore": "gitignore",
                    ".txt": "text"
                }
                lang = lang_map.get(ext, "")
                
                markdown_content += f"## Fichier : `{relative_path}`\\n"
                markdown_content += f"Dossier : `{root}`\\n\\n"
                markdown_content += f"```{lang}\\n"
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        markdown_content += f.read()
                except Exception as e:
                    markdown_content += f"# Erreur de lecture du fichier : {e}\\n"
                
                markdown_content += "\\n```\\n\\n---\\n\\n"
                
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(markdown_content)
    
    print(f"[Automation] {OUTPUT_FILE} mis à jour avec succès.")

if __name__ == "__main__":
    generate_markdown()""",

    "requirements.txt": """blinker==1.9.0
click==8.4.2
colorama==0.4.6
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
greenlet==3.5.3
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
python-dotenv==1.0.1
SQLAlchemy==2.0.51
typing_extensions==4.16.0
Werkzeug==3.1.8""",

    "seed.py": """from app import create_app
from models.db_models import db, Vendeur, Boutique, Produit, Categorie
from tests.fixtures import MOCK_VENDEURS

app = create_app()

def run_seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        for v_data in MOCK_VENDEURS:
            b_data = v_data.pop("boutique")
            produits_data = b_data.pop("produits")
            code_clair = v_data.pop("code_clair")

            vendeur = Vendeur(**v_data)
            vendeur.set_code(code_clair)
            db.session.add(vendeur)
            db.session.flush()

            b_data["vendeur_id"] = vendeur.id
            boutique = Boutique(**b_data)
            db.session.add(boutique)

            cat_defaut = Categorie(nom="Général", boutique_id=boutique.id)
            db.session.add(cat_defaut)
            db.session.flush()

            for p_data in produits_data:
                p_data["boutique_id"] = boutique.id
                p_data["categorie_id"] = cat_defaut.id
                produit = Produit(**p_data)
                db.session.add(produit)

        db.session.commit()
        print("Base de données initialisée avec succès avec les données de test !")

if __name__ == "__main__":
    run_seed()""",

    "models/__init__.py": "",
    "models/boutique.py": "",
    "models/categorie.py": "",
    "models/client.py": "",
    "models/produit.py": "",
    "models/reservation.py": "",
    "models/vendeur.py": "",

    "models/db_models.py": """from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Vendeur(db.Model):
    __tablename__ = 'vendeurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(20), unique=True, nullable=False)
    code_hash = db.Column(db.String(255), nullable=False)
    statut = db.Column(db.String(20), default='actif') # 'actif', 'attente', 'suspendu'
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    boutique = db.relationship('Boutique', backref='vendeur', uselist=False, cascade='all, delete-orphan')

    def set_code(self, code_clair):
        self.code_hash = generate_password_hash(code_clair)

    def check_code(self, code_clair):
        return check_password_hash(self.code_hash, code_clair)


class Boutique(db.Model):
    __tablename__ = 'boutiques'

    id = db.Column(db.String(50), primary_key=True) # Ex: 'marche-frais'
    nom = db.Column(db.String(100), nullable=False)
    categorie_principale = db.Column(db.String(100))
    description = db.Column(db.Text)
    vendeur_id = db.Column(db.Integer, db.ForeignKey('vendeurs.id'), nullable=False)
    
    produits = db.relationship('Produit', backref='boutique', cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', backref='boutique', cascade='all, delete-orphan')


class Categorie(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    boutique_id = db.Column(db.String(50), db.ForeignKey('boutiques.id'), nullable=False)
    
    produits = db.relationship('Produit', backref='categorie_rel', cascade='all, delete-orphan')


class Produit(db.Model):
    __tablename__ = 'produits'

    id = db.Column(db.String(20), primary_key=True) # Ex: 'PRD-0001'
    nom = db.Column(db.String(100), nullable=False)
    type_produit = db.Column(db.String(50))
    prix = db.Column(db.String(20))
    devise = db.Column(db.String(5), default='CDF')
    disponible = db.Column(db.Boolean, default=True)
    autres = db.Column(db.String(255))
    
    boutique_id = db.Column(db.String(50), db.ForeignKey('boutiques.id'), nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(20), unique=True, nullable=False)
    date_premiere_visite = db.Column(db.DateTime, default=datetime.utcnow)
    
    reservations = db.relationship('Reservation', backref='client', cascade='all, delete-orphan')


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    statut = db.Column(db.String(20), default='attente') # 'attente', 'pret', 'servi', 'retire'
    montant = db.Column(db.String(20))
    devise = db.Column(db.String(5), default='CDF')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    boutique_id = db.Column(db.String(50), db.ForeignKey('boutiques.id'), nullable=False)
    
    produits_reserves = db.relationship('LigneReservation', backref='reservation', cascade='all, delete-orphan')


class LigneReservation(db.Model):
    __tablename__ = 'lignes_reservation'

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=False)
    libelle_produit = db.Column(db.String(150), nullable=False)""",

    "routes/__init__.py": "",

    "routes/admin.py": """from flask import Blueprint, render_template
from utils.decorators import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required(role='admin')
def dashboard():
    return render_template(
        'admin.html', 
        vendeurs=[], 
        clients=[], 
        historique_mensuel=[]
    )""",

    "routes/auth.py": """import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db_models import db, Vendeur

auth_bp = Blueprint('auth', __name__)

ADMIN_WHATSAPP = os.environ.get('ADMIN_WHATSAPP')
ADMIN_CODE = os.environ.get('ADMIN_CODE')

@auth_bp.route('/connexion')
def connexion():
    return render_template('connexion.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    whatsapp = request.form.get('whatsapp', '').strip()
    code = request.form.get('code', '').strip()

    if whatsapp == ADMIN_WHATSAPP and code == ADMIN_CODE:
        session['role'] = 'admin'
        return redirect(url_for('admin.dashboard'))

    vendeur = Vendeur.query.filter_by(whatsapp=whatsapp).first()
    if vendeur and vendeur.check_code(code):
        if vendeur.statut == 'suspendu':
            return render_template('connexion.html', error="Votre compte a été suspendu.")
        session['role'] = 'vendeur'
        session['vendeur_id'] = vendeur.id
        session['vendeur_nom'] = vendeur.nom
        session['vendeur_initiales'] = ''.join([n[0] for n in vendeur.nom.split()[:2]]).upper()
        return redirect(url_for('vendeur.dashboard'))

    return render_template('connexion.html', error="Identifiants incorrects.")

@auth_bp.route('/register', methods=['POST'])
def register():
    session['role'] = 'vendeur'
    session['vendeur_nom'] = request.form.get('nom', 'Nouveau vendeur')
    session['vendeur_initiales'] = ''.join([n[0] for n in session['vendeur_nom'].split()[:2]]).upper()
    return redirect(url_for('vendeur.dashboard'))

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))""",

    "routes/main.py": """from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.db_models import db, Boutique, Produit, Client, Reservation, LigneReservation

main = Blueprint('main', __name__)

@main.route('/')
def home():
    boutiques = Boutique.query.all()
    return render_template('home.html', boutiques=boutiques)

@main.route('/reserver', methods=['GET', 'POST'])
def reserver():
    boutique_id = request.args.get('boutique', type=int)
    boutiques = Boutique.query.all()
    boutique = Boutique.query.get(boutique_id) if boutique_id else None

    if request.method == 'POST':
        return redirect(url_for('main.reserver'))

    return render_template('reserver.html', boutiques=boutiques, boutique=boutique)

@main.route('/api/boutique/<string:boutique_id>/produits')
def api_produits_boutique(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)
    produits_data = [{
        'id': p.id,
        'nom': p.nom,
        'prix': p.prix,
        'devise': p.devise,
        'autres': p.autres
    } for p in boutique.produits]
    return jsonify(produits_data)

@main.route('/boutique/<string:boutique_id>')
def voir_boutique(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)
    return render_template('boutique.html', boutique=boutique)

@main.route('/boutique/<string:boutique_id>/reserver', methods=['POST'])
def traitement_reservation(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)

    nom_client = request.form.get('nom_client', '').strip()
    whatsapp_client = request.form.get('whatsapp_client', '').strip()
    produits_selectionnes_ids = request.form.getlist('produits_ids')

    if not nom_client or not whatsapp_client:
        flash("Veuillez renseigner votre nom et votre numéro WhatsApp.", "error")
        return redirect(url_for('main.voir_boutique', boutique_id=boutique_id))

    if not produits_selectionnes_ids:
        flash("Veuillez sélectionner au moins un produit à réserver.", "error")
        return redirect(url_for('main.voir_boutique', boutique_id=boutique_id))

    client = Client.query.filter_by(whatsapp=whatsapp_client).first()
    if not client:
        client = Client(nom=nom_client, whatsapp=whatsapp_client)
        db.session.add(client)
        db.session.commit()

    montant_total = 0
    lignes_a_creer = []

    for p_id in produits_selectionnes_ids:
        produit = Produit.query.filter_by(id=p_id, boutique_id=boutique_id).first()
        if produit:
            try:
                montant_total += float(produit.prix)
            except ValueError:
                pass
            
            lignes_a_creer.append(
                LigneReservation(libelle_produit=f"{produit.nom} ({produit.prix} {produit.devise})")
            )

    nouvelle_reservation = Reservation(
        statut='attente',
        montant=str(montant_total),
        devise='CDF',
        client_id=client.id,
        boutique_id=boutique.id
    )
    
    db.session.add(nouvelle_reservation)
    db.session.commit()

    for ligne in lignes_a_creer:
        ligne.reservation_id = nouvelle_reservation.id
        db.session.add(ligne)
    
    db.session.commit()

    flash("Votre réservation a été enregistrée avec succès ! Le vendeur va la valider.", "success")
    return redirect(url_for('main.home'))""",

    "routes/vendeur.py": """from flask import Blueprint, render_template, redirect, url_for, session
from utils.decorators import login_required

vendeur_bp = Blueprint('vendeur', __name__)

RESERVATIONS_TEMP = [
    {'id': 1, 'client_nom': 'Jonathan M.', 'client_whatsapp': '+243 84 991 2381',
     'nouveau_client': False, 'produits': ['5 kg de riz blanc', "2 litres d'huile végétale", '1 paquet de café moulu']},
    {'id': 2, 'client_nom': 'Jean-Paul N.', 'client_whatsapp': '+243 82 564 7890',
     'nouveau_client': False, 'produits': ['6 bananes plantain', '1 kg de poisson frais']},
    {'id': 3, 'client_nom': 'Lina M.', 'client_whatsapp': '+243 85 300 1122',
     'nouveau_client': True, 'produits': ['1 paquet de farine', '2 litres de lait', '1 bouteille de jus']},
]

@vendeur_bp.route('/boutique')
@login_required(role='vendeur')
def boutique():
    return render_template(
        'boutique.html',
        vendeur={'nom': session['vendeur_nom'], 'initiales': session['vendeur_initiales']},
        boutique={},
        clients=[]
    )

@vendeur_bp.route('/boutique/update', methods=['POST'])
@login_required(role='vendeur')
def update_boutique():
    return redirect(url_for('vendeur.boutique'))

@vendeur_bp.route('/reservation')
@login_required(role='vendeur')
def reservation():
    return render_template(
        'reservation.html',
        vendeur={'nom': session['vendeur_nom'], 'initiales': session['vendeur_initiales']},
        reservations_attente=RESERVATIONS_TEMP,
        boutique={'nom': 'Marché Frais'}
    )

@vendeur_bp.route('/dashboard')
@login_required(role='vendeur')
def dashboard():
    historique_temp = [
        {'date': '12 juil. 2026', 'reservations': 15, 'ca_cdf': '210 000', 'ca_usd': 280, 'nouveaux_clients': 2},
        {'date': '11 juil. 2026', 'reservations': 9, 'ca_cdf': '132 500', 'ca_usd': 150, 'nouveaux_clients': 1},
        {'date': '10 juil. 2026', 'reservations': 18, 'ca_cdf': '265 000', 'ca_usd': 410, 'nouveaux_clients': 4},
    ]
    return render_template(
        'dashboard.html',
        taux_change=2250,
        ca_cdf='184 500',
        reservations_jour=12,
        reservations_attente=4,
        reservations_traitees=8,
        produits_total=38,
        produits_indisponibles=5,
        clients_total=124,
        clients_nouveaux=3,
        historique=historique_temp,
    )""",

    "static/js/admin.js": """const sections = [
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

document.getElementById('btn-gen-code')?.addEventListener('click', () => {
  const code = 'EM-' + Math.random().toString(36).substring(2, 8).toUpperCase();
  const overlay = document.createElement('div');
  overlay.classList.add('modal-overlay', 'active');
  overlay.innerHTML = `
    <div class="modal">
      <h2 class="modal-title">Code d'accès généré</h2>
      <div class="modal-section">
        <p class="modal-label">Code à transmettre au vendeur</p>
        <div class="code-block" id="code-display">${code}</div>
      </div>
      <div class="modal-section">
        <p class="modal-label">Nom du vendeur (optionnel)</p>
        <input type="text" class="form-input" id="code-vendeur" placeholder="Ex : Boulangerie Dorée">
      </div>
      <div class="modal-actions">
        <button class="btn secondary" id="btn-code-fermer">Fermer</button>
        <button class="btn primary" id="btn-code-copier">Copier le code</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  overlay.querySelector('#btn-code-fermer').addEventListener('click', () => overlay.remove());
  overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

  overlay.querySelector('#btn-code-copier').addEventListener('click', () => {
    navigator.clipboard.writeText(code).then(() => {
      const btn = overlay.querySelector('#btn-code-copier');
      btn.textContent = 'Copié ✓';
      btn.style.background = '#27AE60';
      btn.style.borderColor = '#27AE60';
      setTimeout(() => {
        btn.textContent = 'Copier le code';
        btn.style.background = '';
        btn.style.borderColor = '';
      }, 2000);
    });
  });
});""",

    "static/js/boutique.js": """let produits = [];
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

renderProduits();""",

    "static/js/connexion.js": """const tabs = document.querySelectorAll('.auth-tab');
const forms = document.querySelectorAll('.auth-form');

function switchTab(target) {
  tabs.forEach((tab) => tab.classList.toggle('active', tab.dataset.tab === target));
  forms.forEach((form) => form.classList.toggle('active', form.id === `form-${target}`));
}

tabs.forEach((tab) => {
  tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});""",

    "static/js/dashboard.js": """const caTotalCDF = 184500;
const tauxInput = document.getElementById('taux-change');
const caCDFEl = document.getElementById('ca-cdf');
const caUSDEl = document.getElementById('ca-usd');

function formatNombre(n) { return n.toLocaleString('fr-FR'); }

function updateCA() {
  if (!tauxInput || !caCDFEl || !caUSDEl) return;
  const taux = parseFloat(tauxInput.value) || 1;
  const caUSD = (caTotalCDF / taux).toFixed(2);
  caCDFEl.innerHTML = `${formatNombre(caTotalCDF)} <span class="kpi-unit">CDF</span>`;
  caUSDEl.innerHTML = `≈ ${formatNombre(parseFloat(caUSD))} <span class="kpi-unit">USD</span>`;
}

tauxInput?.addEventListener('input', updateCA);
updateCA();""",

    "static/js/home.js": """const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', (e) => e.preventDefault());
}""",

    "static/js/login.js": "",
    "static/js/main.js": """const menuToggle = document.getElementById('menu-toggle');
const burgerMenu = document.querySelector('.burger-menu');

document.addEventListener('click', (e) => {
  if (burgerMenu && !burgerMenu.contains(e.target) && menuToggle) {
    menuToggle.checked = false;
  }
});""",

    "static/js/register.js": "",
    "static/js/reservation.js": """// Script de gestion des notifications WhatsApp et des états de réservations""",
    "static/js/reserver.js": """// Script d'interaction pour la page de réservation""",

    "static/scss/_variables.scss": """/* _variables.scss */
$primary-blue:   #1E90FF;
$dark-blue:      #0A3D62;
$medium-blue:    #1070CC;
$light-blue:     #EAF6FF;
$border-blue:    #D6EAFF;
$muted-blue:     #5B8FB9;
$text-dark:      #2C3E50;
$danger-red:     #e32d2d;
$danger-dark:    #be2424;""",

    "static/scss/admin.scss": """@use 'variables' as *;
.admin-main { background: $light-blue; min-height: calc(100vh - 70px); padding: 50px 20px 70px; }""",

    "static/scss/boutique.scss": """@use 'variables' as *;
.boutique-main { background: $light-blue; min-height: calc(100vh - 70px); padding: 50px 20px 70px; }
.btn-toggle-dispo { background: $light-blue; border: 1px solid $border-blue; color: $primary-blue; }
.btn-delete-produit { background: #FFF5F5; border: 1px solid #FCCACA; color: $danger-red; }"""
}

def generate_project():
    print("🚀 Début de la restauration du projet EasyMarket MVP...")
    created_files = 0
    
    for filepath, content in FILES_DATA.items():
        dirname = os.path.dirname(filepath)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        created_files += 1
        print(f"  ✓ [{created_files}/{len(FILES_DATA)}] Créé : {filepath}")

    print("\n✅ Tous les fichiers du projet ont été régénérés avec succès !")

if __name__ == "__main__":
    generate_project()