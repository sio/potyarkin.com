title: Declaring bankruptcy on Advent of Purescript 2023
tags: programming, purescript, advent-of-code
slug: aoc2023-bankruptcy
date: 2024-01-09

Advent of Code is a [fun challenge] and this year I decided to attempt
[solving it in Purescript][solutions]. Today I'm declaring this attempt a
failure. This post will serve as a postmortem.

[fun challenge]: {filename}/posts/20230309-aoc2022.md
[solutions]: https://sio.github.io/advent-of-code/2023/


## Choosing Purescript

Last year I solved my first Advent of Code using Go. It was fun and I knew
immediately that I will come back for the next AoC. I also knew that I won't
be solving it using the same language - learning on the go (pun intended)
contributed significantly to my enjoyment of AoC 2022.

In November 2023 I listened to an [old podcast] where Richard Feldman
evangelises Elm programming language. I got interested and initially decided
to use Elm for the upcoming Advent of Code. While I was learning the basics of
the language I also learned about the ongoing old controversy in Elm community
related to how its BDFL handles communication and development. I decided that
that's too much drama for my liking and that it has too little hope of
resolving anytime soon
- and that it's better to stay away from Elm.

That's how I ended up with [Purescript]. It was probably the only other
frontend language that offered functional programming with a strong type
system and a [nice UI framework][Halogen]. I hoped that using an
unconventional language would introduce me to frontend development without
dealing with unpleasant Javascript ecosystem.

[old podcast]: https://corecursive.com/teaching-fp-with-richard-feldman/
[Purescript]: https://www.purescript.org/
[Halogen]: https://github.com/purescript-halogen/purescript-halogen


## Learning Purescript

My only prior experience with functional programming was Microsoft's Power
Query [M language]({tag}/m) which is rather narrowly focused on data
processing and is not a general purpose language.

So, with effectively zero prior knowledge I started learning from [The
Purescript Book](https://book.purescript.org/) but quickly switched to
[Functional Programming Made Easier](https://leanpub.com/fp-made-easier) by
Charles Scalfani - the former was too fast paced for me.
Scalfani's book was an enjoyable read even if a little too verbose.
I did not follow author's advice to type out and run all code snippets from
the book - that may have contributed to my eventual failure but I don't think
that it was a major factor.


## Failing Purescript

I enjoyed solving small textbook problems in Purescript. It's a very nice
language. Here are the things I liked most about it:

- Separation of pure and effectful functions
- Fearless refactoring
- Clean and readable syntax
- Pattern matching with exhaustiveness checking
- Function currying, tail call optimisation and other FP niceties
- Type system

I had no problems with understanding recursion, currying, pattern matching,
etc. I had relatively little problems with understanding monads and related
concepts.

My problem was that these nice abstract concepts just did not translate in my
head to applicable programming techniques. Simple practical tasks tripped me
up hard.

Parsing text was painful. For the first AoC puzzle I decided to [tough it out]
with a bespoke char based parser even though I vaguely understood that there
should be a monad based parser combinator library for that. That vague
knowledge was not provided by any of these books, I've picked it up
accidentally from some random blog post on the web.

For the second AoC day I [used the proper library]. It was better but still
felt unnecessarily difficult. When third day's puzzle called for a parser not
based on regular grammar my mind just blanked out. I was loaded up to the brim
with pure theory and I lacked practical knowledge to apply it.

All this time while I was struggling with text parsing the actual tasks I
picked up Purescript for (frontend experiments and puzzle solving) were
deprioritized to background. I have to commend Purescript and Halogen on this
because if it was anything less than straightforward none of UI and/or puzzle
solutions would get done - I just barely devoted any time to that.

The project got stalled. I was reluctant to finish the last chapters of
Scalfani's book because I was confident that they won't provide me with
practical knowledge I was lacking. I was hesitant to go web diving for new,
more practical learning materials because I wasn't sure they exist -
Purescript community is rather small, and most learning resources are
enumerated in multiple places. I evaluated those lists the first time I looked.
I probably should've gone looking for more generic functional programming
knowledge - and that would blow my free time budget.

So I'm just declaring bankruptcy on this project.

[tough it out]: https://github.com/sio/advent-of-code/blob/18c766f757eb71af581ffdeabba056586cf1bd3b/aoc2023/src/Day01/Solve.purs#L137-L147
[used the proper library]: https://github.com/sio/advent-of-code/blob/18c766f757eb71af581ffdeabba056586cf1bd3b/aoc2023/src/Day02/Solve.purs#L112-L120


## Conclusion

Even though I failed to cowboy my way into Purescript I still got [the
solutions to first two days][solutions] of Advent of Code to show off -
all logic executed client side, all UI generated on demand, all type safe and
checked at compile time.

I could probably pour more effort, practise more, find new learning resources
- and complete the remaining challenges. I'm stubborn enough to see this through.
But my hobby time is not unlimited and there are other projects waiting -
I'm certain I will enjoy some of those more.
