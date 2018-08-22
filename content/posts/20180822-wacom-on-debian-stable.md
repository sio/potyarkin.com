title: Installing One by Wacom in Debian Stretch
tags: linux, hardware, Debian
date: 2018-08-22


I believe there are many people who run Debian Stable as their main desktop OS.
This article is a short how-to on enabling newer hardware in Debian Stable
without switching to another version or distribution.


## One by Wacom

Wacom has released their new graphics tablet, [One by Wacom] in the Fall of 2017
(judging by the dates of reviews in online shops). Linux drivers for this model
(Small: CTL-472, Medium: CTL-672) were added to the [git repo][linuxwacom] in
December 2017 and were released in March 2018 ([input-wacom-0.39.0]).

That is several months after the current Debian Stable (Stretch) was released
(June 2017). So there is exactly zero chance of it containing drivers for that
hardware - "stable" means no new software except security updates gets
introduced during the lifetime of the release (until at least 2020).

Fortunately, you don't need to switch distribution to use newer hardware. You
don't even need to compile anything from source. Even more so, **PLEASE DON'T
INSTALL INPUT-WACOM FROM SOURCE**, that will most likely lead to some undesired
side effects.


## Debian backports

Backports project was created exactly for cases like this. It allows users to
install newer versions of some packages without breaking anything while keeping
Debian overall at the same (stable) version.

To enable support for One by Wacom in Debian Stretch you need to:

- [Add backports][backports] to your sources.list

- Install newer kernel from backports:
  `apt-get -t stretch-backports install linux-image-amd64`

  If you're running Debian on different CPU architecture, replace `-amd64` with
  the corresponding suffix, like `-686-pae` for older 32-bit computers or
  `-arm64` for ARMv8 CPUs).

- Reboot your computer

That's it! Newer kernel will have updated drivers for your graphics tablet and
it will be detected automatically. You can start using it right away or tweak
some pressure options in your favorite graphics application (e.g. for Gimp it's
in *Edit -> Input Devices*).


## Further reading

- [Arch wiki] - if you want to fine tune your graphics tablet
- [Debian wiki]


## Timeline recap

- [Debian 9] (Stretch) was released in June 2017 and will be supported until
  at least 2020
- [One by Wacom] (Small: CTL-472, Medium: CTL-672)
  - Available in retail: Fall 2017 (judging by the dates of reviews in online
    shops)
  - Driver for Linux: [patch] added in December 2017, drivers
    [released][input-wacom-0.39.0] in March 2018


## Log messages (for reference)

#### Debian 9 (Stretch) without proper driver

```
# dmesg|grep -i wacom
usb 5-1: Manufacturer: Wacom Co.,Ltd.
input: Wacom Co.,Ltd. CTL-472 Pen as /devices/pci0000:00/0000:00:1d.0/usb5/5-1/5-1:1.0/0003:056A:037A.0001/input/input95
wacom 0003:056A:037A.0001: hidraw0: USB HID v1.10 Mouse [Wacom Co.,Ltd. CTL-472] on usb-0000:00:1d.0-1/input0
wacom 0003:056A:037A.0002: Unknown device_type for 'Wacom Co.,Ltd. CTL-472'. Ignoring.
```

#### Debian with updated kernel from backports

```
# dmesg|grep -i wacom
usb 6-1: Manufacturer: Wacom Co.,Ltd.
input: Wacom Co.,Ltd. CTL-472 as /devices/pci0000:00/0000:00:1d.0/usb6/6-1/6-1:1.0/0003:056A:037A.0001/input/input23
hid-generic 0003:056A:037A.0001: input,hiddev0,hidraw0: USB HID v1.10 Mouse [Wacom Co.,Ltd. CTL-472] on usb-0000:00:1d.0-1/input0
hid-generic 0003:056A:037A.0002: hiddev1,hidraw1: USB HID v1.10 Device [Wacom Co.,Ltd. CTL-472] on usb-0000:00:1d.0-1/input1
input: Wacom One by Wacom S Pen as /devices/pci0000:00/0000:00:1d.0/usb6/6-1/6-1:1.0/0003:056A:037A.0001/input/input24
wacom 0003:056A:037A.0001: hidraw0: USB HID v1.10 Mouse [Wacom Co.,Ltd. CTL-472] on usb-0000:00:1d.0-1/input0
```

[Arch wiki]: https://wiki.archlinux.org/index.php/wacom_tablet#Configuration
[Debian 9]: https://www.debian.org/News/2017/20170617
[Debian wiki]: https://wiki.debian.org/WacomTablets
[One by Wacom]: https://www.wacom.com/en-cn/products/pen-tablets/one-by-wacom
[backports]: https://backports.debian.org/Instructions/
[input-wacom-0.39.0]: https://github.com/linuxwacom/input-wacom/releases/tag/input-wacom-0.39.0
[linuxwacom]: https://github.com/linuxwacom/input-wacom
[patch]: https://github.com/linuxwacom/input-wacom/commit/b12529e589dae810f0b6ef0b22f67b3860f86cde
