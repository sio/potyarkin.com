'''
Jinja2 function for loading YAML data from filesystem
'''

from pathlib import Path
import json


def read(filepath):
    '''Load data from JSON file'''
    filepath = Path(filepath).resolve()
    with open(filepath) as f:
        return json.load(f)
