"""IndexNow: avisa a Bing y otros buscadores de las páginas nuevas o con fecha cambiada."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

SITE = 'https://radarai.es'
ENDPOINT = 'https://api.indexnow.org/indexnow'
# No es un secreto: el protocolo exige publicarla en la raíz del sitio para demostrar que la web es nuestra.
KEY = '610702d9906c4afcc117b882ccda6058'
KEY_FILE = f'{KEY}.txt'
_NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'


def parse_sitemap(xml: str) -> Dict[str, Optional[str]]:
    """{URL: lastmod o None}. ValueError si el texto no es XML."""
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise ValueError(f'sitemap no válido: {exc}') from exc
    return {row.findtext(f'{_NS}loc'): row.findtext(f'{_NS}lastmod') for row in root.findall(f'{_NS}url')}


def changed_urls(old: Dict[str, Optional[str]], new: Dict[str, Optional[str]]) -> List[str]:
    return sorted(url for url, lastmod in new.items() if url not in old or old[url] != lastmod)


def payload(urls: List[str]) -> dict:
    return {'host': SITE.split('//', 1)[1], 'key': KEY, 'keyLocation': f'{SITE}/{KEY_FILE}', 'urlList': urls}
