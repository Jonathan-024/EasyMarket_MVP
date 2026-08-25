# Guide du dossier .ai/

Référence de chaque fichier du dossier `.ai/` : à quoi il sert, comment
l'utiliser, et ce qu'il y a (ou non) à remplir soi-même.

## 1. À coller dans le chat, à chaque nouvelle conversation

### `prompt-template.md`

- **Utilité** : dit à l'IA comment répondre (juste le code demandé, format FILE/PATCH, franc si ce n'est pas du code)
- **Usage** : premier message de chaque conversation, tel quel
- **À remplir** : rien, ne pas y toucher

### `project.md`

- **Utilité** : dit à l'IA ce qu'est EasyMarket (objectif, stack, rôles)
- **Usage** : deuxième message, juste après `prompt-template.md`
- **À remplir** : les deux `[à préciser]` — base de données et cible de déploiement. Une fois rempli, on n'y touche quasi plus.

### `conventions.md`

- **Utilité** : dit à l'IA comment nommer et organiser le code
- **Usage** : à coller seulement si la demande crée un nouveau fichier ou touche la structure (pas pour un simple bug ou un ajustement de design)
- **À remplir** : vérifier que l'arborescence en haut du fichier correspond au vrai projet, la corriger si besoin

## 2. À remplir soi-même de temps en temps

### `decisions.md`

- **Utilité** : garde une trace du "pourquoi" des choix techniques importants
- **Usage** : après un commit important, un brouillon y apparaît automatiquement (fichiers touchés, date). On ajoute juste une ligne pour expliquer le choix. Si le commit n'était pas important, on supprime le brouillon.
- **À remplir** : uniquement le champ "Contexte / Décision" des brouillons qui le méritent

## 3. À lancer en commande, jamais à ouvrir

- **`generate_index.py`** → régénère `index.md` (la carte du projet)
- **`draft_decision.py`** → crée les brouillons dans `decisions.md`
- **`apply_changes.py`** → écrit dans les fichiers le code donné par l'IA :
  ```
  python .ai/apply_changes.py .ai/response.md          # aperçu
  python .ai/apply_changes.py .ai/response.md --apply   # écriture réelle
  ```
- **`install_hook.sh`** → à lancer **une seule fois** (`bash .ai/install_hook.sh`) pour que les deux premiers scripts se lancent automatiquement après chaque commit. Ensuite, on l'oublie.

### `generate_code_md.py`

- **Utilité** : extrait tout le code lié à une fonctionnalité ou partie précise du site
  (ex: footer, boutique, reservation) — fichiers entiers si le nom correspond,
  blocs HTML/SCSS/JS ciblés sinon — et le regroupe dans `code.md`
- **Usage** :
```bash
  python .ai/generate_code_md.py --keywords vendeur boutique --output .ai/code.md
  python .ai/generate_code_md.py --tags footer --classes footer-link footer-content --scan-sections --output .ai/code.md
```
- **Quand l'utiliser** : avant de coller une demande à l'IA qui touche une
  fonctionnalité précise — colle le contenu de `code.md` généré à la place de
  chercher les fichiers toi-même

### `code.md`

- **Utilité** : contient le code extrait par `generate_code_md.py` pour la
  dernière fonctionnalité ciblée
- **Usage** : coller son contenu dans le chat juste après `project.md`
  (et `conventions.md` si la demande touche la structure)
- **À remplir** : rien — régénéré à chaque nouvelle extraction, écrase le
  contenu précédent

## 4. Générés ou remplis automatiquement — jamais à toucher à la main

- **`index.md`** — régénéré automatiquement à chaque commit
- **`response.md`** — on y colle la réponse de l'IA avant de lancer `apply_changes.py`, rien d'autre à en faire

## En résumé

Le seul vrai travail manuel : remplir les deux blancs de `project.md` une
fois, et compléter/nettoyer `decisions.md` de temps en temps. Le reste
tourne tout seul ou se colle tel quel.
