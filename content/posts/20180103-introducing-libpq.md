title: Expanding Power Query standard library - introducing LibPQ
tags: m, excel, power-query, LibPQ
date: 2018-01-03

Power Query formula language (also known as M language) is a very capable yet
not very flexible tool. It lacks some features taken for granted by developers
who are used to other programming languages such as compatibility with version
control systems, extensibility by third-party libraries, etc.

That is why I have started **[LibPQ]** - an open-source M language library
meant to expand the standard library and to make it easier for others to do so.
Its main features are:

### Importing source code from plain text files located on disk or on the web

LibPQ stores its modules as plain text files with `*.pq` extension.  Detaching
source code from the workbooks that execute it has a lot of advantages:

- The source code can be managed by version control system such as git
- Multiple workbooks referring to the same module will always use the same
  (latest) code
- It encourages splitting your code into smaller reusable units
- You can edit the source code with any editor you like (autocompletion and
  syntax highlighting are nice features even though Power Query's Advanced
  Editor does not have them)
- Sharing your code and collaborating becomes much easier

### Supporting several import locations ordered by priority

LibPQ does not dictate where you store your source code. Inspired by Python's
[`sys.path`][sys.path] it enables specifying unlimited number of local and/or
remote sources (ordered by priority). When importing a module, LibPQ will check
these sources one by one until the required module is found.

### Unit testing framework

Having source code detached from the workbooks encourages you to improve and
refactor existing modules. To make sure you do not introduce regressions you
should cover your code with unit tests.

There are no unit testing tools in standard library, but LibPQ offers a basic
unit testing framework that supports test discovery, grouping tests into test
suites and comes with a bunch of handy assertion functions. To learn more read
this [help page][UnitTest].

### A collection of general purpose functions and queries

And last, LibPQ contains some general purpose modules that you might find
useful. If not - go write some new ones, you have the tools now!

LibPQ is built in such way that you do not need me (or anyone else) to approve
of your work.  Save your code to any convenient location, and LibPQ will help
you to import it into your workbooks. You can even keep your modules private,
no pressure here. Have fun and enjoy your coding!

[LibPQ]: https://github.com/sio/LibPQ
[UnitTest]: https://github.com/sio/LibPQ/blob/master/Docs/UnitTesting.md
[sys.path]: https://docs.python.org/3/library/sys.html#sys.path
