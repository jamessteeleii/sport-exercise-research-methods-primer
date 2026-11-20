# Author review preparation on 20 November 2026

The editors requested individual Word chapters preserving the reviewed full-book
file's comments and Track Changes, alongside clean whole-book PDF and HTML
reading proofs. The reviewed Word file and the original are unchanged. The
reviewed source and chapter exports are recorded by checksum in the private
package manifest. This round does not record final author approval.

## Sources and review history

The reviewed whole-book file retains 479 insertions and 273 deletions. The split
historical chapters retain all of these revisions and 128 chapter comment
records, including modern Word thread metadata. Two front-matter comments stay
with the preserved full-book input. The splitter compares revision structure
and comment text against the selected source chapter, and retains only the
chapter's reachable package parts and relevant notes/comment threads.

The separately integrated first-chapter revision remains the maintained
edition. Its current Word proof is therefore supplied alongside the clearly
named historical first-chapter file. Chapters two to nine use the reviewed
whole-book Word input for markup review. These historical copies deliberately
retain their source formatting and citation fields so that the review context
is preserved. The clean proofs show the maintained Quarto formatting.

## Maintained reading edition

- Transferred the chapter two edits by deliberate text changes: the revised
  opening paragraph, forking paths, empirically answered table wording, chronic
  intervention qualifier, mixed approach sentence, observational exposure
  clarification and inductive generalisation qualifier.
- Removed manually typed heading numbers and heading-only emphasis. Clean
  HTML, PDF and current Word proofs use semantic, unnumbered Quarto headings.
  Clear section references were changed to linked heading names; one stale
  behaviourist-example reference was changed to refer to the earlier example.
- Normalised standalone figure/table/box caption labels and removed inherited
  Word highlight styling from the clean reading outputs. Existing figure/table
  numbers are retained for the associated prose references. Corrected the
  duplicate final figure number in chapter nine from 1 to 3.
- Repaired the column boundaries of the 17 grid tables after checking the
  rendered PDF. Cell text is preserved; boundary widths are now consistent
  across all rows. HTML checks reject visible unparsed grid-table borders.
  Wide tables scroll within their own area on mobile screens.
- Grouped all five separately supplied chapter one quotation attributions
  with their quotations and right-aligned them. Other chapter quotations were
  checked for this pattern; the source's five right-aligned attribution
  paragraphs are all in chapter one.
- Recovered chapter seven's first two diagrams from their original Word VML
  shape geometry and exact labels. Static SVG/PNG derivatives are in
  `assets/review-20261120/`. Text wrapping and font size were adjusted for
  legibility; terminology and relationships were retained for author checking.
- Added a prominent draft banner to every HTML page, draft PDF headers and the
  supplied placeholder cover artwork as a separate, explicitly labelled cover
  before the bibliographic title page. Draft output resources explicitly
  exclude editorial records, work folders and Word files.

## Outstanding author and editor questions

The chapter one incomplete phrase recorded in `ch01-revision-20261120.md` still
needs clarification. Chapter four's retracted methodological reference and
other bibliography questions remain in `citation-issues.csv`. Some inherited
cross-chapter LINK/REF placeholders and source-text problems remain for review;
clear link targets were fixed, but ambiguous targets and missing references
were not invented. Chapter eight's figure sequence starts at 2 in the supplied
source; the original Word file contains no additional unimported native shape
diagram for that chapter. Confirm whether a first figure is actually missing
or the labels need deliberate renumbering. Confirm chapter author lists,
affiliations and rights; these are not inferred from conversion.

Automated DOCX rendering failed because LibreOffice is unavailable and native
Word automation could not start in this execution session. Revision/comment
integrity checks are separate from layout verification. Open the files in
desktop Word before circulation to check pagination and markup appearance.
The PDF/HTML checks and package checksums are recorded privately. The review
workflow does not send messages to authors or publish the final edition.

## GitHub Pages

The prepared branch name is `review/author-review-2026-11-20`. The workflow
builds and checks on branch pushes; deployment remains off until the editor
sets `PUBLISH_REVIEW=true` and configures Pages/its deployment environment.
Follow `github-pages-review.md`. The draft banner and author-approval status
remain in place when the review site is enabled.
