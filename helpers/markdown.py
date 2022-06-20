'''Jinja2 filter for rendering markdown from arbitrary input'''

import markdown


def convert(text, renderer=None):
    '''Convert Markdown string to HTML'''
    if renderer is None:
        renderer = markdown.Markdown()
    return renderer.convert(text)


def custom(options):
    '''Create custom convert() function with preapplied Markdown config'''
    if 'extension_configs' in options:
        options['extensions'] = set(options['extension_configs']).union(options.get('extensions', []))
    renderer = markdown.Markdown(**options)
    converter = lambda text: convert(text, renderer)
    return converter
