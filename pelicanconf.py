#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Page generator configuration
PATH = 'content'
LOCALE = 'C'
DEFAULT_LANG = 'EN'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_DATE = 'fs'  # get post's date from filesystem

# Special paths inside content/
ARTICLE_PATHS = [
    'posts',
    ]
STATIC_PATHS = [
    'images',
    'static',
    ]
EXTRA_PATH_METADATA = {
    'static/CNAME': {'path': 'CNAME'},
    'static/README-for-docs.md': {'path': 'README.md'},
    }

# Cleaner URL paths
ARTICLE_URL = '{category}/{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'

# Custom configuration for potyarkin.ml
AUTHOR = 'Vitaly Potyarkin'
BIO = 'Unsorted ramblings, sometimes related to programming'
SITENAME = 'Randomize'
SITEURL = ''
TIMEZONE = 'Europe/Moscow'

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
    ('archive', '/archive/'),
    ('tags', '/tags.html'),
    ('email', 'mailto:sio.wtf@gmail.com'),
    ('github', 'https://github.com/sio'),
    ]

DEFAULT_PAGINATION = 5

# Pelican plugins
PLUGIN_PATHS = [
    'plugins/pelican-plugins',
    ]
PLUGINS = [
    ]

# Configuring current theme
THEME = 'themes/attila'
CSS_OVERRIDE = ['static/attila_override.css']
HEADER_COLOR = 'rgb(242,106,61)'
MENUITEMS = [(name.title(), url) for name, url in SOCIAL]
SOCIAL.append(('feed', 'docs/feeds/all.atom.xml'))
