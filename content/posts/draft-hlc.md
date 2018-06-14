title: Accidental submersion into web development

## The Library Problem

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

[source]: https://github.com/sio/HomeLibraryCatalog
