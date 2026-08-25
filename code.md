# Code Source du Projet

Ce fichier regroupe l'ensemble du code source du projet par fichier.

## Fichier : `.env`
Dossier : `.`

```
# Clé de sécurité Flask
SECRET_KEY=be9babffad3afcd6e9a4349108c8aba3b0d981c4b63a64587ab4de80a38db965
DATABASE_URL=sqlite:///instance/easymarket.db
FLASK_ENV=production
FLASK_DEBUG=0
ADMIN_WHATSAPP=+243849912381
ADMIN_CODE=EM-ADMIN-2026-SECURE
```

---

## Fichier : `.gitignore`
Dossier : `.`

```
__pycache__/
*.pyc
.env
instance/
venv/
.vscode/
.DS_Store

tests/

generate_code_md.py
code.md

prompt_rules.md
prompt_templates.md
roadmap_mvp.md
test_api.py
seed.py
init_db.py
```

---

## Fichier : `app.py`
Dossier : `.`

```python
import os
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
    app.run(debug=True)
```

---

## Fichier : `apply_update.py`
Dossier : `.`

```python
import os

# --- CONFIGURATION DES TÂCHES ---
TASKS = [
    {
        "file": "templates/base.html",
        "action": "replace_block",
        "start_marker": "<!-- FOOTER -->",
        "end_marker": "</footer>",
        "content": """<!-- FOOTER -->
  <footer>
    <div class="footer-content">
      <div class="footer-top">
        <div class="footer-brand">
          <span class="brand-name">
            <span class="brand-easy">Easy</span><span class="brand-market">Market |</span>
            <span class="footer-tagline">Le marché facile — pour tous !</span>
          </span>
        </div>
        <div class="footer-links">
          <a href="https://wa.me/VOTRE_NUMERO" class="footer-link" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="#25D366" aria-hidden="true"><path d="M20.52 3.48A11.93 11.93 0 0012 0C5.37 0 0 5.37 0 12c0 2.11.55 4.16 1.6 5.97L0 24l6.18-1.57A11.94 11.94 0 0012 24c6.63 0 12-5.37 12-12 0-3.2-1.25-6.21-3.48-8.52zM12 22c-1.85 0-3.66-.5-5.23-1.43l-.37-.22-3.87.98.99-3.76-.24-.38A9.94 9.94 0 012 12C2 6.48 6.48 2 12 2c2.67 0 5.18 1.04 7.07 2.93A9.94 9.94 0 0122 12c0 5.52-4.48 10-10 10zm5.44-7.3c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.79-1.68-2.09-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.6-.91-2.2-.24-.58-.48-.5-.67-.51H6.9c-.2 0-.52.07-.79.37C5.84 8.2 5.1 8.9 5.1 10.35s1.05 2.87 1.2 3.07c.15.2 2.07 3.16 5.01 4.43.7.3 1.25.48 1.67.62.7.22 1.34.19 1.84.12.56-.08 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 EasyMarket. Tous droits réservés.</p>
        <a href="#" class="footer-link legal-link">Mentions légales</a>
      </div>
    </div>
  </footer>"""
    },
    {
        "file": "static/scss/main.scss",
        "action": "append",
        "content": """

/* ─── Footer ────────────────────────────────────────────── */
footer {
  background: #0A3D62;
  color: #fff;
  padding: 30px 20px 24px;

  .footer-content {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;

    .footer-top {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .footer-brand {
        display: flex;
        flex-direction: column;
        gap: 6px;

        .brand-name {
          font-size: 1.3rem;
          font-weight: 800;
          letter-spacing: -0.3px;

          .brand-easy {
            color: #4EABFF;
          }
          .brand-market {
            color: #fff;
          }
        }

        .footer-tagline {
          font-size: 1rem;
          font-weight: 200;
          color: rgba(255, 255, 255, 0.45);
        }
      }
    }

    .footer-links {
      display: flex;
      align-items: center;
      gap: 10px;

      .footer-link {
        display: flex;
        align-items: center;
        gap: 7px;
        text-decoration: none;
        font-size: 0.7rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.7);
        transition: color 0.2s ease;
        &:hover {
          color: #fff;
        }
      }
    }
    
    .footer-bottom {
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      text-align: center;

      p {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
      }
    }

    .legal-link {
      display: inline-block;
      margin-top: 10px;
      text-decoration: none;
      font-size: 0.85rem;
      color: darken($primary-blue, 10%);
      &:hover {
        color: $primary-blue;
        text-decoration: underline;
      }
    }
  }
}"""
    }
]

def apply_updates():
    for task in TASKS:
        try:
            if not os.path.exists(task['file']):
                print(f"⚠️ Fichier introuvable : {task['file']}")
                continue

            with open(task['file'], 'r', encoding='utf-8') as f:
                content = f.read()

            if task['action'] == 'replace_block':
                start = content.find(task['start_marker'])
                end = content.find(task['end_marker'], start) + len(task['end_marker'])
                if start != -1 and end != -1:
                    new_content = content[:start] + task['content'] + content[end:]
                    with open(task['file'], 'w', encoding='utf-8') as f:
                        f.write(new_content)
                else:
                    print(f"❌ Marqueurs non trouvés dans {task['file']}")
                    continue
            
            elif task['action'] == 'append':
                with open(task['file'], 'a', encoding='utf-8') as f:
                    f.write(task['content'])
            
            print(f"✅ Succès : {task['file']} mis à jour.")
        except Exception as e:
            print(f"❌ Erreur sur {task['file']} : {e}")

if __name__ == "__main__":
    apply_updates()
```

---

## Fichier : `config.py`
Dossier : `.`

```python
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Définir le chemin du répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-a-changer-en-production-2026')
    # Le chemin absolu vers le fichier de base de données dans le dossier 'instance'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "instance" / "easymarket.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## Fichier : `generate_code_md.py`
Dossier : `.`

```python
import os

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
    markdown_content = "# Code Source du Projet\n\nCe fichier regroupe l'ensemble du code source du projet par fichier.\n\n"
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in sorted(files):
            if should_process(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.normpath(file_path)
                if relative_path.startswith("./") or relative_path.startswith(".\\"):
                    relative_path = relative_path[2:]
                
                ext = os.path.splitext(file)[1].lower()
                lang_map = {
                    ".py": "python", ".html": "html", ".scss": "scss",
                    ".js": "javascript", ".env": "env", ".gitignore": "gitignore", ".txt": "text"
                }
                lang = lang_map.get(ext, "")
                
                markdown_content += f"## Fichier : `{relative_path}`\n"
                markdown_content += f"Dossier : `{root}`\n\n"
                markdown_content += f"```{lang}\n"
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        markdown_content += f.read()
                except Exception as e:
                    markdown_content += f"# Erreur de lecture du fichier : {e}\n"
                
                markdown_content += "\n```\n\n---\n\n"
                
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(markdown_content)
    
    print(f"[Automation] {OUTPUT_FILE} mis à jour avec succès.")

if __name__ == "__main__":
    generate_markdown()
```

---

## Fichier : `init_db.py`
Dossier : `.`

```python
from app import create_app
from models.db_models import db

app = create_app()

def init_clean_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ La base de données a été réinitialisée. Elle est totalement vide et prête !")

if __name__ == "__main__":
    init_clean_db()
```

---

## Fichier : `requirements.txt`
Dossier : `.`

```text
blinker==1.9.0
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
Werkzeug==3.1.8
```

---

## Fichier : `seed.py`
Dossier : `.`

```python
from app import create_app
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
    run_seed()
```

---

## Fichier : `test_api.py`
Dossier : `.`

```python
import requests

# URL de ton serveur Flask (généralement localhost:5000)
BASE_URL = "http://127.0.0.1:5000"

def test_connection():
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Backend en ligne et opérationnel !")
        else:
            print(f"⚠️ Backend répond, mais avec le code : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur : Impossible de contacter le backend. Il est peut-être éteint. Détail : {e}")

if __name__ == "__main__":
    test_connection()
```

---

## Fichier : `models\__init__.py`
Dossier : `.\models`

```python

```

---

## Fichier : `models\boutique.py`
Dossier : `.\models`

```python

```

---

## Fichier : `models\categorie.py`
Dossier : `.\models`

```python

```

---

## Fichier : `models\client.py`
Dossier : `.\models`

```python

```

---

## Fichier : `models\db_models.py`
Dossier : `.\models`

```python
from datetime import datetime
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
    libelle_produit = db.Column(db.String(150), nullable=False)
```

---

## Fichier : `models\produit.py`
Dossier : `.\models`

```python

```

---

## Fichier : `models\reservation.py`
Dossier : `.\models`

```python

```

---

## Fichier : `models\vendeur.py`
Dossier : `.\models`

```python

```

---

## Fichier : `routes\__init__.py`
Dossier : `.\routes`

```python

```

---

## Fichier : `routes\admin.py`
Dossier : `.\routes`

```python
from flask import Blueprint, render_template, request, jsonify
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
    })
```

---

## Fichier : `routes\auth.py`
Dossier : `.\routes`

```python
import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db_models import db, Vendeur, Boutique

auth_bp = Blueprint('auth', __name__)

ADMIN_WHATSAPP = os.environ.get('ADMIN_WHATSAPP')
ADMIN_CODE = os.environ.get('ADMIN_CODE')


def normalize_whatsapp(value):
    value = (value or '').strip()
    value = re.sub(r'[\s\-.]', '', value)
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
    return redirect(url_for('main.home'))
