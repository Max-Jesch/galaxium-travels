import os
import sys
import subprocess
import fnmatch

# Source directory for raw md files
SOURCE_DIR = '97_raw_markdown_files'

# Hardcoded ignore list (patterns relative to SOURCE_DIR, applied to relative path)
IGNORE_LIST = [
    'README.md',
    '*database*',
]

def is_ignored(rel_path):
    for pattern in IGNORE_LIST:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

# Recursively find all .md files in SOURCE_DIR, excluding ignore list
md_files = []
for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.endswith('.md'):
            rel_path = os.path.relpath(os.path.join(root, file), SOURCE_DIR)
            if not is_ignored(rel_path):
                md_files.append((os.path.join(root, file), rel_path))

if not md_files:
    print('No Markdown files found.')
    sys.exit(0)

print(f'Found {len(md_files)} Markdown files to convert.')

success = 0
fail = 0
for src_path, rel_path in md_files:
    pdf_rel_path = os.path.splitext(rel_path)[0] + '.pdf'
    pdf_out_path = os.path.join('.', pdf_rel_path)
    os.makedirs(os.path.dirname(pdf_out_path), exist_ok=True)
    print(f'Converting {src_path} -> {pdf_out_path}')
    try:
        subprocess.run([
            sys.executable, '98_utils/md_to_pdf_weasy.py',
            src_path, pdf_out_path
        ], check=True)
        success += 1
    except subprocess.CalledProcessError:
        print(f'Failed to convert {src_path}')
        fail += 1

print(f'\nConversion complete. {success} succeeded, {fail} failed.') 