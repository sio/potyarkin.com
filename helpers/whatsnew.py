'''
Check what's new on sites I've previously bookmarked
'''

import atexit
import hashlib
import json
import logging
import yaml
from collections import defaultdict
from datetime import datetime, timezone
from html.parser import HTMLParser
from itertools import chain
from textwrap import dedent
from urllib.parse import urlparse

from feedparser.http import get as http_get
from .webring import CachingFeedReader


log = logging.getLogger(__name__)


NOISY_FEED_DOMAINS = {
    'bigthink.com',
    'en.wikipedia.org',
    'habr.com',
    'news.ycombinator.com',
    'old.reddit.com',
    'pure.mpg.de',
    'queue.acm.org',
    'www.reddit.com',
}
NOISY_URL_PATTERNS = {
    '/#comment',
}
MAX_AGE_DAYS = 365


def main():
    bookmarks_file = 'content/bookmarks.yml'
    bookmarks_checksum = checksum(bookmarks_file)
    render(whatsnew(bookmarks_file, cache_key=bookmarks_checksum))


def render(output, pelican=True):
    '''Render a simple Markdown document with a list of links'''
    title = "What's new? (on the sites I've bookmarked)"
    if pelican:
        print(dedent(f'''
            title: {title}
            status: hidden
            slug: whatsnew
            ''').strip())
    else:
        print(f"# {title}")
    links_seen = set()
    prev_date = ''
    for link in sorted(output, key=lambda x: x['date'], reverse=True):
        url = link['url']
        if url in links_seen:
            continue
        links_seen.add(url)

        date = '-'.join(f'{x:02d}' for x in link['date'][:3])
        if date != prev_date:
            print(f'\n## <center>{date}</center>\n')
        prev_date = date

        domain = urlparse(url).netloc.lower()
        if domain.startswith('www.'):
            domain = domain[len('www.'):]
        print(f'  - [{link["title"]}]({url}) ({domain})')


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
            now = datetime.now(tz=timezone.utc).timestamp()
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


@persistent_cache('cache/whatsnew.json', max_age=3*24*60*60)
def whatsnew(bookmarks_file, cache_dir='cache/whatsnew', fetch_last_articles=3, cache_key=None):
    '''Find new posts on pages mentioned in bookmarks'''
    bookmarks = deserialize(bookmarks_file)
    reader = CachingFeedReader(cache_dir)
    feeds_seen = set()
    output = list()
    now = datetime.now()
    for section in bookmarks:
        links = section.get('links')
        if not links:
            continue
        for link in links:
            if not link.get('url'):
                continue
            page_url = link['url']
            for feed_url in find_feeds(page_url):
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
                    if any(pattern in entry.link for pattern in NOISY_URL_PATTERNS):
                        continue
                    if (now - datetime(*entry.published_parsed[:3])).days > MAX_AGE_DAYS:
                        continue
                    output.append(dict(
                        title=entry.title,
                        url=entry.link,
                        summary=entry.get('summary'),
                        date=list(entry.published_parsed),
                    ))
    return output


def find_feeds(url):
    '''Find feeds related to URL'''
    urlparts = urlparse(url)
    site = f'{urlparts.scheme}://{urlparts.netloc}'
    path = urlparts.path.split('/')

    always_check_subdirectories = {
        'blog',
        'wiki',
        'posts',
    }

    default_feeds = set(feedlinks(url))
    default_feeds.update(feedlinks(site))
    if len(path) >= 2 and path[1].lower() in always_check_subdirectories:
        default_feeds.update(feedlinks(f'{site}/{path[1]}/'))
        default_feeds.update(feedlinks(f'{site}/{path[1]}'))
    if default_feeds:
        yield from default_feeds
        return []

    while path:
        last = path.pop()
        if not last.strip():
            continue
        feeds = feedlinks(f'{site}{"/".join(path)}')
        if feeds:
            yield from feeds
            return []
    return []

@persistent_cache('cache/feedlinks.json', max_age=7*24*60*60)
def feedlinks(url):
    '''Return links to RSS/Atom feeds from a web page URL'''
    http = dict()
    try:
        page = http_get(url, result=http)
    except Exception as exc:
        log.error('%s while fetching %s', exc, url)
        return list()
    urlparts = urlparse(url)
    parser = FeedLinkParser()
    try:
        parser.feed(page.decode())
    except Exception as exc:
        log.error('%s while searching for feed links in %s', exc, url)
        return list()
    feeds = set()
    for link in parser.results:
        if link.startswith('//'):   # same-scheme links
            feeds.add(f'{urlparts.scheme}:{link}')
        elif link.startswith('/'):  # absolute links
            feeds.add(f'{urlparts.scheme}://{urlparts.netloc}{link}')
        elif '://' not in link:   # relative links
            path = urlparts.path.rstrip('/')
            feeds.add(f'{urlparts.scheme}://{urlparts.netloc}{path}/{link}')
        else:
            feeds.add(link)
    return list(feeds)


class FeedLinkParser(HTMLParser):
    def __init__(self, *a, **ka):
        self.results = set()
        super().__init__(*a, **ka)

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in {'link', 'a'}:
            return
        attrs = dict(attrs)
        if attrs.get('rel', '').lower() != 'alternate':
            return
        link_type = attrs.get('type', '').lower()
        if 'application/atom' not in link_type \
        and 'application/rss' not in link_type:
            return
        self.results.add(attrs['href'].strip())


def deserialize(yamlfile):
    with open(yamlfile) as f:
        return yaml.safe_load(f)


def checksum(filename, algorithm='sha256'):
    hasher = getattr(hashlib, algorithm)()
    with open(filename, 'rb') as file:
        for chunk in iter(lambda: file.read(2**16), bytes()):
            hasher.update(chunk)
    return f'{algorithm}:{hasher.hexdigest()}'


if __name__ == '__main__':
    main()
