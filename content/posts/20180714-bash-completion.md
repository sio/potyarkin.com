title: Enhanced file path completion in bash (like in zsh)
date: 2018-07-14
tags: bash, gist

Zsh offers a lot of significant improvements over traditional shell experience.
Some of those can also be implemented in bash, but others are not. For a long
time I've thought that advanced file path expansion is something that can't be
done in bash. Today I prove myself wrong.

## Background

When the Tab key is pressed, zsh expands incomplete file path assuming any of
its elements might be incomplete, while bash expands only the last piece. For
example: `cd /u/s/app<Tab>` will produce nothing in bash, but will be expanded
to `cd /usr/share/applications` in zsh.

This feature is a huge time saver, but it does not justify switching the shell
completely (for me). So I've been looking for a way to enable the same behavior
in bash.

The solution had to be:

- Portable between Linux and Windows (msys);
- Implemented in configuration files or short scripts that can be carried
  around easily. No third-party tools like `fzf` that would require system-wide
  installation or other tricks to enable.

All I've been able to find was
[this StackOverflow thread](https://stackoverflow.com/q/25076611).
Accepted answer suggests using a new bash function that is later bound to Tab
keypress. The function provided is a quick hack that was not tested thoroughly
and has problems with spaces in file path. The author recommends to use his
function along with the default completer, not instead of it, so it was not
what I needed.

## Workaround

Typing `cd /u*/s*/app*<Tab>` is somewhat better but not as streamlined an
experience as the one zsh offers.

This turned out to be an inspiration for the proper completer function though.

## Better solution

I have coded a small function that adds wildcards to each element in the path
and executes normal bash completion procedures with modified input. After a bit
of documentation digging I've been able to inject this function into normal
bash completion process. I'm pretty happy with path expansion now.

To enable the described behavior source [**this file**][gist] from your
~/.bashrc. Supported features are:

- Special characters in completed path are automatically escaped if present
- Tilde expressions are properly expanded (as per [bash documentation])
- If user had started writing the path in quotes, no character escaping is
  applied. Instead the quote is closed with a matching character after expanding
  the path.
- If [bash-completion] package is already in use, this code will safely override
  its `_filedir` function. No extra configuration is required.

Watch a demo screencast to see this feature in action:
[![asciicast](https://asciinema.org/a/0zhzOYbkF22pWLmbx1RHCYyqQ.png)](https://asciinema.org/a/0zhzOYbkF22pWLmbx1RHCYyqQ)


[bash-completion]: https://salsa.debian.org/debian/bash-completion
[bash documentation]: https://www.gnu.org/software/bash/manual/html_node/Tilde-Expansion.html
[gist]: https://github.com/sio/bash-complete-partial-path/blob/master/bash_completion
