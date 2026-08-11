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