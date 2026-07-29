import os
from flask import Flask
from config import Config
from models.db_models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # --- SOLUTION : S'assurer que le dossier instance existe physiquement ---
    instance_path = app.instance_path
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
    # ------------------------------------------------------------------------

    print("Avant init :", app.config["SQLALCHEMY_DATABASE_URI"])
    
    # Initialisation de SQLAlchemy
    db.init_app(app)
    print("Après init :", app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        from models.db_models import Vendeur, Boutique, Produit, Categorie, Client, Reservation, LigneReservation
        db.create_all()

    from routes.main import main
    from routes.auth import auth_bp
    from routes.vendeur import vendeur_bp
    from routes.admin import admin_bp

    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(vendeur_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)