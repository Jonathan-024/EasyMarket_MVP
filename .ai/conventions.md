# EasyMarket — Conventions de code

> Fichier stable, quasi jamais modifié. À coller avec project.md si la demande
> touche à la structure du code (nouveau fichier, nouvelle route, etc.).
> Sinon, il est déjà couvert par les règles de prompt-template.md.

## Structure des dossiers
```
easymarket/
├── .ai/
├── docs/
├── instance/
├── models/
├── routes/
├── scripts/
├── static/
│   ├── css/
│   ├── js/
│   └── scss/
├── templates/
├── tests/ 
├── utils/ 
├── .env
├── .gitignore
├── app.py
├── config.py
├── README.md
└── requirements.txt
```
[Ajuste cet arbre à ta structure réelle si elle diffère.]

## Nommage
- Python : snake_case pour fonctions/variables, PascalCase pour les classes
- Routes Flask : préfixées par blueprint (ex: `/vendeur/dashboard`)
- Fichiers SCSS : un fichier par composant, partials préfixés `_` (ex: `_button.scss`)
- Classes CSS : kebab-case, méthodologie BEM si le composant est complexe

## Règles backend
- Toute route qui modifie des données passe par une vérification de rôle (`@login_required` + check de rôle)
- Pas de logique métier dans les templates Jinja2
- Variables sensibles uniquement via `.env`, jamais en dur dans le code

## Règles frontend
- SCSS : variables de couleurs centralisées dans `_variables.scss`, jamais de couleurs en dur ailleurs
- JS : vanilla, pas de framework sauf décision contraire actée dans decisions.md
