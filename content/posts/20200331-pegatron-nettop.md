title: Pegatron Cape 7 nettop (thin client)
tags: hardware,
slug: pegatron-cape-7

> Below are hardware details of an outdated compact computer that had since
> become available for low price on second-hand market. I bought mine for $15
> (in March 2020).
>
> This post is inspired by [ParkyTowers Thin Client
> Database](https://www.parkytowers.me.uk/thin/) - many thanks to David
> Parkinson for gathering and sharing all that knowledge!


**Pegatron Cape 7** was announced in early 2009 ([marketing booklet][booklet]
is dated by 2009-04-13). It is based on Intel Atom 230 series CPU along with
SiS 968/672 (models A, B, C, D) or nVidia Ion chipset (models E, F). The unit
I have is model D, all further photos and description apply to that model.

[![Pegatron Cape 7 photos][overview-thumb]][gallery]

The hardware is similar to [Dell
FX160](https://www.parkytowers.me.uk/thin/dell/fx160/) but is packaged into a
significantly more compact case and uses external power supply. Pegatron is an
[ODM manufacturer] which means the units were sold to end users under a
variety of brand names. Mine was sold in Russia as **Depo Sky 153**. I've also
seen mentions of it being sold as [Pegasus CutePC] in Indonesia, as unknown
model under [iClient] brand in Brazil, and under some local brand in Poland.

**Cape 7** is capable of running mainstream operating systems (mine came with
Windows XP preinstalled), general purpose Linux distributions are also
supported.


## Specifications

- **Motherboard**: Pegatron IPP71-CP with SiS 672 northbridge and SiS 968 southbridge
- **Processor**: Intel Atom 230 (1.6GHz, single core, two threads)
- **RAM**: DDR2 SO-DIMM, 1GB by default (mine came with 2GB preinstalled by seller)
- **Video**: SiS Mirage 3
- **Storage**: 2.5" SATA HDD
- **Ports**:
    - **Network**: Realtek 8111EL 10/100/1000
    - **USB**: 6 USB 2.0 ports (2 front, 4 back)
    - **Video**: 1 DVI output (other Cape 7 models may use D-Sub or HDMI)
    - **Audio**: 3.5mm audio out, 3.5mm microphone in - Realtek ALC662
    - **Serial**: none
    - **Parallel**: none
    - **PS/2**: none
    - **Other**: 1 unknown port (next to DCIN), probably for Wi-Fi antenna
- **Power**: External power supply - 19V DC, 2A, 5.5mm x 2.5mm connector
  (same as in many ASUS laptops)
- **Cooling**: passive, completely silent. One removable aluminum heatsink for
  CPU, several thermal pads to transfer heat from northbridge/southbridge to
  metal case frame.
- **Dimensions**: approx. 173 x 154 x 20mm, the bottom of the case is
  slightly wider (26mm).


## Processor

<details>
<summary>Click to view <strong>/proc/cpuinfo</strong></summary>
```
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 28
model name	: Intel(R) Atom(TM) CPU  230   @ 1.60GHz
stepping	: 2
microcode	: 0x218
cpu MHz		: 1599.527
cache size	: 512 KB
physical id	: 0
siblings	: 2
core id		: 0
cpu cores	: 1
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 10
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
pat clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc
arch_perfmon pebs bts nopl cpuid aperfmperf pni dtes64 monitor ds_cpl tm2
ssse3 cx16 xtpr pdcm movbe lahf_lm dtherm
bugs		:
bogomips	: 3199.05
clflush size	: 64
cache_alignment	: 64
address sizes	: 32 bits physical, 48 bits virtual
power management:

processor	: 1
vendor_id	: GenuineIntel
cpu family	: 6
model		: 28
model name	: Intel(R) Atom(TM) CPU  230   @ 1.60GHz
stepping	: 2
microcode	: 0x218
cpu MHz		: 1599.365
cache size	: 512 KB
physical id	: 0
siblings	: 2
core id		: 0
cpu cores	: 1
apicid		: 1
initial apicid	: 1
fpu		: yes
fpu_exception	: yes
cpuid level	: 10
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
pat clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc
arch_perfmon pebs bts nopl cpuid aperfmperf pni dtes64 monitor ds_cpl tm2
ssse3 cx16 xtpr pdcm movbe lahf_lm dtherm
bugs		:
bogomips	: 3199.05
clflush size	: 64
cache_alignment	: 64
address sizes	: 32 bits physical, 48 bits virtual
power management:
```
</details>


## BIOS <!-- TODO -->


## PCI

<details>
<summary>Click to view <strong>lspci -nn</strong></summary>
```
00:00.0 Host bridge [0600]: Silicon Integrated Systems [SiS] 671MX [1039:0671]
00:01.0 PCI bridge [0604]: Silicon Integrated Systems [SiS] AGP Port (virtual PCI-to-PCI bridge) [1039:0003]
00:02.0 ISA bridge [0601]: Silicon Integrated Systems [SiS] SiS968 [MuTIOL Media IO] [1039:0968] (rev 01)
00:02.5 IDE interface [0101]: Silicon Integrated Systems [SiS] 5513 IDE Controller [1039:5513] (rev 01)
00:03.0 USB controller [0c03]: Silicon Integrated Systems [SiS] USB 1.1 Controller [1039:7001] (rev 0f)
00:03.1 USB controller [0c03]: Silicon Integrated Systems [SiS] USB 1.1 Controller [1039:7001] (rev 0f)
00:03.3 USB controller [0c03]: Silicon Integrated Systems [SiS] USB 2.0 Controller [1039:7002]
00:05.0 IDE interface [0101]: Silicon Integrated Systems [SiS] SATA Controller / IDE mode [1039:1183] (rev 03)
00:06.0 PCI bridge [0604]: Silicon Integrated Systems [SiS] PCI-to-PCI bridge [1039:000a]
00:0f.0 Audio device [0403]: Silicon Integrated Systems [SiS] Azalia Audio Controller [1039:7502]
00:1f.0 PCI bridge [0604]: Silicon Integrated Systems [SiS] PCI-to-PCI bridge [1039:0004]
01:00.0 VGA compatible controller [0300]: Silicon Integrated Systems [SiS] 771/671 PCIE VGA Display Adapter [1039:6351] (rev 10)
02:00.0 Ethernet controller [0200]: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller [10ec:8168] (rev 03)
```
</details>


## Disassembly

The case can be opened without any tools. All visible screws are holding
internal components, not the cover. Bottom corners of the cover are easy to
get a grip of - pull gently on those and expand the opening until plastic
locks click open one by one.


## Expansion

**RAM**: The unit accepts a single DDR2 SO-DIMM. Default module can be easily
replaced with a larger one. I did not test with 4GB (DDR2 SO-DIMM of that size
is expensive!), but I've seen multiple reports of 2GB working fine. My unit
uses Kingston KVR800D2S6/2G module.

**Storage**: Cape 7 provides conventional SATA slot with enough space to fit a
laptop HDD or SATA SSD. Using SSD might not provide the expected performance
benefit because SATA bus appears to be limited at 300 Mbps (37.6 MB/s) -
numbers are from block diagram (page 15 of the [booklet]).


## Pictures

See [the gallery][gallery] or download individual images in high resolution:


- [Nettop overview - standing][outlook]
- [Nettop overview - lying][overview]
- [Front panel][front]
- [Back panel][back]
- [Open case][open]
- [Motherboard (front)][motherboard-front]
- [Motherboard (back)][motherboard-back]
- [Empty case (inside)][case]


<!-- internal links -->
[booklet]: {static}/resources/pegatron/booklet.pdf
[gallery]: {filename}/pages/pegatron-photos.md "More photos of Pegatron Cape 7"
[overview-thumb]: {static}/resources/pegatron/thumb/0-overview.jpg
[overview]: {static}/resources/pegatron/img/0-overview.jpg
[outlook]: {static}/resources/pegatron/img/1-outlook.jpg
[front]: {static}/resources/pegatron/img/2-front.jpg
[back]: {static}/resources/pegatron/img/3-back.jpg
[open]: {static}/resources/pegatron/img/4-open.jpg
[motherboard-front]: {static}/resources/pegatron/img/5-motherboard-front.jpg
[motherboard-back]: {static}/resources/pegatron/img/6-motherboard-back.jpg
[case]: {static}/resources/pegatron/img/7-case.jpg

<!-- external links -->
[ODM manufacturer]: https://en.wikipedia.org/wiki/Original_design_manufacturer
[iClient]: https://produto.mercadolivre.com.br/MLB-1283040839-thin-cliente-intel-atom-memoria-ram-2gb-ddr2hd-160gb-c-w-_JM
[Pegasus CutePC]: https://forums.vrzone.com/singapore-marketplace-garage-sales/487593-wts-pegatron-cape-7-mini-net-pc-brand-new.html
