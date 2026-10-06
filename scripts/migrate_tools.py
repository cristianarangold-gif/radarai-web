"""Migración única: extrae el objeto TOOLS del index.html antiguo a data/tools.json.

Uso: python scripts/migrate_tools.py [ruta_index_html]
Por defecto lee index.html de la rama main con `git show`.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALIASES = {
    'IA general': 'ia-general', 'Escritura': 'escritura', 'Imágenes': 'imagenes',
    'Vídeo': 'video', 'Audio y música': 'audio', 'Programación': 'programacion',
    'Educación': 'educacion', 'Marketing': 'marketing', 'Productividad': 'productividad',
}


def extract_tools(html: str) -> dict:
    start = html.find('const TOOLS')
    start = html.find('{', start)
    end = html.find('\n};', start)
    literal = html[start:end + 2]
    as_json = re.sub(r'(?<=[{,])\s*(\w+):', r'"\1":', literal)
    tools = json.loads(as_json)
    for t in tools.values():
        t['cat'] = ALIASES.get(t['cat'], t['cat'])
    return dict(sorted(tools.items()))


def main():
    if len(sys.argv) > 1:
        html = Path(sys.argv[1]).read_text(encoding='utf-8')
    else:
        html = subprocess.run(['git', 'show', 'main:index.html'], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout
    tools = extract_tools(html)
    out = ROOT / 'data' / 'tools.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(tools, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'OK: {len(tools)} herramientas -> {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
