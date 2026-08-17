#!/usr/bin/env bash
# À lancer une seule fois à la racine du repo git : bash install_hook.sh
set -e
HOOK=".git/hooks/post-commit"
cat > "$HOOK" << 'EOF'
#!/usr/bin/env bash
python generate_index.py . --out index.md
python draft_decision.py --decisions decisions.md
git add index.md decisions.md
git commit --amend --no-edit --no-verify -q || true
EOF
chmod +x "$HOOK"
echo "Hook post-commit installé : index.md et les brouillons de decisions.md seront régénérés après chaque commit."
