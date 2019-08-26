title: Cygheap base mismatch in Git for Windows
tags: bash, windows, git
date: 2019-08-26


This error has haunted me for several months:
```
4 [main] head (6660) C:\...\usr\bin\head.exe:r
*** fatal error - cygheap base mismatch detected - 0x612C7410/0xAF7410.

This problem is probably due to using incompatible versions of the cygwin DLL.
Search for cygwin1.dll using the Windows Start->Find/Search facility
and delete all but the most recent version.  The most recent version *should*
reside in x:\cygwin\bin, where 'x' is the drive on which you have
installed the cygwin distribution.  Rebooting is also suggested if you
are unable to find another cygwin DLL.
```

The tricky part is I am not even using Cygwin. I'm running bash with Git for
Windows [as published at the official website][git-windows].

I've tried suggested solution from the error message, googled around quite a
bit, I've even dabbled with Windows Security settings (ASLR) - nothing helped
and have almost made my peace with the fact that every fifth commandline action
will fail loudly.

And yet after recent release I've decided to try one more time. This time I've
downloaded the portable build for 64-bit architecture, and it worked! I don't
know if it was the fact that I was previously running a 32-bit Git and bash on
64-bit Windows 7 or if Git maintainers have tweaked their build process for 2.23.

If you're experiencing segmentation faults while running bash from Git for
Windows package, you should check for **architecture mismatch** with your OS
and/or for **newer (2.23+) Git version**.


[git-windows]: https://git-scm.com/download/win
