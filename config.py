import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.resolve()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-a-changer-en-production')
    # Fichier stocké directement à la racine du projet
    SQLALCHEMY_DATABASE_URI = 'sqlite:///easymarket.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{(BASE_DIR / "instance" / "easymarket.db").as_posix()}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False