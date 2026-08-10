from flask import Blueprint, render_template
from utils.decorators import login_required

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