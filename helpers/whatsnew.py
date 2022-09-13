'''
Check what's new on sites I've previously bookmarked
'''

import atexit
import json
import logging
import yaml
from collections import defaultdict
from datetime import datetime
from functools import cache
from html.parser import HTMLParser
from itertools import chain
from urllib.parse import urlparse

from feedparser.http import get as http_get
from .webring import CachingFeedReader


log = logging.getLogger(__name__)


NOISY_FEED_DOMAINS = {
    'news.ycombinator.com',
    'pure.mpg.de',
    'queue.acm.org',
}


def main():
    bookmarks_file = 'content/bookmarks.yml'
    cache_dir = 'cache/whatsnew'
    fetch_last_articles = 5

    reader = CachingFeedReader(cache_dir)
    bookmarks = deserialize(bookmarks_file)
    feeds_seen = set()
    output = list()
    for section in bookmarks:
        links = section.get('links')
        if not links:
            continue
        for link in links:
            if not link.get('url'):
                continue
            page = link['url']
            url = urlparse(page)
            site = f'{url.scheme}://{url.netloc}'
            for feed_url in chain(feedlinks(page), feedlinks(site)):
                if feed_url in feeds_seen:
                    continue
                feeds_seen.add(feed_url)
                if urlparse(feed_url).netloc in NOISY_FEED_DOMAINS:
                    continue
                try:
                    feed = reader.feed(title=feed_url, url=feed_url)
                except Exception as exc:
                    log.error('%s while processing feed: %s', exc, feed_url)
                    continue
                entries = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)
                for entry in entries[:fetch_last_articles]:
                    output.append(dict(
                        title=entry.title,
                        url=entry.link,
                        summary=entry.get('summary'),
                        date=list(entry.published_parsed),
                        site=site,
                    ))
    render(output)


def render(output):
    '''Render a simple Markdown document with a list of links'''
    print("# What's new?")
    links_seen = set()
    for link in sorted(output, key=lambda x: x['date'], reverse=True):
        if link['url'] in links_seen:
            continue
        links_seen.add(link['url'])
        date = '-'.join(f'{x:02d}' for x in link['date'][:3])
        print(f'  - **{link["title"]}** ({date})  ')
        print(f'    <{link["url"]}>')
        print()


def persistent_cache(filename, max_age=12*60*60):
    cache = dict()
    try:
        with open(filename) as f:
            cache = json.load(f)
    except (IOError, ValueError):
        pass
    atexit.register(lambda: json.dump(cache, open(filename, 'w'), indent=2, sort_keys=True))
    def decorator(original_function):
        def new_function(*args, **kwargs):
            now = datetime.now().timestamp()
            key = str((args, kwargs))
            if key not in cache \
            or now > cache[key]['timestamp'] + max_age:
                cache[key] = dict(
                    timestamp=now,
                    result=original_function(*args, **kwargs)
                )
            return cache[key]['result']
        return new_function
    return decorator


@persistent_cache('cache/feedlinks.json', max_age=7*24*60*60)
def feedlinks(url):
    '''Return links to RSS/Atom feeds from a web page URL'''
    http = dict()
    page = http_get(url, result=http)
    urlparts = urlparse(url)
    parser = FeedLinkParser()
    try:
        parser.feed(page.decode())
    except Exception as exc:
        log.error('%s while searching for feed links in %s', exc, url)
        return list()
    feeds = set()
    for link in parser.results:
        if link.startswith('/'):  # absolute links
            feeds.add(f'{urlparts.scheme}://{urlparts.netloc}{link}')
        elif '://' not in link:   # relative links
            feeds.add(f'{urlparts.scheme}://{urlparts.netloc}{urlparts.path}/{link}')
        else:
            feeds.add(link)
    return list(feeds)


class FeedLinkParser(HTMLParser):
    def __init__(self, *a, **ka):
        self.results = set()
        super().__init__(*a, **ka)

    def handle_starttag(self, tag, attrs):
        if tag != 'link':
            return
        attrs = dict(attrs)
        link_type = attrs.get('type', '').lower()
        if 'application/atom' not in link_type \
        and 'application/rss' not in link_type:
            return
        self.results.add(attrs['href'].strip())


def deserialize(yamlfile):
    with open(yamlfile) as f:
        return yaml.safe_load(f)


if __name__ == '__main__':
    main()
