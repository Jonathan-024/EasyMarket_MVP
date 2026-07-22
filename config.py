import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-a-changer-en-production')
    # Fichier stocké directement à la racine du projet
    SQLALCHEMY_DATABASE_URI = 'sqlite:///easymarket.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False