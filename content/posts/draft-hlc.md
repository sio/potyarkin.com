title: Accidental submersion into web development

## The Library Problem

I love reading books. My wife loves reading books. We enjoy shopping for books
and we live a ten minute commute away from a huge used books store. That means
we have a lot of books. Like, really a lot. A little more than one thousand.

We have lost count how many times we've bought a book that we already owned.
Even more often we had foregone buying a book we liked because we were sure we
have already bought it - only to find out we've been mistaken and have only
considered buying that very book earlier. This has become a problem. The Library
Problem.

We needed a way to catalog all our books. The catalog had to be accessible from
mobile devices (to look up a book while at the book store) and to be easy to
use. That is to add and edit book information, of which we've needed plenty: in
addition to standard set of author, title and publishing year we wanted to be
able to track book series and keep the list of missing books to look out for the
next time.

I admit my research into the subject matter was not scientifically thorough.
I've dug up several comparisons of existing tools and have read several blog
posts of people who have faced the same problem before. I particularly recommend
[this one][blog]. And I have decided that no pre-existing tool will meet our
growing expectations.

## Naive foray into application architecture

I have never developed an application for any end user other than myself and I
didn't even know I was about to start developing one.

### Single spreadsheet approach

The initial idea was that of a "document". It had to contain some essential
information about every book we own and (optionally) a second list of books we
want to acquire. Excel spreadsheet seemed like a natural fit. We are both
spending a better half of each workday juggling spreadsheets in Excel, so
developing and maintaining such "document" appeared doable.

I have started drafting the column structure, applied some formatting tweaks and
the skeleton of the "document" was ready. We have entered the test batch of
books and were about to begin testing.

Obstacles arose when we were entering information for the first fifteen books.
Manually typing in all the fields is tiresome and slow. Errors inevitably
happen. What if I miss one letter in the author's name?  That book will be lost
when applying filter on author column. We need autocompletion! What if I
accidentally switch the order of digits in ISBN? We won't be able to do a web
lookup for that book later. We have to write a custom ISBN validator in VBA!

And the spreadsheet began to amass VBA code, data validation and conditional
formatting rules. Full-blown spaghetti style. Version control has become a
problem. What's the difference between versions 0.0.13 and 0.0.19? I had only a
vague idea.

I stopped myself when I was about to sketch up a UserForm for data input. Excel
road was leading me nowhere. It was difficult and even if all the difficulties
were to be overcome it imposed some suboptimal compromises on us:

- Single table storage limited the data structures we would be able to enter and
  view. If the book was written by two authors, which one should come first in
  the "author" string?  How would we do column filtering in that case? What
  about sort order?
- The local nature of storage meant there had to be one designated place for
  making changes (home laptop). Any changes made in other locations (smartphone,
  thumb drive) had to be agreed to be declared discardable.
- The spreadsheet had to be exported to HTML to be accessible from smartphones.
  XML and XSLT made this possible but not very pleasant. Although, I am rather
  proud of the VBA code I wrote to save/load XML data automatically upon opening
  the workbook. The data was completely decoupled from the representation.

I'm glad I did not waste more time pursuing this path, but it was still hard to
let go. It took quite some time for me to return to this project afterwards.

### Local database driven application with web interface

A relational database was the logical solution to spreadsheet limitations.
Store authors separate from books and manage how the former *relate* to the
latter! Scientists who pioneered the [relational model] in 1970s were pure
geniuses and now the whole world relies on their work.

I drafted the database schema on a piece of paper and have discussed it
extensively with my wife. That's probably the point where book reviews were
added to the requirements list. The database idea made me very enthusiastic and
had swallowed a lot of free time, but that idea alone could not provide a
complete solution for the problem at hand.

Data input and representation are what the Library project was all about. Yet
relational database management systems provide only the storage solution, not
the full package (if you don't take Microsoft Access into account). So I had to
figure out how to implement the user interface on my own. I chose to write it in
Python because I was somewhat familiar with the language and I enjoy how clean
and readable Python code is. I'm not a programmer, so other options were either
learning a new language or choosing between VBA and Bash, none of which could be
considered enjoyable.

I have briefly considered building a conventional desktop GUI. The UserForm
experience was still fresh and rather traumatic, so I was reluctant to dive into
another UI toolkit. Even if I were to, which one should I have chosen? Qt seemed
nice, but its Python support reports were contradictory. GTK? Installing it was
rather tricky in Windows. Something non-crossplatform? And what about my Linux
laptop?

I've had a bunch of HTML templates left from XML/XSLT operations and they could
be trivially transformed to be used in conjunction with the database. While the
catalog pages could be statically generated, the data input required some sort
of server to interact with. And I've had zero experience with that.

Quick Google search has introduced me to the concept of web frameworks and I
have semi-randomly chosen [Bottle]. At that moment I've had no intention to
expose it to the open network, the app and the database were to be stored on the
USB stick and launched locally when needed. Smartphone interaction was planned
either via LAN or using saved HTML pages for read-only access when not at home.
Bottle uses no dependencies other than standard library and the whole framework
is packaged into a single file. It was perfect for the portable app scenario.

After the development started and I saw how difficult it is to make a web
application, I've decided there is no point to confine the result of all that
labor to a single computer. Why use static (maybe even outdated) HTML dumps on
the smartphone when we could access full functionality of the application via
web site?

### Traditional web application

## The unknown unknowns

Little did I know that while I was keeping myself busy with seemingly important
problems such as whether to store images as blobs in database or as files on the
file system a number of much more important problems were creeping up behind me.
Donald Rumsfeld has called these things *the unknown unknowns* - the things that
we don't know while remaining unaware about the very fact of not knowing.

### ORM
### Multi-threading
### Database migrations
### JavaScript is a lot of work
### Modular design
### MVC

## It works!

After all the difficulties and complications (both expected and unexpected) I
can proudly say that the Library project is a success. The website is up and
running for almost a year. There has been no significant downtimes and no data
loss, most of our books have been catalogued. And most important, me and my wife
do enjoy using it!

The application supports:

- Creating and editing book entries.
- Storing and displaying book metadata, cover thumbnail and arbitrary related
  files. Each book can be connected with any number of authors, series and/or
  tags.
- Using ISBN to fetch book information from several third-party sources
- Queuing ISBNs for input. This is helpful when you process a lot of books with
  barcode scanner and don't have the time to clean up automatic metadata on each
  one of them
- Adding 1-to-5 star ratings and text reviews to any book in the library
- Searching for books by exact metadata match and with wildcards

You can access [the source code][source] on GitHub and see the site in action at
https://morebooks.ml (registration is for family members only, sorry).  Of
course, there are plenty of improvements to be made (you can see how long the
TODO list is), but the maintenance itself requires almost zero attention now
and I can happily switch from being a developer to becoming the end user.

[Bottle]: https://bottlepy.org/
[blog]: http://www.zackgrossbart.com/hackito/the-library-problem/
[relational model]: https://en.wikipedia.org/wiki/Relational_model#History
[source]: https://github.com/sio/HomeLibraryCatalog
