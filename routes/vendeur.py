from flask import Blueprint, render_template, redirect, url_for, session
from utils.decorators import login_required
from models.db_models import db, Reservation, Boutique, Produit, Client

vendeur_bp = Blueprint('vendeur', __name__)

@vendeur_bp.route('/boutique')
@login_required(role='vendeur')
def boutique():
    vendeur_id = session.get('vendeur_id')
    boutique_obj = Boutique.query.filter_by(vendeur_id=vendeur_id).first()
    
    return render_template(
        'boutique.html',
        vendeur={'nom': session.get('vendeur_nom'), 'initiales': session.get('vendeur_initiales')},
        boutique=boutique_obj,
        clients=Client.query.all() if boutique_obj else []
    )

@vendeur_bp.route('/boutique/update', methods=['POST'])
@login_required(role='vendeur')
def update_boutique():
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