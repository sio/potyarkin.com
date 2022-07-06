import os, sys
sys.path.append(os.curdir)


# Page generator configuration
PATH = 'content'
DEFAULT_CATEGORY= 'posts'
LOCALE = 'en_GB.UTF-8'
DEFAULT_LANG = 'EN'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

# Special paths inside content/
ARTICLE_PATHS = [
    'posts',
    ]
PAGE_PATHS = [
    'pages',
    'blogroll.md',
    'bookmarks.md',
    'webring.md',
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
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            'anchorlink': True,
            'title': 'Contents',
        },
        'markdown.extensions.sane_lists': {},
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
CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'
CATEGORIES_URL = ''
CATEGORIES_SAVE_AS = ''
AUTHOR_URL = ''
AUTHOR_SAVE_AS = ''
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

DEFAULT_PAGINATION = 10

# Pelican plugins
import microblog.pelican
PLUGINS = [
    microblog.pelican,
    'neighbors',
    ]

# Configuring current theme
from pelican.themes import smallweb
THEME = smallweb.path()
THEME_TEMPLATES_OVERRIDES = ['content/templates/']
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = [(name.title(), url) for name, url in SOCIAL]
MENUITEMS.append(('feed', '/feeds/'))
MENUITEMS.append(('bookmarks', '/bookmarks/'))
SMALLWEB_HASHES = smallweb.hashes()
SMALLWEB_COLORS = smallweb.colors()
from helpers import checksum
CSS_OVERRIDE = [
    f'static/custom.css?cache={checksum.hash("content/static/custom.css")}',
]


# Jinja2 customization

import helpers.json
import helpers.yaml
JINJA_GLOBALS = {
    'json': helpers.json.read,
    'yaml': helpers.yaml.read,
}

from datetime import datetime
import helpers.markdown
JINJA_FILTERS = {
    'md': helpers.markdown.custom(MARKDOWN),
    'strftime': datetime.strftime,
    'strptime': datetime.strptime,
}


# Microblog
import microblog.storage
MICROBLOG = microblog.storage.GitStorage('./micro/')
