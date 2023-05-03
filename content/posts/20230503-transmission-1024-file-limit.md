title: A pull request 10 years in the making
tags: opensource, programming,
slug: 10-year-pull-request
date: 2023-05-03

> Once upon a time there was a bug in a free software project that annoyed me
> for long enough that I've learned C to fix it. And it felt good.

Now that we've got a TL;DR out of the way, here is the story.

[![story timeline][timeline]][timeline]

There is a good torrent client called [Transmission]. It's lightweight, fast
and reliable. I have compared it against alternatives several times and
Transmission had always come out on top.

In 2011 I've found out that Transmission had open file limit essentially
hardcoded to a value of 1024. Given that in Unix-like systems this limit
is also spent on open network sockets the number seemed extremely low.

Back then FOSS culture was still very foreign to me, so I did what any
consumer would naturally do: I contacted support. Helpful visitors of
Transmission forums told me that open file limit is indeed hardcoded and
pointed me to a [bug tracker ticket][trac4164] which discussed this issue and
which was closed several months prior without any real fix.

Bug tracker discussion pointed out that there was a good reason for setting
such limit, a decades old limitation in glibc - important enough to be
featured first in BUGS section of [`man 2 select`][BUGS]. Since Transmission
had hit this limitation via intermediate library (libcurl) there wasn't
much else for Transmission developers to do at the time besides to hardcode a
safe low value. Facebook had contributed an alternative libcurl API to work
around that bug only [a year later][curl_multi_wait].

I did not handle the news well. In fact I did not understand most of it at the
time, only that developers were aware of a problem and that they were not
going to do anything about it. I switched to another torrent client and went
on to moan on local forums about how silly Transmission is and how it's useful
only for toy workloads. For several years every time someone mentioned
Transmission in IRC/XMPP chats I would snarkily introduce them to this bug.
Not my finest hour, I know.

In the mean time I was hitting the limitations of other torrent clients and
remembered Transmission mostly fondly (if not for that one bug). Some time
later I even returned to Transmission and was sharding workloads between
multiple instances to avoid exhausting open files limit. I reviewed the
alternatives from time to time and have not found any other client to be better enough
to switch to.

As time went on other people got burned by the same bug. Some of them started
badmouthing Transmission like I did. Forums posts and bug tracker tickets
piled on, but no forward progress was made.

Unrelated to Transmission, I got introduced to FOSS scene. I've acquired a
habit of checking if I could understand the source code upon encountering a
nasty bug in a piece of software. I submitted a few small PRs to other
projects I used, shared a few projects of my own and experienced being on the
receiving end of an issue/PR. After many years I decided to look at that
Transmission issue again.

Turned out that thanks to all commenters on Trac and on GitHub, the issue has
been investigated to its root already. Libcurl was the culprit. Quick web
search had introduced me to `curl_multi_wait` API, and after some introductory C
tutorials I was able to replace all `select()` calls with the new API.

I submitted the [pull request] in April 2019 and the rest is history:

- My PR got merged into Transmission in July 2020, providing closure to more
  than a dozen of bug reports
- The first stable version of Transmission featuring my fix (v4.0.0) has
  become available in 2023

It felt good to finally remove this thorn instead of complaining about it.
I probably should have done that much sooner.

[Transmission]: https://transmissionbt.com/
[trac4164]: https://trac.transmissionbt.com/ticket/4164
[curl_multi_wait]: https://daniel.haxx.se/blog/2012/09/03/introducing-curl_multi_wait/
[BUGS]: https://manpages.debian.org/bullseye/manpages-dev/select.2.en.html#BUGS
[pull request]: https://github.com/transmission/transmission/pull/893
[timeline]: {static}/resources/pr893_timeline.svg
