import logging
import re
import yaml
from pprint import pprint
from datetime import datetime


logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')


DATE = re.compile(r'^## (?P<month>.*)$', re.MULTILINE)
HEADER = re.compile(r'\s*^- \**\[(?P<title>[^\]]+)\]\((?P<url>.*)\)\**(?: +-|$)', re.MULTILINE)


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
            period=datetime.strptime(date["month"], '%B %Y').strftime('%Y-%m'),
            links=[],
        )
        bookmarks.append(month)
        cursor = date.end()
        link = None
        while True:
            header = HEADER.search(markdown, cursor)
            if link and header and header.start() != cursor:
                if date:
                    endpos = min(header.start(), date.start())
                else:
                    endpos = header.start()
                description = markdown[cursor:endpos].strip()
                if description:
                    link["description"] = description
            if link:
                month["links"].append(link)
            if not header:
                logging.info(f'Header not found at cursor {cursor}')
                break
            date = DATE.search(markdown, cursor)
            if header and date and date.start() < header.start():
                break
            link = dict(
                title=header["title"].strip(),
                url=header["url"],
            )
            logging.info(f'Title: {header["title"]}, URL: {header["url"]}')
            cursor = header.end()
    count = sum(len(d['links']) for d in bookmarks)
    logging.info(f'Parsed {count} bookmarks within {len(bookmarks)} periods')
    for month in bookmarks:
        logging.info(f'  {month["period"]}: {len(month["links"])}')
    return bookmarks

def dump(obj, filename):
    '''Save bookmarks to file'''
    def str_presenter(dumper, data):  # https://stackoverflow.com/a/33300001
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)
    with open(filename, 'w') as out:
        yaml.safe_dump(
            obj, out,
            allow_unicode=True,
            default_flow_style=False,
            indent=0,
            sort_keys=False,
        )

def main():
    filepath = 'content/pages/bookmarks.md'
    with open(filepath) as f:
        markdown = f.read()
    bookmarks = parse(markdown)
    dump(bookmarks, 'output.yml')


if __name__ == '__main__':
    main()
