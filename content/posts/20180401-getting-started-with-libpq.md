title: Getting started with LibPQ
tags: m, power-query, LibPQ
date: 2018-04-01

This is a step by step guide to getting started with [LibPQ], an illustrated
version of ["Installation and usage"][Installation] section of the official
documentation.

## Installation
### LibPQ source code

The source code of the library has to be present in each workbook that uses it.

- Create a new blank query: `Data > Get & Transform > From Other Sources >
  Blank Query`
- Go to "Advanced editor" and replace the query code with the contents of
  [`LibPQ.pq`][LibPQ] (switch to "Raw" view to make selecting easier)
- Save new query under the name `LibPQ`

[![Main module of LibPQ][img-main]][img-main]

### Specifying modules location

After the previous step LibPQ doesn't know yet where it should get the modules'
source code from. You can specify an unlimited number of local and web locations
where the modules are saved:

- Create a new blank query and name it `LibPQPath`
- Copy the contents of [LibPQPath-sample.pq] and modify it in Advanced editor.

[![LibPQ-Path][img-path]][img-path]

LibPQ will search for your modules first in local directories (in order they
are listed), then in web locations. If the module is found, no further
locations are checked.

It helps with the name collisions:

- Let's say you have a module `FavoritePets.pq` stored in your module
  collection at `http://yoursite.com/PowerQueryModules/`
- At the same time you use some modules from a friend's module collection
  at `http://friendname.com/PowerQueryModules/`
- If your friend adds a module with the same name to their collection, all
  you need to do to ignore it is to make sure that your collection address
  is higher in the `LibPQPath` than your friend's.
- That works both ways: you and your friend can continue sharing your
  module collections while using personal modules with colliding names
  without any problems.

### Reusable template

It is not necessary to repeat the installation steps every time you want to use LibPQ. You can add LibPQ to an empty workbook and save is as a template for future use.

## Usage
### Importing existing module

Import any available module with `LibPQ("ModuleName")` when writing your
queries in Advanced editor. LibPQ will search for the file named
`ModuleName.pq` in all locations that you've listed in LibPQPath. If the module
is found, its source code will be evaluated and the result will be returned.

For example, let's import `Date.Parse` from standard LibPQ collection:

[![Date.Parse][img-date-parse]][img-date-parse]

That works because `LibPQPath` contains reference to
`https://raw.githubusercontent.com/sio/LibPQ/master/Modules/`, where the source
code for `Date.Parse.pq` is located.

### Creating a new module

You can save any reusable Power Query function or query to be imported by LibPQ
later:

- Copy the code of that module to any text editor (I recommend Notepad++) and
  save it with `*.pq` extension
- Place the module into any location listed in `LibPQPath` and it will become
  available for importing

If you have any futher questions about LibPQ please create an [issue] on GitHub
or contact me via [e-mail].

[LibPQ]: {filename}20180103-introducing-libpq.md
[LibPQ.pq]: https://github.com/sio/LibPQ/blob/master/LibPQ.pq
[LibPQPath-sample.pq]: https://github.com/sio/LibPQ/blob/master/LibPQPath-sample.pq
[Installation]: https://github.com/sio/LibPQ/blob/master/README.md#installation-and-usage
[issue]: https://github.com/sio/LibPQ/issues
[e-mail]: mailto:sio.wtf@gmail.com

[img-main]: {attach}/resources/libpq-main-module.png
[img-path]: {attach}/resources/libpq-path-editor.png
[img-date-parse]: {attach}/resources/libpq-date-parse.png
