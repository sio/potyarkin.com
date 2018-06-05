title: Excel as a CSV editor (with VBA)
tags: excel, vba, gist
date: 2018-06-01

One might think that Excel is a decent CSV editor as it is, but it's not. It is
a very capable CSV reader, I do not dispute that. When it comes to writing though,
Excel does not match what you'd expect from a mature application:

- It might change the delimiter character arbitrarily;
- It might write numbers in the regional format that does not map to a number
  anywhere outside Excel;
- It might add quotes that are inconsistent with the rest of the file.

If you're collaborating on the CSV file with others, their Excel version might
have different defaults and produce incompatible output.  Even if you're the only
one working on that CSV, you can forget about clean diffs and sensible atomic
commits to your version control system.

The only solution is not to overwrite CSV files you've opened with Excel. Use
another tool designed specifically for dealing with CSV or edit the file
manually in the text editor of your choosing.

## Append to CSV with VBA

I wrote a small helper utility to append data rows to the CSV files from Excel that
ensures you won't mess up the existing data. This is a one-day hobby project, and
Excel serves more as the UI toolkit and runtime environment than as the
spreadsheet application, so you should be careful if you decide to rely on that
code. The project is licensed under the [Apache License, Version 2.0][license].

Here is the code:

- [Main VBA module][CSVAppend.bas]
- The resulting [application], packaged in a workbook.

The application reads parameters from named ranges, opens the required file,
parses CSV header and displays a submission form for a new data row. Upon
submission it combines new values into a CSV string and appends it to the file.
All data manipulation is done in VBA. This app could have and should have been
written in any modern language - it would probably have cleaner code. Excel is
super easy to draft a simple UI though :)

The code is pretty straightforward so I'll highlight only the most interesting
parts.

## Reading and writing Unicode with VBA

Visual Basic for Applications is a hopelessly outdated environment. Unicode
support can be achieved only with the help of COM interoperability, namely the
`ADODB.Stream` object. This object provides a very comfortable interface for
reading and writing text files in a bytestream mode, and also handles character
encoding nicely.

Appending to a file is done via combination of seeking to the end of stream
and writing the new data.

## CSV packing and unpacking

I'm not exactly proud of how CSV string manipulations are implemented in the code.
If VBA would've provided some nicer regex capabilities or a CSV-aware library it
would've been better. I know about `VBScript.RegExp`, but it's an overkill for a
small task my app was created to accomplish.

Current implementation can not handle a quote symbol in the middle of the field
value. This is a known bug.

## Demo

This the main and the only UI my utility offers. Inputs and buttons are meant to
be self explaining. No value conversion is done when saving - the value of the
cell is written as is, quotes are added if delimiter character occurs within
the value.

Screenshot below is produced after loading demo CSV file with the following
header:

```
ID,Column1,Column2,Column3 with very long header,"Column4, with delimiter in the name"
```

[![CSV Append][screenshot]][screenshot]

The project is published for educational and archival purposes. I'll be glad if
you'll find any use for it.

[CSVAppend.bas]:
[application]:
[license]: http://www.apache.org/licenses/LICENSE-2.0
[screenshot]: {attach}/resources/csv-append.png
