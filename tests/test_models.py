from radar.models import Page


def make_page(**kw):
    base = dict(kind='noticia', slug='x', url='/noticias/x/', title='T', description='D',
                body_html='<p>hola</p>', date=None, updated=None, author='Cristian Arango',
                sources=[], draft=False, word_count=1, extra={})
    base.update(kw)
    return Page(**base)


def test_draft_page_not_indexable():
    assert make_page(draft=True).indexable is False
    assert make_page(draft=False).indexable is True


def test_noindex_extra_not_indexable():
    assert make_page(extra={'noindex': 'si'}).indexable is False
