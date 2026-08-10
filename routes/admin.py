from flask import Blueprint, render_template, request, jsonify
from utils.decorators import login_required
from models.db_models import db, Vendeur, Client

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required(role='admin')
def dashboard():
    vendeurs = Vendeur.query.all()
    clients = Client.query.all()
    historique_mensuel = []

    return render_template(
        'admin.html',
        vendeurs=vendeurs,
        clients=clients,
        historique_mensuel=historique_mensuel
    )

@admin_bp.route('/generer-code', methods=['POST'])
@login_required(role='admin')
def generer_code():
    vendeur_id = request.form.get('vendeur_id')
    code = 'EM-' + ''.join(__import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))

    vendeur = Vendeur.query.get(vendeur_id) if vendeur_id else None

    if vendeur is not None:
        vendeur.set_code(code)
        db.session.commit()

    return jsonify({
        'code': code,
        'vendeur_id': vendeur.id if vendeur else None,
        'vendeur_nom': vendeur.nom if vendeur else None
    })