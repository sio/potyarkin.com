title: Why software translation is a waste of time
tags: l10n, i18n
date: 2017-10-07 23:10

> **Disclaimer**: I am not a professional software developer, and my opinion
> might not be as authoritative as yours.

My native language is not English and since my first encounter with computers I
have used multiple localized and non-localized computer programs. All these
years of *"user experience"* have led me to believe that software localization
is more often harmful than not.

Software translation is a waste of time. Generally.

I am not against localization as a whole. It has many positive aspects like
supporting foreign date and currency formats, right-to-left writing or
alphabetical sorting. But translating user interface, configuration files,
error and log messages to other languages had destructive consequences most of
the times I've seen it.

## Documentation loss

The moment software is translated its documentation becomes fragmented and
incomplete. Even if the developer translates 100% of official documentation
they will still lose everything written by others (blog posts, forum questions,
bug reports).

I was twelve when a friend of mine gave me a book on photo editing. The authors
explained how images are stored on computers, what is the difference between
raster and vector graphics, but the narrative was mostly centered on using Adobe Photoshop -
version 7.0, if I recall correctly. And that was one large useless book.
Because the authors used the English version of that editor and all we've had
was the translated one.

You might think it was a mistake on the authors' part, but they were smart and
experienced people. They knew it was pointless to reference a translated version
because no professional user would have used Russian interface at that time.
And they knew that the next version might come with totally different
translation for the same UI elements.

## Incomplete or wrong translation is worse than no translation at all

If you are not sure you can afford a good translation, don't do one. I can not
stress enough how confusing it is to have a piece of software that uses your
native language, and not to be able to understand the meaning of its messages
without translating them back to English first. This happens all the time when
software is translated by people who do not use it daily and do not understand
all the usecases there are.

I took part in translation of an open source program once. I was a student and
I've had a lot of free time, so I thought I could do some good and contribute
back to the software I thought was worthy.

It was a social media plugin for a bigger application. We had a team of maybe a
dozen volunteer translators and a coordinator with write access to the source
control system. Usually he would email us a day before the next release with a
file containing strings that needed to be translated. And then the farce
started.

Those of us who were available at the moment started translating. We didn't
know where in the application we would later see those strings. Even if we
weren't lazy (guilty) and would've launched non-localized development version
of the application, we would not have been able to match 100% of new strings to
all the places they'd be used at. The coordinator was not any less blind than
the rest of us. He knew a lot about the application code base, but he was not a
superhuman - he could not possibly track all the developers and understand all
their intentions. So we shipped some embarrassing translation errors... I'm
glad no lives depended on that software!

## Lost in translation

I concede that our team was lacking in terms of organizational skills, after
all we were just part-time volunteers. But the translators hired by big
corporations are merely human too, and they make mistakes. Especially when the
headquarters is pressuring to ship a new product.

For more than ten years Microsoft Excel, a flagman spreadsheet application used
by millions, has had two duplicate entries in row/column context menu: "Вставить"
and "Вставить". The first one had a nice icon and meant "Paste (copied cells)"
and the second one was iconless and meant "Insert (new row/column)". They've
removed the text from the first one now, converting it to a button. Ambiguity
still remains (the pop-up text for the button is the same) but is less
confusing. Especially since users are already accustomed to it :)

## Unsearchable error messages

Have you ever received a cryptic error message and had no idea what it meant?
I'm sure you have. That message would only become more cryptic if it was
translated. And if the error is not exactly common or the app is not popular in
your country, Google will not be able to help you either.

So, for the sake of your users' sanity, please do not ever localize error
messages and log files! Help people to help themselves.

## Untranslatable abstractions

Some ideas are just so new, or the problem domain is so narrow that there is no
point translating the terms. The concept of `File` was foreign to every person
seeing the computer for the first time - but that knowledge is easily acquired.
It would not have been any easier explaining that same concept and labeling it
`Файл` (Russian translation), so why bother introducing two terms?

"File" ship has long sailed, but new abstractions are being introduced every
day. Translating them to multiple languages just slows their adoption and
hinders communication between users.

## Afterword

I'm not hoping we will wake up one day and The Tower of Babel didn't happen.
This rant is mostly useless, but if at any time because of it a software
developer will decide that their users are educated enough to understand
written English or a software user will decide to acquire entry-level English
skills, I'll consider my time well spent.

> This has been stewing for quite some time... At least since 2012, after I've
> read [this](https://joeyh.name/blog/entry/on_localization_and_progress/).
