'''
Fetch newest articles from my blogroll
'''

from datetime import datetime
from hashlib import sha256
from pathlib import Path
import logging
import json
import re

import feedparser
import yaml


logging.basicConfig(format='%(levelname)-8s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


JSON_PARAMS = dict(
    indent=2,
    ensure_ascii=False,
    default=repr,
)


def main():
    reader = CachingFeedReader('cache')
    webring = []
    for section in blogroll('content/blogroll.yml'):
        for blog in section['blogs'] or []:
            if not 'feed' in blog:
                continue
            try:
                feed = reader.feed(title=blog['title'], url=blog['feed'])
            except Exception:
                log.exception(f'Error while fetching {blog["feed"]}')
                continue
            entries = sorted(feed.entries, key=lambda x: x.updated_parsed, reverse=True)
            latest = entries[0]
            webring.append(dict(blog=blog, entry=latest))
    print(json.dumps(webring, **JSON_PARAMS))


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

    def feed(self, title, url):
        '''Parse feed from URL, use cache if applicable'''
        cache = self._cache(title, url)
        if cache.hot():
            return cache.read()
        fetch_params = dict()
        if cache.exists():
            for key in ['etag', 'modified']:
                if key in cache.metadata:
                    fetch_params[key] = cache_metadata[key]
        feed = feedparser.parse(url, **fetch_params)
        if feed.status == 200:
            cache.save(feed)
            return feed
        elif cache.exists():
            log.error(f'HTTP {feed.status}: {url}, continuing from cache: {cache.directory}')
            return cache.read()
        else:
            raise RuntimeError(f'HTTP {feed.status}: {url}')

    def _cache(self, title, url):
        '''Return cache object for a given feed'''
        return FeedCache(self.cachedir, title, url)


class FeedCache:
    '''Cache object for a single feed'''

    LIFETIME_MINUTES = 24*60
    METADATA_VERSION = 1

    def __init__(self, cachedir, title, url):
        sanitized_title = re.sub(r'\W', '_', title)
        sanitized_title = re.sub(r'_+', '_', sanitized_title)
        url_hash = sha256(url.encode()).hexdigest()[-8:]

        self._directory = cachedir / f'{sanitized_title}_{url_hash}'
        self._metadata = self._directory / 'metadata'
        self._feed = self._directory / 'feed'

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
        self._directory.mkdir(exist_ok=True)
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
            return json.load(f, object_hook=feedparser.util.FeedParserDict)


if __name__ == '__main__':
    main()
