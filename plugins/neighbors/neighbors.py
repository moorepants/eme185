# -*- coding: utf-8 -*-
"""
Neighbor Articles Plugin for Pelican
====================================

This plugin adds ``next_page`` (newer) and ``prev_page`` (older) variables to
the page's context.
"""
from pelican import signals


def iter3(seq):
    it = iter(seq)
    nxt = None
    cur = next(it)
    for prv in it:
        yield nxt, cur, prv
        nxt, cur = cur, prv
    yield nxt, cur, None


def get_translation(page, prefered_language):
    if not page:
        return None
    for translation in page.translations:
        if translation.lang == prefered_language:
            return translation
    return page


def set_neighbors(pages, next_name, prev_name):
    pages = sorted(pages, key=(lambda x: x.title), reverse=True)
    # make sure we are only using pages from the projects directory
    pages = [p for p in pages if str(p.metadata['category']) == "projects"]
    for nxt, cur, prv in iter3(pages):
        setattr(cur, next_name, nxt)
        setattr(cur, prev_name, prv)

        for translation in cur.translations:
            setattr(translation, next_name,
                    get_translation(nxt, translation.lang))
            setattr(translation, prev_name,
                    get_translation(prv, translation.lang))


def neighbors(generator):
    set_neighbors(generator.hidden_pages, 'next_page', 'prev_page')


def register():
    signals.page_generator_finalized.connect(neighbors)
