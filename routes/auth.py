import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db_models import db, Vendeur, Boutique

auth_bp = Blueprint('auth', __name__)

ADMIN_WHATSAPP = os.environ.get('ADMIN_WHATSAPP')
ADMIN_CODE = os.environ.get('ADMIN_CODE')


def normalize_whatsapp(value):
    value = (value or '').strip()
    value = re.sub(r'[\s\-.]', '', value)
    if not value:
        return ''
    if value.startswith('00'):
        value = '+' + value[2:]
    if value.startswith('0'):
        value = '+243' + value[1:]
    if not value.startswith('+'):
        value = '+' + value
    return value


@auth_bp.route('/connexion')
def connexion():
    return render_template('connexion.html', initial_tab='login')


@auth_bp.route('/inscription')
def inscription():
    return render_template('connexion.html', initial_tab='register')


@auth_bp.route('/login', methods=['POST'])
def login():
    whatsapp = normalize_whatsapp(request.form.get('whatsapp', ''))
    code = request.form.get('code', '').strip()

    if whatsapp == ADMIN_WHATSAPP and code == ADMIN_CODE:
        session['role'] = 'admin'
        return redirect(url_for('admin.dashboard'))

    vendeur = Vendeur.query.filter_by(whatsapp=whatsapp).first()
    if vendeur is None:
        return render_template('connexion.html', error="Compte vendeur introuvable. Vérifiez votre numéro WhatsApp.")

    if not vendeur.check_code(code):
        return render_template('connexion.html', error="Code d’accès incorrect. Réessayez.")

    if vendeur.statut == 'suspendu':
        return render_template('connexion.html', error="Votre compte a été suspendu.")

    session['role'] = 'vendeur'
    session['vendeur_id'] = vendeur.id
    session['vendeur_nom'] = vendeur.nom
    session['vendeur_initiales'] = ''.join([n[0] for n in vendeur.nom.split()[:2]]).upper()
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/register', methods=['POST'])
def register():
    nom = (request.form.get('nom', '') or '').strip()
    boutique_nom = (request.form.get('boutique', '') or '').strip()
    whatsapp = normalize_whatsapp(request.form.get('whatsapp', ''))
    code = (request.form.get('code', '') or '').strip()

    if not nom or not boutique_nom or not whatsapp or not code:
        return render_template('connexion.html', error="Tous les champs sont requis pour l’inscription.")

    if Vendeur.query.filter_by(whatsapp=whatsapp).first():
        return render_template('connexion.html', error="Ce numéro WhatsApp est déjà utilisé.")

    vendeur = Vendeur(nom=nom, whatsapp=whatsapp, statut='actif')
    vendeur.set_code(code)

    boutique_id = boutique_nom.lower().replace(' ', '-')
    boutique = Boutique(
        id=boutique_id,
        nom=boutique_nom,
        categorie_principale=request.form.get('categorie_principale', 'Général'),
        description=request.form.get('description', ''),
        vendeur=vendeur
    )

    db.session.add(vendeur)
    db.session.add(boutique)
    db.session.commit()

    session['role'] = 'vendeur'
    session['vendeur_id'] = vendeur.id
    session['vendeur_nom'] = vendeur.nom
    session['vendeur_initiales'] = ''.join([n[0] for n in vendeur.nom.split()[:2]]).upper()
    return redirect(url_for('vendeur.dashboard'))


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))