// Shared proof typography. Imported table content remains unchanged.
#set table(
  inset: 6pt,
  stroke: (x: 0.35pt + rgb("ccd3c6"), y: 0.35pt + rgb("ccd3c6")),
  fill: (x, y) => if calc.odd(y) { rgb("f2f5ee") } else { white },
)
#show table: set text(size: 8.5pt)
#show table.cell: set par(justify: false, leading: 0.55em)
#show table.header: set text(weight: "bold")
#show figure.caption: set text(size: 9pt)
#show figure.caption: set par(justify: false)
