import json
import logging
import pytest
from pathlib import Path

import feedparser
from helpers import webring


FEED = 'https://potyarkin.ml/feeds/all.atom.xml'
TITLE = 'Orange Sun'
CACHE = Path('cache/test')
CACHE.mkdir(parents=True, exist_ok=True)


def test_fetch(caplog):
    '''Test that feed fetching works'''
    caplog.set_level(logging.DEBUG)
    storage = webring.CachingFeedReader(CACHE)
    for _ in range(3):
        feed = storage.feed(TITLE, FEED)
        assert len(feed.entries) > 0
        assert feed.feed.title == 'Orange Sun'
    logs = [r for r in caplog.records if r.name == 'helpers.webring']
    assert len(logs) >= 3
    hits = [r for r in logs if r.msg.startswith('Reading cache')]
    assert len(hits) >= 2


def test_http_headers(caplog):
    '''Test if HTTP headers signal about unmodified feed'''
    reader = webring.CachingFeedReader(CACHE)
    feed = reader.feed(TITLE, FEED)

    # Artificially age cache
    cache = reader._cache(TITLE, FEED)
    metadata = cache.metadata
    metadata['cache_created'] = 1500000000  # somewhere in 2017
    with cache._metadata.open('w') as out:
        json.dump(metadata, out, **webring.JSON_PARAMS)

    caplog.set_level(logging.DEBUG)
    repeat = reader.feed(TITLE, FEED)
    assert 'HTTP 304' in caplog.records[0].msg
    assert caplog.records[1].msg.startswith('Reading cache')
    assert len(caplog.records) == 2
