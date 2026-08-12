import os

FILES_DATA = {
    ".env": """# Clé de sécurité Flask 
SECRET_KEY=be9babffad3afcd6e9a4349108c8aba3b0d981c4b63a64587ab4de80a38db965

# URL de la base de données SQLite
DATABASE_URL=sqlite:///instance/easymarket.db

# Mode de l'application
FLASK_ENV=production
FLASK_DEBUG=0

# Identifiants de l'Administrateur principal
ADMIN_WHATSAPP=+243849912381
ADMIN_CODE=EM-ADMIN-2026-SECURE""",

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
    
    instance_path = app.instance_path
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)

    db.init_app(app)

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
from pathlib import Path

load_dotenv()

# Définir le chemin du répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-a-changer-en-production-2026')
    # Le chemin absolu vers le fichier de base de données dans le dossier 'instance'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "instance" / "easymarket.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False""",

    "generate_code_md.py": """import os

EXTENSIONS = {".py", ".html", ".scss", ".js", ".txt", ".env"}
SPECIAL_FILES = {".gitignore", ".env"}
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", "venv", ".venv"}

OUTPUT_FILE = "code.md"

def should_process(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXTENSIONS or filename in SPECIAL_FILES:
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
                    ".py": "python", ".html": "html", ".scss": "scss",
                    ".js": "javascript", ".env": "env", ".gitignore": "gitignore", ".txt": "text"
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

    "init_db.py": """from app import create_app
from models.db_models import db

app = create_app()

def init_clean_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ La base de données a été réinitialisée. Elle est totalement vide et prête !")

if __name__ == "__main__":
    init_clean_db()""",

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
    statut = db.Column(db.String(20), default='actif')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    boutique = db.relationship('Boutique', backref='vendeur', uselist=False, cascade='all, delete-orphan')

    def set_code(self, code_clair):
        self.code_hash = generate_password_hash(code_clair)

    def check_code(self, code_clair):
        return check_password_hash(self.code_hash, code_clair)


class Boutique(db.Model):
    __tablename__ = 'boutiques'

    id = db.Column(db.String(50), primary_key=True)
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

    id = db.Column(db.String(20), primary_key=True)
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
    statut = db.Column(db.String(20), default='attente')
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

    "routes/admin.py": """from flask import Blueprint, render_template, request, jsonify
from utils.decorators import login_required
from models.db_models import db, Vendeur, Client

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required(role='admin')
def dashboard():
    vendeurs = Vendeur.query.all()
    clients = Client.query.all()
    historique_mensuel = []

    return render_template(
        'admin.html',
        vendeurs=vendeurs,
        clients=clients,
        historique_mensuel=historique_mensuel
    )

@admin_bp.route('/generer-code', methods=['POST'])
@login_required(role='admin')
def generer_code():
    vendeur_id = request.form.get('vendeur_id')
    code = 'EM-' + ''.join(__import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))

    vendeur = Vendeur.query.get(vendeur_id) if vendeur_id else None

    if vendeur is not None:
        vendeur.set_code(code)
        db.session.commit()

    return jsonify({
        'code': code,
        'vendeur_id': vendeur.id if vendeur else None,
        'vendeur_nom': vendeur.nom if vendeur else None
    })""",

    "routes/auth.py": """import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db_models import db, Vendeur, Boutique

auth_bp = Blueprint('auth', __name__)

ADMIN_WHATSAPP = os.environ.get('ADMIN_WHATSAPP')
ADMIN_CODE = os.environ.get('ADMIN_CODE')


def normalize_whatsapp(value):
    value = (value or '').strip()
    value = re.sub(r'[\\s\\-.]', '', value)
    if not value:
        return ''
    if value.startswith('00'):
        value = '+' + value[2:]
    if value.startswith('0'):
        value = '+243' + value[1:]
    if not value.startswith('+'):
        value = '+' + value
    return value


@auth_bp.route('/connexion')
def connexion():
    return render_template('connexion.html', initial_tab='login')


@auth_bp.route('/inscription')
def inscription():
    return render_template('connexion.html', initial_tab='register')


