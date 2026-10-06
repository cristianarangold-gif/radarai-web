"""Descarga una vez los iconos de Simple Icons (CC0) que usa data/brands.json.

Uso: python scripts/fetch_logos.py
Guarda cada icono en static/logos/<icono>.svg. Las marcas sin icono usan su monograma.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = '16.34.0'
URL = 'https://cdn.jsdelivr.net/npm/simple-icons@{v}/icons/{icon}.svg'


def main() -> None:
    brands = json.loads((ROOT / 'data' / 'brands.json').read_text(encoding='utf-8'))
    out = ROOT / 'static' / 'logos'
    out.mkdir(parents=True, exist_ok=True)
    for icon in sorted({b['icon'] for b in brands.values() if b.get('icon')}):
        try:
            with urllib.request.urlopen(URL.format(v=VERSION, icon=icon), timeout=15) as r:
                (out / f'{icon}.svg').write_bytes(r.read())
            print(f'OK  {icon}')
        except Exception as exc:  # noqa: BLE001 - informar y seguir
            print(f'ERROR {icon}: {exc}')


if __name__ == '__main__':
    main()
