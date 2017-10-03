#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Vitaly Potyarkin'
BIO = 'Unsorted ramblings, sometimes related to programming'
SITENAME = 'Randomize'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'EN'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = [
    ('calendar', '/archive/'),
    ('tags', '/tags.html'),
    ('email', 'mailto:sio.wtf@gmail.com'),
    ('github', 'https://github.com/sio'),
    ]

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Custom configuration for potyarkin.ml
LOCALE = "C"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATE = "fs"  # get post's date from filesystem

STATIC_PATHS = [
    'images',
    'static',
    'static/CNAME'
    ]
EXTRA_PATH_METADATA = {
    'static/CNAME': {'path': 'CNAME'},
    }

ARTICLE_PATHS = ['posts',]
ARTICLE_URL = '{category}/{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{slug}/index.html'
ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Configuring current theme
THEME = "themes/attila"
CSS_OVERRIDE = ["static/attila_override.css"]
HEADER_COLOR = "rgb(242,106,61)"
MENUITEMS = [(name.title(), url) for name, url in SOCIAL]
SOCIAL.append(("feed", "docs/feeds/all.atom.xml"))

PLUGIN_PATHS = [
    'plugins/pelican-plugins']
PLUGINS = [
    ]
SHARE_BUTTONS = [
    'reddit',
    'facebook',
    'twitter',
    ]
