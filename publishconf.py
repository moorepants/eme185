#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://moorepants.github.io/eme185'
RELATIVE_URLS = False

FEED_ATOM = None
FEED_RSS = None

DELETE_OUTPUT_DIRECTORY = True

MENUITEMS =[('Syllabus', '/eme185/pages/syllabus.html'),
            ('Schedule', '/eme185/pages/schedule.html'),
            ('Assignments', '/eme185/pages/assignments.html'),
            ('Projects', 'https://www.moorepants.info/jkm/courses/eme185-2018/pages/projects.html'),
            ('Resources', '/eme185/pages/resources.html')]

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
GOOGLE_ANALYTICS = "UA-15966419-8"
