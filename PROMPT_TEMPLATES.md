# Modèles de Prompts - EasyMarket_MVP

## Modèle A : Correction de Bug (Debugging)
**À utiliser lorsque :** Une erreur survient dans le backend ou le frontend.

> **Rôle :** Expert en résolution de bugs sur Flask et Next.js.
> **Contexte :** Je développe EasyMarket. Mon code actuel dysfonctionne sur le module suivant.
> **Problème :** [Décrire l'erreur ou coller le message d'erreur du terminal/console].
> **Fichier concerné :** [Chemin du fichier, ex: backend/app.py].
> **Extrait de code actuel :** 
> ```python
> [Coller uniquement la fonction ou la partie qui pose problème]
> ```
> **Tâche :** Corrige ce bug de manière ciblée.
> **Contraintes :** Ne renvoie que l'extrait corrigé (prêt pour apply_update.py). Pas de bavardage.


## Modèle B : Ajout d'une Fonctionnalité / Composant
**À utiliser lorsque :** Tu veux créer un nouvel élément (bouton, formulaire, route).

> **Rôle :** Développeur Full-Stack pragmatique.
> **Contexte :** Projet EasyMarket_MVP.
> **Tâche :** Je dois ajouter la fonctionnalité suivante : [Décrire la fonctionnalité, ex: un bouton de validation de commande].
> **Spécifications :** 
> **Contraintes :** Fournis uniquement les blocs de code nécessaires pour mettre à jour mes fichiers cibles. Respecte la structure de code.md. Pas d'explications superflues.


## Modèle C : Analyse / Revue d'un Script pour `apply_update.py`
**À utiliser lorsque :** Tu veux t'assurer qu'un script de modification est correct avant de l'exécuter.

> **Rôle :** Code Reviewer rigoureux.
> **Contexte :** Je prépare une mise à jour atomique pour EasyMarket via mon script apply_update.py.
> **Code prévu :**
> ```python
> [Coller ton code d'apply_update.py]
> ```
> **Tâche :** Vérifie s'il y a des erreurs de syntaxe, des oublis d'importation ou un risque de régression.
> **Contraintes :** Réponds par "OK, le script est valide" ou donne directement la correction en une ligne si une erreur est présente.