title: Turn Excel into a CSV editor with VBA
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
have different tastes and produce incompatible output.  Even if you're the only
one working on that CSV, you can forget about clean diffs and sensible atomic
commits to your version control system.

The only solution is not to overwrite CSV files you've opened with Excel. Use
another tool designed specifically for dealing with CSV or edit the file
manually in the text editor of your choosing.

I wrote a small helper tool to append data rows to the CSV files from Excel that
ensures you won't mess up the existing data. This is a one-day hobby project, and
Excel serves more as the UI toolkit and runtime environment than as the
spreadsheet application, so you should be careful if you decide to rely on that
code. The project is licensed under the Apache License, Version 2.0.

Here is the code:

- [Main VBA module][CSVAppend.bas]
- The resulting [application], packaged in a workbook.

[CSVAppend.bas]:
[application]:
