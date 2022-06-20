import logging
import re
import yaml
from pprint import pprint


logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')


DATE = re.compile(r'^## (?P<month>.*)$', re.MULTILINE)
HEADER = re.compile(r'\s*^- \**\[(?P<title>.+)\]\((?P<url>.*)\)\** +-', re.MULTILINE)


def where(text, cursor):
    '''Show where cursor is in text'''
    return (
        f'Cursor: {cursor}\n'
        f'Before: {text[cursor-20:cursor]}\n'
        f'After: {text[cursor:cursor+20]}\n'
    )

def parse(markdown):
    '''Parse bookmarks from Markdown to Python objects'''
    bookmarks = []
    cursor = 0
    while cursor <= len(markdown):
        date = DATE.search(markdown, cursor)
        if not date:
            logging.info(f'No more timestamps found after cursor {cursor}')
            break
        logging.info(f'Date: {date["month"]}')
        month = dict(
            month=date["month"],
            links=[],
        )
        bookmarks.append(month)
        cursor = date.end()
        link = None
        while True:
            header = HEADER.search(markdown, cursor)
            if not header:
                logging.info(f'Header not found at cursor {cursor}')
                break
            if link and header.start() != cursor:
                description = markdown[cursor:min(header.start(), date.start())]
                link["description"] = description
            if link:
                month["links"].append(link)
            date = DATE.search(markdown, cursor)
            if header and date and date.start() < header.start():
                break
            link = dict(
                title=header["title"],
                url=header["url"],
            )
            logging.info(f'Title: {header["title"]}, URL: {header["url"]}')
            cursor = header.end()
    return bookmarks

def main():
    filepath = 'content/pages/bookmarks.md'
    with open(filepath) as f:
        markdown = f.read()
    bookmarks = parse(markdown)
    with open('output.yml', 'w') as out:
        yaml.dump(bookmarks, out)


if __name__ == '__main__':
    main()
