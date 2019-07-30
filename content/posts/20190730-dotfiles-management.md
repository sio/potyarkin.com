title: On dotfiles management
tags: linux, windows, automation, bash
date: 2019-07-30


This will be yet another description of dotfiles management by some random
person on the Internet. I will try to explain what my setup is like and why it
is that way.

If you're not yet using version control software for your configuration files
I strongly encourage you to start doing so, whichever way you like. These
pages are good places to start:

- [An unofficial guide to dotfiles on GitHub](http://dotfiles.github.io/)
- [Arch wiki article on dotfiles](https://wiki.archlinux.org/index.php/Dotfiles)


## My chosen approach

After several attempts that have spanned across many years I've understood
that neither tracking home directory directly with Git nor symlinking all of
the dotfiles from a single directory tree is working for me. Both ways lead to
a mess in the repository and made the whole endeavor of tracking changes
cognitively expensive, so I inevitably started slacking off.

I've looked at the existing tools that are meant to automate some of the
process and did not find one that would suit all my needs. I've ended up
writing a small shell [script] that takes care of dotfiles installation but
the main value for me is in the repo layout, not the script itself.

All configuration files are grouped into directories by topic. These
directories are somewhat similar to packages in GNU [stow]. Topic directories
recreate the directory structure for the target location, by default $HOME.
Files that are meant to be installed into target location have to contain an
appropriate suffix at the end of filename (any other files are ignored):

- `.copy` - for files to be copied over to new location
- `.link` - for files to be linked to from new location
- `.append` - for files to be appended to the target file

Default behavior may be altered by a `dotfiles.meta` file placed into the
topic directory. It is essentially a shell script that is being sourced during
topic installation. Its main purpose is to provide alternative values for
PREFIX and SCOPE variables:

- PREFIX value determines target directory where the dotfiles will be placed.
  Also if PREFIX is set the dotfiles will not get an extra dot in front of
  their filename (which is the default behavior otherwise).
- SCOPE variable may be used to indicate that a topic requires root privileges
  to be installed (`SCOPE=system`).

Multiple topics may be installed at once either by providing all of their
names as command line arguments or by listing them all in a text file and
providing path to that file as an argument to the installation [script].


## Examples

- `topic-foo/vimrc.link` will be symlinked from `~/.vimrc`
- `topic-bar/bashrc.copy` will be copied over to `~/.bashrc`
- `topic-baz/default/keyboard.copy` with `PREFIX=/etc` will be copied to `/etc/default/keyboard`
- `topic-baz/file/without/valid/suffix` will be ignored

More examples may be found in my [dotfiles repo][dotfiles].


## Comparison with existing tools

#### Strengths

- Very small number of dependencies makes this script usable across all my
  Linux and Windows machines. It requires only the core GNU userland: bash,
  coreutils, find and grep.
- Multiple install actions are supported (copy, link, append) unlike [stow]
  that only makes symlinks. More than that, my script detects if it's being
  executed on Windows machine and copies over any file that was meant to be
  symlinked - because symlinks on Windows are so tricky they're might as well
  be not supported at all.
- Destination directory may be specified for each topic individually which
  makes it possible to install topics targeting different directories in one
  run.
- Simple partial deployment. If machine requires only a subset of topics
  tracked in the repository it is easy to list them all in a plain text file
  or to provide them as command line arguments to the bootstrap script.
  [yadm], for example does not provide such ability.
- Dotfiles are not hidden in the repo by default. It makes no sense to have
  `~/.bashrc` point to `repo/bash/.bashrc` instead of `repo/bash/bashrc`, so
  dots are added automatically for topics with default target PREFIX.
- All operations are reversible because all overwritten files are backed up
  beforehand.


#### Weaknesses

- Single pass execution. It means some topics may be left partially configured
  in case of errors. [stow] is a good example of cautious approach. This is an
  implementation detail and may be fixed in later versions of bootstrap
  script.
- No support for tree folding/unfolding. I consider that an overkill for
  simple configuration management.
- No automated reverse operation. In case you want to undo the changes made by
  this [script] you'll have to restore backups manually from `$DOTFILES_BACKUP`


[stow]: https://www.gnu.org/software/stow/
[yadm]: https://thelocehiliosan.github.io/yadm/
[script]: https://gitlab.com/sio/server_common/blob/master/dotfiles/bootstrap.sh
[dotfiles]: https://gitlab.com/sio/server_common/tree/master/dotfiles
