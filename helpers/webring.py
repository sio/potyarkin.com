'''
Fetch newest articles from my blogroll
'''

from argparse import ArgumentParser
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import logging
import json
import re

import feedparser
import yaml


logging.basicConfig(format='%(levelname)-8s %(message)s', level=logging.INFO + 1)
log = logging.getLogger(__name__)


JSON_PARAMS = dict(
    indent=2,
    ensure_ascii=False,
    default=repr,
)
feedparser.USER_AGENT = 'helpers/webring.py +https://github.com/sio/potyarkin.com'


def main():
    args = parse_args()
    reader = CachingFeedReader(args.cache)
    webring = []
    for section in blogroll(args.blogroll):
        for blog in section['blogs'] or []:
            if not 'feed' in blog:
                continue
            try:
                feed = reader.feed(title=blog['title'], url=blog['feed'])
            except Exception:
                log.exception(f'Error while fetching {blog["feed"]}')
                continue
            entries = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)
            if len(entries) == 0:
                continue
            latest = entries[0]
            blog['section'] = section['section']
            webring.append(dict(blog=blog, entry=latest))
    if args.output:
        args.output = open(args.output, 'w')
    print(json.dumps(webring, **JSON_PARAMS), file=args.output)
    if args.output:
        args.output.close()


def parse_args(*a, **ka):
    parser = ArgumentParser(
        description='Fetch newest articles from feeds in blogroll',
    )
    parser.add_argument(
        'blogroll',
        metavar='BLOGROLL',
        type=Path,
        help='Path to YAML file with blogroll sources',
    )
    parser.add_argument(
        'output',
        metavar='OUTPUT',
        default=None,
        nargs='?',
        help='Path to output JSON file, default: stdout',
    )
    parser.add_argument(
        '--cache',
        metavar='DIR',
        type=Path,
        default='cache/webring',
        help='Path to cache directory, default: cache/webring',
    )
    parser.add_argument(
        '--cache-mkdir',
        dest='cache_mkdir',
        action='store_true',
        default=False,
        help='Create cache directory if not exists',
    )
    args = parser.parse_args(*a, **ka)
    if args.cache_mkdir:
        args.cache.mkdir(parents=True, exist_ok=True)
    if not args.cache.exists():
        parser.error(f'cache directory does not exist: {args.cache}')
    if not args.cache.is_dir():
        parser.error(f'cache path is not a directory: {args.cache}')
    return args


def blogroll(filepath):
    '''Parse blogroll from YAML file'''
    with open(filepath) as f:
        return yaml.safe_load(f)


class CachingFeedReader:
    '''RSS/Atom feed reader with local cache'''

    def __init__(self, cachedir):
        self.cachedir = Path(cachedir).resolve()
        if not self.cachedir.is_dir():
            raise ValueError(f'cache directory does not exist: {self.cachedir}')

    def cached(self, title, url):
        '''Read feed from cache without accessing network'''
        cache = self._cache(title, url)
        return cache.read()

    def feed(self, title, url):
        '''Parse feed from URL, use cache if applicable'''
        cache = self._cache(title, url)
        if cache.hot():
            return cache.read()
        fetch_params = dict()
        if cache.exists():
            for key in ['etag', 'modified']:
                if key in cache.metadata:
                    fetch_params[key] = cache.metadata[key]
        feed = feedparser.parse(url, **fetch_params)
        if feed.get('status') in {200, 301, 302}:
            cache.save(feed)
            return feed
        elif cache.exists():
            msg = None
            if feed.bozo:
                report = log.error
                msg = f'Bozo: {feed.bozo_exception}'
            elif 'status' not in feed:
                report = log.error
                msg = f'feed object has no status: {url}\n{feed}'
            elif feed.status < 400:
                report = log.info
            else:
                report = log.error
            if not msg:
                msg = f'HTTP {feed.get("status")}: {url}'
            report(f'{msg}, continuing from {cache}')
            return cache.read()
        else:
            if feed.bozo:
                log.warning('Bozo feed: %s, %s entries, status=%s', url, len(feed.entries), feed.get('status'))
                if isinstance(feed.bozo_exception, Exception):
                    raise feed.bozo_exception
                else:
                    raise RuntimeError(f'Bozo: {feed.bozo_exception}')
            raise RuntimeError(f'HTTP {feed.status}: {url}')

    def _cache(self, title, url):
        '''Return cache object for a given feed'''
        return FeedCache(self.cachedir, title, url)


