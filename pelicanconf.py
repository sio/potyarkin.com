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
    'resources',
    ]
EXTRA_PATH_METADATA = {
    'static/CNAME': {'path': 'CNAME'},
    'static/favicon.ico': {'path': 'favicon.ico'},
    'static/README-for-docs.md': {'path': 'README.md'},
    'static/google684a6a967bc36817.html': {'path': 'google684a6a967bc36817.html'},
    }

# Markdown customization
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            'anchorlink': True,
            'title': 'Contents',
        },
    },
    'output_format': 'html5',
}

# Cleaner URL paths
ARTICLE_URL = '{category}/{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARCHIVES_URL = 'archive/'
ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_URL = 'archive/{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
TAG_URL = 'tags/{slug}/'
TAG_SAVE_AS = 'tags/{slug}/index.html'
TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_URL = 'category/'
CATEGORIES_SAVE_AS = 'category/index.html'
AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
AUTHORS_SAVE_AS = ''
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/{number}/', '{base_name}/{number}/index.html'),
)

# Custom configuration for potyarkin.ml
AUTHOR = 'Vitaly Potyarkin'
SITENAME = 'Orange Sun'
SITESUBTITLE = 'Unsorted ramblings, sometimes related to programming'
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
    ('tags', '/tags/'),
    ('email', 'mailto:sio.wtf@gmail.com'),
    ('github', 'https://github.com/sio'),
    ]

DEFAULT_PAGINATION = 5

# Pelican plugins
PLUGIN_PATHS = [
    'plugins/pelican-plugins',
    ]
PLUGINS = [
    'neighbors',
    ]

# Configuring current theme
THEME = 'themes/attila'
CSS_OVERRIDE = ['static/attila_override.css']
HEADER_COLOR = 'rgb(242,106,61)'
MENUITEMS = [(name.title(), url) for name, url in SOCIAL]
SOCIAL.append(('feed', '/feeds/all.atom.xml'))