```

---

## Fichier : `routes\client.py`
Dossier : `.\routes`

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.db_models import db, Boutique, Client, Reservation, LigneReservation

client_bp = Blueprint('client', __name__)

@client_bp.route('/reserver', methods=['GET', 'POST'])
def reserver():
    boutiques = Boutique.query.all()
    if request.method == 'POST':
        boutique_id = request.form.get('boutique_id')
        nom = request.form.get('nom_client')
        whatsapp = request.form.get('whatsapp_client')
        produits = request.form.getlist('produits_custom') # Entrés manuellement par le client
        
        if not boutique_id or not nom or not produits:
            flash("Erreur: informations manquantes")
            return redirect(url_for('client.reserver'))
            
        client = Client.query.filter_by(whatsapp=whatsapp).first()
        if not client:
            client = Client(nom=nom, whatsapp=whatsapp)
            db.session.add(client)
            db.session.commit()
            
        reservation = Reservation(client_id=client.id, boutique_id=boutique_id)
        db.session.add(reservation)
        db.session.commit()
        
        for p in produits:
            if p.strip():
                db.session.add(LigneReservation(reservation_id=reservation.id, libelle_produit=p.strip()))
        
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('reserver.html', boutiques=boutiques)

```

---

## Fichier : `routes\main.py`
Dossier : `.\routes`

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
    return redirect(url_for('main.home'))
```

---

## Fichier : `routes\vendeur.py`
Dossier : `.\routes`

```python
from uuid import uuid4
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
    )
```

---

## Fichier : `static\js\admin.js`
Dossier : `.\static\js`

```javascript
const sections = [
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
      btn.textContent = 'Générer un code d\'accès';
    }
  }
});
```

---

## Fichier : `static\js\boutique.js`
Dossier : `.\static\js`

```javascript
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
```

---

## Fichier : `static\js\connexion.js`
Dossier : `.\static\js`

```javascript
const tabs = document.querySelectorAll('.auth-tab');
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
});
```

---

## Fichier : `static\js\dashboard.js`
Dossier : `.\static\js`

```javascript
const tauxInput = document.getElementById('taux-change');
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
updateCA();
```

---

## Fichier : `static\js\home.js`
Dossier : `.\static\js`

```javascript
const form = document.querySelector('.contact-form');
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
}
```

---

## Fichier : `static\js\login.js`
Dossier : `.\static\js`

```javascript

```

---

## Fichier : `static\js\main.js`
Dossier : `.\static\js`

```javascript
const menuToggle = document.getElementById('menu-toggle');
const burgerMenu = document.querySelector('.burger-menu');

document.addEventListener('click', (e) => {
  if (burgerMenu && !burgerMenu.contains(e.target) && menuToggle) {
    menuToggle.checked = false;
  }
});
```

---

## Fichier : `static\js\register.js`
Dossier : `.\static\js`

```javascript

```

---

## Fichier : `static\js\reservation.js`
Dossier : `.\static\js`

```javascript
document.addEventListener('DOMContentLoaded', () => {
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
});
```

---

## Fichier : `static\js\reserver.js`
Dossier : `.\static\js`

```javascript
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
```

---

## Fichier : `static\scss\_variables.scss`
Dossier : `.\static\scss`

```scss
/* _variables.scss */
$primary-blue:   #1E90FF;
$dark-blue:      #0A3D62;
$medium-blue:    #1070CC;
$light-blue:     #EAF6FF;
$border-blue:    #D6EAFF;
$muted-blue:     #5B8FB9;
$text-dark:      #2C3E50;
$danger-red:     #e32d2d;
$danger-dark:    #be2424;
```

---

## Fichier : `static\scss\admin.scss`
Dossier : `.\static\scss`

```scss
@use 'variables' as *;
.admin-main { background: $light-blue; min-height: calc(100vh - 70px); padding: 50px 20px 70px; }
```

---

## Fichier : `static\scss\boutique.scss`
Dossier : `.\static\scss`

```scss
@use 'variables' as *;
.boutique-main { background: $light-blue; min-height: calc(100vh - 70px); padding: 50px 20px 70px; }
.btn-toggle-dispo { background: $light-blue; border: 1px solid $border-blue; color: $primary-blue; }
.btn-delete-produit { background: #FFF5F5; border: 1px solid #FCCACA; color: $danger-red; }
```

---

## Fichier : `static\scss\connexion.scss`
Dossier : `.\static\scss`

```scss
/* connexion.scss */
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
}
```

---

## Fichier : `static\scss\dashboard.scss`
Dossier : `.\static\scss`

```scss
/* dashboard.scss */
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
}
```

---

## Fichier : `static\scss\home.scss`
Dossier : `.\static\scss`

```scss
/* home.scss */

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
}
```

---

## Fichier : `static\scss\login.scss`
Dossier : `.\static\scss`

```scss

```

---

## Fichier : `static\scss\main.scss`
Dossier : `.\static\scss`

```scss
/* main.scss */

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
}

// Footer
footer {
  background: #0A3D62;
  color: #fff;
  padding: 30px 20px 24px;

  .footer-content {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;

    .footer-top {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .footer-brand {
        display: flex;
        flex-direction: column;
        gap: 6px;

        .brand-name {
          font-size: 1.3rem;
          font-weight: 800;
          letter-spacing: -0.3px;

          .brand-easy {
            color: #4EABFF;
          }
          .brand-market {
            color: #fff;
          }
        }

        .footer-tagline {
          font-size: 1rem;
          font-weight: 200;
          color: rgba(255, 255, 255, 0.45);
        }
      }
    }

    .footer-links {
      display: flex;
      align-items: center;
      gap: 10px;

      .footer-link {
        display: flex;
        align-items: center;
        gap: 7px;
        text-decoration: none;
        font-size: 0.7rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.7);
        transition: color 0.2s ease;
        &:hover {
          color: #fff;
        }
      }
    }
    
    .footer-bottom {
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      text-align: center;

      p {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
      }
    }

    .legal-link {
      display: inline-block;
      margin-top: 10px;
      text-decoration: none;
      font-size: 0.85rem;
      color: darken($primary-blue, 10%);
      &:hover {
        color: $primary-blue;
        text-decoration: underline;
      }
    }
  }
}
```

---

## Fichier : `static\scss\register.scss`
Dossier : `.\static\scss`

```scss

```

---

## Fichier : `static\scss\reservation.scss`
Dossier : `.\static\scss`

```scss
/* reservation.scss */
@use 'variables' as *;

/* ─── Page ──────────────────────────────────────────────── */
.reservation-main {
  background: $light-blue;
  min-height: calc(100vh - 70px);
  padding: 50px 20px 70px;
}

.reservation-container {
  max-width: 720px;
  margin: 0 auto;

  .page-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 36px;

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
}

/* ─── Layout avec nav latérale ───────────────────────────── */
.reservation-layout {
  display: flex;
  align-items: flex-start;
  gap: 28px;
  max-width: 1000px;
  margin: 0 auto;
}

.reservation-container {
  flex: 1;
  min-width: 0;
}

/* ─── Nav latérale ───────────────────────────────────────── */
.side-nav {
  width: 180px;
  flex-shrink: 0;
  position: sticky;
  top: 80px;
  background: #fff;
  border: 1px solid $border-blue;
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);

  .side-nav-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: $muted-blue;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid $border-blue;
  }

  .side-nav-link {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 10px;
    border-radius: 7px;
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 500;
    color: $text-dark;
    transition: background 0.2s ease, color 0.2s ease;
    margin-bottom: 4px;

    &:hover {
      background: $light-blue;
      color: $primary-blue;
    }

    &.active {
      background: $light-blue;
      color: $primary-blue;
      font-weight: 700;
    }
  }
}

/* ─── Badges nav latérale ────────────────────────────────── */
.side-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;

  &--blue {
    background: $light-blue;
    color: $primary-blue;
    border: 1px solid $border-blue;
  }

  &--orange {
    background: #FEF3E2;
    color: #E67E22;
    border: 1px solid #FDEBD0;
  }

  &--green {
    background: #E8F8F1;
    color: #27AE60;
    border: 1px solid #A9DFBF;
  }
}

/* ─── Liste ─────────────────────────────────────────────── */
.reservation-list {
  display: flex;
  flex-direction: column;
  gap: 20px;

  .section-count--blue {
    background: $light-blue;
    color: $primary-blue;
  }
}

/* ─── Card ──────────────────────────────────────────────── */
.reservation-card {
  background: #fff;
  border: 1px solid $border-blue;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);
  display: flex;
  flex-direction: column;
  gap: 20px;

  .reservation-card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;

    .card-label {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: $muted-blue;
      margin-bottom: 4px;
    }

    .client-name {
      font-size: 1.1rem;
      font-weight: 700;
      color: $dark-blue;
    }

    .client-contact {
      font-size: 0.88rem;
      color: $muted-blue;
      margin-top: 2px;
    }
  }
}

/* ─── Badge ─────────────────────────────────────────────── */
.badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  flex-shrink: 0;

  &.badge-new {
    background: #E8F8F1;
    color: #27AE60;
    border: 1px solid #A9DFBF;
  }
}