@auth_bp.route('/login', methods=['POST'])
def login():
    whatsapp = normalize_whatsapp(request.form.get('whatsapp', ''))
    code = request.form.get('code', '').strip()

    if whatsapp == ADMIN_WHATSAPP and code == ADMIN_CODE:
        session['role'] = 'admin'
        return redirect(url_for('admin.dashboard'))

    vendeur = Vendeur.query.filter_by(whatsapp=whatsapp).first()
    if vendeur is None:
        return render_template('connexion.html', error="Compte vendeur introuvable. Vérifiez votre numéro WhatsApp.")

    if not vendeur.check_code(code):
        return render_template('connexion.html', error="Code d’accès incorrect. Réessayez.")

    if vendeur.statut == 'suspendu':
        return render_template('connexion.html', error="Votre compte a été suspendu.")

    session['role'] = 'vendeur'
    session['vendeur_id'] = vendeur.id
    session['vendeur_nom'] = vendeur.nom
    session['vendeur_initiales'] = ''.join([n[0] for n in vendeur.nom.split()[:2]]).upper()
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/register', methods=['POST'])
def register():
    nom = (request.form.get('nom', '') or '').strip()
    boutique_nom = (request.form.get('boutique', '') or '').strip()
    whatsapp = normalize_whatsapp(request.form.get('whatsapp', ''))
    code = (request.form.get('code', '') or '').strip()

    if not nom or not boutique_nom or not whatsapp or not code:
        return render_template('connexion.html', error="Tous les champs sont requis pour l’inscription.")

    if Vendeur.query.filter_by(whatsapp=whatsapp).first():
        return render_template('connexion.html', error="Ce numéro WhatsApp est déjà utilisé.")

    vendeur = Vendeur(nom=nom, whatsapp=whatsapp, statut='actif')
    vendeur.set_code(code)

    boutique_id = boutique_nom.lower().replace(' ', '-')
    boutique = Boutique(
        id=boutique_id,
        nom=boutique_nom,
        categorie_principale=request.form.get('categorie_principale', 'Général'),
        description=request.form.get('description', ''),
        vendeur=vendeur
    )

    db.session.add(vendeur)
    db.session.add(boutique)
    db.session.commit()

    session['role'] = 'vendeur'
    session['vendeur_id'] = vendeur.id
    session['vendeur_nom'] = vendeur.nom
    session['vendeur_initiales'] = ''.join([n[0] for n in vendeur.nom.split()[:2]]).upper()
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/logout', methods=['GET', 'POST'])
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
    boutique_id = request.args.get('boutique', type=str)
    boutiques = Boutique.query.all()
    boutique = Boutique.query.get(boutique_id) if boutique_id else None

    if request.method == 'POST':
        boutique_id = request.form.get('boutique_id')
        if boutique_id:
            return redirect(url_for('main.voir_boutique', boutique_id=boutique_id))
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
    produits_selectionnes = request.form.getlist('produits_ids')
    produits_personnalises = request.form.getlist('produits_custom')

    if not nom_client or not whatsapp_client or (not produits_selectionnes and not produits_personnalises):
        flash("Informations incomplètes ou aucun produit sélectionné.", "error")
        return redirect(url_for('main.voir_boutique', boutique_id=boutique_id))

    client = Client.query.filter_by(whatsapp=whatsapp_client).first()
    if not client:
        client = Client(nom=nom_client, whatsapp=whatsapp_client)
        db.session.add(client)
        db.session.commit()

    montant_total = 0.0
    lignes_a_creer = []

    for produit_ref in produits_selectionnes:
        if not produit_ref:
            continue

        if produit_ref.startswith('custom:'):
            libelle = produit_ref.replace('custom:', '', 1).replace('+', ' ')
            lignes_a_creer.append(LigneReservation(libelle_produit=libelle))
            continue

        if produit_ref.startswith('custom_'):
            libelle = produit_ref.replace('custom_', '', 1).replace('+', ' ')
            lignes_a_creer.append(LigneReservation(libelle_produit=libelle))
            continue

        produit = Produit.query.get(produit_ref)
        if not produit or produit.boutique_id != boutique_id:
            continue

        if not produit.disponible:
            continue

        try:
            montant_total += float(produit.prix)
        except (TypeError, ValueError):
            pass

        lignes_a_creer.append(
            LigneReservation(libelle_produit=f"{produit.nom} ({produit.prix} {produit.devise})")
        )

    for produit_personnalise in produits_personnalises:
        if not produit_personnalise:
            continue
        lignes_a_creer.append(LigneReservation(libelle_produit=produit_personnalise.strip()))

    if not lignes_a_creer:
        flash("Aucun produit valide n'a été sélectionné pour cette réservation.", "error")
        return redirect(url_for('main.voir_boutique', boutique_id=boutique_id))

    nouvelle_reservation = Reservation(
        statut='attente',
        montant=str(montant_total),
        devise='CDF',
        client_id=client.id,
        boutique_id=boutique.id,
    )

    db.session.add(nouvelle_reservation)
    db.session.commit()

    for ligne in lignes_a_creer:
        ligne.reservation_id = nouvelle_reservation.id
        db.session.add(ligne)

    db.session.commit()

    flash("Votre réservation a été transmise avec succès au vendeur !", "success")
    return redirect(url_for('main.home'))""",

    "routes/vendeur.py": """from uuid import uuid4
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from utils.decorators import login_required
from models.db_models import db, Reservation, Boutique, Produit, Client, Vendeur, Categorie

vendeur_bp = Blueprint('vendeur', __name__)

