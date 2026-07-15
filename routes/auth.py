from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/connexion')
def connexion():
    return render_template('connexion.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/register', methods=['POST'])
def register():
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('main.home'))