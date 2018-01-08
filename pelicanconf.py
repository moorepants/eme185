#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os.path import join, expanduser
from datetime import datetime

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
PLUGIN_PATHS = [join(expanduser("~"), 'src', 'pelican-plugins'),
                'pelican-plugins',  # for travis-ci
                'plugins']
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
DUE_DATES = \
    {
     'memo_01': '2018-01-12 22:00:00',
     'memo_02': '2018-01-26 22:00:00',
     'memo_03': '2018-02-02 22:00:00',
     'memo_04': '2018-02-09 22:00:00',
     'memo_05': '2018-03-02 22:00:00',
     'report_01': '2018-02-16 22:00:00',
     'report_02': '2018-03-19 22:00:00',
     'report_03': '2018-05-04 22:00:00',
     'report_04': '2018-06-10 22:00:00',
    }
DUE_DATES = {k: datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
             for k, v in DUE_DATES.items()}
