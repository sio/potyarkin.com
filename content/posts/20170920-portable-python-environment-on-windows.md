# Portable development setup for Python on Windows
## WinPython
https://winpython.github.io/

All-in-one distribution which comes with many difficult-to-build packages
preinstalled. And their ...-Zero version is great for thumb drives!

Pip works just fine, but installing packages that require C compiler is
always a pain on Windows. May be I should look into conda and see if it
offers a portable variant.

**NOTE:** there are unofficial binary wheels for most common Python packages
at http://www.lfd.uci.edu/~gohlke/pythonlibs/ The site's hosting is a little
unreliable, so it might take a few trys to fetch a package.


## Git Portable
https://git-scm.com/download/win

Git for Windows is now recommended by official Git website, and there always
is a portable version.

This package provides not only Git but also bash and a basic MSYS environment
(coreutils, sed, grep, awk, etc) which make life on Window *so much* easier!
Also, it comes with VIM preinstalled, which is a damn good editor and is
preferred by many developers.


## GNU Make
http://www.equation.com/servlet/equation.cmd?fa=make

Unfortunately Git for Windows does not come with GNU make preinstalled, so
we have to download it manually. Great guys at Equation Solution are regularly
building standalone versions of GNU Make for 32-bit and 64-bit Windows.

Downloaded file has to be placed somewhere in PATH.


## GitHub with SSH keys
https://help.github.com/articles/connecting-to-github-with-ssh/

I don't know if it is even possible to setup HTTPS authentication without
installing GitHub Desktop, and SSH key authentication works with GitHub
same as everywhere.

I keep the keys on my laptop and the rest of the environment is on a thumb
drive. That way I can develop anywhere I want, Windows comes as a given (sadly),
and I don't have to worry about keys security, because they are not exposed
to random computers.

Official documentation recommends using HTTPS just because it's easier for
newcomers (https://stackoverflow.com/questions/11041729)
- It does not require generating public/private keys and uploading the correct
  one to GitHub
- HTTPS is allowed everywhere and SSH might be blocked by a firewall