@vendeur_bp.route('/boutique')
@login_required(role='vendeur')
def boutique():
    vendeur_id = session.get('vendeur_id')
    boutique_obj = Boutique.query.filter_by(vendeur_id=vendeur_id).first()
    categories = Categorie.query.filter_by(boutique_id=boutique_obj.id).all() if boutique_obj else []
    produits = boutique_obj.produits if boutique_obj else []

    return render_template(
        'boutique.html',
        vendeur={'nom': session.get('vendeur_nom'), 'initiales': session.get('vendeur_initiales')},
        boutique=boutique_obj,
        categories=categories,
        produits=produits,
        clients=Client.query.all() if boutique_obj else []
    )


@vendeur_bp.route('/boutique/update', methods=['POST'])
@login_required(role='vendeur')
def update_boutique():
    vendeur_id = session.get('vendeur_id')
    vendeur = Vendeur.query.get(vendeur_id)
    boutique_obj = Boutique.query.filter_by(vendeur_id=vendeur_id).first()

    if not boutique_obj:
        boutique_obj = Boutique(
            id=f"boutique-{vendeur_id or 'new'}",
            nom='Nouvelle boutique',
            categorie_principale='Général',
            vendeur_id=vendeur_id
        )
        db.session.add(boutique_obj)

    nom_boutique = (request.form.get('boutique_nom') or '').strip()
    categorie = (request.form.get('categorie') or '').strip()
    description = (request.form.get('description') or '').strip()
    vendeur_nom = (request.form.get('vendeur_nom') or '').strip()

    if nom_boutique:
        boutique_obj.nom = nom_boutique
    if categorie:
        boutique_obj.categorie_principale = categorie
    if description:
        boutique_obj.description = description

    if vendeur:
        if vendeur_nom:
            vendeur.nom = vendeur_nom
        session['vendeur_nom'] = vendeur.nom
        session['vendeur_initiales'] = ''.join([n[0] for n in vendeur.nom.split()[:2]]).upper()

    db.session.commit()
    flash('Boutique mise à jour avec succès.', 'success')
    return redirect(url_for('vendeur.boutique'))


@vendeur_bp.route('/boutique/categorie', methods=['POST'])
@login_required(role='vendeur')
def ajouter_categorie():
    vendeur_id = session.get('vendeur_id')
    boutique_obj = Boutique.query.filter_by(vendeur_id=vendeur_id).first()
    if not boutique_obj:
        flash('Aucune boutique trouvée pour ce vendeur.', 'error')
        return redirect(url_for('vendeur.boutique'))

    nom = (request.form.get('nom') or '').strip()
    if not nom:
        flash('Le nom de la catégorie est requis.', 'error')
        return redirect(url_for('vendeur.boutique'))

    existe = Categorie.query.filter_by(boutique_id=boutique_obj.id, nom=nom).first()
    if existe:
        flash('Cette catégorie existe déjà.', 'warning')
        return redirect(url_for('vendeur.boutique'))

    categorie = Categorie(nom=nom, boutique_id=boutique_obj.id)
    db.session.add(categorie)
    db.session.commit()
    flash('Catégorie ajoutée avec succès.', 'success')
    return redirect(url_for('vendeur.boutique'))


@vendeur_bp.route('/boutique/produit', methods=['POST'])
@login_required(role='vendeur')
def ajouter_produit():
    vendeur_id = session.get('vendeur_id')
    boutique_obj = Boutique.query.filter_by(vendeur_id=vendeur_id).first()
    if not boutique_obj:
        flash('Aucune boutique trouvée pour ce vendeur.', 'error')
        return redirect(url_for('vendeur.boutique'))

    nom = (request.form.get('nom') or '').strip()
    prix = (request.form.get('prix') or '').strip()
    if not nom or not prix:
        flash('Le nom et le prix du produit sont requis.', 'error')
        return redirect(url_for('vendeur.boutique'))

    produit = Produit(
        id=f"prod-{uuid4().hex[:10]}",
        nom=nom,
        prix=prix,
        devise=(request.form.get('devise') or 'CDF').upper(),
        disponible=(request.form.get('disponible', '1') == '1'),
        autres=(request.form.get('autres') or '').strip(),
        boutique_id=boutique_obj.id
    )

    categorie_id = request.form.get('categorie_id', type=int)
    if categorie_id:
        produit.categorie_id = categorie_id

    db.session.add(produit)
    db.session.commit()
    flash('Produit ajouté avec succès.', 'success')
    return redirect(url_for('vendeur.boutique'))


@vendeur_bp.route('/reservation')
@login_required(role='vendeur')
def reservation():
    vendeur_id = session.get('vendeur_id')
    boutique_obj = Boutique.query.filter_by(vendeur_id=vendeur_id).first()

    reservations_attente = []
    if boutique_obj:
        reservations_attente = Reservation.query.filter_by(
            boutique_id=boutique_obj.id,
            statut='attente'
        ).all()

    return render_template(
        'reservation.html',
        vendeur={'nom': session.get('vendeur_nom'), 'initiales': session.get('vendeur_initiales')},
        reservations_attente=reservations_attente,
        boutique=boutique_obj
    )


