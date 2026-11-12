"""Comprueba el tuit del día y genera su enlace de «publicar con un toque» en X.

Uso: python scripts/tweet.py social/x/AAAA-MM-DD.md
Si el tuit es válido, imprime el enlace https://x.com/intent/post?... y sale con 0.
Si no, imprime cada problema y sale con 1: corrige el archivo y vuelve a ejecutarlo.
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List

SITE = 'https://radarai.es/'
LIMIT = 280
LINK_WEIGHT = 23  # X cuenta cualquier enlace como 23 caracteres.
TYPES = {'noticia', 'disponibilidad', 'precios', 'comparativa', 'prompt', 'guia', 'glosario', 'utilidad', 'profesion'}
HASHTAG = re.compile(r'(?<!\w)#\w+')


def parse_tweet(raw: str) -> Dict[str, str]:
    """Metadatos «clave: valor» hasta la primera línea en blanco; después, el texto del tuit."""
    head, _, body = raw.strip().partition('\n\n')
    tweet = {}
    for line in head.splitlines():
        key, sep, value = line.partition(':')
        if sep:
            tweet[key.strip()] = value.strip()
    tweet['texto'] = body.strip()
    return tweet


def weighted_length(text: str) -> int:
    """Longitud tal como la cuenta X: letras latinas (con tildes) valen 1; emojis y otros símbolos, 2."""
    total, skip = 0, False
    for ch in text:
        cp = ord(ch)
        if skip:
            skip = False
            continue
        if cp in (0xFE0E, 0xFE0F) or 0x1F3FB <= cp <= 0x1F3FF:
            continue  # variantes de presentación y tonos de piel no suman
        if cp == 0x200D:
            skip = True  # un emoji compuesto cuenta como uno solo
            continue
        light = cp <= 0x10FF or 0x2000 <= cp <= 0x200D or 0x2010 <= cp <= 0x201F or 0x2032 <= cp <= 0x2037
        total += 1 if light else 2
    return total


def is_live(url: str) -> bool:
    req = urllib.request.Request(url.split('#', 1)[0], headers={'User-Agent': 'RadarIA-tuit/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status == 200
    except (urllib.error.URLError, OSError):
        return False


def problems(tweet: Dict[str, str], live: Callable[[str], bool] = is_live) -> List[str]:
    found = [f'falta el metadato «{key}»' for key in ('fecha', 'tipo', 'url') if not tweet.get(key)]
    text, url = tweet.get('texto', ''), tweet.get('url', '')
    if tweet.get('tipo') and tweet['tipo'] not in TYPES:
        found.append(f'tipo desconocido «{tweet["tipo"]}»; usa uno de: {", ".join(sorted(TYPES))}')
    if not text:
        found.append('falta el texto del tuit')
    total = weighted_length(text) + 1 + LINK_WEIGHT
    if total > LIMIT:
        found.append(f'ocupa {total} caracteres con el enlace; el máximo es {LIMIT}')
    tags = len(HASHTAG.findall(text))
    if not 1 <= tags <= 2:
        found.append(f'lleva {tags} hashtags; pon uno o dos')
    if re.search(r'https?://|radarai\.es', text):
        found.append('no escribas el enlace en el texto: va en el metadato «url» y X lo añade al final')
    if url and not url.startswith(SITE):
        found.append(f'el enlace debe ser una página de radarai.es ({SITE}...)')
    elif url and not live(url):
        found.append(f'{url} no responde con 200: enlaza solo páginas ya publicadas')
    return found


def intent_link(tweet: Dict[str, str]) -> str:
    return 'https://x.com/intent/post?' + urllib.parse.urlencode({'text': tweet['texto'], 'url': tweet['url']})


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    tweet = parse_tweet(Path(sys.argv[1]).read_text(encoding='utf-8'))
    found = problems(tweet)
    if found:
        for problem in found:
            print(f'- {problem}')
        return 1
    print(intent_link(tweet))
    return 0


if __name__ == '__main__':
    sys.exit(main())
