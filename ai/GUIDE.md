# EasyMarket — Guide d'utilisation efficace

> Référence rapide. Relis-le si tu sens que tu colles trop de contexte
> ou pas assez.

## Quoi coller selon la demande

| Type de demande | prompt-template.md + project.md | conventions.md | extrait de index.md | fichier(s) réel(s) concerné(s) |
|---|---|---|---|---|
| Début de toute conversation | ✅ une fois | — | — | — |
| Bug sur un élément existant | déjà collé | non | non (tu sais déjà quel fichier) | ✅ juste le fichier en cause |
| Design / déplacement d'un élément | déjà collé | non | non | ✅ le SCSS/HTML concerné |
| Nouvelle route / fonctionnalité | déjà collé | ✅ | ✅ (pour voir où ça s'intègre) | selon ce que ça touche |
| Nouveau fichier dans la structure existante | déjà collé | ✅ | ✅ | — |
| Question non-code (archi, choix technique) | déjà collé | selon le sujet | non | non |

## Règles d'efficacité

1. **prompt-template.md et project.md se collent une seule fois par conversation**, pas à chaque message. Le modèle garde le contexte tant que la conversation continue.
2. **Une conversation = un sujet cohérent** (ex : tout le module réservation). Pour un sujet sans rapport, ouvre une nouvelle conversation plutôt que d'accumuler du contexte inutile qui bouffe des tokens à chaque tour.
3. **Ne colle jamais index.md en entier** — seulement la section du dossier concerné (ex : juste `## app/blueprints/vendeur/`), le reste ne sert à rien pour la demande en cours.
4. **Toujours prévisualiser avant --apply** : `python .ai/apply_changes.py .ai/response.md` sans `--apply` d'abord, relis, puis relance avec `--apply`. Ne saute jamais cette étape même pour un petit changement — un `[PATCH]` mal formé peut échouer silencieusement sur le mauvais extrait.
5. **Modèle très limité en tokens (free tier, ~4-8k)** : saute conventions.md sauf si la demande touche vraiment la structure, et ne colle que le fichier réel concerné, pas d'extrait d'index.md en plus — laisse le modèle inférer le style du fichier collé lui-même.
6. **Maintenance hebdo (2 minutes)** : relis `.ai/decisions.md`, supprime les brouillons non pertinents ou complète leur "pourquoi" ; coche les cases faites dans `docs/ROADMAP_MVP.md`.
