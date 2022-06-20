'''
Jinja2 function for loading YAML data from filesystem
'''

from pathlib import Path
import yaml


def read(filepath):
    '''Load data from YAML file'''
    filepath = Path(filepath).resolve()
    with open(filepath) as f:
        return yaml.safe_load(f)
