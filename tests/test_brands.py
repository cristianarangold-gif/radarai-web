import json
from pathlib import Path

import pytest

from radar.brands import icon_path, load_brands, logo_html

ROOT = Path(__file__).resolve().parent.parent


def setup(tmp_path, brands):
    (tmp_path / 'brands.json').write_text(json.dumps(brands), encoding='utf-8')
    logos = tmp_path / 'logos'
    logos.mkdir()
    (logos / 'openai.svg').write_text(
        '<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
        '<title>OpenAI</title><path d="M1 1z"/></svg>', encoding='utf-8')
    return load_brands(tmp_path / 'brands.json', logos), logos


BASE = {
    'chatgpt': {'name': 'ChatGPT', 'color': '#10a37f', 'icon': 'openai', 'monograma': 'C'},
    'runway': {'name': 'Runway', 'color': '#151515', 'icon': 'runway', 'monograma': 'R'},
    'hf': {'name': 'Hugging Face', 'color': '#ffd21e', 'icon': None, 'monograma': 'H'},
}


def test_load_brands_reads_color_icon_and_monogram(tmp_path):
    b, _ = setup(tmp_path, BASE)
    assert b['chatgpt'].icon == 'openai' and b['chatgpt'].color == '#10a37f'
    assert b['chatgpt'].name == 'ChatGPT' and b['chatgpt'].monograma == 'C' and b['chatgpt'].id == 'chatgpt'


def test_missing_logo_file_falls_back_to_monogram(tmp_path):
    b, logos = setup(tmp_path, BASE)
    assert b['runway'].icon is None
    html = str(logo_html(b['runway'], 40, logos))
    assert '>R<' in html and '<svg' not in html


def test_bad_color_raises(tmp_path):
    with pytest.raises(ValueError, match='color'):
        setup(tmp_path, {'x': {'name': 'X', 'color': 'verde', 'icon': None, 'monograma': 'X'}})


def test_missing_monogram_raises(tmp_path):
    with pytest.raises(ValueError, match='monograma'):
        setup(tmp_path, {'x': {'name': 'X', 'color': '#000000', 'icon': None}})


def test_icon_path_reads_first_path(tmp_path):
    b, logos = setup(tmp_path, BASE)
    assert icon_path(b['chatgpt'], logos) == 'M1 1z'
    assert icon_path(b['hf'], logos) is None


def test_logo_html_inlines_path_white_on_brand(tmp_path):
    b, logos = setup(tmp_path, BASE)
    html = str(logo_html(b['chatgpt'], 40, logos))
    assert 'd="M1 1z"' in html and '--brand:#10a37f' in html and 'aria-hidden="true"' in html
    assert 'fill="#fff"' in html and 'width:40px' in html


def test_logo_on_light_brand_uses_dark_ink(tmp_path):
    b, logos = setup(tmp_path, BASE)
    assert 'color:#151515' in str(logo_html(b['hf'], 40, logos))


def test_real_brands_file_is_valid():
    b = load_brands(ROOT / 'data' / 'brands.json', ROOT / 'static' / 'logos')
    assert {'chatgpt', 'claude', 'gemini', 'midjourney', 'perplexity', 'openai', 'google', 'anthropic'} <= b.keys()
    assert b['claude'].icon == 'claude'
