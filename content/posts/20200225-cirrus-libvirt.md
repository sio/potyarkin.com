title: Running Libvirt (KVM) in Cirrus CI
tags: ci, automation
date: 2020-02-25

Up until the middle of 2019 it was very unusual to even expect that any CI
service would allow nested virtualization. Those who required such
functionality had to maintain their own CI runners on their own
infrastructure. Things changed when Google Cloud introduced [nested
KVM][google-cloud-kvm] support.

[Cirrus CI][cirrus] was probably the first CI service to [officially
support][kvm-support] nested virtualization in free tier. There are reports
that Travis CI currently also provides such feature but no public announcement
has been made yet.

It turns out I was the first person to try using Libvirt in Cirrus CI (I've
even hit a previously unknown [bug] which was promptly fixed by their staff).
Since the process has some subtle differences to the popular documented use
cases I've decided to describe it here.

## Hypervisor environment

Cirrus CI uses Docker images as environment for their runners. It
significantly simplifies the setup and enables efficient caching between runs.

Since popular Docker images do not include any hypervisor packages we need to
build our own image. I've decided to add the required packages to Debian base
image. The whole [Dockerfile] is essentially one `apt-get` statement.

Keep in mind that libvirt package in Debian drops root privileges when
launching `qemu-kvm`. You'll either need to disable that in
`/etc/libvirt/qemu.conf` (as I did) or to change permissions for `/dev/kvm` to
allow access by `libvirtd` user.

## Required system services

Default entry point for CI runner is not customizable in Cirrus CI - it's an
agent process that communicates with CI service and sends progress reports you
see in web interface. Because of that no systemd units are started automatically
as it would have been the case on a normal system. More than that, starting
systemd manually also looks impossible.

That means all the daemons required by libvirt must be started manually (see
documentation on [background_script] syntax):

```yaml
# .cirrus.yml
dbus_background_script:
  - mkdir -p /var/run/dbus
  - /usr/bin/dbus-daemon --system --nofork --nopidfile
virtlogd_background_script:
  - /usr/sbin/virtlogd
libvirtd_background_script:
  - sleep 2 && /usr/sbin/libvirtd
```

## Firewall configuration

Hypervisor kernel is provided as is, and it currently runs legacy iptables
firewall. Trying to use iptables-nft (which is the default in current Debian)
produces a misconfigured guest network that is hard to debug.

That's why we need to tell Debian to use legacy iptables interface across the whole
system:

```yaml
# .cirrus.yml
iptables_legacy_script:
  - update-alternatives --set iptables /usr/sbin/iptables-legacy
```

## &nbsp;

That's it! Following these steps I was able to execute Libvirt (via
Vagrant-Libvirt, via Molecule) in Cirrus CI environment. [Full configuration]
is available here, it includes some extra caching steps and many debug
statements that helped me to implement this process in the first place.


[background_script]: https://cirrus-ci.org/guide/writing-tasks/#background-script-instruction
[bug]: https://github.com/cirruslabs/cirrus-ci-docs/issues/564
[cirrus]: https://cirrus-ci.org/
[Dockerfile]: https://gitlab.com/sio/server_common/-/blob/master/ansible/tests/Dockerfile.host-kvm
[Full configuration]: https://gitlab.com/sio/server_common/-/blob/master/.cirrus.yml.j2
[google-cloud-kvm]: https://cloud.google.com/compute/docs/instances/enable-nested-virtualization-vm-instances
[kvm-support]: https://cirrus-ci.org/guide/linux/#kvm-enabled-privileged-containers
