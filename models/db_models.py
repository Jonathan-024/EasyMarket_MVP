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
    statut = db.Column(db.String(20), default='actif') # 'actif', 'attente', 'suspendu'
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
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
    
    # Relations
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
    type_produit = db.Column(db.String(50)) # Équivalent de l'ancienne catégorie libre
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
    libelle_produit = db.Column(db.String(150), nullable=False)