/* ─── Produits ──────────────────────────────────────────── */
.reservation-block {
  display: flex;
  flex-direction: column;
  gap: 10px;

  .block-title {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: $muted-blue;
  }

  .reservation-items {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;

    li {
      background: $light-blue;
      border: 1px solid $border-blue;
      border-radius: 6px;
      padding: 9px 12px;

      label {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.92rem;
        color: $text-dark;
        cursor: pointer;

        input[type="checkbox"] {
          width: 16px;
          height: 16px;
          accent-color: $primary-blue;
          cursor: pointer;
          flex-shrink: 0;
        }
      }
    }

    li:has(input:checked) {
      background: #E8F8F1;
      border-color: #A9DFBF;

      label {
        color: $muted-blue;
        text-decoration: line-through;
      }
    }
  }
}

/* ─── Action row ────────────────────────────────────────── */
.reservation-action-row {
  padding-top: 16px;
  border-top: 1px solid $border-blue;
  display: flex;
  flex-direction: column;
  gap: 10px;

  .amount-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: $muted-blue;
  }

  .amount-group {
    display: flex;
    gap: 10px;
    align-items: stretch;

    .amount-input-wrapper {
      display: flex;
      flex: 1;
      border: 1px solid $border-blue;
      border-radius: 8px;
      overflow: hidden;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;

      &:focus-within {
        border-color: $primary-blue;
        box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.1);
      }

      .amount-input {
        flex: 1;
        border: none;
        border-radius: 0;
        padding: 11px 14px;
        font-size: 1rem;
        font-weight: 600;
        color: $dark-blue;
        outline: none;
        box-shadow: none;

        &::placeholder {
          font-weight: 400;
          color: $muted-blue;
        }

        &:focus {
          border-color: transparent;
          box-shadow: none;
        }
      }

      .amount-select {
        border: none;
        border-left: 1px solid $border-blue;
        border-radius: 0;
        padding: 11px 10px;
        font-size: 0.88rem;
        font-weight: 700;
        color: $primary-blue;
        background: $light-blue;
        cursor: pointer;
        outline: none;
        appearance: none;
        width: 70px;
        text-align: center;
      }
    }

    .notify-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 11px 18px;
      white-space: nowrap;
      flex-shrink: 0;
    }
  }
}

/* ─── Sections prêts / servis ────────────────────────────── */
.reservation-section {
  margin-top: 48px;

  .section-heading {
    font-size: 1.2rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid $border-blue;
    display: flex;
    align-items: center;
    gap: 10px;

    &::after { display: none; }
  }

  .section-count {
    font-size: 0.8rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    background: #FEF3E2;
    color: #E67E22;
    border: 1px solid #FDEBD0;

    &--green {
      background: #E8F8F1;
      color: #27AE60;
      border-color: #A9DFBF;
    }
  }
}

.empty-state {
  font-size: 0.9rem;
  color: $muted-blue;
  font-style: italic;
  padding: 16px 0;
}

/* ─── Card prêt ─────────────────────────────────────────── */
.pret-card {
  background: #fff;
  border: 1px solid #FDEBD0;
  border-left: 4px solid #E67E22;
  border-radius: 10px;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(230, 126, 34, 0.06);
  margin-bottom: 12px;

  .pret-info {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .pret-client {
      font-size: 1rem;
      font-weight: 700;
      color: $dark-blue;
    }

    .pret-montant {
      font-size: 0.88rem;
      color: $muted-blue;
    }
  }

  .btn-servir {
    background: #E67E22;
    color: #fff;
    border: 2px solid #E67E22;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.88rem;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
    transition: all 0.2s ease;

    &:hover {
      background: #CA6F1E;
      border-color: #CA6F1E;
    }
  }
}

/* ─── Card servi ─────────────────────────────────────────── */
.servi-card {
  background: #fff;
  border: 1px solid #A9DFBF;
  border-left: 4px solid #27AE60;
  border-radius: 10px;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(39, 174, 96, 0.06);
  margin-bottom: 12px;

  .servi-info {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .servi-client {
      font-size: 1rem;
      font-weight: 700;
      color: $dark-blue;
    }

    .servi-montant {
      font-size: 0.88rem;
      color: $muted-blue;
    }
  }

  .btn-annuler-servi {
    background: transparent;
    color: $muted-blue;
    border: 1px solid $border-blue;
    padding: 8px 14px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.82rem;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
    transition: all 0.2s ease;

    &:hover {
      border-color: $danger-red;
      color: $danger-red;
    }
  }
}

/* ─── Commission summary ─────────────────────────────────── */
.commission-summary {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  background: #fff;
  border: 1px solid $border-blue;
  border-left: 4px solid $primary-blue;
  border-radius: 10px;
  padding: 14px 20px;
  margin-bottom: 32px;
  font-size: 0.88rem;
  color: $text-dark;
  box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);

  span { color: $muted-blue; }
  strong { color: $dark-blue; }
}

/* ─── Pret actions ───────────────────────────────────────── */
.pret-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;

  .btn-retire {
    background: #E8F8F1;
    border: 1px solid #A9DFBF;
    color: #27AE60;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s ease;

    &:hover { background: #27AE60; color: #fff; border-color: #27AE60; }
  }

  .btn-servir {
    background: $light-blue;
    border: 1px solid $border-blue;
    color: $muted-blue;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s ease;

    &:hover { background: $border-blue; color: $dark-blue; }
  }
}

/* ─── Badge retrait ──────────────────────────────────────── */
.servi-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.badge-retire {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;

  &.retire--oui {
    background: #E8F8F1;
    color: #27AE60;
    border: 1px solid #A9DFBF;
  }

  &.retire--non {
    background: #FFF5F5;
    color: $danger-red;
    border: 1px solid #FCCACA;
  }
}
```

---

## Fichier : `static\scss\reserver.scss`
Dossier : `.\static\scss`

```scss
/* reserver.scss */

@use 'variables' as *;

/* ─── Page ──────────────────────────────────────────────── */
.reserver-main {
  background: $light-blue;
  min-height: calc(100vh - 70px);
  padding: 50px 20px 70px;
}

.reserver-container {
  max-width: 600px;
  margin: 0 auto;

  .reserver-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 32px;
    padding-bottom: 10px;

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
}

/* ─── Formulaire ────────────────────────────────────────── */
.reserver-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  background: #fff;
  border: 1px solid $border-blue;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(30, 144, 255, 0.06);

  .form-section-title {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: $primary-blue;
    margin-bottom: 16px;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;

  & + .form-group {
    margin-top: 14px;
  }

  label {
    font-size: 0.9rem;
    font-weight: 600;
    color: $dark-blue;
  }
}

/* ─── Champs ────────────────────────────────────────────── */
.form-input {
  width: 100%;
  padding: 11px 14px;
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

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%231E90FF' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 36px;
  cursor: pointer;
}

/* ─── Produits ──────────────────────────────────────────── */
.produit-input-row {
  display: flex;
  flex-direction: column;
  gap: 10px;

  .input-row {
    display: flex;
    gap: 10px;

    .form-input {
      flex: 1;
    }

    .btn.primary {
      flex-shrink: 0;
      padding: 11px 18px;
    }
  }
}

.produits-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;

  .produit-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: $light-blue;
    border: 1px solid $border-blue;
    border-radius: 7px;
    padding: 10px 14px;
    font-size: 0.9rem;
    color: $text-dark;

    .produit-remove {
      background: none;
      border: none;
      cursor: pointer;
      color: $muted-blue;
      font-size: 1rem;
      line-height: 1;
      padding: 0 2px;
      transition: color 0.2s ease;

      &:hover {
        color: $dark-blue;
      }
    }
  }
}

.produit-input-row {
}

/* ─── Bouton Envoyer ────────────────────────────────────── */
.form-submit {
  .btn.primary {
    width: 100%;
    padding: 12px;
    font-size: 1rem;
    text-align: center;
  }
}

.error-msg {
  font-size: 0.8rem;
  color: #fff;
  background: $danger-red;
  padding: 6px 10px;
  border-radius: 6px;
  margin-top: 4px;
}

/* ─── Modal confirmation ─────────────────────────────────── */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(10, 61, 98, 0.45);
  z-index: 200;
  align-items: center;
  justify-content: center;

  &.active {
    display: flex;
  }
}

.modal {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  width: 100%;
  max-width: 480px;
  margin: 20px;
  box-shadow: 0 16px 48px rgba(30, 144, 255, 0.15);

  .modal-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 24px;
    padding-bottom: 10px;
    border-bottom: 2px solid $border-blue;
  }

  #modal-boutique {
    font-size: 1.3rem;
    font-weight: 700;
    color: $dark-blue;
    margin-bottom: 5px;
  }

  .modal-section.modal-indispo {
    .modal-indispo-title {
      color: $danger-red;
    }

    .modal-produits li {
      background: #FDDEDE !important;
      border-color: #FCCACA !important;
      color: $danger-red !important;
    }
  }

  .modal-section {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 16px;

    .modal-label {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: $muted-blue;
    }

    .modal-value {
      font-size: 0.95rem;
      color: $text-dark;
      font-weight: 500;
    }

    .modal-produits {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: 4px;

      li {
        background: $light-blue;
        border: 1px solid $border-blue;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 0.9rem;
        color: $text-dark;
      }
    }
  }

  .modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid $border-blue;

    .btn {
      flex: 1;
      text-align: center;
      padding: 11px;
    }
  }
}
```

---

## Fichier : `templates\404.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}

{% block title %}EasyMarket - Page introuvable{% endblock %}

