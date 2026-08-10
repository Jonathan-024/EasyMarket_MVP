from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
    return redirect(url_for('main.home'))