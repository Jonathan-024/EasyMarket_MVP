import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db_models import db, Vendeur

auth_bp = Blueprint('auth', __name__)

ADMIN_WHATSAPP = os.environ.get('ADMIN_WHATSAPP')
ADMIN_CODE = os.environ.get('ADMIN_CODE')

@auth_bp.route('/connexion')
def connexion():
    return render_template('connexion.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    whatsapp = request.form.get('whatsapp', '').strip()
    code = request.form.get('code', '').strip()

    if whatsapp == ADMIN_WHATSAPP and code == ADMIN_CODE:
        session['role'] = 'admin'
        return redirect(url_for('admin.dashboard'))

    vendeur = Vendeur.query.filter_by(whatsapp=whatsapp).first()
    if vendeur and vendeur.check_code(code):
        if vendeur.statut == 'suspendu':
            return render_template('connexion.html', error="Votre compte a été suspendu.")
        session['role'] = 'vendeur'
        session['vendeur_id'] = vendeur.id
        session['vendeur_nom'] = vendeur.nom
        session['vendeur_initiales'] = ''.join([n[0] for n in vendeur.nom.split()[:2]]).upper()
        return redirect(url_for('vendeur.dashboard'))

    return render_template('connexion.html', error="Identifiants incorrects.")

@auth_bp.route('/register', methods=['POST'])
def register():
    session['role'] = 'vendeur'
    session['vendeur_nom'] = request.form.get('nom', 'Nouveau vendeur')
    session['vendeur_initiales'] = ''.join([n[0] for n in session['vendeur_nom'].split()[:2]]).upper()
    return redirect(url_for('vendeur.dashboard'))

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))