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

SHOWCASE_REG_URL = 'https://ucdavis.co1.qualtrics.com/jfe/form/SV_1NvJvbejIFfjleR'
DUE_DATES = \
    {
     'mem_01': '2018-01-12 22:00:00',
     'mem_02': '2018-01-26 22:00:00',
     'mem_03': '2018-02-02 22:00:00',
     'mem_04': '2018-03-02 22:00:00',
     'rep_01': '2018-02-16 22:00:00',
     'rep_02': '2018-03-19 22:00:00',
     'rep_03': '2018-05-04 22:00:00',
     'rep_04': '2018-06-10 22:00:00',
     'pre_01': '2018-03-05 00:00:00',  # design review 1
     'pre_02': '2018-03-15 00:00:00',  # lightning talk
     'pre_03': '2018-05-25 12:00:00',  # showcase poster
     'pre_04': '2018-06-11 22:00:00',  # design review 2
     'show_reg': '2018-04-27 23:59:59', # showcase registration
     'show': '2018-06-07 13:30:00',  # showcase
     'workroom': '2018-06-15 23:59:59',  # clear workroom
    }
DUE_DATES = {k: datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
             for k, v in DUE_DATES.items()}
