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
