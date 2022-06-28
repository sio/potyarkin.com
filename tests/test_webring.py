import pytest
import logging
from pathlib import Path

CACHE = Path('cache/test')
FEED = 'https://potyarkin.ml/feeds/all.atom.xml'
TITLE = 'Orange Sun'

def test_fetch(caplog):
    caplog.set_level(logging.DEBUG)
    CACHE.mkdir(parents=True, exist_ok=True)
    from helpers import webring
    storage = webring.CachingFeedReader(CACHE)
    for _ in range(3):
        feed = storage.feed(TITLE, FEED)
        assert len(feed.entries) > 0
        assert feed.feed.title == 'Orange Sun'
    logs = [r for r in caplog.records if r.name == 'helpers.webring']
    assert len(logs) >= 3
    hits = [r for r in logs if r.msg.startswith('Reading cache')]
    assert len(hits) >= 2
