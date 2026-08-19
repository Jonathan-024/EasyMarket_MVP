#!/usr/bin/env python3
"""
Regarde le dernier commit et, s'il est "significatif", ajoute un brouillon
d'entrée en haut de decisions.md avec le factuel déjà rempli (date, message
de commit, fichiers touchés). Le Contexte/Décision/Alternative reste à
remplir à la main — ou à supprimer si le commit n'était pas structurant.

Seuils de "significatif" (ajustables ci-dessous) :
- au moins 1 fichier créé ou supprimé, OU
- plus de SEUIL_LIGNES lignes changées au total

Usage : python draft_decision.py [--decisions decisions.md]
Branché automatiquement par install_hook.sh dans le hook post-commit.
"""
import argparse
import re
import subprocess
from datetime import date

SEUIL_LIGNES = 40


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def commit_is_significant():
    stat = git("diff", "--shortstat", "HEAD~1", "HEAD")
    name_status = git("diff", "--name-status", "HEAD~1", "HEAD")
    created_or_deleted = any(line.startswith(("A\t", "D\t")) for line in name_status.splitlines())

    m = re.search(r"(\d+) insertion.*?(\d+) deletion", stat) or re.search(r"(\d+) insertion", stat)
    total_lines = 0
    for n in re.findall(r"(\d+) (?:insertion|deletion)", stat):
        total_lines += int(n)

    return created_or_deleted or total_lines > SEUIL_LIGNES, name_status.splitlines()


def build_draft(files):
    msg = git("log", "-1", "--pretty=%s").strip()
    today = date.today().isoformat()
    file_list = "\n".join(f"  - {f}" for f in files) or "  - (aucun)"
    return f"""### [{today}] BROUILLON — {msg}
- Fichiers touchés :
{file_list}
- Contexte : [à remplir — pourquoi ce changement ?]
- Décision : [à remplir]
- Alternative écartée : [à remplir, ou supprimer cette ligne si aucune]

"""


def insert_draft(path, draft):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    marker = "## Historique\n"
    if marker in content:
        content = content.replace(marker, marker + "\n" + draft, 1)
    else:
        content += "\n" + draft
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", default="decisions.md")
    args = parser.parse_args()

    try:
        significant, files = commit_is_significant()
    except subprocess.CalledProcessError:
        return  # pas assez d'historique (ex: premier commit) — on ignore silencieusement

    if not significant:
        return

    draft = build_draft(files)
    insert_draft(args.decisions, draft)
    print("Brouillon ajouté dans decisions.md — à compléter ou supprimer.")


if __name__ == "__main__":
    main()
