'''
Generate monthly Atom feed for bookmarks.yml
'''

from datetime import datetime, timezone, timedelta
from pathlib import Path
from textwrap import dedent

from pelican import signals
from pelican.generators import Generator

from . import yaml


def get_generators(pelican):
    return LinkFeedGenerator


def register():
    signals.get_generators.connect(get_generators)


class LinkFeedGenerator(Generator):

    def generate_context(self):
        self.feed_path = self.settings.get('BOOKMARKS_FEED_ATOM', 'feeds/extra/bookmarks.atom.xml')
        self.feed_title = self.settings.get('BOOKMARKS_FEED_TITLE', f'Bookmarks - {self.settings["SITENAME"]}')
        self.feed_template = self.env.from_string(LINKFEED_TEMPLATE)
        self.month_format = self.settings.get('BOOKMARKS_MONTH_FORMAT', '%Y-%m')
        self.bookmarks = Path(self.settings.get('BOOKMARKS_YML', 'bookmarks.yml'))

    def generate_output(self, writer):
        bookmarks = yaml.read(self.settings['PATH'] / self.bookmarks)
        current_month = datetime.now().strftime(self.month_format)
        feed_items = []
        for section in bookmarks:
            if not section.get('links'):
                continue
            if current_month == section['period']:
                continue  # do not add incomplete months to feed
            feed_items.append(LinkFeedItem(
                period=section['period'],
                links=section['links'],
                generator=self,
            ))
        writer.write_feed(
            feed_items,
            self.context,
            feed_title=self.feed_title,
            path=self.feed_path,
        )

def start_of_next_month(dt: datetime) -> datetime:
    '''
    https://stackoverflow.com/a/59199379
    '''
    return (dt.replace(day=1) + timedelta(days=32)).replace(day=1)

class LinkFeedItem:

    def __init__(self, period, links, generator):
        period_parsed = datetime.strptime(period, generator.month_format)
        period_parsed = period_parsed.replace(tzinfo=timezone.utc)
        self.title = period_parsed.strftime('%B %Y')
        self.url = generator.settings.get('SITEURL', '') + '/bookmarks/#' + period
        self.category = 'bookmarks'
        self.date = start_of_next_month(period_parsed)
        self.author = generator.settings.get('AUTHOR', 'Bookmarks')
        self.summary = generator.feed_template.render(links=links)


    def get_content(self, *a, **ka):
        return self.summary


LINKFEED_TEMPLATE = dedent('''
    <ul>
      {% for link in links %}
      <li>
        <p><strong>
        <a href="{{ link.url }}">{{ link.title }}</a>
        {% if link.by|default(False) %}
        by {{ link.by }}
        {% endif %}
        </strong></p>
        {% if link.description|default(False) %}
        {{ link.description|md }}
        {% endif %}
      </li>
      {% endfor %}
    </ul>
    ''')
