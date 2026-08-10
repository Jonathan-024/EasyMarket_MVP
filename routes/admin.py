from flask import Blueprint, render_template, request, jsonify
from utils.decorators import login_required
from models.db_models import db, Vendeur

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required(role='admin')
def dashboard():
    return render_template(
        'admin.html', 
        vendeurs=[], 
        clients=[], 
        historique_mensuel=[]
    )

@admin_bp.route('/generer-code', methods=['POST'])
@login_required(role='admin')
def generer_code():
    vendeur_id = request.form.get('vendeur_id')
    code = 'EM-' + __import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') + __import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') + __import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') + __import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') + __import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') + __import__('random').SystemRandom().choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789')

    vendeur = None
    if vendeur_id:
        vendeur = Vendeur.query.get(vendeur_id)
        if vendeur:
            vendeur.set_code(code)
            db.session.commit()

    return jsonify({
        'code': code,
        'vendeur_id': vendeur.id if vendeur else None,
        'vendeur_nom': vendeur.nom if vendeur else None
    })