import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageFont

from radar.covers import CoverSpec, cover_for, cover_svg, og_rel, write_cover_png
from radar.models import Brand, Tool
from tests.helpers import make_page, news

ROOT = Path(__file__).resolve().parent.parent
LOGOS = ROOT / 'static' / 'logos'
FONTS = ROOT / 'static' / 'fonts'
BRANDS = {
    'chatgpt': Brand('chatgpt', 'ChatGPT', '#10a37f', None, 'C'),
    'google': Brand('google', 'Google', '#4285f4', 'google', 'G'),
}
TOOLS = {'chatgpt': Tool(id='chatgpt', name='ChatGPT', cat='ia-general', desc='', price='', level='',
                         platform='', lang='', tags=[], url='https://chatgpt.com/', has_page=True)}


def test_cover_for_kinds():
    ficha = cover_for(make_page(kind='ficha', slug='chatgpt', url='/herramientas/chatgpt/'), BRANDS, TOOLS)
    assert ficha.label == 'ChatGPT' and ficha.brand.id == 'chatgpt' and ficha.symbol is None
    g = cover_for(news('n', 1, extra={'empresa': 'google'}), BRANDS, TOOLS)
    assert g.label == 'Google' and g.brand.id == 'google'
    plain = cover_for(news('n', 1), BRANDS, TOOLS)
    assert plain.label == 'Noticia' and plain.brand is None and plain.symbol is None
    assert cover_for(make_page(kind='comparativa'), BRANDS, TOOLS) == CoverSpec('Comparativa', None, 'star')
    assert cover_for(make_page(kind='guia'), BRANDS, TOOLS) == CoverSpec('Guía', None, 'book')
    assert cover_for(make_page(kind='pagina'), BRANDS, TOOLS) == CoverSpec('Radar IA', None, None)
    assert cover_for(make_page(kind='utilidad'), BRANDS, TOOLS) == CoverSpec('Radar IA', None, None)


def test_ficha_without_brand_uses_tool_name():
    tools = dict(TOOLS, rara=Tool(id='rara', name='Rara AI', cat='x', desc='', price='', level='',
                                  platform='', lang='', tags=[], url='https://x/', has_page=True))
    spec = cover_for(make_page(kind='ficha', slug='rara', url='/herramientas/rara/'), BRANDS, tools)
    assert spec == CoverSpec('Rara AI', None, None)


def test_cover_svg_escapes_label_and_is_wellformed():
    svg = str(cover_svg(CoverSpec('A & B <x> «c»', None, None), LOGOS))
    ET.fromstring(svg)
    assert 'A &amp; B &lt;X&gt; «C»' in svg and '&amp;amp;' not in svg
    assert 'viewBox="0 0 1200 630"' in svg


def test_cover_svg_with_icon_and_symbols_are_wellformed():
    for spec in (CoverSpec('Google', BRANDS['google'], None), CoverSpec('ChatGPT', BRANDS['chatgpt'], None),
                 CoverSpec('Comparativa', None, 'star'), CoverSpec('Guía', None, 'book')):
        ET.fromstring(str(cover_svg(spec, LOGOS)))
    assert '#4285f4' in str(cover_svg(CoverSpec('Google', BRANDS['google'], None), LOGOS))


def test_cover_svg_has_no_ids():
    # Varias portadas en la misma página no deben repetir atributos id.
    assert ' id="' not in str(cover_svg(CoverSpec('Google', BRANDS['google'], None), LOGOS))


def test_og_rel():
    assert og_rel('/') == 'og/inicio.png'
    assert og_rel('/noticias/x/') == 'og/noticias/x.png'
    assert og_rel('/mejor-ia-gratis/') == 'og/mejor-ia-gratis.png'


def test_write_cover_png_size(tmp_path):
    for i, spec in enumerate((CoverSpec('OpenAI', BRANDS['chatgpt'], None), CoverSpec('Comparativa', None, 'star'),
                              CoverSpec('Guía', None, 'book'), CoverSpec('Radar IA', None, None))):
        dest = tmp_path / 'sub' / f'{i}.png'
        write_cover_png(spec, dest, FONTS)
        with Image.open(dest) as im:
            assert im.size == (1200, 630) and im.mode == 'RGB'


def test_fonts_load_with_pillow():
    fonts = list(FONTS.glob('*.woff2'))
    assert len(fonts) == 7
    for f in fonts:
        ImageFont.truetype(str(f), 20)
