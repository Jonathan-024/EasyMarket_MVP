from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/connexion')
def connexion():
    return render_template('connexion.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    # logique de vérification à venir
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/register', methods=['POST'])
def register():
    # logique de création de compte à venir
    return redirect(url_for('vendeur.dashboard'))