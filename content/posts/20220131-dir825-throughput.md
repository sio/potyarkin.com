title: D-Link DIR-825 (rev.B1) throughput test
tags: hardware, router
date: 2022-01-31

So, the year is 2022 and I'm still using D-Link [DIR-825], rev.B1 as my edge
router at home.

Thanks to the power of opensource it is running a modern and secure OS
(OpenWRT) long after the manufacturer has abandoned this product.
Even though OpenWRT (and Linux in general) has increased the system
requirements, DIR-825 still meets the minimal [8/64] criteria.

![Photo of D-Link DIR-825, rev.B1][router]

To put things into perspective: I bought this very device in November, 2011
for the equivalent of $120. Its WiFi standard is pretty outdated (802.11n),
but that's enough since all my essential devices are hardwired.

Up until a few weeks ago it was pointless for me to think about router
upgrade. The Ethernet cable coming into my apartment from ISP equipment was
crimped to use only 2 twisted pairs which would never allow for speeds above
100Mbit. And DIR-825 routes 100Mbit just fine. Thankfully, a completely
unrelated incident occurred and an ISP technician was on site - I seized the
opportunity and asked them to recrimp their end (*4 missing wires were just
bent aside right before a connector, why would anyone do that?!*)

Now that I have an option to upgrade above 100Mbit, the valid question is:
*Will my DIR-825 be able to handle that?*

To test router throughput I used two laptops booted into Debian 11 live image,
one of them running a DHCP server and connected to WAN port of the router, the
other one connected to one of LAN ports. I put together all the
required commands into a [Makefile] to avoid having to memorize them - you
might find this repo useful if you ever need to perform a similar test on
your router.

To establish a [baseline] I connected the laptops directly to each other
without any routers or switches in between. I got the expected near-gigabit
speeds: 932Mbps down, 941Mbps up - nothing unusual here.

Here are the test results with router in between
(full logs: [part one][test1], [part two][test2])

![average: bidir 130/162Mbps, down 262Mbps, up 382Mbps][results]

Maximum throughput was achieved in upload tests (*382Mbps*). This is
probably explained by having to process less firewall rules for outgoing
traffic. Download speed even with a very basic iptables configuration was
significantly less (*256Mbps*), and bidirectional tests with
simultaneous traffic in both directions confirm that ~300Mbps is a hardware
limit (bidirectional speed was *130Mbps down + 162Mbps up =
292Mbps total*). top was showing 99% sirq load during these tests, but
running a monitoring tool did not have any significant impact on the results
(first 5 tests were executed before top was launched).

## Conclusion

These tests show that while DIR-825 is a perfectly capable router for 100Mbps,
it's completely out of its depth with faster connections. Even 300Mbps will
frequently become underutilized if the traffic will happen to flow in both
directions at once.

Looks like I finally need a new router after almost 11 years with DIR-825...


[DIR-825]: https://openwrt.org/toh/d-link/dir-825
[8/64]: https://openwrt.org/supported_devices/864_warning
[Makefile]: https://github.com/sio/router-throughput-test
[baseline]: {static}/resources/dir825/baseline.log
[test1]: {static}/resources/dir825/test1.log
[test2]: {static}/resources/dir825/test2.log
[iptables]: {static}/resources/dir825/iptables.cfg
[results]: {static}/resources/dir825/results.svg
[router]: {static}/resources/dir825/router.jpg