{% block content %}
<main style="min-height:60vh; display:flex; align-items:center; justify-content:center; text-align:center; padding:40px 20px;">
  <div>
    <h1 style="font-size:2.5rem; color:#0A3D62; margin-bottom:12px;">404</h1>
    <p style="color:#5B8FB9; margin-bottom:24px;">Cette page n'existe pas ou plus.</p>
    <a href="{{ url_for('main.home') }}" class="btn primary" style="text-decoration:none; display:inline-block; padding:10px 24px;">Retour à l'accueil</a>
  </div>
</main>
{% endblock %}
```

---

## Fichier : `templates\admin.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}

{% block title %}EasyMarket - Administration{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/admin.css') }}">
{% endblock %}

{% block content %}
<main class="admin-main">
  <div class="admin-layout">

    <aside class="side-nav">
      <p class="side-nav-title">Administration</p>
      <a href="#section-overview" class="side-nav-link active">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
        Vue d'ensemble
      </a>
      <a href="#section-vendeurs" class="side-nav-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path d="M3 9l2.5-5h13L21 9"/><line x1="12" y1="9" x2="12" y2="21"/></svg>
        Vendeurs
      </a>
      <a href="#section-clients" class="side-nav-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
        Clients
      </a>
      <a href="#section-historique" class="side-nav-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
        Historique
      </a>
      <a href="#section-commission" class="side-nav-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
        Commissions
      </a>
    </aside>

    <div class="admin-container">
      <h1 class="page-title">Panneau d'administration</h1>

      <!-- A) Vue d'ensemble -->
      <section class="admin-section" id="section-overview">
        <h2 class="section-heading">Vue d'ensemble</h2>

        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-icon kpi-icon--blue">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path d="M3 9l2.5-5h13L21 9"/></svg>
            </div>
            <div class="kpi-info">
              <p class="kpi-label">Vendeurs actifs</p>
              <p class="kpi-value">{{ vendeurs_actifs|default(0) }}</p>
              <p class="kpi-sub">{{ vendeurs_attente|default(0) }} en attente de confirmation</p>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon kpi-icon--green">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
            </div>
            <div class="kpi-info">
              <p class="kpi-label">Clients total</p>
              <p class="kpi-value">{{ clients_total|default(0) }}</p>
              <p class="kpi-sub">{{ clients_nouveaux_mois|default(0) }} nouveaux ce mois</p>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon kpi-icon--orange">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            </div>
            <div class="kpi-info">
              <p class="kpi-label">Réservations ce mois</p>
              <p class="kpi-value">{{ reservations_mois|default(0) }}</p>
              <p class="kpi-sub">{{ reservations_evolution|default('—') }}</p>
            </div>
          </div>

          <div class="kpi-card kpi-card--danger">
            <div class="kpi-icon kpi-icon--red">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
            </div>
            <div class="kpi-info">
              <p class="kpi-label">Commission du mois</p>
              <p class="kpi-value">{{ commission_mois|default(0) }} <span class="kpi-unit">CDF</span></p>
              <p class="kpi-sub">Forfait · {{ vendeurs_actifs|default(0) }} vendeurs actifs</p>
            </div>
          </div>
        </div>
      </section>

      <!-- B) Vendeurs -->
      <section class="admin-section" id="section-vendeurs">
        <h2 class="section-heading">Vendeurs</h2>

        <div class="admin-actions">
          <button class="btn primary" id="btn-gen-code">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>
            Générer un code d'accès
          </button>
        </div>

        <div class="vendeurs-list" id="vendeurs-list">
          {% for v in vendeurs %}
          <div class="vendeur-card" data-statut="{{ v.statut }}" data-id="{{ v.id }}" tabindex="0">
            <div class="vendeur-info">
              <div class="vendeur-avatar">{{ v.initiales }}</div>
              <div>
                <p class="vendeur-nom">{{ v.nom }}</p>
                <p class="vendeur-contact">{{ v.contact }}</p>
                <p class="vendeur-meta">
                  {% if v.statut == 'actif' %}
                    CA déclaré : {{ v.ca_declare }} CDF · {{ v.nb_produits }} produits · {{ v.nb_clients }} clients
                  {% elif v.statut == 'attente' %}
                    En attente de confirmation
                  {% elif v.statut == 'suspendu' %}
                    Suspendu le {{ v.date_suspension }}
                  {% endif %}
                </p>
              </div>
            </div>
            <div class="vendeur-right">
              <span class="badge-statut statut--{{ v.statut }}">
                {% if v.statut == 'actif' %}Actif
                {% elif v.statut == 'attente' %}En attente
                {% elif v.statut == 'suspendu' %}Suspendu
                {% endif %}
              </span>
              <div class="vendeur-actions">
                {% if v.statut == 'actif' %}
                  <button class="action-btn action-btn--warn" title="Avertir">⚠</button>
                  <button class="action-btn action-btn--suspend" title="Suspendre">⏸</button>
                  <button class="action-btn action-btn--delete" title="Supprimer">✕</button>
                {% elif v.statut == 'attente' %}
                  <button class="action-btn action-btn--confirm" title="Confirmer">✓</button>
                  <button class="action-btn action-btn--delete" title="Rejeter">✕</button>
                {% elif v.statut == 'suspendu' %}
                  <button class="action-btn action-btn--confirm" title="Réactiver">↺</button>
                  <button class="action-btn action-btn--delete" title="Supprimer">✕</button>
                {% endif %}
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </section>

      <!-- C) Clients -->
      <section class="admin-section" id="section-clients">
        <h2 class="section-heading">Clients</h2>

        <div class="clients-filtres" id="clients-filtres">
          <button class="filtre-btn active">Tous</button>
          <button class="filtre-btn">Nouveaux</button>
          <button class="filtre-btn">Habitués</button>
        </div>

        <div class="admin-clients-list">
          {% for c in clients %}
          <div class="admin-client-card">
            <div class="client-info">
              <div class="client-avatar">{{ c.initiales }}</div>
              <div>
                <p class="client-name">{{ c.nom }}</p>
                <p class="client-whatsapp">{{ c.whatsapp }}</p>
              </div>
            </div>
            <div class="client-stats">
              <div class="client-stat-item">
                <span class="stat-label">Réservations</span>
                <span class="stat-value">{{ c.nb_reservations }}</span>
              </div>
              <div class="client-stat-item">
                <span class="stat-label">Boutiques</span>
                <span class="stat-value">{{ c.nb_boutiques }}</span>
              </div>
              <div class="client-stat-item">
                <span class="stat-label">Dernière activité</span>
                <span class="stat-value">{{ c.derniere_activite }}</span>
              </div>
            </div>
            <span class="badge {{ 'badge-new' if c.nouveau else 'badge-old' }}">
              {{ 'Nouveau' if c.nouveau else 'Habitué' }}
            </span>
          </div>
          {% endfor %}
        </div>
      </section>

      <!-- D) Historique -->
      <section class="admin-section" id="section-historique">
        <h2 class="section-heading">Historique mensuel</h2>

        <table class="historique-table">
          <thead>
            <tr>
              <th>Mois</th>
              <th>Vendeurs actifs</th>
              <th>Réservations</th>
              <th>CA déclaré (CDF)</th>
              <th>Commission (CDF)</th>
              <th>Incidents</th>
            </tr>
          </thead>
          <tbody>
            {% for m in historique_mensuel %}
            <tr>
              <td>{{ m.mois }}</td>
              <td>{{ m.vendeurs_actifs }}</td>
              <td>{{ m.reservations }}</td>
              <td>{{ m.ca_declare }}</td>
              <td>{{ m.commission }}</td>
              <td>{{ m.incidents }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </section>

      <section class="admin-section" id="section-commission">
        <h2 class="section-heading">Commissions & Retraits</h2>
        <div id="commission-admin"></div>
      </section>

    </div>
  </div>
</main>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/admin.js') }}"></script>
{% endblock %}
```

---

## Fichier : `templates\base.html`
Dossier : `.\templates`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}EasyMarket{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
  {% block extra_css %}{% endblock %}
</head>
<body>

  <!-- HEADER / NAV -->
  <header>
    <nav class="navbar">
      <div class="navbar-inner">
        <a href="{{ url_for('main.home') }}" class="navbar-brand">
          <svg class="logo" width="30" height="40" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M32 38 C32 20 68 20 68 38" stroke="#1E90FF" stroke-width="9" stroke-linecap="round" fill="none"/>
            <path d="M14 42 Q12 42 11 48 L6 88 Q5 98 15 100 L85 100 Q95 98 94 88 L89 48 Q88 42 86 42 Z" fill="#EAF6FF" stroke="#1E90FF" stroke-width="9" stroke-linejoin="round"/>
            <line x1="32" y1="42" x2="32" y2="54" stroke="#1E90FF" stroke-width="9" stroke-linecap="round"/>
            <line x1="68" y1="42" x2="68" y2="54" stroke="#1E90FF" stroke-width="9" stroke-linecap="round"/>
            <polyline points="30,72 44,86 70,60" stroke="#0A3D62" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
          </svg>
          <span class="brand-name">
            <span class="brand-easy">Easy</span><span class="brand-market">Market</span>
          </span>
        </a>

        <div class="navbar-actions">
          {% block navbar_actions %}
          <button class="btn primary" onclick="location.href='{{ url_for('main.reserver') }}'">Réserver</button>
          <a class="btn secondary vendor-btn" href="{{ url_for('auth.inscription') }}">Devenir Vendeur</a>
          {% if not session.role %}
          <button class="btn secondary" onclick="location.href='{{ url_for('auth.connexion') }}'">Connexion</button>
          {% endif %}
          {% endblock %}

          <!-- Menu burger -->
          <div class="burger-menu">
            <input type="checkbox" id="menu-toggle">
            <label for="menu-toggle" class="menu-icon" aria-label="Menu">
              <span></span>
              <span></span>
              <span></span>
            </label>
            <div class="menu-content">
              {% block menu_profile %}
              {% if session.role == 'vendeur' %}
              <div class="menu-profile">
                <div class="menu-profile-avatar">{{ session.vendeur_initiales }}</div>
                <div class="menu-profile-info">
                  <p class="name">{{ session.vendeur_nom }}</p>
                  <p class="status">Vendeur</p>
                </div>
              </div>
              <div class="menu-divider"></div>
              {% elif session.role == 'admin' %}
              <div class="menu-profile">
                <div class="menu-profile-avatar">AD</div>
                <div class="menu-profile-info">
                  <p class="name">Administrateur</p>
                  <p class="status">Admin</p>
                </div>
              </div>
              <div class="menu-divider"></div>
              {% endif %}
              {% endblock %}

              <a href="{{ url_for('main.home') }}" class="menu-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E90FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                Accueil
              </a>

              {% if session.role == 'vendeur' %}
              <a href="{{ url_for('vendeur.boutique') }}" class="menu-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E90FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path d="M3 9l2.5-5h13L21 9"/><line x1="12" y1="9" x2="12" y2="21"/></svg>
                Boutique
              </a>
              <a href="{{ url_for('vendeur.reservation') }}" class="menu-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E90FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                Réservation
              </a>
              <a href="{{ url_for('vendeur.dashboard') }}" class="menu-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E90FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
                Tableau de bord
              </a>
              {% endif %}

              {% if session.role == 'admin' %}
              <a href="{{ url_for('admin.dashboard') }}" class="menu-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E90FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
                Administration
              </a>
              {% endif %}

              <a href="{{ url_for('main.home') }}#about" class="menu-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E90FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                À propos
              </a>
              <a href="{{ url_for('main.home') }}#contact" class="menu-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E90FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                Aide
              </a>

              {% block menu_extra_links %}{% endblock %}

              <div class="menu-divider"></div>
              {% block menu_logout %}
              {% if session.role %}
              <form action="{{ url_for('auth.logout') }}" method="post" style="margin:0;">
                <button type="submit" class="btn danger">Déconnexion</button>
              </form>
              {% endif %}
              {% endblock %}
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <!-- MAIN -->
  {% block content %}{% endblock %}

  <!-- FOOTER -->
  <footer>
    <div class="footer-content">
      <div class="footer-top">
        <div class="footer-brand">
          <span class="brand-name">
            <span class="brand-easy">Easy</span><span class="brand-market">Market |</span>
            <span class="footer-tagline">Le marché facile — pour tous !</span>
          </span>
        </div>
        <div class="footer-links">
          <a href="https://wa.me/VOTRE_NUMERO" class="footer-link" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="#25D366" aria-hidden="true"><path d="M20.52 3.48A11.93 11.93 0 0012 0C5.37 0 0 5.37 0 12c0 2.11.55 4.16 1.6 5.97L0 24l6.18-1.57A11.94 11.94 0 0012 24c6.63 0 12-5.37 12-12 0-3.2-1.25-6.21-3.48-8.52zM12 22c-1.85 0-3.66-.5-5.23-1.43l-.37-.22-3.87.98.99-3.76-.24-.38A9.94 9.94 0 012 12C2 6.48 6.48 2 12 2c2.67 0 5.18 1.04 7.07 2.93A9.94 9.94 0 0122 12c0 5.52-4.48 10-10 10zm5.44-7.3c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.79-1.68-2.09-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.6-.91-2.2-.24-.58-.48-.5-.67-.51H6.9c-.2 0-.52.07-.79.37C5.84 8.2 5.1 8.9 5.1 10.35s1.05 2.87 1.2 3.07c.15.2 2.07 3.16 5.01 4.43.7.3 1.25.48 1.67.62.7.22 1.34.19 1.84.12.56-.08 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 EasyMarket. Tous droits réservés.</p>
        <a href="#" class="footer-link legal-link">Mentions légales</a>
      </div>
    </div>
  </footer>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  {% block extra_js %}{% endblock %}

</body>
</html>
```

---

## Fichier : `templates\boutique.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}

{% block title %}EasyMarket - Boutique{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/boutique.css') }}">
{% endblock %}

{% block content %}
<main class="boutique-main">
  <div class="boutique-layout">

    <aside class="side-nav">
      <p class="side-nav-title">Mon espace</p>
      <a href="#section-boutique" class="side-nav-link active">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path d="M3 9l2.5-5h13L21 9"/><line x1="12" y1="9" x2="12" y2="21"/></svg>
        Boutique
      </a>
      <a href="#section-produits" class="side-nav-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
        Produits
      </a>
      <a href="#section-clients" class="side-nav-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
        Clients
      </a>
    </aside>

    <div class="boutique-container">
      <h1 class="page-title">Mon espace boutique</h1>

      <!-- A) Boutique -->
      <section class="boutique-section" id="section-boutique">
        <h2 class="section-heading">Boutique</h2>

        <form class="boutique-form" id="form-boutique" method="post" action="{{ url_for('vendeur.update_boutique') }}" novalidate>
          <div class="form-grid">

            <div class="form-group">
              <label for="boutique-nom">Nom de la boutique</label>
              <input type="text" id="boutique-nom" name="boutique_nom" class="form-input" placeholder="Ex : Marché Frais" value="{{ boutique.nom|default('') }}">
            </div>

            <div class="form-group">
              <label for="vendeur-nom">Nom du vendeur</label>
              <input type="text" id="vendeur-nom" name="vendeur_nom" class="form-input" placeholder="Ex : Jean Dupont" value="{{ session.vendeur_nom or '' }}">
            </div>

            <div class="form-group">
              <label for="boutique-adresse">Adresse</label>
              <input type="text" id="boutique-adresse" name="adresse" class="form-input" placeholder="Ex : Avenue du Commerce, N°12" value="{{ boutique.adresse|default('') }}">
            </div>

            <div class="form-group">
              <label for="boutique-email">Email</label>
              <input type="email" id="boutique-email" name="email" class="form-input" placeholder="Ex : contact@boutique.com" value="{{ boutique.email|default('') }}">
            </div>

            <div class="form-group">
              <label for="boutique-whatsapp">Numéro WhatsApp</label>
              <input type="tel" id="boutique-whatsapp" name="whatsapp" class="form-input" placeholder="Ex : +243 81 234 5678" value="{{ boutique.whatsapp|default('') }}">
            </div>

            <div class="form-group">
              <label for="boutique-categorie">Catégorie</label>
              <input type="text" id="boutique-categorie" name="categorie" class="form-input" placeholder="Ex : Épicerie générale" value="{{ boutique.categorie_principale|default('') }}">
            </div>

            <div class="form-group form-group--full">
              <label>Horaires d'ouverture</label>
              <div class="horaires-grid">
                <div class="horaire-row">
                  <span class="horaire-label">Ouverture</span>
                  <input type="time" id="heure-ouverture" name="heure_ouverture" class="form-input horaire-input" value="{{ boutique.heure_ouverture|default('07:00') }}">
                </div>
                <div class="horaire-row">
                  <span class="horaire-label">Fermeture</span>
                  <input type="time" id="heure-fermeture" name="heure_fermeture" class="form-input horaire-input" value="{{ boutique.heure_fermeture|default('20:00') }}">
                </div>
              </div>
            </div>

            <div class="form-group form-group--full">
              <label>Jours d'ouverture</label>
              <div class="jours-grid">
                {% set jours_ouverts = boutique.jours_ouverture|default(['lun','mar','mer','jeu','ven','sam']) %}
                <label class="jour-label"><input type="checkbox" name="jours" value="lun" {{ 'checked' if 'lun' in jours_ouverts }}> Lun</label>
                <label class="jour-label"><input type="checkbox" name="jours" value="mar" {{ 'checked' if 'mar' in jours_ouverts }}> Mar</label>
                <label class="jour-label"><input type="checkbox" name="jours" value="mer" {{ 'checked' if 'mer' in jours_ouverts }}> Mer</label>
                <label class="jour-label"><input type="checkbox" name="jours" value="jeu" {{ 'checked' if 'jeu' in jours_ouverts }}> Jeu</label>
                <label class="jour-label"><input type="checkbox" name="jours" value="ven" {{ 'checked' if 'ven' in jours_ouverts }}> Ven</label>
                <label class="jour-label"><input type="checkbox" name="jours" value="sam" {{ 'checked' if 'sam' in jours_ouverts }}> Sam</label>
                <label class="jour-label"><input type="checkbox" name="jours" value="dim" {{ 'checked' if 'dim' in jours_ouverts }}> Dim</label>
              </div>
            </div>

            <div class="form-group form-group--full">
              <label for="boutique-desc">Description</label>
              <textarea id="boutique-desc" name="description" class="form-input" rows="3" placeholder="Décrivez votre boutique en quelques mots...">{{ boutique.description|default('') }}</textarea>
            </div>

          </div>

          <div class="form-submit">
            <button type="submit" class="btn primary">Enregistrer</button>
          </div>
        </form>
      </section>

      <!-- B) Produits -->
      <section class="boutique-section" id="section-produits">
        <h2 class="section-heading">Produits</h2>

        <div class="produits-actions">
          <button class="btn primary" id="btn-add-produit" type="button">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Ajouter un produit
          </button>
          <button class="btn secondary" id="btn-add-categorie" type="button">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Ajouter une catégorie
          </button>
        </div>

        <form method="post" action="{{ url_for('vendeur.ajouter_produit') }}" class="inline-form" style="margin-top: 16px; display: none;" id="form-add-produit">
          <input type="text" name="nom" class="form-input" placeholder="Nom du produit" required>
          <input type="text" name="prix" class="form-input" placeholder="Prix" required>
          <input type="text" name="autres" class="form-input" placeholder="Détails" >
          <select name="devise" class="form-input">
            <option value="CDF">CDF</option>
            <option value="USD">USD</option>
          </select>
          <button type="submit" class="btn primary">Valider</button>
        </form>

        <form method="post" action="{{ url_for('vendeur.ajouter_categorie') }}" class="inline-form" style="margin-top: 16px; display: none;" id="form-add-categorie">
          <input type="text" name="nom" class="form-input" placeholder="Nom de la catégorie" required>
          <button type="submit" class="btn secondary">Ajouter</button>
        </form>

        <!-- Catégories -->
        <div class="produits-block">
          <h3 class="produits-block-title">Par catégorie</h3>
          <div class="categories-list" id="categories-list">
            {% if categories %}
              {% for categorie in categories %}
                <span class="badge category-badge">{{ categorie.nom }}</span>
              {% endfor %}
            {% else %}
              <p class="empty-state">Aucune catégorie ajoutée.</p>
            {% endif %}
          </div>
        </div>

        <!-- Tous les produits -->
        <div class="produits-block">
          <h3 class="produits-block-title">Tous les produits</h3>
          <div class="produits-filtres" id="produits-filtres"></div>
          <div class="produits-list" id="produits-list">
            {% if produits %}
              {% for produit in produits %}
                <div class="produit-item">
                  <strong>{{ produit.nom }}</strong>
                  <span>{{ produit.prix }} {{ produit.devise }}</span>
                  {% if produit.autres %}<small>{{ produit.autres }}</small>{% endif %}
                </div>
              {% endfor %}
            {% else %}
              <p class="empty-state">Aucun produit ajouté.</p>
            {% endif %}
          </div>
        </div>

      </section>

      <!-- C) Clients -->
      <section class="boutique-section" id="section-clients">
        <h2 class="section-heading">Clients</h2>

        <div class="clients-list" id="clients-list">
          {% for c in clients %}
          <div class="client-card">
            <div class="client-info">
              <div class="client-avatar">{{ c.initiales }}</div>
              <div>
                <p class="client-name">{{ c.nom }}</p>
                <p class="client-whatsapp">{{ c.whatsapp }}</p>
              </div>
            </div>
            <div class="client-meta">
              <span class="badge {{ 'badge-new' if c.nouveau else 'badge-old' }}">
                {{ 'Nouveau' if c.nouveau else 'Habitué' }}
              </span>
              <p class="client-stat">{{ c.nb_reservations }} réservation{{ 's' if c.nb_reservations != 1 else '' }}</p>
              <p class="client-date">Dernière : {{ c.derniere_reservation }}</p>
            </div>
          </div>
          {% endfor %}
        </div>
      </section>

    </div>
  </div>
