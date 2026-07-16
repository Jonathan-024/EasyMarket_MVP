from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

ADMIN_WHATSAPP = '+243000000000'
ADMIN_CODE = 'ADMIN-2026'

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

    # Sinon, connexion vendeur (temporaire, sans vérification réelle)
    session['role'] = 'vendeur'
    session['vendeur_nom'] = 'Jean Dupont'
    session['vendeur_initiales'] = 'JD'
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/register', methods=['POST'])
def register():
    # Vérification du code d'accès à venir avec la DB
    session['role'] = 'vendeur'
    session['vendeur_nom'] = request.form.get('nom', 'Nouveau vendeur')
    session['vendeur_initiales'] = ''.join([n[0] for n in session['vendeur_nom'].split()[:2]]).upper()
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))