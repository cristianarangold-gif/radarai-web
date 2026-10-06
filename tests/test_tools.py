import json
from pathlib import Path

from radar.tools import CATEGORIES, load_tools

ROOT = Path(__file__).resolve().parent.parent
CAT_KEYS = {k for k, _ in CATEGORIES}


def test_catalog_has_126_tools_with_required_fields(tmp_path):
    tools = load_tools(ROOT / 'data' / 'tools.json', tmp_path)
    assert len(tools) == 126
    for tid, t in tools.items():
        assert t.id == tid
        assert t.name.strip(), tid
        assert t.url.startswith('https://'), tid
        assert t.cat in CAT_KEYS, (tid, t.cat)


def test_no_literal_unicode_escapes():
    raw = (ROOT / 'data' / 'tools.json').read_text(encoding='utf-8')
    assert '\\u' not in raw
    data = json.loads(raw)
    assert data['runway']['desc'].count('vídeo') == 1


def test_has_page_flag(tmp_path):
    (tmp_path / 'herramientas').mkdir()
    (tmp_path / 'herramientas' / 'claude.md').write_text('titulo: Claude\n\nx', encoding='utf-8')
    tools = load_tools(ROOT / 'data' / 'tools.json', tmp_path)
    assert [t for t in tools if tools[t].has_page] == ['claude']


def test_every_ficha_id_exists_in_catalog():
    ids = set(json.loads((ROOT / 'data' / 'tools.json').read_text(encoding='utf-8')))
    fichas = {p.stem for p in (ROOT / 'content' / 'herramientas').glob('*.md')}
    assert fichas <= ids, fichas - ids


def test_every_utility_has_app_js_entry():
    import re
    app = (ROOT / 'static' / 'utilidades' / 'app.js').read_text(encoding='utf-8')
    for md in (ROOT / 'content' / 'utilidades').glob('*.md'):
        tool = re.search(r'data-tool="([a-z-]+)"', md.read_text(encoding='utf-8')).group(1)
        assert tool == md.stem
        assert f"'{tool}':[" in app, tool
