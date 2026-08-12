from app import create_app
from models.db_models import db

app = create_app()

def init_clean_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ La base de données a été réinitialisée. Elle est totalement vide et prête !")

if __name__ == "__main__":
    init_clean_db()