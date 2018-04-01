title: Unit testing in Power Query M Language
tags: m, power-query, LibPQ
date: 2018-04-01 12:00

As you code base gets bigger,
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
- Subtests to execute the same test on a sequence of sample inputs
- Test runner and test discovery functions to execute your test suites
- Test results table that can be analyzed either manually or with any
  automation tool you create

Inner workings of the test framework are described in the
[documentation][UnitTest]. This article will demonstrate how it works.

## UnitTest demo

All modules described here are imported with LibPQ, so a basic familiarity with the library is assumed ([readme], [getting started]).

This is how a simple test suite looks like:
```javascript
/* Demo test suite */
[
    Assert = LibPQ("UnitTest.Assert"),
    testFirstTest = Assert[Equal](6*7, 42),
    testAlwaysFail = Assert[Equal]("foo", "bar")
] meta LibPQ.TestSuite = 1
```

The test suite is a record (note the square brackets surrounding the code) that
contains:

- Two test cases (values prefixed with "test")
- And one related value: `Assert` is a helper for building test functions. Its
  use is not required, but makes writing tests much easier.

The last line contains metadata that marks the test suite as such and allows
test discovery tools to distinguish it from just another record.

Here is what [UnitTest.Discover] function will do when invoked:

- Search all locally available modules for valid test suites (hence the metadata)
- Execute every found test suite with [UnitTest.Run]
- Return the test results as a table

[LibPQ]: https://github.com/sio/LibPQ
[UnitTest]: https://github.com/sio/LibPQ/blob/master/Docs/UnitTesting.md
[readme]: https://github.com/sio/LibPQ/blob/master/README.md

[getting started]: {filename}20180401-getting-started-with-libpq.md
