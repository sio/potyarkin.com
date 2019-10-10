title: Unit testing in Power Query M Language
tags: m, power-query, LibPQ
date: 2018-04-01 12:00

As your code base gets bigger,
[test automation](https://en.wikipedia.org/wiki/Test_automation) becomes more
and more important. This applies to any development platform, including Power
Query / PowerBI. If you reuse your code and improve some low level function
later, test automation allows you to make sure your changes did not break
anything that depends on the part of code you've just modified.

As far as I know, there are no tools that allow us to perform automated testing
of functions and queries written in Power Query M language. That's why I've
built a simple unit testing framework into [LibPQ].

## LibPQ UnitTest framework

The [UnitTest] framework is modelled after the only other unit testing tool I
have experience with: Python's
[unittest](https://docs.python.org/3/library/unittest.html). It offers the
following features:

- Test suites to arbitrarily group individual test cases
- Assertion functions to test simple statements
- Subtests to execute the same test on a sequence of sample inputs
- Test runner and test discovery functions to execute your test suites
- Test results table that can be analyzed either manually or with any
  automation tool you create

Inner workings of the test framework are described in the
[documentation][UnitTest]. This article will demonstrate how it works.

## UnitTest demo

All modules described here are imported with LibPQ, so a basic familiarity with the library is assumed ([readme], [getting started]).

Let's create a basic test suite and save it in the directory listed in `LibPQPath`:

```javascript
/* DemoTests.pq - sample test suite */
[
    Assert = LibPQ("UnitTest.Assert"),
    testFirstTest = Assert[Equal](6*7, 42),
    testAlwaysFail = Assert[Equal]("foo", "bar")
] meta [LibPQ.TestSuite = 1]
```

The test suite is a record (note the square brackets surrounding the code) that
contains:

- Two test cases (values prefixed with "test")
    - The first test will pass because 6 times 7 is 42
    - The second test will always fail because "foo" and "bar" are different
    strings
- And one related value: `Assert` is a helper for building test functions. Its
  use is not required, but makes writing tests much easier.

The last line contains metadata that marks the test suite as such and allows
test discovery tools to distinguish it from just another record.

Here is what [UnitTest.Discover] function will do when invoked:

- Search all locally available modules for valid test suites (hence the metadata)
- Execute each located test suite with [UnitTest.Run]
- Return the test results as a table, reporting as much data about the failed
  tests as possible

[![Test results][img-unittest-long]][img-unittest-long]

In the screenshot above we invoke [UnitTest.Discover] with `compact_output =
false` but when you'll have dozens of test cases you'll probably prefer default
behavior (group test results by status).

## More about UnitTest in LibPQ

If you liked the idea of unit testing M language code, check out the main
[UnitTest] documentation and a more extensive [test sample] that makes use of
subtests.

[LibPQ]: https://libpq.ml
[UnitTest.Discover]: https://github.com/sio/LibPQ/blob/master/Modules/UnitTest.Discover.pq
[UnitTest.Run]: https://github.com/sio/LibPQ/blob/master/Modules/UnitTest.Run.pq
[UnitTest]: https://libpq.ml/Docs/UnitTesting
[readme]: https://libpq.ml
[test sample]: https://github.com/sio/LibPQ/blob/master/Samples/Tests.Sample.pq

[getting started]: {filename}20180401-getting-started-with-libpq.md
[img-unittest-long]: {attach}/resources/libpq-unittest-long.png
