from argparse import ArgumentParser
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json

from .webring import (
    CachingFeedReader,
    JSON_PARAMS,
    blogroll,
    log,
)

def main():
    args = parse_args()
    reader = CachingFeedReader(args.cache)
    newspaper = []
    now = datetime.now(timezone.utc)
    sections = []
    for section in blogroll(args.blogroll):
        sections.append(section['section'])
        for blog in section['blogs'] or []:
            blog['section'] = section['section']
            if not 'feed' in blog:
                continue
            try:
                feed = reader.cached(title=blog['title'], url=blog['feed'])
            except Exception:
                log.exception(f'Error while fetching {blog["feed"]}')
                continue
            for entry in feed.entries:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if (now - published).total_seconds() > args.max_age * 24 * 60 * 60:
                    continue
                newspaper.append(dict(blog=blog, entry=entry))

    def sortkey(item):
        '''Sort key for newspaper entries'''
        section = sections.index(item['blog']['section'])
        today = datetime(*now.timetuple()[:3])
        published = datetime(*item['entry']['published_parsed'][:3])
        age = today - published
        return age, section, item['entry']['published_parsed']

    newspaper = sorted(newspaper, key=sortkey)
    if args.output:
        args.output = open(args.output, 'w')
    print(json.dumps(newspaper, **JSON_PARAMS), file=args.output)
    if args.output:
        args.output.close()


def parse_args(*a, **ka):
    parser = ArgumentParser(
        description='Prepare newspaper data from a blogroll',
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
        '--max-age',
        metavar='DAYS',
        default=100,
        help='Include items not older than this number of days',
    )
    args = parser.parse_args(*a, **ka)
    if not args.cache.exists():
        parser.error(f'cache directory does not exist: {args.cache}')
    if not args.cache.is_dir():
        parser.error(f'cache path is not a directory: {args.cache}')
    return args


if __name__ == '__main__':
    main()