class FeedCache:
    '''Cache object for a single feed'''

    LIFETIME_MINUTES = 12*60
    METADATA_VERSION = 1
    CACHE_VERSION = 1

    def __init__(self, cachedir, title, url):
        sanitized_title = re.sub(r'\W', '_', title)
        url_hash = sha256(url.encode()).hexdigest()[-8:]
        safe_dirname = f'{sanitized_title}_{url_hash}'
        safe_dirname = re.sub(r'_+', '_', safe_dirname)

        self._directory = cachedir / safe_dirname
        self._metadata = self._directory / 'metadata'
        self._feed = self._directory / 'feed'

    def __repr__(self):
        return f'{self.__class__.__name__}: {self._directory}'

    def timestamp(self):
        return datetime.now().timestamp()

    @property
    def metadata(self):
        with self._metadata.open() as f:
            metadata = json.load(f)
        if metadata.get('version') == self.METADATA_VERSION:
            return metadata
        else:
            log.error(f'Mismatching metadata version ({self._metadata}): '
                      f'got {metadata.get("version")} instead of {self.METADATA_VERSION}')
            return dict()

    def exists(self):
        return self._metadata.exists() and self._feed.exists()

    def hot(self):
        '''Check if cache is still hot'''
        if not self.exists():
            return False
        timestamp = self.metadata.get('cache_created')
        if timestamp and self.timestamp() - timestamp < self.LIFETIME_MINUTES * 60:
            return True
        return False

    def save(self, feed):
        '''Save feed to cache'''
        log.info(f'Saving cache: {self._directory}')
        if feed.bozo:
            log.warning(f'Feed contains parsing errors: {feed.bozo_exception} ({self})')
        self._directory.mkdir(exist_ok=True)
        for entry in feed.entries:
            if 'published_parsed' in entry:
                continue
            if 'updated_parsed' in entry:
                entry['published_parsed'] = entry['updated_parsed']
                entry['published'] = entry['updated']
                continue
            if 'published_parsed' in feed:
                entry['published_parsed'] = list(feed['published_parsed'])
                entry['published'] = feed['published']
                continue
            if 'updated_parsed' in feed:
                entry['published_parsed'] = list(feed['updated_parsed'])
                entry['published'] = feed['updated']
                continue
            entry['published_parsed'] = [0] * 9

        feed['cache_version'] = self.CACHE_VERSION
        with self._feed.open('w') as f:
            json.dump(feed, f, **JSON_PARAMS)
        metadata = dict()
        for key in ['etag', 'modified', 'modified_parsed']:
            if key in feed:
                metadata[key] = feed[key]
        metadata['cache_created'] = self.timestamp()
        metadata['version'] = self.METADATA_VERSION
        with self._metadata.open('w') as f:
            json.dump(metadata, f, **JSON_PARAMS)

    def read(self):
        '''Read feed from cache'''
        log.info(f'Reading cache: {self._directory}')
        with self._feed.open() as f:
            feed = json.load(f, object_hook=feedparser.util.FeedParserDict)
        if 'cache_version' not in feed or feed.cache_version != self.CACHE_VERSION:
            log.warning(f'Updating cache to current version: {self}')
            self.save(feed)
            feed = self.read()
        if feed.bozo:
            log.warning(f'Feed contains parsing errors: {feed.bozo_exception} ({self})')
        return feed


if __name__ == '__main__':
    main()
