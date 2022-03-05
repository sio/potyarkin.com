title: Unexpected workaround for Libvirt VMs with cgroups v2 in Cirrus CI
tags: ci, automation, libvirt
slug: libvirt-cirrusci-workaround
date: 2022-03-02

> Today I wrote a [commit message] that was several screens long.
> I think it deserves to be a blog post of its own

> *Update:* the commit linked above required some [modification] to remove
> flakiness, but the workaround still stands. Diff provided in this blog post
> was updated to reflect current state of affairs

[commit message]: https://gitlab.com/sio/server_common/-/commit/5777cfae5446e7056fd95408c10e5273cd6529fd
[modification]: https://gitlab.com/sio/server_common/-/commit/ebde5a880fc648be382a157454bc1ab17a8e0cd5

Recently Cirrus CI builds that were using nested Libvirt VMs have started
failing with the following error:

    Call to virDomainCreateWithFlags failed: unable to open
    '/sys/fs/cgroup/machine/qemu-2-defaultdebian11-server.libvirt-qemu/':
    No such file or directory

First recorded failure occured on
[February 25th, 2022](https://cirrus-ci.com/task/5115427394158592)

Error message clearly indicates that the issue is related to Linux control
groups (cgroups), and on a hunch I assumed that Cirrus CI (or Google Cloud)
images were updated to use cgroups v2 by default. Unfortunately I haven't
been recording debug information for cgroups before the failure, so I can
not confirm my guess. Currently cgroups2 are in use, so the hypothesis stands.

Web search has led me to several useful pages:

[redhat]: https://bugzilla.redhat.com/show_bug.cgi?id=1985377#c1
[docs]: https://libvirt.org/cgroups.html

#### [RedHat bugzilla][redhat]

Running Libvirt from inside a container (similar to how Cirrus does) produced
the same error.  The reason is that default cgroups mode was changed in podman
when upgrading from cgroups v1 (host mode) to v2 (private mode).

I took note of this issue, but I moved on with my research since as a user
I can not change the configuration of container runtime at Cirrus CI.

#### [Libvirt documentation][docs]

> Libvirt will not auto-create the cgroups directory to back this
> partition. In the future, libvirt / virsh will provide APIs / commands
> to create custom partitions, but currently this is left as an exercise
> for the administrator.

Based on the documentation quoted above I have tried to manually create
the required cgroup with a simple `mkdir -p $CGROUP`. Please note that
Libvirt uses different cgroup layouts when running on systems with and
without systemd. Cirrus CI runners use a different (non-systemd) init in
their containers, so the cgroup path in our case is
`$MOUNTPOINT/machine/qemu-$ID-$MACHINENAME.libvirt-qemu/`

Manual creation of cgroup did not lead to any changes in Libvirt behavior.
Error message stayed the same: no such file or directory.

Report author at [RedHat bugzilla][redhat] had mentioned that they had trouble
with manually moving QEMU process into a different cgroup, so I've tried to do
that and see if the error message will provide any further information.

I configured Cirrus CI to create a long-running background process and to
migrate it to the newly created cgroup. I was expecting this to fail, so I
did not comment out the code that later would launch a Libvirt VM on CI
runner. *Imagine my surprise when the pipeline turned green!* Not only did
the migration succeed, but its success had somehow lead to the success of
Libvirt VM!

A few trial runs later I noticed that the name of cgroup used in the first
step does not even have to match the cgroup (or cgroups) that will be used
by Libvirt domains.

This is why I'm adding this meaningless cgroups burn-in to my pipelines.
"It ain't stupid if it works", right?

#### Full commit diff

```diff
diff --git a/.cirrus.yml.j2 b/.cirrus.yml.j2
--- a/.cirrus.yml.j2
+++ b/.cirrus.yml.j2
@@ -21,6 +21,8 @@ task:
     # VENVDIR must be absolute path for 'cd && make' approach to work
     # VENVDIR should not be cached! Cirrus CI drops some binaries randomly

+    CGROUP_WORKAROUND: /sys/fs/cgroup/machine/qemu-cgroup_workaround.libvirt-qemu
+
     # Pass values from cirrus-run environment
     CLONE_URL: "{{ CI_REPOSITORY_URL }}"
     CLONE_SHA: "{{ CI_COMMIT_SHA }}"
@@ -61,6 +63,16 @@ task:
   libvirtd_background_script:
     - sleep 2 && /usr/sbin/libvirtd

+  # Workaround for cgroups v2
+  # I have no idea why or how this works (see commit message for a longer rant)
+  cgroups_workaround_background_script:
+    - mkdir -p "$CGROUP_WORKAROUND"
+    - ls -lF "$CGROUP_WORKAROUND"
+    - bash -c 'echo $$ > /tmp/cgroups_workaround.pid; sleep infinity' &
+    - sleep 1
+    - cat /tmp/cgroups_workaround.pid >> $CGROUP_WORKAROUND/cgroup.procs
+    - cat $CGROUP_WORKAROUND/cgroup.procs
+
   # Execute automated tests
   test_script:
     - cd ansible/tests
@@ -70,6 +82,9 @@ task:
   always:
     cache_debug_script:
       - find "$HOME/cache" -type f || echo "Exit code: $?"
+    cgroups_debug_script:
+      - fgrep cgroup /proc/mounts || echo "Exit code: $?"
+      - find /sys/fs/cgroup -exec ls -ldF {} \; || echo "Exit code: $?"
     kvm_debug_script:
       - free -h
       - pstree -alT
```
