import os

# --- CONFIGURATION DE LA TÂCHE ---
# Remplace ici les chemins et le contenu pour chaque nouvelle tâche
TASKS = [
    {
        "file": "frontend/components/ButtonX.js",
        "action": "write", # 'write' pour remplacer tout, 'append' pour ajouter à la fin
        "content": "export const ButtonX = () => <button>Action</button>;"
    },
    {
        "file": "backend/app.py",
        "action": "append",
        "content": "\n@app.route('/action-x')\ndef action_x(): return 'Success'"
    }
]

def apply_updates():
    for task in TASKS:
        try:
            mode = 'w' if task['action'] == 'write' else 'a'
            with open(task['file'], mode) as f:
                f.write(task['content'])
            print(f"✅ Succès : {task['file']} mis à jour.")
        except Exception as e:
            print(f"❌ Erreur sur {task['file']} : {e}")

if __name__ == "__main__":
    apply_updates()