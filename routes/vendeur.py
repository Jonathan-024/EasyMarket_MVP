from flask import Blueprint, render_template

vendeur_bp = Blueprint('vendeur', __name__)


@vendeur_bp.route('/boutique')
def boutique():
    return render_template('boutique.html')


@vendeur_bp.route('/reservation')
def reservation():
    return render_template('reservation.html')


@vendeur_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')