title: "No user exists for uid" when pushing to git repo
tags: linux, ssh, git
slug: no-user-exists-for-uid
date: 2022-07-21


Today I tried to automate pushing to a Git repository from a Docker container.
And like many others I failed with an error:

```
$ git push
No user exists for uid 2918
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

Following best practices I was running the container under a random UID to
drop root privileges, and of course there was no user with that UID in the
system. I don't think that's egregious enough to warrant an error instead
of a warning from `git push`, so I've started digging.

I was very surprised to learn where this error [comes from][ssh.c]:

[ssh.c]: https://github.com/openssh/openssh-portable/blob/c46f6fed419167c1671e4227459e108036c760f8/ssh.c#L659-L664

```c
/*
 * openssh/ssh.c: Main program for the ssh client.
 */
int main(int ac, char **av) {

    // ...lines omitted...

    /* Get user data. */
    pw = getpwuid(getuid());
    if (!pw) {
        logit("No user exists for uid %lu", (u_long)getuid());
        exit(255);
    }
```

`getuid()` is pretty self-explanatory, it returns UID of current user.
Afterwards `getpwuid()` attempts to fetch data for the provided UID from
`/etc/passwd`. It fails, of course, and returns NULL. OpenSSH client treats
that as a show stopper and exits with an error.

I was hoping that finding the place where error is generated will help me to
come up with a setup that avoids problematic code branch altogether,
but no luck this time. It's straight in the `main()` function of ssh client,
no conditional branching whatsoever.

I will be [looking into generating][bogus] a bogus `/etc/passwd` entry on-the-fly prior
to launching my application in container. I would very much like to avoid
hardcoding the UID at build time.

[bogus]: https://github.com/sio/microblog-server/blob/1468a8832805f8a72252473020085495d31efcb9/container/addpasswd.c

*Meanwhile, here is a punchline for you:*

When current UID is not in /etc/passwd OpenSSH client can not even print a
usage message:

```
$ ssh
No user exists for uid 3432

$ ssh --help
No user exists for uid 3432
```
