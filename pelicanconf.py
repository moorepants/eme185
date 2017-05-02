#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os.path import join, expanduser

AUTHOR = u'Jason K. Moore'
SITENAME = u'EME 185: Mechanical Systems Design Project'
SITEURL = ''

PATH = 'content'
THEME = 'theme'
PAGE_ORDER_BY = 'sortorder'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = u'en'

TEMPLATE_PAGES = {'projects.html': 'projects.html'}

STATIC_PATHS = ['images', 'docs']

# NOTE: The order here is important. The last item is the first to be searched
# it seems.
PLUGIN_PATHS = [join(expanduser("~"), 'src', 'pelican-plugins'), "plugins"]
PLUGINS = ['neighbors', 'render_math', 'headerid', 'jinja2content']

# headerid options
HEADERID_LINK_CHAR = "¶"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

IGNORE_FILES = ['README*']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

POSTER_DUE_DATE = 'May 25, 2017 12 PM'
SHOWCASE_REG_DATE = 'April 28, 2017'
SHOWCASE_REG_URL = 'https://goo.gl/forms/IVpYlkIAlfUYblw32'
