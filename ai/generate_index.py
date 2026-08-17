#!/usr/bin/env python3
"""
Régénère index.md : une arborescence légère du projet + une description
courte par fichier (extraite du premier commentaire/docstring, sinon vide).

But : donner à l'IA une carte du projet qui coûte quasi rien en tokens,
plutôt qu'un dump complet du code à chaque fois. Tu colles ensuite dans le
chat seulement le contenu du/des fichier(s) réellement concernés par la
demande en cours.

Usage :
    python generate_index.py [chemin_du_projet] [--out index.md]

À brancher sur un hook git post-commit (voir install_hook.sh).
"""
import argparse
import os

INCLUDE_EXT = {".py", ".html", ".scss", ".css", ".js", ".txt"}
INCLUDE_NAMES = {".gitignore", ".env.example", "requirements.txt"}
EXCLUDE_DIRS = {".git", "venv", ".venv", "__pycache__", "node_modules", "instance"}
# Ne JAMAIS inclure .env (secrets réels) — seulement .env.example
EXCLUDE_FILES = {".env"}


def first_description_line(path):
    """Retourne la première ligne de commentaire/docstring d'un fichier, sinon ''."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                stripped = line.strip()
                for marker in ('"""', "#", "//", "<!--"):
                    if stripped.startswith(marker):
                        return stripped.lstrip('"#/<!-- ').rstrip('"-->').strip()
    except OSError:
        pass
    return ""


def build_index(root):
    lines = ["# Index du projet\n", "> Généré automatiquement — ne pas éditer à la main.\n"]
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        rel_dir = os.path.relpath(dirpath, root)
        relevant = [
            f for f in sorted(filenames)
            if f not in EXCLUDE_FILES
            and (os.path.splitext(f)[1] in INCLUDE_EXT or f in INCLUDE_NAMES)
        ]
        if not relevant:
            continue
        header = "." if rel_dir == "." else rel_dir
        lines.append(f"\n## {header}/\n")
        for f in relevant:
            full_path = os.path.join(dirpath, f)
            desc = first_description_line(full_path)
            lines.append(f"- `{f}`" + (f" — {desc}" if desc else ""))
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Racine du projet")
    parser.add_argument("--out", default="index.md", help="Fichier de sortie")
    args = parser.parse_args()

    content = build_index(args.root)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"index.md régénéré ({content.count(chr(10))} lignes) -> {args.out}")


if __name__ == "__main__":
    main()
