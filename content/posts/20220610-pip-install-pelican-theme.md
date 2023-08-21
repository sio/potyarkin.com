slug: pip-install-pelican-theme
date: 2022-06-10
title: Pip-installable Pelican themes
tags: pelican, python, pip

Installing [Pelican] themes [the default way][installing-themes] is not very
pleasant:

- You need to invoke a separate CLI tool
- You may need to create some symlinks and ensure that they don't go stale the
  next time you use Pelican
- Some people (me) have resorted to git submodules instead of official CLI

As a workaround I've been packaging my Pelican themes into simple Python
packages with a sole `__init__.py`:

```python
from pkg_resources import resource_filename
def path():
    '''
    Return path to theme templates and assets
    Use this value for THEME in Pelican settings
    '''
    return resource_filename(__name__, '')
```

This adds a dependency on [setuptools] but it's already present in most
Python venvs anyways, so not a big deal.
`pkg_resources` exposes full path to wherever pip installs the theme. It
also handles unpacking to temporary directory if required (in case of wheels and
zipped installs).

I have been using this trick for some time already, but only recently I noticed
that Pelican plugins have [officially transitioned][pelican-plugins-pip] to
being pip-installable. They use a clever hack of adding extra packages to
`pelican.plugins` namespace and I though it would be cool to use the same
approach with themes.

Turns out it's not easy to do with setuptools, but is [pretty
straightforward][poetry-config] with poetry. As a result I can now publish [my
themes] to PyPI and provide easy invocation instructions:

```python
# pelicanconf.py
from pelican.themes import smallweb
THEME = smallweb.path()
```

All the end users need to do is to add another line mentioning my theme to
whichever [file they use][requirements.txt] to create their Pelican venv.

On developer side we need to create `pelican/themes/themename` folder
structure and point poetry at `pelican` for top-level package name. All theme
files should be placed into `pelican/themes/themename` and one extra
`__init__.py` file should be added there to provide `path()` method.
See [SmallWeb] repository for an example.

[Pelican]: https://blog.getpelican.com/
[setuptools]: https://setuptools.pypa.io/en/latest/userguide/index.html
[installing-themes]: https://docs.getpelican.com/en/3.6.3/pelican-themes.html#installing-themes
[pelican-plugins-pip]: https://docs.getpelican.com/en/stable/plugins.html#namespace-plugin-structure
[poetry-config]: https://github.com/sio/pelican-smallweb/blob/master/pyproject.toml
[my themes]: https://pypi.org/project/pelican-theme-smallweb/
[requirements.txt]: https://github.com/sio/potyarkin.com/blob/smallweb/requirements.txt#L3
[SmallWeb]: https://github.com/sio/pelican-smallweb
