# Local formatting and cross-reference proof, 23 November 2026

Requested by James after the author-review circulation package was frozen.
These changes are local proofs awaiting his review. The earlier dated package
has not been regenerated or overwritten. No staging, commit, push or deployment
was performed.

## Presentation

- Shared HTML rules now control cover size and reading geometry in both themes.
  The cover is 245 px wide on desktop and 175 px on small screens. The landing
  page and 88 chapter-three heading/paragraph/table elements had identical
  dimensions when switching between light and dark mode.
- The desktop chapter sidebar ends before the reading gutter, rather than
  extending into it. The gutter scales from 48 to 80 px with window width;
  the reading area continues to fill the available space. Mobile retains the
  collapsible menu and contained table scrolling.
- Table captions are retained whether imported as a title row, a separate
  paragraph, or a native Pandoc caption. This restores chapter three's Table 1
  in the PDF and removes its previously printed column-width attribute.
- Real column headings are promoted into table headers, including the two-tier
  headings in chapter two's design comparison and chapter five's Anscombe table.
  Chapter seven's two-column analysis summaries have neutral Analysis/Focus
  labels. Chapter nine's split Table 1 has an explicit continued caption and
  repeated column headings. Its original grid was widened to accommodate the
  added Figure 2 link without disrupting the cells or their images.
- Chapter three's effect-size table has usable widths in all four columns.
  Two chapter-eight breakout boxes imported as layout tables are presented as
  boxes; they are not additional numbered data tables.

## Numbering and references

All captions retain chapter-local numbers. Explicit source links target unique
chapter-specific caption anchors in HTML and the merged PDF. The manifest is
`config/crossref-manifest.json`; `scripts/validate_crossrefs.py` checks caption
sequences, duplicate/missing targets, linked numbers and real table headers.
The review validator calls these checks as part of future proof builds.

Corrections:

- Chapter one's first philosophical-traditions table citation pointed to
  Table 2; it now points to Table 1.
- Chapter eight had four figures numbered 2–5. They and their in-text citations
  now run consecutively from 1–4.
- Chapter two's Figure 1 citation links to the figure in chapter one.
- Figure-panel references (4.1–4.3 and 10a/10b in chapter one) link to their
  parent figures while retaining the panel labels in the text.

External table references in chapter three and the quoted hypothetical
manuscript Table 1 in chapter nine remain unlinked to this book's tables.

**Unresolved:** chapter nine's final summary refers to a resources Table 3, but
that table is absent from both the maintained chapter and the original Word
draft. The original proceeds from that paragraph to the closing paragraph,
Acknowledgements and References without it. No replacement table or misleading
link has been invented. The editors/authors need to supply the intended table
or agree an amendment to that sentence.

## Verification and review limits

Quarto 1.9.38 was used to rebuild HTML and Typst/PDF. Source/bibliography,
rendered citation, local link/anchor, private-file exclusion, caption-sequence
and table-header checks pass: 78 numbered captions, 93 HTML table/figure links,
685 bibliographic links and 12 draft pages. The PDF's 78 captions and sampled
table/figure link annotations were checked against their destination text and
chapter. Thirty-three representative PDF pages were rendered for visual review;
the final effect-size column-width adjustment was inspected separately. Native
page footnotes and chapter reference sections remain in the PDF.

The original Word SHA256 still matches the source manifest:
`6d79f2e5f27ab77f2a6675e4f6e56e3557ce99f1eb06a96206612b1a773d3109`.
Source comparison preserves prose, bibliographic citations and all image paths,
apart from the listed numbering corrections and added cross-reference links.
Existing editorial placeholders, pending author sign-off and publication
metadata remain unresolved. This is a formatting proof, not publication approval.

## Execution and next handoff

The process still runs as `codexsandboxoffline`. Source edits, local rendering
and the preview server worked without escalation. The main directory's Git
metadata reports an unborn `main` and all project sources as untracked; this
state was preserved. The existing `work/author-review-20261123-checkout` is clean
on `review/author-review-2026-11-20` tracking the corresponding origin branch.
Use that existing history deliberately after James reviews the proof; do not
create another workaround checkout or stage the main directory wholesale.
