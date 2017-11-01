title: Loops in Power Query M language
tags: m, excel, power-query
date: 2017-10-31

Power Query Formula Language (also known as M language) is sometimes difficult
to get your head around. This article explains how someone familiar with loops
in other programming languages can approach the same concept in M language.

First of all let's look at the [definition][1] given by Microsoft:

> The Power Query M formula language is optimized for building highly flexible
> data mashup queries. It's a **functional**, case sensitive language similar
> to F#, which can be used with Power BI Desktop, Power Query in Excel, and Get
> & Transform in Excel 2016.

"Functional" is the key word.

Understanding (and accepting) that M is entirely different from most of common
programming languages has helped me as much as (maybe even more than) the
exhaustive reference at MSDN. Functional language implies declarative
programming paradigm: you describe *what* you want the computer to do instead
of telling *how* to do it.

The code in M is not an explicit sequence of steps that will always be executed
in the same order, it is just a bunch of ground rules that allow the computer
to arrive to the solution. You can check that the order of lines within the
`let` statement doesn't matter: as long as all necessary intermediate steps are
described, Power Query will produce the same result even if you rearrange them
randomly.

And that is the reason you don't get familiar control flow statements. *If* is
kinda there, but it has its own quirks too. Loops are out of the question,
unless you somehow manage to implement the function that does the looping for
you. But...

There already is such a function! It is `List.Generate`!

## List.Generate
- 4 functions as parameters
- returns list

## An example from real world
- Copy sample from my workbook
- Add a thorough explanation

PS: Also, please keep in mind that the dot symbol in `List.Generate` does not
have the same meaning as in other languages either. There are no object methods
in M, and there are no namespaces, so the dot is just another character without
any special meaning.  It could have been a dash or an underscore - it wouldn't
have mattered.

[1]: https://msdn.microsoft.com/en-us/library/mt211003.aspx
