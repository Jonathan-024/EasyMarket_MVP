from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

BOUTIQUES_TEMP = [
    {'id': 'marche-frais', 'nom': 'Marché Frais', 'categorie': 'Fruits & Légumes',
     'description': 'Produits frais du marché local, sélectionnés chaque matin directement auprès des producteurs.'},
    {'id': 'boucherie-centrale', 'nom': 'Boucherie Centrale', 'categorie': 'Viandes & Charcuterie',
     'description': 'Viandes de qualité, découpées à la demande par nos bouchers experts.'},
    {'id': 'fromagerie', 'nom': 'La Fromagerie', 'categorie': 'Fromages & Produits laitiers',
     'description': "Une sélection raffinée de fromages artisanaux locaux et d'importation."},
    {'id': 'epicerie-coin', 'nom': 'Épicerie du Coin', 'categorie': 'Épicerie générale',
     'description': "Tout le nécessaire du quotidien : conserves, céréales, condiments et produits d'entretien."},
    {'id': 'boulangerie-doree', 'nom': 'Boulangerie Dorée', 'categorie': 'Boulangerie & Pâtisserie',
     'description': 'Pains artisanaux, viennoiseries et pâtisseries fraîches préparées chaque jour.'},
    {'id': 'poissonnerie-bleue', 'nom': 'Poissonnerie Bleue', 'categorie': 'Poissons & Fruits de mer',
     'description': 'Poissons frais et fruits de mer livrés quotidiennement depuis les ports locaux.'},
]


@main_bp.route('/')
def home():
    return render_template('home.html', boutiques=BOUTIQUES_TEMP)


@main_bp.route('/reserver')
def reserver():
    return render_template('reserver.html', boutiques=BOUTIQUES_TEMP)