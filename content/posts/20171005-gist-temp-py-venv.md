title: Temporary virtual environment for Python
tags: windows, script, gist
date: 2017-10-05 16:50

Using Python on Windows does not come as naturally as on Unix-like systems, so
any help is appreciated.

I wrote a batch script to automate creation, setup and deletion of Python virtual
environment. This can come handy when you want to test something in a clean env,
or to play with `pip install` and get acquainted with a new package from PyPI.


## venv-temp.bat
You can download the script from
[https://gist.github.com/sio/...](https://gist.github.com/sio/fbc46ae41607b206ce9099dc8485df34)

The code is licensed under a permissive opensource license (Apache License,
Version 2.0) so feel free to use it for your hobby and work projects.

Report any bugs, ideas, feature requests via GitHub issues/comments -
all feedback is welcome!


## Installation
Downloaded script does not require any installation.

If `python` is not available from your `%PATH%`, you have to specify the location
of `python.exe` in the script (change the value of `PYTHON` variable).


## Usage
Launch the script from `cmd.exe` to read all error output (if any) or by
double-clicking if you're confident it works on your system.

After you're done experimenting and are ready to discard the venv, just end shell
session with `exit` - the script will take care of cleanup.

If you close the
terminal window without typing `exit`, the script will be terminated before it
performs cleanup. This has no harmful consequences except taking 20-50MB of disk
space. Old venv directory will be purged before reusing, so no changes you've
made will affect the environment you'll get next time.

**NOTE:** If you have no internet connection, the script remains usable, but `pip`
will print a lot of error messages while trying to update itself. Don't worry, that's ok.
