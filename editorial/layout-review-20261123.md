# Reading proof and accessibility updates, 23 November 2026

Requested by James before contributing-author review. These are draft reading
proofs; author approval and existing editorial questions remain pending.

## Changes

- HTML uses the available desktop/ultrawide width, retaining chapter navigation
  and the chapter contents sidebar. Tablet/phone layouts use the reading width
  with collapsible navigation and contained, keyboard-focusable table scrolling.
- Light is the initial theme. Native Quarto theme switching plus labelled
  reading controls provide dark mode and an optional OpenDyslexic font. Font
  files and their SIL OFL licence are bundled; preferences survive navigation.
- Whole-book search is visible in the desktop sidebar and via the phone/tablet
  search button. Search results link to matching chapters/sections.
- Each chapter has its own APA reference list, processed independently with
  Pandoc citeproc, including citations in notes, captions and tables. Chapter-end
  Footnotes precede References in HTML. PDF retains normal page-level footnotes,
  as clarified by James after the initial proof. No whole-book bibliography is
  rendered. Reference identifiers are unique within the merged PDF.
- Chapter one Acknowledgements is a level-two heading. James's supplied eight
  foreword paragraphs and signature follow Eimear's text, under separate names.
- Standalone figures are centred. Figure and table captions are smaller and
  shaded, with separation from body prose. Figure/caption groups and raster
  table/caption groups stay together in PDF. Compact native tables stay together;
  larger tables can split across pages with supported repeated headers.
- Native PDF tables have cell padding, thin rules and alternating shading.
  Imported caption rows are separated from actual column headings. Dense
  five/six-column tables have landscape pages; chapter nine's figure-examples
  tables have corrected column proportions so the images are legible.
- Fourteen inspected figures have padded white-margin crops using SVG viewports
  embedding the unchanged original raster bytes. Originals remain unchanged.
  Crops and hashes are in `config/figure-crops.json`; web fonts and hashes are in
  `config/web-fonts.json`.

## Verification

Used the tested Quarto 1.9.38 bundled with RStudio; no R execution was required.
Source and chapter bibliography checks pass (661 bibliography entries, 491 cited
works, 557 citation groups, 685 individual citations). All 685 rendered citation
links resolve, as do local assets and anchors. Twelve HTML pages retain the
draft banner. There is no obsolete References page, private editorial folder,
or Word file in the built site. Font files and their licence are local assets.

Live Chrome checks covered 3440-pixel ultrawide, 1920-pixel desktop, 768-pixel
tablet and 390-pixel phone viewports. No page-wide horizontal overflow was
observed. Dark-mode text/background, actual OpenDyslexic loading, full-width
tablet reading, contained 600-pixel tables on phone, the opening chapter menu
and a successful phone search for "Bayesian" linking from chapter one to chapter
five were verified. The viewport override was reset and the proof left in light
mode with the standard font. These are viewport simulations, not physical
device/browser compatibility certification.

PDF checks used page text/geometry plus rendered page images. Figure, table,
box, chapter-note and reference pages were visually inspected in contact sheets;
the Rubin vase/caption and a dense landscape table were also inspected at larger
size. Text-boundary checks found no text outside the printable area. Some short
landscape tables naturally leave page space; they use the wider page to preserve
readable text. Existing source placeholders and unresolved reference/editorial
questions remain as recorded in prior notes. No historical Word revisions or
comments were accepted/rejected, and no author approval was inferred.

After James clarified the footnote placement, the PDF was rebuilt with all 116
native footnotes, keeping the HTML's collected notes unchanged. The first notes,
Newton note and a long methodological note were checked in the regenerated PDF;
chapter reference lists and printable text boundaries were checked again. The
review validator now checks the retained Typst source for page-level PDF
footnotes, absence of collected PDF Footnotes headings and nine References
sections.

Changes and proofs are local. No commit, push, deployment, domain change, author
contact or press submission was performed.
