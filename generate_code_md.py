import os

EXTENSIONS = {".py", ".html", ".scss", ".js", ".txt", ".env"}
SPECIAL_FILES = {".gitignore", ".env"}
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", "venv", ".venv"}

OUTPUT_FILE = "code.md"

def should_process(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXTENSIONS or filename in SPECIAL_FILES:
        return True
    return False

def generate_markdown():
    markdown_content = "# Code Source du Projet\n\nCe fichier regroupe l'ensemble du code source du projet par fichier.\n\n"
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in sorted(files):
            if should_process(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.normpath(file_path)
                if relative_path.startswith("./") or relative_path.startswith(".\\"):
                    relative_path = relative_path[2:]
                
                ext = os.path.splitext(file)[1].lower()
                lang_map = {
                    ".py": "python", ".html": "html", ".scss": "scss",
                    ".js": "javascript", ".env": "env", ".gitignore": "gitignore", ".txt": "text"
                }
                lang = lang_map.get(ext, "")
                
                markdown_content += f"## Fichier : `{relative_path}`\n"
                markdown_content += f"Dossier : `{root}`\n\n"
                markdown_content += f"```{lang}\n"
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        markdown_content += f.read()
                except Exception as e:
                    markdown_content += f"# Erreur de lecture du fichier : {e}\n"
                
                markdown_content += "\n```\n\n---\n\n"
                
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(markdown_content)
    
    print(f"[Automation] {OUTPUT_FILE} mis à jour avec succès.")

if __name__ == "__main__":
    generate_markdown()