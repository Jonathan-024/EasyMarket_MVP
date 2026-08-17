# EasyMarket MVP

Plateforme web de réservation de produits — client / vendeur / admin.

## Stack
Flask + Jinja2 (blueprints), SQLAlchemy, HTML/SCSS/JS vanilla.

## Installation
```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # puis remplis les valeurs
```

## Base de données
```bash
python scripts/init_db.py       # réinitialise la DB (vide)
python scripts/seed.py          # réinitialise + données de test
```

## Lancer le projet
```bash
flask run
```

## Tests
```bash
python tests/test_api.py        # smoke test — le serveur doit être lancé
```

## Documentation
- Roadmap et état d'avancement : [`docs/ROADMAP_MVP.md`](docs/ROADMAP_MVP.md)
- Contexte projet pour l'assistant IA : [`.ai/project.md`](.ai/project.md)
- Conventions de code : [`.ai/conventions.md`](.ai/conventions.md)
- Historique des décisions techniques : [`.ai/decisions.md`](.ai/decisions.md)

## Structure
```
app/        code applicatif (blueprints, templates, static, models)
tests/      tests automatisés
scripts/    scripts d'exploitation (init DB, seed) — jamais exécutés par l'app
docs/       documentation humaine
.ai/        outillage pour le développement assisté par IA
```
