#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jason K. Moore'
SITENAME = u'EME 185: Mechanical Systems Design Project'
SITEURL = ''

PATH = 'content'
THEME = 'theme'
PAGE_ORDER_BY = 'sortorder'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = u'en'

TEMPLATE_PAGES = {'projects.html': 'projects.html'}

PLUGIN_PATHS = ['plugins', '/moorepants/src/pelican-plugins']
PLUGINS = ['neighbors']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
