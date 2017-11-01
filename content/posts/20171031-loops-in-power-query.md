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

## "Functional" is the key word

Understanding (and accepting) that M is entirely different from most common
programming languages has helped me as much as (maybe even more than) the
exhaustive reference at MSDN. Functional language implies declarative
programming paradigm: you describe *what* you want the computer to do instead
of telling *how* to do it. If you're familiar with LISP or Erlang or Haskell, M
might not look so foreign to you.

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

This function takes 3 or 4 parameters, all of them functions.  (You should
always treat the `each` statement as a function [because it is][2] a shortcut
for function definition.)

The parameters are:
- **start**: a function that takes zero arguments and returns the first loop
  item.
- **condition**: a function that takes one argument (loop item) and returns
  boolean value. If this function returns `false` the iteration stops,
  otherwise the loop item is added to the list of results. This function will
  be called at the end of each iteration.
- **next**: a function that takes one argument (loop item) and returns the next
  loop item. This is the worker body of the loop. Be careful to return the next
  item as the same data type with the same structure, because the returned
  value will be fed to `condition()` and `next()` functions later. This
  function will be called at the beginning of each iteration.
- **transform**: optional argument. A function that takes one argument - the
  item from the list of results and transforms it into something else.  This
  function gets called once per each item in the list of results, and the list
  of values it returns becomes the return value of `List.Generate`. If
  `transform()` function is not specified, `List.Generate` will return the list
  of items at the moment when `condition()` returns `false`.

`List.Generate` might be easier to understand with the following pseudocode:
```python
def List.Generate(start, condition, next, transform=None):
    results = list()
    item = start()
    while condition(item) == True:
        results.append(item)
        item = next(item)
    if transform is not None:
        output = list()
        for item in results:
            output.append(transform(item))
    else:
        output = results
    return output
```

## A simple example

We will generate a table of data points for plotting a parabola. Internally we
will be storing each item as the record with `x` and `y` fields.  After that we
will transform that data into a Power Query table for output.

```
let
    data = List.Generate(
        () => [x=-10, y=100],
        each [x]<=10,
        each [x=[x]+1, y=x*x]
    ),
    output = Table.FromRecords(data)
in output
```

In this example `start()` is an anonymous function that always returns the
first data point, `condition()` and `next()` are also functions even though
they are written using `each` shortcut. There is no `transform()` function
because it is an optional parameter.

## An example from real world

In the real world you will not need the `List.Generate` magic for such simple
tasks, but you will still need it. Here is how I've used it recently.

Assume you have a list of tables that contain the data in the same format but
for different time periods or for different locations. You have a separate list
of locations (in the correct order), but each individual table does not contain
that information. That's why combining all these tables into one would create a
mess: you have to know which row comes from what table.

This can be done with `List.Generate`:

```
NamedTables = List.Generate(
    () => [i=-1, table=#table({},{})],  // initialize loop variables
    each [i] < List.Count(Tables),
    each [
        i=[i]+1,
        table=Table.AddColumn(Tables{i}, "TableName", each Names{i})
    ],
    each [table]
),
```

This code snippet assumes you have the list of tables in the `Tables` variable
and the list of their respective names in the `Names` variable. The loop starts
with index of -1 and an empty table, and adds a "TableName" column to each of
the tables. After this modification the tables can be safely combined with
`Table.Combine(NamedTables)` - no data loss will occur.

## Conclusion

Using `List.Generate` should be considered a last-ditch attempt to looping. M
has dedicated iterative functions for most common looping tasks, so please
check the standard library reference before creating such C-style loops
manually. They are rather hard to read, and readability counts!

I hope this article will help you to understand the Power Query Formula
Language a little more. It is a powerful tool and even though it is not
perfect, I hope you will find a lot of uses for it in your data crunching
tasks.

## An afterthought

Also, please keep in mind that the dot symbol in `List.Generate` does not have
the same meaning as in other languages either. There are no object methods in
M, and there are no namespaces, so the dot is just another character without
any special meaning.  It could have been a dash or an underscore - it wouldn't
have mattered.

[1]: https://msdn.microsoft.com/en-us/library/mt211003.aspx
[2]: https://msdn.microsoft.com/en-us/library/mt185361.aspx
