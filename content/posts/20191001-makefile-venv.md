title: Manage Python virtual environment from your Makefile
date: 2019-10-01
tags: python, automation

I often use Makefiles not just as a build tool but as a handy way to execute
sequences of commands. The commands I've found myself executing again and
again lately are the ones to manage Python virtual environments:

- Create new venv
- Update pip to the latest version that enables all the cool new features
- Install project requirements
- Delete venv and redo it again to see if everything still works from clean slate

The process is tedious and begs to be automated. And Makefile is a good fit
because in addition to basic scripting capabilities it offers proper
dependency handling that simplifies the task quite a bit.

The outcome of my attempts at such automation is [Makefile.venv] - a Makefile
that seamlessly handles all virtual environment routines without ever needing
to be explicitly invoked. Instead, you write make targets that depend on
`venv` and refer to all executables in virtual environment via
`$(VENV)/executable`, e.g. `$(VENV)/python` or `$(VENV)/pip`.

Using [Makefile.venv] is easy:

```Makefile
.PHONY: test
test: venv
	$(VENV)/python -m unittest

include Makefile.venv  # All the magic happens here
```

Despite its apparent simplicity this Makefile will do very much when invoked:

- A virtual environment will be created in current directory
- Pip will be automatically updated to the latest version
- Project requirements will be installed (both `requirements.txt` and
  `setup.py` are supported)
- If `setup.py` is present, the project will be installed in development mode
  into venv (`pip install -e`) - all changes to the source code will
  immediately affect the package in virtual environment.

All these steps will be repeated in case `requirements.txt` or `setup.py`
is modified. That means you'll never have to worry about syncing venv with its
description. Add new dependency to `setup.py` and consider it installed,
because there is no way it'll be forgotten the next time you invoke `make`.

If you'll need to debug something interactively, there are `make python` and
`make ipython` for REPL and `make bash` (or `shell` or `zsh`) for shell, but I
rarely use those. Most of the time running `make` with my targets for
executing the entry point or running unit tests is enough. In fact, I've
noticed that after introducing [Makefile.venv] into my workflow I've
completely stopped activating virtual environments manually.

I encourage you to try [Makefile.venv] and hope you'll find this approach
useful. If you have some comments or would like to point out the faults of
using Makefiles for venv, please shoot me an e-mail or create an [issue] at
GitHub project's page.


> PS: [Makefile.venv] was inspired by [this StackOverflow
> thread][stackoverflow] and by [this blog post][bottle] from the authors of
> Bottle.py


[Makefile.venv]: https://github.com/sio/Makefile.venv
[issue]: https://github.com/sio/Makefile.venv/issue

[bottle]: http://blog.bottlepy.org/2012/07/16/virtualenv-and-makefiles.html
[stackoverflow]: https://stackoverflow.com/questions/24736146
