import os
import re
import argparse
from bs4 import BeautifulSoup

EXTENSIONS = {'.py', '.html', '.scss', '.css', '.js'}
IGNORE_DIRS = {'venv', '__pycache__', '.git', 'node_modules', 'instance', '.ai'}


def match_feature(filepath, keywords):
    path_lower = filepath.lower()
    return any(kw.lower() in path_lower for kw in keywords)


def extract_html_by_class(content, classes, tags=None):
    soup = BeautifulSoup(content, 'html.parser')
    blocks = []

    if tags:
        for tag_name in tags:
            for tag in soup.find_all(tag_name):
                blocks.append(tag.prettify())

    if classes:
        for cls in classes:
            for tag in soup.find_all(class_=re.compile(rf'\b{re.escape(cls)}\b')):
                if not any(str(tag) in b for b in blocks):
                    blocks.append(tag.prettify())

    return '\n\n'.join(blocks)


def extract_css_js_section(content, keywords):
    lines = content.splitlines()
    matched_blocks = []
    buffer = []
    depth = 0
    capturing = False

    for line in lines:
        if not capturing and any(kw.lower() in line.lower() for kw in keywords):
            capturing = True
            buffer = [line]
            depth = line.count('{') - line.count('}')
            if depth <= 0 and '{' not in line:
                matched_blocks.append(line)
                capturing = False
            continue

        if capturing:
            buffer.append(line)
            depth += line.count('{') - line.count('}')
            if depth <= 0:
                matched_blocks.append('\n'.join(buffer))
                capturing = False
                buffer = []

    return '\n\n'.join(matched_blocks)


def generate_code_md(root_dir, keywords, classes, tags, output_file, full_file_mode):
    header_parts = []
    if keywords:
        header_parts.append(f"mots-clés : {', '.join(keywords)}")
    if classes:
        header_parts.append(f"classes : {', '.join(classes)}")
    if tags:
        header_parts.append(f"tags : {', '.join(tags)}")

    output_lines = [f"# Code extrait — {' | '.join(header_parts)}\n"]
    blocks_found = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext not in EXTENSIONS:
                continue

            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_dir)

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (UnicodeDecodeError, PermissionError):
                continue

            file_matches_name = keywords and match_feature(rel_path, keywords)

            if file_matches_name:
                output_lines.append(f"\n## {rel_path}\n```{ext.lstrip('.')}\n{content}\n```")
                blocks_found += 1
                continue

            if not full_file_mode:
                if ext == '.html' and (classes or tags):
                    section = extract_html_by_class(content, classes, tags)
                    if section.strip():
                        output_lines.append(f"\n## {rel_path} (extrait HTML)\n```html\n{section}\n```")
                        blocks_found += 1

                elif ext in {'.scss', '.css', '.js'} and (classes or keywords):
                    search_terms = (classes or []) + (keywords or [])
                    section = extract_css_js_section(content, search_terms)
                    if section.strip():
                        output_lines.append(f"\n## {rel_path} (extrait)\n```{ext.lstrip('.')}\n{section}\n```")
                        blocks_found += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"✅ {output_file} généré — {blocks_found} bloc(s) trouvé(s)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extrait le code lié à une fonctionnalité du projet EasyMarket.")
    parser.add_argument('--root', default='.', help="Racine du projet (par défaut : dossier courant)")
    parser.add_argument('--keywords', nargs='*', default=[], help="Mots-clés dans le nom de fichier (ex: vendeur boutique)")
    parser.add_argument('--classes', nargs='*', default=[], help="Classes CSS à cibler (ex: footer-link footer-content)")
    parser.add_argument('--tags', nargs='*', default=[], help="Balises HTML à cibler (ex: footer nav)")
    parser.add_argument('--output', default='.ai/code.md', help="Fichier de sortie")
    parser.add_argument('--scan-sections', action='store_true',
                         help="Cherche aussi des blocs/balises précis à l'intérieur des gros fichiers globaux")
    args = parser.parse_args()

    generate_code_md(
        root_dir=args.root,
        keywords=args.keywords,
        classes=args.classes,
        tags=args.tags,
        output_file=args.output,
        full_file_mode=not args.scan_sections
    )