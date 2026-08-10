from app import create_app
from models.db_models import db, Vendeur, Boutique, Produit, Categorie
from tests.fixtures import MOCK_VENDEURS

app = create_app()

def run_seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        for v_data in MOCK_VENDEURS:
            b_data = v_data.pop("boutique")
            produits_data = b_data.pop("produits")
            code_clair = v_data.pop("code_clair")

            vendeur = Vendeur(**v_data)
            vendeur.set_code(code_clair)
            db.session.add(vendeur)
            db.session.flush()

            b_data["vendeur_id"] = vendeur.id
            boutique = Boutique(**b_data)
            db.session.add(boutique)

            cat_defaut = Categorie(nom="Général", boutique_id=boutique.id)
            db.session.add(cat_defaut)
            db.session.flush()

            for p_data in produits_data:
                p_data["boutique_id"] = boutique.id
                p_data["categorie_id"] = cat_defaut.id
                produit = Produit(**p_data)
                db.session.add(produit)

        db.session.commit()
        print("Base de données initialisée avec succès avec les données de test !")

if __name__ == "__main__":
    run_seed()