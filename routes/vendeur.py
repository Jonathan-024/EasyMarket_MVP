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