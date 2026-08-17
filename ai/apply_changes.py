#!/usr/bin/env python3
"""
Applique au projet le code renvoye par l'IA. Deux formats supportes :

1) Fichier neuf ou remplacement complet :
    ### FILE: chemin/vers/fichier.ext
    <code complet>
    ### END FILE

2) Modification ciblee d'un fichier existant (mode par defaut pour les
   petits changements -- deplacement, design, etc.) :
    ### FILE: chemin/vers/fichier.ext [PATCH]
    ### REPLACE
    <extrait exact a remplacer, avec assez de contexte pour etre unique>
    ### WITH
    <nouveau contenu>
    ### END FILE

Usage :
    python apply_changes.py response.md            # apercu seul
    python apply_changes.py response.md --apply     # ecrit reellement
"""
import argparse
import os
import re

BLOCK_RE = re.compile(
    r"### FILE:\s*(?P<path>\S+)\s*(?P<flag>\[PATCH\])?\s*\n(?P<body>.*?)\n### END FILE",
    re.DOTALL,
)
PATCH_RE = re.compile(
    r"### REPLACE\s*\n(?P<old>.*?)\n### WITH\s*\n(?P<new>.*)",
    re.DOTALL,
)


def strip_fences(text):
    text = text.strip("\n")
    lines = text.split("\n")
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)


def parse_blocks(text):
    blocks = []
    for m in BLOCK_RE.finditer(text):
        path = m.group("path").strip()
        is_patch = bool(m.group("flag"))
        body = m.group("body")
        if is_patch:
            pm = PATCH_RE.search(body)
            if not pm:
                blocks.append((path, "error", "Mode [PATCH] declare mais ### REPLACE / ### WITH introuvables ou mal formes.", None))
                continue
            old = strip_fences(pm.group("old"))
            new = strip_fences(pm.group("new"))
            blocks.append((path, "patch", old, new))
        else:
            blocks.append((path, "full", strip_fences(body) + "\n", None))
    return blocks


def resolve_patch(path, old, new):
    if not os.path.exists(path):
        return None, f"Fichier introuvable : {path} (le mode PATCH suppose un fichier existant)"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    count = content.count(old)
    if count == 0:
        return None, "L'extrait a remplacer ('### REPLACE') ne correspond a rien dans le fichier -- copie exacte requise."
    if count > 1:
        return None, f"L'extrait apparait {count} fois dans le fichier -- elargis-le pour le rendre unique."
    return content.replace(old, new, 1), None


def preview(path, mode, a, b):
    print(f"\n{'=' * 60}")
    if mode == "error":
        print(f"ERREUR sur {path} : {a}")
        return
    if mode == "full":
        exists = os.path.exists(path)
        print(f"{'REMPLACE ENTIEREMENT' if exists else 'NOUVEAU'} : {path}")
        print("-" * 60)
        print(a[:400] + ("..." if len(a) > 400 else ""))
    else:  # patch
        print(f"MODIFICATION CIBLEE : {path}")
        result, err = resolve_patch(path, a, b)
        if err:
            print(f"  -> {err}")
        else:
            print("  -> extrait localise, remplacement pret")


def apply(path, mode, a, b, backup):
    if mode == "full":
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if backup and os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                old_full = f.read()
            with open(path + ".bak", "w", encoding="utf-8") as f:
                f.write(old_full)
        with open(path, "w", encoding="utf-8") as f:
            f.write(a)
        print(f"Ecrit (complet) : {path}")
    elif mode == "patch":
        result, err = resolve_patch(path, a, b)
        if err:
            print(f"Ignore ({path}) : {err}")
            return
        if backup:
            with open(path + ".bak", "w", encoding="utf-8") as f:
                with open(path, "r", encoding="utf-8", errors="ignore") as f2:
                    f.write(f2.read())
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Ecrit (patch) : {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("response_file")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()

    with open(args.response_file, "r", encoding="utf-8") as f:
        text = f.read()

    blocks = parse_blocks(text)
    if not blocks:
        print("Aucun bloc '### FILE: ...' trouve. Verifie le format de la reponse.")
        return

    for path, mode, a, b in blocks:
        preview(path, mode, a, b)

    valid = [blk for blk in blocks if blk[1] != "error"]
    if not args.apply:
        print(f"\n{len(valid)} fichier(s) valide(s) sur {len(blocks)}. Apercu seul -- relance avec --apply pour ecrire.")
        return

    confirm = input(f"\nAppliquer ces {len(valid)} fichier(s) ? [o/N] ").strip().lower()
    if confirm != "o":
        print("Annule.")
        return

    for path, mode, a, b in blocks:
        if mode == "error":
            continue
        apply(path, mode, a, b, backup=not args.no_backup)


if __name__ == "__main__":
    main()
