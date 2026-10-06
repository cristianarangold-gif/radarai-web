from datetime import date

from radar.models import Page


def make_page(**kw):
    base = dict(kind='pagina', slug='x', url='/x/', title='T', description='D',
                body_html='<p>hola</p>', date=None, updated=None, author='Cristian Arango',
                sources=[], draft=False, word_count=1, extra={})
    base.update(kw)
    return Page(**base)


def news(slug, day, **kw):
    kw.setdefault('title', slug)
    return make_page(kind='noticia', slug=slug, url=f'/noticias/{slug}/',
                     date=date(2026, 10, day), **kw)