</main>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/boutique.js') }}"></script>
{% endblock %}
```

---

## Fichier : `templates\boutique_publique.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}
{% block title %}{{ boutique.nom }} - Vitrine Officielle{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/boutique.css') }}">
{% endblock %}

{% block content %}
<div class="public-store-header">
    <h1>{{ boutique.nom }}</h1>
    <p>{{ boutique.description }}</p>
</div>

<div class="public-store-container">
    <form id="form-reservation-publique" action="{{ url_for('main.traitement_reservation', boutique_id=boutique.id) }}" method="POST">
        <h3>Catalogue des articles</h3>
        <div class="grid-produits">
            {% for p in produits %}
            <div class="card-produit">
                <input type="checkbox" name="produits_ids" value="{{ p.id }}" id="p-{{ p.id }}" data-nom="{{ p.nom }}" data-prix="{{ p.prix }} {{ p.devise }}">
                <label for="p-{{ p.id }}">
                    <strong>{{ p.nom }}</strong>
                    <span>{{ p.prix }} {{ p.devise }}</span>
                </label>
            </div>
            {% else %}
            <p>Aucun produit disponible pour le moment.</p>
            {% endfor %}
        </div>

        <div class="client-info-section">
            <h3>Vos informations de réservation</h3>
            <input type="text" id="nom_client" name="nom_client" placeholder="Votre nom complet" required>
            <input type="text" id="whatsapp_client" name="whatsapp_client" placeholder="Votre numéro WhatsApp" required>
            <button type="submit" class="btn-primary">Valider la réservation</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/boutique.js') }}"></script>
{% endblock %}
```

---

## Fichier : `templates\boutique_vendeur.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}
{% block title %}Gestion Boutique - Vendeur{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/boutique.css') }}">
{% endblock %}

{% block content %}
<div class="vendeur-boutique-container">
    <h1>Gestion de mon catalogue</h1>
    {% if boutique %}
        <h3>Lien public de votre boutique : 
            <a href="{{ url_for('main.boutique_publique', boutique_id=boutique.id) }}" target="_blank">
                {{ request.host_url }}b/{{ boutique.id }}
            </a>
        </h3>

        <table style="width:100%; border-collapse: collapse; margin-top: 20px;">
            <thead style="background:#0A3D62; color:white;">
                <tr>
                    <th style="padding:12px;">Nom</th>
                    <th style="padding:12px;">Prix</th>
                    <th style="padding:12px;">Statut</th>
                    <th style="padding:12px;">Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for p in boutique.produits %}
                <tr style="border-bottom:1px solid #D6EAFF;">
                    <td style="padding:12px;">{{ p.nom }}</td>
                    <td style="padding:12px;">{{ p.prix }} {{ p.devise }}</td>
                    <td style="padding:12px;">{{ "Disponible" if p.disponible else "Masqué" }}</td>
                    <td style="padding:12px;">
                        <form action="{{ url_for('vendeur.toggle_produit', produit_id=p.id) }}" method="POST" style="display:inline;">
                            <button type="submit" style="padding:6px 12px; background:#1E90FF; color:white; border:none; border-radius:4px; cursor:pointer;">
                                {{ "Masquer" if p.disponible else "Afficher" }}
                            </button>
                        </form>
                        <form action="{{ url_for('vendeur.delete_produit', produit_id=p.id) }}" method="POST" style="display:inline; margin-left:8px;">
                            <button type="submit" style="padding:6px 12px; background:#e32d2d; color:white; border:none; border-radius:4px; cursor:pointer;">Supprimer</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Vous n'avez pas encore configuré de boutique.</p>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/boutique.js') }}"></script>
{% endblock %}
```

---

## Fichier : `templates\connexion.html`
Dossier : `.\templates`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EasyMarket - Connexion</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/connexion.css') }}">
</head>
<body>

  <div class="auth-page">

    <!-- Logo -->
    <a href="{{ url_for('main.home') }}" class="auth-brand">
      <svg width="34" height="34" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M32 38 C32 20 68 20 68 38" stroke="#1E90FF" stroke-width="9" stroke-linecap="round" fill="none"/>
        <path d="M14 42 Q12 42 11 48 L6 88 Q5 98 15 100 L85 100 Q95 98 94 88 L89 48 Q88 42 86 42 Z" fill="#EAF6FF" stroke="#1E90FF" stroke-width="9" stroke-linejoin="round"/>
        <line x1="32" y1="42" x2="32" y2="54" stroke="#1E90FF" stroke-width="9" stroke-linecap="round"/>
        <line x1="68" y1="42" x2="68" y2="54" stroke="#1E90FF" stroke-width="9" stroke-linecap="round"/>
        <polyline points="30,72 44,86 70,60" stroke="#0A3D62" stroke-width="8.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </svg>
      <span class="brand-name">
        <span class="brand-easy">Easy</span><span class="brand-market">Market</span>
      </span>
    </a>

    <!-- Card auth -->
    <div class="auth-card">

      <h1 class="auth-context-title">Espace vendeur</h1>

      <!-- Tabs -->
      <div class="auth-tabs">
        <button class="auth-tab active" data-tab="login">Connexion</button>
        <button class="auth-tab" data-tab="register">Inscription</button>
      </div>

      <!-- Formulaire Connexion -->
      <form class="auth-form active" id="form-login" method="post" action="{{ url_for('auth.login') }}" novalidate>
        <div class="form-group">
          <label for="login-whatsapp">Numéro WhatsApp</label>
          <input type="tel" id="login-whatsapp" name="whatsapp" class="form-input" placeholder="Ex : +243 81 234 5678">
        </div>

        <div class="form-group">
          <label for="login-code">Code d'accès</label>
          <input type="password" id="login-code" name="code" class="form-input" placeholder="Ex : EM-XXXXXX">
        </div>

        <button type="submit" class="btn primary auth-submit">Se connecter</button>

        <p class="auth-switch">
          Pas encore de compte vendeur ?
          <button type="button" class="auth-switch-link" data-tab="register">S'inscrire</button>
        </p>
      </form>

      <!-- Formulaire Inscription -->
      <form class="auth-form" id="form-register" method="post" action="{{ url_for('auth.register') }}" novalidate>
        <div class="form-group">
          <label for="register-boutique">Nom de la boutique</label>
          <input type="text" id="register-boutique" name="boutique" class="form-input" placeholder="Ex : Marché Frais">
        </div>

        <div class="form-group">
          <label for="register-nom">Nom du vendeur</label>
          <input type="text" id="register-nom" name="nom" class="form-input" placeholder="Ex : Jean Dupont">
        </div>

        <div class="form-group">
          <label for="register-whatsapp">Numéro WhatsApp</label>
          <input type="tel" id="register-whatsapp" name="whatsapp" class="form-input" placeholder="Ex : +243 81 234 5678">
        </div>

        <div class="form-group">
          <label for="register-email">Email</label>
          <input type="email" id="register-email" name="email" class="form-input" placeholder="Ex : contact@boutique.com">
        </div>

        <div class="form-group">
          <label for="register-code">Code d'accès reçu</label>
          <input type="text" id="register-code" name="code" class="form-input" placeholder="Ex : EM-XXXXXX">
          <p class="form-hint">Ce code vous a été transmis par l'équipe EasyMarket après validation.</p>
        </div>

        <button type="submit" class="btn primary auth-submit">Créer mon compte</button>

        <p class="auth-switch">
          Déjà inscrit ?
          <button type="button" class="auth-switch-link" data-tab="login">Se connecter</button>
        </p>
      </form>

    </div>

    <p class="auth-footer-note">
      En continuant, vous acceptez les
      <a href="#">conditions d'utilisation</a> d'EasyMarket.
    </p>

  </div>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  <script src="{{ url_for('static', filename='js/connexion.js') }}"></script>
</body>
</html>
```