@vendeur_bp.route('/dashboard')
@login_required(role='vendeur')
def dashboard():
    vendeur_id = session.get('vendeur_id')
    boutique_obj = Boutique.query.filter_by(vendeur_id=vendeur_id).first()

    produits = Produit.query.filter_by(boutique_id=boutique_obj.id).all() if boutique_obj else []
    total_produits = len(produits)
    indisponibles = sum(1 for p in produits if not p.disponible)

    reservations = Reservation.query.filter_by(boutique_id=boutique_obj.id).all() if boutique_obj else []

    return render_template(
        'dashboard.html',
        taux_change=2250,
        ca_cdf='0',
        reservations_jour=len(reservations),
        reservations_attente=sum(1 for r in reservations if r.statut == 'attente'),
        reservations_traitees=sum(1 for r in reservations if r.statut != 'attente'),
        produits_total=total_produits,
        produits_indisponibles=indisponibles,
        clients_total=Client.query.count(),
        clients_nouveaux=0,
        historique=[]
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

document.querySelectorAll('.vendeur-card').forEach((card) => {
  card.addEventListener('click', () => {
    document.querySelectorAll('.vendeur-card').forEach((item) => item.classList.remove('selected'));
    card.classList.add('selected');
  });
});

document.getElementById('btn-gen-code')?.addEventListener('click', async () => {
  const selectedCard = document.querySelector('.vendeur-card.selected');
  const vendeurId = selectedCard ? selectedCard.dataset.id : null;
  const btn = document.getElementById('btn-gen-code');

  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Génération...';
  }

  try {
    const formData = new URLSearchParams();
    if (vendeurId) {
      formData.append('vendeur_id', vendeurId);
    }

    const response = await fetch('/admin/generer-code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData.toString()
    });

    const data = await response.json();
    if (!response.ok || !data.code) {
      throw new Error(data.error || 'Impossible de générer le code.');
    }

    const overlay = document.createElement('div');
    overlay.classList.add('modal-overlay', 'active');
    overlay.innerHTML = `
      <div class="modal">
        <h2 class="modal-title">Code d'accès généré</h2>
        <div class="modal-section">
          <p class="modal-label">Code à transmettre au vendeur</p>
          <div class="code-block" id="code-display">${data.code}</div>
        </div>
        <div class="modal-section">
          <p class="modal-label">Vendeur</p>
          <div class="code-block" id="code-vendeur-display">${data.vendeur_nom || 'Génération libre'}</div>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" id="btn-code-fermer" type="button">Fermer</button>
          <button class="btn primary" id="btn-code-copier" type="button">Copier le code</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#btn-code-fermer').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

    overlay.querySelector('#btn-code-copier').addEventListener('click', async () => {
      const btnCopy = overlay.querySelector('#btn-code-copier');
      try {
        await navigator.clipboard.writeText(data.code);
        btnCopy.textContent = 'Copié ✓';
        btnCopy.style.background = '#27AE60';
        btnCopy.style.borderColor = '#27AE60';
        setTimeout(() => {
          btnCopy.textContent = 'Copier le code';
          btnCopy.style.background = '';
          btnCopy.style.borderColor = '';
        }, 2000);
      } catch (error) {
        btnCopy.textContent = 'Code prêt';
        alert(data.code);
      }
    });
  } catch (error) {
    alert(error.message || 'Erreur lors de la génération du code.');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Générer un code d\\'accès';
    }
  }
});""",

    "static/js/boutique.js": """document.addEventListener('DOMContentLoaded', () => {
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
});""",

    "static/js/connexion.js": """const tabs = document.querySelectorAll('.auth-tab');
const forms = document.querySelectorAll('.auth-form');

function switchTab(target) {
  tabs.forEach((tab) => tab.classList.toggle('active', tab.dataset.tab === target));
  forms.forEach((form) => form.classList.toggle('active', form.id === `form-${target}`));
}

const params = new URLSearchParams(window.location.search);
const initialTab = params.get('tab') === 'register' ? 'register' : 'login';
switchTab(initialTab);

tabs.forEach((tab) => {
  tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});""",

    "static/js/dashboard.js": """const tauxInput = document.getElementById('taux-change');
const caCDFEl = document.getElementById('ca-cdf');
const caUSDEl = document.getElementById('ca-usd');

function formatNombre(n) { return n.toLocaleString('fr-FR'); }

function updateCA() {
  if (!tauxInput || !caCDFEl || !caUSDEl) return;
  const caTotalCDF = 0;
  const taux = parseFloat(tauxInput.value) || 1;
  const caUSD = (caTotalCDF / taux).toFixed(2);
  caCDFEl.innerHTML = `${formatNombre(caTotalCDF)} <span class="kpi-unit">CDF</span>`;
  caUSDEl.innerHTML = `≈ ${formatNombre(parseFloat(caUSD))} <span class="kpi-unit">USD</span>`;
}

tauxInput?.addEventListener('input', updateCA);
updateCA();""",

    "static/js/home.js": """const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', (event) => {
    const isAjax = form.dataset.ajax === 'true';

    if (!isAjax) {
      return;
    }

    event.preventDefault();

    fetch(form.action || window.location.href, {
      method: form.method || 'POST',
      body: new FormData(form),
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Erreur lors de l’envoi du formulaire.');
        }
        return response.text();
      })
      .then(() => {
        form.reset();
      })
      .catch(() => {
        console.warn('Le formulaire de contact n’a pas de traitement backend configuré.');
      });
  });
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
    "static/js/reservation.js": """document.addEventListener('DOMContentLoaded', () => {
  const notifyButtons = document.querySelectorAll('.notify-btn');

  notifyButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const card = button.closest('.reservation-card');
      const clientName = card?.querySelector('.client-name')?.textContent?.trim() || 'client';

      button.disabled = true;
      button.textContent = 'Notifié ✓';
      button.classList.add('is-sent');

      alert(`Notification envoyée à ${clientName}.`);
    });
  });

  const navLinks = document.querySelectorAll('.side-nav-link');
  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.forEach((item) => item.classList.remove('active'));
      link.classList.add('active');
    });
  });
});""",

    "static/js/reserver.js": """document.addEventListener('DOMContentLoaded', () => {
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
});""",

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
.btn-delete-produit { background: #FFF5F5; border: 1px solid #FCCACA; color: $danger-red; }""",

    "static/scss/connexion.scss": """/* connexion.scss */
@use 'variables' as *;

.auth-page {
  min-height: 100vh;
  background: $light-blue;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  margin-bottom: 32px;

  .brand-name {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.3px;

    .brand-easy   { color: #4EABFF; }
    .brand-market { color: $dark-blue; }
  }
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border: 1px solid $border-blue;
  border-radius: 14px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(30, 144, 255, 0.1);

  .auth-context-title {
    font-size: 1rem;
    font-weight: 700;
    color: $muted-blue;
    text-align: center;
    margin-bottom: 20px;
  }
}

.auth-tabs {
  display: flex;
  background: $light-blue;
  border-radius: 10px;
  padding: 4px;
  margin-bottom: 28px;

  .auth-tab {
    flex: 1;
    padding: 10px;
    border: none;
    background: transparent;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 700;
    color: $muted-blue;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s ease;

    &.active {
      background: #fff;
      color: $primary-blue;
      box-shadow: 0 2px 8px rgba(30, 144, 255, 0.12);
    }
  }
}

.auth-form {
  display: none;
  flex-direction: column;
  gap: 16px;

  &.active {
    display: flex;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;

  label {
    font-size: 0.85rem;
    font-weight: 600;
    color: $dark-blue;
  }
}

.form-input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid $border-blue;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  color: $text-dark;
  background: #fff;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;

  &::placeholder { color: $muted-blue; }

  &:focus {
    border-color: $primary-blue;
    box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.1);
  }
}

.form-hint {
  font-size: 0.78rem;
  color: $muted-blue;
  margin-top: 2px;
}

.auth-submit {
  width: 100%;
  padding: 13px;
  font-size: 0.95rem;
  margin-top: 8px;
  text-align: center;
}

.auth-switch {
  text-align: center;
  font-size: 0.85rem;
  color: $muted-blue;
  margin-top: 6px;

  .auth-switch-link {
    background: none;
    border: none;
    color: $primary-blue;
    font-weight: 700;
    cursor: pointer;
    font-size: 0.85rem;
    font-family: inherit;
    padding: 0;
    margin-left: 4px;

    &:hover {
      text-decoration: underline;
    }
  }
}

.auth-footer-note {
  margin-top: 24px;
  font-size: 0.8rem;
  color: $muted-blue;
  text-align: center;

  a {
    color: $primary-blue;
    text-decoration: none;

    &:hover { text-decoration: underline; }
  }
}""",

    "static/scss/dashboard.scss": """/* dashboard.scss */
@use 'variables' as *;

.dashboard-main {
  background: $light-blue;
  min-height: calc(100vh - 70px);
  padding: 50px 20px 70px;
}

.dashboard-container {
  max-width: 900px;
  margin: 0 auto;

  .page-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 32px;
  }

  .dashboard-shortcuts {
    display: flex;
    gap: 16px;
    margin-bottom: 40px;

    .shortcut-card {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 12px;
      background: #fff;
      border: 1px solid $border-blue;
      border-radius: 10px;
      padding: 18px 22px;
      text-decoration: none;
      color: $dark-blue;
      font-weight: 700;
      font-size: 0.95rem;
      box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);
      transition: all 0.2s ease;

      svg { color: $primary-blue; flex-shrink: 0; }

      &:hover {
        background: $light-blue;
        border-color: $primary-blue;
        transform: translateY(-2px);
      }
    }
  }
}

.taux-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  font-size: 0.88rem;
  font-weight: 600;
  color: $muted-blue;

  label {
    color: $dark-blue;
    font-weight: 700;
  }

  .taux-input {
    width: 90px;
    padding: 6px 10px;
    border: 1px solid $border-blue;
    border-radius: 6px;
    font-size: 0.88rem;
    font-weight: 700;
    color: $dark-blue;
    font-family: inherit;
    outline: none;
    text-align: center;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;

    &:focus {
      border-color: $primary-blue;
      box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.1);
    }
  }
}

.kpi-card--danger {
  border-color: #FCCACA;

  &:hover {
    box-shadow: 0 8px 24px rgba(231, 76, 60, 0.1);
  }
}

.kpi-icon--red {
  background: #FFF5F5;
  color: $danger-red;
  border: 1px solid #FCCACA;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 48px;
}

.kpi-card {
  background: #fff;
  border: 1px solid $border-blue;
  border-radius: 10px;
  padding: 20px 24px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(30, 144, 255, 0.1);
  }

  .kpi-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    &--blue   { background: $light-blue;  color: $primary-blue; border: 1px solid $border-blue; }
    &--orange { background: #FEF3E2; color: #E67E22; border: 1px solid #FDEBD0; }
    &--green  { background: #E8F8F1; color: #27AE60; border: 1px solid #A9DFBF; }
    &--purple { background: #F3EEFF; color: #8E44AD; border: 1px solid #D7BEF5; }
  }

  .kpi-info {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .kpi-label {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: $muted-blue;
    }

    .kpi-value {
      font-size: 1.5rem;
      font-weight: 800;
      color: $dark-blue;
      line-height: 1.1;

      &--small {
        font-size: 1rem;
        font-weight: 600;
        color: $muted-blue;
      }

      .kpi-unit {
        font-size: 0.75rem;
        font-weight: 600;
        color: $muted-blue;
      }
    }

    .kpi-sub {
      font-size: 0.8rem;
      color: $muted-blue;
      margin-top: 2px;
    }
  }
}

.historique-section {
  .section-heading {
    font-size: 1.2rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid $border-blue;
  }
}

.historique-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid $border-blue;
  box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);

  thead {
    background: $dark-blue;
    color: #fff;

    th {
      padding: 13px 16px;
      text-align: left;
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      white-space: nowrap;
    }
  }

  tbody {
    tr {
      border-bottom: 1px solid $border-blue;
      transition: background 0.15s ease;

      &:last-child { border-bottom: none; }
      &:hover { background: $light-blue; }
    }

    td {
      padding: 13px 16px;
      font-size: 0.9rem;
      color: $text-dark;

      &:first-child {
        font-weight: 600;
        color: $dark-blue;
      }
    }
  }
}""",

    "static/scss/home.scss": """/* home.scss */

.boutique-card,
.contact-channel,
.footer-link,
.menu-link,
.btn {
  transition: all 0.25s ease;
}

html {
  scroll-behavior: smooth;
}

header {
  position: sticky;
  top: 0;
  z-index: 50;
}

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: #fff;
  color: $text-dark;
}

.navbar {
  background: #fff;
  border-bottom: 2px solid $primary-blue;
  box-shadow: 0 2px 8px rgba(30, 144, 255, 0.08);
  padding: 14px 20px;

  .navbar-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 800px;
    margin: 0 auto;
  }

  .navbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;

    .logo {
      display: block;
      flex-shrink: 0;
    }

    .brand-name {
      font-size: 1.4rem;
      font-weight: 700;
      letter-spacing: -0.3px;

      .brand-easy {
        color: darken($primary-blue, 10%);
      }

      .brand-market {
        color: $dark-blue;
      }
    }
  }

  .navbar-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}

.btn {
  padding: 8px 18px;
  border-radius: 6px;
  border: 2px solid transparent;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  font-family: inherit;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;

  &.primary {
    background: $primary-blue;
    color: #fff;
    border-color: $primary-blue;

    &:hover {
      background: $medium-blue;
      border-color: $medium-blue;
    }
  }

  &.secondary {
    background: $light-blue;
    border-color: $primary-blue;
    color: $medium-blue;
    text-decoration: none; 

    &:hover {
      background: $primary-blue;
      color: #fff;
    }
  }

  &.danger {
    background: $danger-red;
    color: #fff;
    border-color: $danger-red;
    width: 100%;
    margin-top: 4px;

    &:hover {
      background: $danger-dark;
      border-color: $danger-dark;
    }
  }
}

.burger-menu {
  position: relative;

  #menu-toggle {
    display: none;
  }

  .menu-icon {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: $light-blue;
    }

    span {
      display: block;
      width: 22px;
      height: 4px;
      background: $dark-blue;
      border-radius: 2px;
      transition: all 0.25s ease;
      transform-origin: center;
    }
  }

  #menu-toggle:checked ~ .menu-icon span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(2) {
    opacity: 0;
    transform: scaleX(0);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
  }

  .menu-content {
    display: none;
    position: absolute;
    right: 0;
    top: calc(100% + 12px);
    background: #fff;
    border: 1px solid $border-blue;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
    flex-direction: column;
    gap: 2px;
    min-width: 200px;
    z-index: 100;
  }

  #menu-toggle:checked ~ .menu-content {
    display: flex;
  }

  .menu-profile {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    margin-bottom: 6px;
    background: $light-blue;
    border-radius: 7px;

    .menu-profile-avatar {
      width: 34px;
      height: 34px;
      background: $primary-blue;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 700;
      font-size: 0.85rem;
      flex-shrink: 0;
    }

    .menu-profile-info {
      .name {
        font-weight: 700;
        font-size: 0.9rem;
        color: $dark-blue;
      }

      .status {
        font-size: 0.78rem;
        color: $muted-blue;
      }
    }
  }

  .menu-divider {
    height: 1px;
    background: $border-blue;
    margin: 6px 0;
  }

  .menu-link {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 9px 10px;
    text-decoration: none;
    color: $text-dark;
    font-weight: 500;
    font-size: 0.9rem;
    border-radius: 6px;
    transition: background 0.15s, color 0.15s;

    svg {
      flex-shrink: 0;
      opacity: 0.7;
      transition: opacity 0.15s;
    }

    &:hover {
      background: $light-blue;
      color: $primary-blue;

      svg {
        opacity: 1;
      }
    }
  }
}

.hero {
  display: flex;
  align-items: center;
  gap: 60px;
  background: linear-gradient(135deg, $light-blue 60%, #D6EAFF 100%);
  padding: 80px 20px;
  max-width: 800px;
  margin: 0 auto;

  .hero-brand {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
    flex-shrink: 0;

    .hero-logo-name {
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -1px;
      line-height: 1;

      .brand-easy   { color: darken($primary-blue, 10%); }
      .brand-market { color: $dark-blue; }
    }

    .hero-actions {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }

    .btn {
      min-height: 42px;
    }

    .btn.primary {
      width: auto;
      min-width: 120px;
      font-size: 1rem;
      padding: 10px 18px;
      text-align: center;
    }

    .vendor-btn {
      min-width: 170px;
      padding: 10px 18px;
    }
  }

  .hero-pitch {
    background: #fff;
    border-left: 4px solid $primary-blue;
    border-radius: 0 10px 10px 0;
    padding: 28px 28px 28px 32px;
    box-shadow: 0 4px 16px rgba(30, 144, 255, 0.08);

    .hero-tagline {
      font-size: 1rem;
      line-height: 1.75;
      color: $text-dark;
      margin-bottom: 16px;
    }

    .hero-slogan {
      font-size: 1.05rem;
      font-weight: 700;
      color: $dark-blue;
      padding-top: 12px;
      border-top: 1px solid $border-blue;
    }
  }
}

.boutiques {
  background: #fff;
  padding: 60px 20px 70px;
  max-width: 800px;
  margin: 0 auto;

  .section-title {
    position: relative;
    padding-bottom: 10px;
    font-size: 1.5rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 28px;

    &::after {
      content: '';
      display: block;
      width: 40px;
      height: 3px;
      background: $primary-blue;
      border-radius: 2px;
      margin-top: 8px;
    }
  }

  .boutiques-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }

  .boutique-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 16px;
    background: #fff;
    border: 1px solid $border-blue;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;

    &:hover {
      box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
      transform: translateY(-2px);
    }

    .boutique-info {
      display: flex;
      flex-direction: column;
      gap: 6px;

      .boutique-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: $dark-blue;
      }

      .boutique-category {
        font-size: 0.78rem;
        font-weight: 600;
        color: $primary-blue;
        background: $light-blue;
        padding: 2px 8px;
        border-radius: 20px;
        align-self: flex-start;
      }

      .boutique-desc {
        font-size: 0.9rem;
        line-height: 1.6;
        color: $text-dark;
      }
    }

    .btn.primary {
      width: 100%;
      text-align: center;
    }
  }
}

.about {
  background: $light-blue;
  padding: 50px 20px;
  max-width: 800px;
  margin: 0 auto;

  h2 {
    font-size: 1.5rem;
    font-weight: 700;
    position: relative;
    padding-bottom: 10px;
    margin-bottom: 15px;
    color: $dark-blue;

    &::after {
      content: '';
      display: block;
      width: 40px;
      height: 3px;
      background: $primary-blue;
      border-radius: 2px;
      margin-top: 8px;
    }
  }

  p {
    font-size: 1rem;
    line-height: 1.7;
    color: $text-dark;
  }
}

.contact {
  background: #fff;
  padding: 60px 20px 70px;
  max-width: 800px;
  margin: 0 auto;

  .section-title {
    position: relative;
    padding-bottom: 10px;
    font-size: 1.5rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 28px;

    &::after {
      content: '';
      display: block;
      width: 40px;
      height: 3px;
      background: $primary-blue;
      border-radius: 2px;
      margin-top: 8px;
    }
  }

  .contact-wrapper {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .contact-form {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .form-input {
      width: 100%;
      padding: 12px 16px;
      border: 1px solid $border-blue;
      border-radius: 8px;
      font-size: 0.95rem;
      font-family: inherit;
      color: $text-dark;
      background: #fff;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;

      &::placeholder {
        color: $muted-blue;
      }

      &:focus {
        border-color: $primary-blue;
        box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.1);
      }
    }

    textarea.form-input {
      resize: vertical;
      min-height: 110px;
    }

    .btn.primary.form-input {
      padding: 12px 16px;
      text-align: center;
      align-self: stretch;
      background: $primary-blue;
      color: #fff;
      border-color: $primary-blue;

      &:hover {
        background: $medium-blue;
        border-color: $medium-blue;
      }
    }
  }
}

main > section {
  border-top: 1px solid $border-blue;
}

main > section:first-child {
  border-top: none;
}

.input-error {
  border-color: $danger-red;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.error-msg {
  font-size: 0.8rem;
  color: $danger-red;
  margin-top: -6px;
}""",

    "static/scss/login.scss": "",
    "static/scss/main.scss": """/* main.scss */

@use 'variables' as *;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: #fff;
  color: $text-dark;
}

.navbar {
  background: #fff;
  border-bottom: 2px solid $primary-blue;
  box-shadow: 0 2px 8px rgba(30, 144, 255, 0.08);
  padding: 14px 20px;

  .navbar-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 800px;
    margin: 0 auto;
  }

  .navbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;

    .logo {
      display: block;
      flex-shrink: 0;
    }

    .brand-name {
      font-size: 1.4rem;
      font-weight: 700;
      letter-spacing: -0.3px;

      .brand-easy {
        color: darken($primary-blue, 10%);
      }

      .brand-market {
        color: $dark-blue;
      }
    }
  }

  .navbar-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 8px 18px;
  border-radius: 6px;
  border: 2px solid transparent;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  font-family: inherit;
  line-height: 1.2;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;

  &.primary {
    background: $primary-blue;
    color: #fff;
    border-color: $primary-blue;

    &:hover {
      background: $medium-blue;
      border-color: $medium-blue;
    }
  }

  &.secondary {
    background: $light-blue;
    border-color: $primary-blue;
    color: $medium-blue;
    text-decoration: none;

    &:hover {
      background: $primary-blue;
      color: #fff;
    }

    &.vendor-btn {
      min-height: 42px;
      padding: 10px 18px;
      font-size: 0.95rem;
      letter-spacing: 0.01em;
    }
  }

  &.danger {
    background: $danger-red;
    color: #fff;
    border-color: $danger-red;
    width: 100%;
    margin-top: 4px;

    &:hover {
      background: $danger-dark;
      border-color: $danger-dark;
    }
  }
}

.burger-menu {
  position: relative;

  #menu-toggle {
    display: none;
  }

  .menu-icon {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: $light-blue;
    }

    span {
      display: block;
      width: 22px;
      height: 4px;
      background: $dark-blue;
      border-radius: 2px;
      transition: all 0.25s ease;
      transform-origin: center;
    }
  }

  #menu-toggle:checked ~ .menu-icon span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(2) {
    opacity: 0;
    transform: scaleX(0);
  }
  #menu-toggle:checked ~ .menu-icon span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
  }

  .menu-content {
    display: none;
    position: absolute;
    right: 0;
    top: calc(100% + 12px);
    background: #fff;
    border: 1px solid $border-blue;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 8px 24px rgba(30, 144, 255, 0.12);
    flex-direction: column;
    gap: 2px;
    min-width: 200px;
    z-index: 100;
  }

  #menu-toggle:checked ~ .menu-content {
    display: flex;
  }
}"""
}

def generate_project():
    print("🚀 Début de la mise à jour des fichiers du projet EasyMarket MVP...")
    created_files = 0
    
    for filepath, content in FILES_DATA.items():
        dirname = os.path.dirname(filepath)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        created_files += 1
        print(f"  ✓ [{created_files}/{len(FILES_DATA)}] Créé/Mis à jour : {filepath}")

    print("\n✅ Régénération du projet terminée avec succès !")

if __name__ == "__main__":
    generate_project()