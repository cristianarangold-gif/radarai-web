"""Valida _site/ y sale con código 1 si hay errores.

Uso: python scripts/check.py [--site _site]
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from radar.check import check_site  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', default=str(ROOT / '_site'))
    errors = check_site(Path(parser.parse_args().site))
    for e in errors:
        print('ERROR:', e)
    if errors:
        print(f'{len(errors)} errores')
        sys.exit(1)
    print('OK: sitio validado sin errores')


if __name__ == '__main__':
    main()
