#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os.path import join, expanduser
from datetime import datetime

AUTHOR = u'Jason K. Moore'
SITENAME = u'EME 185: Mechanical Systems Design Project'
SITEURL = ''
YEAR = '2019'
LECTURE_ROOM = 'California Hall 1100'

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

# Manually curate the top bar menu
DISPLAY_PAGES_ON_MENU = False

MENUITEMS =[('Syllabus', ''),
            ('Schedule', '/pages/schedule.html'),
            ('Assignments', '/pages/assignments.html'),
            ('Projects', 'https://www.moorepants.info/jkm/courses/eme185-2018/pages/projects.html'),
            ('Resources', '/pages/resources.html')]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

SHOWCASE_REG_URL = 'https://'
DUE_DATES = \
    {
     'mem_01': '2019-01-11 23:59:59',
     'mem_02': '2019-01-25 23:59:59',
     'mem_03': '2019-02-01 23:59:59',
     'mem_04': '2019-03-01 23:59:59',
     'rep_01': '2019-02-15 23:59:59',
     'rep_02': '2019-03-18 23:59:59',
     'rep_03': '2019-05-03 23:59:59',
     'rep_04': '2019-06-09 23:59:59',
     'pre_01': '2019-03-04 00:00:00',  # design review 1
     'pre_02': '2019-03-14 00:00:00',  # lightning talk
     'pre_03': '2019-05-24 12:00:00',  # showcase poster
     'pre_04': '2019-06-10 23:59:59',  # design review 2
     'show_reg': '2019-04-19 23:59:59',  # showcase registration
     'show': '2019-06-06 13:00:00',  # showcase
     'workroom': '2019-06-14 23:59:59',  # clear workroom
    }
DUE_DATES = {k: datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
             for k, v in DUE_DATES.items()}