---

## Fichier : `templates\dashboard.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}

{% block title %}EasyMarket - Tableau de bord{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
{% endblock %}

{% block content %}
<main class="dashboard-main">
  <div class="dashboard-container">

    <h1 class="page-title">Tableau de bord</h1>

    <div class="dashboard-shortcuts">
      <a href="{{ url_for('vendeur.reservation') }}" class="shortcut-card">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        <span>Réservations</span>
      </a>
      <a href="{{ url_for('vendeur.boutique') }}" class="shortcut-card">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18v10a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path d="M3 9l2.5-5h13L21 9"/><line x1="12" y1="9" x2="12" y2="21"/></svg>
        <span>Ma boutique</span>
      </a>
    </div>

    <div class="taux-row">
      <label for="taux-change">Taux de change :</label>
      <span>1 USD =</span>
      <input type="number" id="taux-change" class="taux-input" value="{{ taux_change|default(2250) }}">
      <span>CDF</span>
    </div>

    <div class="kpi-grid">

      <div class="kpi-card">
        <div class="kpi-icon kpi-icon--blue">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
        </div>
        <div class="kpi-info">
          <p class="kpi-label">Chiffre d'affaires</p>
          <p class="kpi-value" id="ca-cdf">{{ ca_cdf|default(0) }} <span class="kpi-unit">CDF</span></p>
          <p class="kpi-value kpi-value--small" id="ca-usd"></p>
        </div>
      </div>

      <div class="kpi-card kpi-card--danger">
        <div class="kpi-icon kpi-icon--red">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
        </div>
        <div class="kpi-info">
          <p class="kpi-label">Commission EasyMarket (10%)</p>
          <p class="kpi-value" id="commission-cdf"></p>
          <p class="kpi-value kpi-value--small" id="commission-usd"></p>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon kpi-icon--orange">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <div class="kpi-info">
          <p class="kpi-label">Réservations aujourd'hui</p>
          <p class="kpi-value">{{ reservations_jour|default(0) }}</p>
          <p class="kpi-sub">{{ reservations_attente|default(0) }} en attente · {{ reservations_traitees|default(0) }} traitées</p>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon kpi-icon--green">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
        </div>
        <div class="kpi-info">
          <p class="kpi-label">Produits</p>
          <p class="kpi-value">{{ produits_total|default(0) }}</p>
          <p class="kpi-sub">{{ produits_indisponibles|default(0) }} indisponibles</p>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon kpi-icon--purple">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
        </div>
        <div class="kpi-info">
          <p class="kpi-label">Clients</p>
          <p class="kpi-value">{{ clients_total|default(0) }}</p>
          <p class="kpi-sub">{{ clients_nouveaux|default(0) }} nouveaux aujourd'hui</p>
        </div>
      </div>

    </div>

    <section class="historique-section">
      <h2 class="section-heading">Historique récent</h2>

      <table class="historique-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Réservations</th>
            <th>CA (CDF)</th>
            <th>CA (USD)</th>
            <th>Nouveaux clients</th>
          </tr>
        </thead>
        <tbody>
          {% for jour in historique %}
          <tr>
            <td>{{ jour.date }}</td>
            <td>{{ jour.reservations }}</td>
            <td>{{ jour.ca_cdf }}</td>
            <td>{{ jour.ca_usd }}</td>
            <td>{{ jour.nouveaux_clients }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </section>

  </div>
</main>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
{% endblock %}
```

---

## Fichier : `templates\home.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}

{% block title %}EasyMarket - Accueil{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/home.css') }}">
{% endblock %}

{% block content %}
<main>
  <section class="hero">
    <div class="hero-brand">
      <span class="hero-logo-name">
        <span class="brand-easy">Easy</span><span class="brand-market">Market</span>
      </span>
      <div class="hero-actions">
        <button class="btn primary" onclick="location.href='{{ url_for('main.reserver') }}'">Réserver</button>
      </div>
    </div>

    <div class="hero-pitch">
      <p class="hero-tagline">Réservez vos produits en avance, évitez l'attente et profitez d'une expérience d'achat sereine. Pour les vendeurs, c'est plus d'organisation, moins de stress et une clientèle fidélisée.</p>
      <p class="hero-slogan">Votre temps a de la valeur — on le respecte.</p>
    </div>
  </section>

  <section class="boutiques" id="boutiques">
    <h2 class="section-title">Boutiques</h2>

    <div class="boutiques-grid">
      {% for boutique in boutiques %}
      <div class="boutique-card">
        <div class="boutique-info">
          <h3 class="boutique-name">{{ boutique.nom }}</h3>
          <span class="boutique-category">{{ boutique.categorie_principale or boutique.categorie or 'Boutique' }}</span>
          <p class="boutique-desc">{{ boutique.description or 'Boutique active sur EasyMarket.' }}</p>
        </div>
        <button class="btn primary" onclick="location.href='{{ url_for('main.reserver') }}?boutique={{ boutique.id }}'">Réserver</button>
      </div>
      {% endfor %}
    </div>
  </section>

  <section class="about" id="about">
    <h2>À propos</h2>
    <p>
      EasyMarket est une plateforme de réservation de produits en boutique, conçue pour éliminer les longues files d'attente. Les clients réservent leur créneau à l'avance, les vendeurs gèrent leur flux sereinement — tout le monde y gagne du temps et de la tranquillité.
    </p>
  </section>

  <section class="contact" id="contact">
    <h2 class="section-title">Contactez-nous</h2>

    <div class="contact-wrapper">
      <div class="contact-form">
        <input type="text" class="form-input" placeholder="Votre nom">
        <input type="email" class="form-input" placeholder="Votre email">
        <textarea class="form-input" rows="4" placeholder="Votre message"></textarea>
        <button class="btn primary form-input">Envoyer</button>
      </div>
    </div>
  </section>
</main>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/home.js') }}"></script>
{% endblock %}
```

---

## Fichier : `templates\reservation.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}

{% block title %}EasyMarket - Réservations en attente{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/reservation.css') }}">
{% endblock %}

{% block content %}
<main class="reservation-main">
  <div class="reservation-layout">

    <aside class="side-nav">
      <p class="side-nav-title">Vue d'ensemble</p>
      <a href="#section-attente" class="side-nav-link active">
        <span>En attente</span>
        <span class="side-badge side-badge--blue" id="side-count-attente">{{ reservations_attente|length|default(0) }}</span>
      </a>
      <a href="#section-prets" class="side-nav-link">
        <span>Non servis</span>
        <span class="side-badge side-badge--orange" id="side-count-prets">0</span>
      </a>
      <a href="#section-servis" class="side-nav-link">
        <span>Servis</span>
        <span class="side-badge side-badge--green" id="side-count-servis">0</span>
      </a>
    </aside>

    <div class="reservation-container">

      <h1 class="page-title">Tableau de bord — {{ boutique.nom|default('Boutique') }}</h1>

      <section class="reservation-section" id="section-attente">
        <h2 class="section-heading">
          Réservations en attente
          <span class="section-count section-count--blue" id="count-attente">{{ reservations_attente|length|default(0) }}</span>
        </h2>
        <div class="reservation-list" id="reservation-list">
          {% for r in reservations_attente %}
          <article class="reservation-card" data-reservation-id="{{ r.id }}">
            <div class="reservation-card-top">
              <div>
                <p class="card-label">Client</p>
                <h2 class="client-name">{{ r.client_nom }}</h2>
                <p class="client-contact">{{ r.client_whatsapp }}</p>
              </div>
              {% if r.nouveau_client %}
              <span class="badge badge-new">Nouveau client</span>
              {% endif %}
            </div>

            <div class="reservation-block">
              <p class="block-title">Produits demandés</p>
              <ul class="reservation-items">
                {% for produit in r.produits %}
                <li><label><input type="checkbox"> {{ produit }}</label></li>
                {% endfor %}
              </ul>
            </div>

            <div class="reservation-action-row">
              <p class="amount-label">Montant total à payer</p>
              <div class="amount-group">
                <div class="amount-input-wrapper">
                  <input id="amount-{{ r.id }}" type="text" class="form-input amount-input" placeholder="0">
                  <select class="amount-select" aria-label="Devise">
                    <option value="cdf" selected>CDF</option>
                    <option value="usd">USD</option>
                  </select>
                </div>
                <button class="btn primary notify-btn">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.22 1.18 2 2 0 012.18 0h3a2 2 0 012 1.72c.13 1.05.37 2.08.72 3.08a2 2 0 01-.45 2.11L6.91 7.91a16 16 0 006.18 6.18l1-1a2 2 0 012.11-.45c1 .35 2.03.59 3.08.72A2 2 0 0122 16.92z"/></svg>
                  Notifier le client
                </button>
              </div>
            </div>
          </article>
          {% endfor %}
        </div>
      </section>

      <div class="commission-summary" id="commission-summary"></div>

      <section class="reservation-section" id="section-prets">
        <h2 class="section-heading">
          Prêts — non servis
          <span class="section-count" id="count-prets">0</span>
        </h2>
        <div class="prets-list" id="prets-list">
          <p class="empty-state" id="empty-prets">Aucun produit prêt pour le moment.</p>
        </div>
      </section>

      <section class="reservation-section" id="section-servis">
        <h2 class="section-heading">
          Servis
          <span class="section-count section-count--green" id="count-servis">0</span>
        </h2>
        <div class="servis-list" id="servis-list">
          <p class="empty-state" id="empty-servis">Aucun produit servi pour le moment.</p>
        </div>
      </section>

    </div>
  </div>
</main>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/reservation.js') }}"></script>
{% endblock %}
```

---

## Fichier : `templates\reserver.html`
Dossier : `.\templates`

```html
{% extends "base.html" %}

{% block title %}EasyMarket - Réserver{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/reserver.css') }}">
{% endblock %}

{% block content %}
<main class="reserver-main">
  <div class="reserver-container">

    <h1 class="reserver-title">Nouvelle réservation</h1>

    <form class="reserver-form" id="reserver-form" method="POST" action="{{ url_for('main.traitement_reservation', boutique_id=boutique.id) if boutique else '#' }}" novalidate>

      <fieldset class="form-section">
        <legend class="form-section-title">Votre identité</legend>
        <div class="form-group">
          <label for="client-nom">Nom complet</label>
          <input type="text" id="client-nom" name="nom_client" class="form-input" placeholder="Ex : Jean Dupont" required>
        </div>
        <div class="form-group">
          <label for="client-whatsapp">Numéro WhatsApp</label>
          <input type="tel" id="client-whatsapp" name="whatsapp_client" class="form-input" placeholder="Ex : +243 81 234 5678" required>
        </div>
      </fieldset>

      <fieldset class="form-section">
        <legend class="form-section-title">Produits à réserver</legend>
        <div class="produit-input-row">
          <div class="input-row">
            <input type="text" id="produit-input" name="produit_custom" class="form-input" placeholder="Ex : Tomates fraîches — 2kg — 5000 FC">
            <button type="button" class="btn primary" id="btn-ajouter">Ajouter</button>
          </div>
        </div>
        
        {% if boutique and boutique.produits %}
        <div class="produits-checkbox-list">
          <p class="form-hint">Cochez les produits que vous souhaitez réserver :</p>
          {% for produit in boutique.produits %}
          <div class="produit-checkbox-item">
            <label>
              <input type="checkbox" name="produits_ids" value="{{ produit.id }}" data-nom="{{ produit.nom }}" data-prix="{{ produit.prix }} {{ produit.devise }}" data-disponible="{{ 'true' if produit.disponible else 'false' }}">
              <strong>{{ produit.nom }}</strong> — {{ produit.prix }} {{ produit.devise }} 
              <span class="produit-details">({{ produit.autres }})</span>
            </label>
          </div>
          {% endfor %}
        </div>
        {% endif %}
      </fieldset>

      <fieldset class="form-section">
        <legend class="form-section-title">Boutique</legend>
        <div class="form-group">
          <label for="select-boutique">Choisir une boutique</label>
          <select id="select-boutique" class="form-input form-select" name="boutique_id">
            <option value="" disabled {% if not boutique %}selected{% endif %}>-- Sélectionnez une boutique --</option>
            {% for b in boutiques %}
            <option value="{{ b.id }}" {{ 'selected' if boutique and boutique.id == b.id else '' }}>{{ b.nom }} — {{ b.categorie_principale|default(b.categorie) }}</option>
            {% endfor %}
          </select>
          <p class="form-hint">
            Vous êtes commerçant ? <a href="{{ url_for('auth.inscription') }}">Inscrivez votre boutique ici</a>
          </p>
          {% if boutique %}
          <button type="button" class="btn btn-choisir-boutique" data-id="{{ boutique.id }}">Choisir cette boutique</button>
          {% endif %}
        </div>
      </fieldset>

      <div class="form-submit">
        <button type="button" class="btn primary" id="btn-ouvrir-confirmation">Envoyer</button>
      </div>

    </form>

    <div id="modal-confirmation" style="display:none;" class="modal">
      <h2>Vérification de votre commande</h2>
      <div id="recap-produits-container"></div>
      <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:16px;">
        <button type="button" id="btn-annuler-modal">Annuler</button>
        <button type="button" id="btn-valider-final" class="btn-primary">Valider la réservation</button>
      </div>
    </div>
  </div>
</main>

<!-- MODAL CONFIRMATION -->
<div class="modal-overlay" id="modal-overlay">
  <div class="modal">
    <h2 class="modal-title">Confirmer la réservation</h2>

    <div class="modal-section">
      <p class="modal-label">Boutique</p>
      <p class="modal-value" id="modal-boutique"></p>
    </div>

    <div class="modal-section modal-indispo" id="modal-indispo" style="display:none;">
      <p class="modal-label modal-indispo-title">⚠ Produits indisponibles</p>
      <ul class="modal-produits modal-indispo-list" id="modal-indispo-list"></ul>
    </div>

    <div class="modal-section">
      <p class="modal-label">Produits demandés</p>
      <ul class="modal-produits" id="modal-produits"></ul>
    </div>

    <div class="modal-section">
      <p class="modal-label">Nom</p>
      <p class="modal-value" id="modal-nom"></p>
    </div>

    <div class="modal-section">
      <p class="modal-label">WhatsApp</p>
      <p class="modal-value" id="modal-whatsapp"></p>
    </div>

    <div class="modal-actions">
      <button class="btn secondary" id="btn-annuler">Annuler</button>
      <button class="btn primary" id="btn-confirmer">Confirmer</button>
    </div>
  </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/reserver.js') }}"></script>
{% endblock %}
```

---

## Fichier : `tests\__init__.py`
Dossier : `.\tests`

```python

```

---

## Fichier : `tests\fixtures.py`
Dossier : `.\tests`

```python
# tests/fixtures.py

MOCK_VENDEURS = [
    {
        "nom": "Jean-Marc Kabuya",
        "whatsapp": "+243810000001",
        "code_clair": "vendeur123",
        "statut": "actif",
        "boutique": {
            "id": "marche-frais",
            "nom": "Au Marché Frais",
            "categorie_principale": "Alimentation",
            "description": "Produits frais locaux et de qualité supérieure.",
            "produits": [
                {"id": "PRD-0101", "nom": "Tomates (Panier)", "type_produit": "Légumes", "prix": "5000", "devise": "CDF", "disponible": True, "autres": "Panier d'environ 2kg"},
                {"id": "PRD-0102", "nom": "Oignons (Tas)", "type_produit": "Légumes", "prix": "2500", "devise": "CDF", "disponible": True, "autres": "Tas de 5 gros oignons"}
            ]
        }
    },
    {
        "nom": "Sarah Tshimanga",
        "whatsapp": "+243820000002",
        "code_clair": "vendeur456",
        "statut": "actif",
        "boutique": {
            "id": "saveurs-pastels",
            "nom": "Saveurs & Pâtisserie",
            "categorie_principale": "Gastronomie",
            "description": "Samoussas croustillants et douceurs faits maison.",
            "produits": [
                {"id": "PRD-0201", "nom": "Samoussas Viande (x10)", "type_produit": "Snack", "prix": "10000", "devise": "CDF", "disponible": True, "autres": "Bien chauds et croustillants"},
                {"id": "PRD-0202", "nom": "Jus de Gingembre (1L)", "type_produit": "Boisson", "prix": "4000", "devise": "CDF", "disponible": True, "autres": "Fait maison, légèrement sucré"}
            ]
        }
    }
]
```

---

## Fichier : `utils\__init__.py`
Dossier : `.\utils`

```python

```

---

## Fichier : `utils\decorators.py`
Dossier : `.\utils`

```python
from functools import wraps
from flask import session, redirect, url_for, abort

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'role' not in session:
                return redirect(url_for('auth.connexion'))
            if role and session.get('role') != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator
```

---

