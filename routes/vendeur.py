from flask import Blueprint, render_template, redirect, url_for, session
from utils.decorators import login_required

vendeur_bp = Blueprint('vendeur', __name__)

RESERVATIONS_TEMP = [
    {'id': 1, 'client_nom': 'Jonathan M.', 'client_whatsapp': '+243 90 677 9261',
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
    )