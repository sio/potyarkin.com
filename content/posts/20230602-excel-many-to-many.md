title: Many-to-many relationships in Excel data model
tags: excel
slug: excel-many-to-many
date: 2023-06-02

This is a quick hack to build many-to-many relationships in Excel data model
even though they are not supported out of the box.

  - Create intermediate [calculated table][DAX table] and use DAX to fill it
    with unique values from related columns on both sides of the relationship:

        EVALUATE
          FILTER(
            DISTINCT(
              UNION(
                VALUES('TableA'[Field]),
                VALUES('TableB'[Field])
              )
            ),
            NOT(ISBLANK([Field]))
          )

  - Create two one-to-many relationships placing this intermediate table in
    between

For all intents and purposes you may now forget that this intermediate table
exists: it will get updated automatically whenever you update the data model,
and it will not consume much resources. Pivot tables and DAX formulas will
work as if the two original tables were directly connected via many-to-many
link.

A similar intermediate table may be created with Power Query, but that's a lot
less elegant (unless you're already using Power Query elsewhere in the
workbook) and takes significantly longer to recalculate.

[DAX table]: https://stackoverflow.com/a/70682229
