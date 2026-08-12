import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Définir le chemin du répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-a-changer-en-production-2026')
    # Le chemin absolu vers le fichier de base de données dans le dossier 'instance'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "instance" / "easymarket.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False