#!/usr/bin/env bash
# À lancer une seule fois à la racine du repo git : bash ai/install_hook.sh
set -e
HOOK=".git/hooks/post-commit"
cat > "$HOOK" << 'EOF'
#!/usr/bin/env bash
python .ai/generate_index.py . --out .ai/index.md
python .ai/draft_decision.py --decisions .ai/decisions.md
git add .ai/index.md .ai/decisions.md
git commit --amend --no-edit --no-verify -q || true
EOF
chmod +x "$HOOK"
echo "Hook post-commit installé : .ai/index.md et les brouillons de .ai/decisions.md seront régénérés après chaque commit."
