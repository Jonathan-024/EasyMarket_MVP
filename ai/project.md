# EasyMarket — Contexte projet

> Ce fichier est collé en 2e message de chaque nouvelle conversation avec l'IA,
> juste après prompt-template.md. Il ne change presque jamais — à mettre à jour
> seulement quand l'objectif ou la stack évolue réellement.

## Objectif
Plateforme web de réservation de produits, avec trois profils d'utilisateurs :
client, vendeur, administrateur.

## Stack technique
- Backend : Flask + Jinja2, architecture par blueprints, sessions basées sur les rôles, SQLAlchemy
- Frontend : HTML + SCSS (palette bleue), JS vanilla, logo en SVG inline — PAS de framework JS (pas de Next.js/React)
- Base de données : [à préciser — SQLite / PostgreSQL / autre]
- Déploiement cible : [à préciser — Render / Railway / VPS / autre]

## Rôles et pages
- **Client** : accueil, réservations
- **Vendeur** : dashboard, gestion boutique
- **Admin** : panel admin
- **Commun** : login

## État actuel
Voir le détail phase par phase dans docs/ROADMAP_MVP.md — ce fichier ne
duplique pas la checklist pour éviter deux sources de vérité en conflit.

## Mode de travail
- Développement itératif, un bloc fonctionnel à la fois (ex : "le bouton de réservation", pas "toute la page")
- Toujours demander/fournir uniquement le code lié au bloc en cours, jamais un fichier entier sauf demande explicite
- Respecter les conventions listées dans conventions.md
