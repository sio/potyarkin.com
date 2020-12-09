title: Ansible apt module fails to install python3-apt on Debian Testing
tags: ansible,
slug: ansible-apt-debian-testing
date: 2020-12-09

I have encountered an unexpected Ansible failure today that turned out to be not
a bug.

Ansible apt module had failed to auto install the required `python3-apt`
package - only on Debian Testing. Same playbook worked fine with Debian
Stable.

```
TASK [install some apt packages] *********************************************
[WARNING]: Updating cache and auto-installing missing dependency: python3-apt
ok: [debian10]
fatal: [debian11]: FAILED! => changed=false
  msg: 'Could not import python modules: apt, apt_pkg. Please install python3-apt package.'
```

After some troubleshooting I've been able to find the reason for this failure:
Python interpreter was being automatically upgraded to the next minor version
while installing `python3-apt`.

Since the `apt_pkg` module is distributed as compiled platform-specific binary
(e.g. `apt_pkg.cpython-37m-x86_64-linux-gnu.so`), it is only compatible with
Python version it's been built for. In my case the Python interpreter at the
moment of Ansible module invocation was at version 3.8.6, but doing
`apt update; apt install python3-apt` had upgraded it to 3.9.1 and installed
`apt_pkg` was only compatible with new version of interpreter.

Ansible apt module was still running under the old version of interpreter and
therefore was unable to import `apt_pkg` that it had just installed.

Such errors are a non-issue on Debian Stable where Python is never upgraded to
the next upstream version, and even in Testing/Sid it's a rare occurence. More
than that, I see no way to add a workaround to the Ansible module that could
allow it to handle this edge case: the whole module is executed with one
instance of Python interpreter and it can not accomodate such change in a
single invocation.

The solution I see is to explicitly install `python3-apt` on Debian
Testing/Sid systems before invoking apt module with Ansible. This can either
be done with `raw` module or with the provisioning tools (machine template,
preseed, terraform/packer/etc).
