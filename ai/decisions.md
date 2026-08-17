# EasyMarket — Journal de décisions

> Une entrée courte (5-10 lignes) par décision technique qui n'est pas évidente
> en lisant le code. Objectif : qu'une IA (ou toi dans 3 mois) comprenne le
> "pourquoi" sans que tu aies à le réexpliquer à chaque session.
> Ajoute une entrée seulement quand une vraie décision structurante est prise —
> pas pour chaque petit choix.

## Format
```
### [AAAA-MM-JJ] Titre court de la décision
- Contexte : pourquoi ce choix s'est posé
- Décision : ce qui a été choisi
- Alternative écartée : ce qui n'a pas été retenu, et pourquoi
```

## Historique

### [2026-XX-XX] Migration de statique vers Flask/Jinja2
- Contexte : le MVP a démarré en HTML/SCSS/JS statique
- Décision : migration vers Flask + Jinja2 avec blueprints par rôle
- Alternative écartée : garder du statique + API séparée (jugé trop lourd pour la taille du MVP)

<!-- Ajoute tes prochaines décisions au-dessus de cette ligne -->
