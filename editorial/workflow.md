# Editorial and publication workflow

## Current state

The original Full-Book_241026.docx is unchanged and intentionally ignored by Git. Its SHA-256 identity is in config/source-manifest.json. The reading sources are a provisional import of its current-text view, including tracked insertions and excluding tracked deletions only in the derivative. The original still contains all tracked changes and comments. The import is not an approval of them.

Private comment anchors and revision records are in editorial/private. Their status is unreviewed. Keep the original and private records backed up in approved editorial storage. Do not publish them. The original's 129 comment records can include replies or resolved discussions; review context in Word before treating every record as an open issue.

The Word TOC and original title page were replaced by Quarto navigation/title metadata. Chapter headings were normalised for navigation. Author lines, affiliations, prose and formatted reference lists were retained. Fifteen single-column Word layout tables became semantic prose/exercise blocks; 26 comparative tables remain tables. Footnote labels are unique across chapters. The initial import retained subsection numbers. The November review edition now uses unnumbered semantic headings in the clean reading proofs; historical Word files retain their original review context. Imported Word diagrams and tables still require comparison with the original. Embedded citation fields are not a reconstructed bibliographic database.

## Author review

The 29 October 2026 citation migration supersedes the initial formatted reference lists: maintained sources now use native citations and a consolidated Better BibLaTeX bibliography, with generated book/chapter lists. See citation-audit.md and citation-issues.csv before requesting final author approval, particularly the retracted methodological source identified in chapter four. The historical import records and Word original remain unchanged.

1. Review the import against Word, including the current-text view, all comments and tracked edits. Check tables, equations, captions, figures, internal links, references and affiliations.
2. Choose the right Word export. `scripts/build.ps1 -Target review` creates clean reading copies from Quarto. To preserve historical comments and tracked changes, run `scripts/export_author_review.py --source 'Full-Book_241026 - For review.docx' --output _review/NEW-REVIEW-ROUND/chapters`. This splits the reviewed Word package without accepting or rejecting revisions and verifies revision and comment integrity. Keep these files private. Chapter one additionally needs its current Quarto proof because the separately reconciled author revision supersedes the historical chapter in the full-book Word file.
3. Share the relevant file with the author yourself. Ask for Track Changes and comments. Record sent/return dates in editorial/author-review.csv. Store returned files under editorial/private.
4. Address and transfer agreed edits into the chapter qmd. Compare the next render and obtain final approval for that version.
5. Record author_approval, approved_source_sha256 and approved_date in config/publication.json. Synchronise citation metadata before taking the final source hash. Retain the evidence privately and update the review CSV for coordination.

The CSV coordinates correspondence; config/publication.json is authoritative for the approval gate. All approvals start pending. The build does not send messages.

## Kinesiology Books submission

This checklist is derived from the supplied STORK_OMP-Submission-Procedures 1.pdf (updated 2026-09-21). The user performs submission; agents do not interact with the press automatically.

1. Prepare the edited volume metadata and whole-book and individual-chapter files. Enter volume editors and chapter authors with their correct roles. Keep email/country correspondence metadata private rather than putting it in a public tracking file.
2. Generate the draft PDF, then scripts/export_submission.py --stage submission after approvals are recorded. The chapter PDFs are extracted from the exact whole-book PDF, preserving the book's page numbering. Verify displayed page ranges for OMP's Pages fields; the manifest's physical PDF page positions are not automatically those labels.
3. Submit as an Edited Volume and associate each chapter with the correct contributors and file. Record the actual assigned chapter identifiers. Ask the press to confirm the book DOI; do not guess it from a pattern.
4. Enter confirmed book/chapter DOIs and the publication date in config/publication.json, run scripts/sync_metadata.py, inspect citation metadata and rebuild all formats. Citation changes change the source hash and may require a renewed proof approval record.
5. Upload DOI-bearing final PDF proofs at Copyediting as instructed by the press. Generate with --stage final-proofs only after approved hashes and confirmed metadata are present. Name files clearly and verify every DOI in the PDFs.
6. At publication, check title, authors, editors, abstracts, page ranges, references, identifiers, final cover, licence, ISBN if assigned, and the correct final files. The guidance also describes adding the Quarto URL as a separate website publication format.
7. Keep the exact whole-book approved PDF on the website and in the press submission, with a SHA-256 manifest. Confirm DOI resolution after registration; do not assume the timing is guaranteed.

## Website and editions

No custom domain, site-url, publishing date, licence, DOI or ISBN has been invented. The opt-in review deployment workflow builds the dedicated review branch and publishes only `_book/` when the repository variable `PUBLISH_REVIEW` is exactly `true`. See `github-pages-review.md` for setup. Draft publication is separate from final publication approval.

Replace the concept cover before publication: its displayed title, subtitle and editor names are not the actual final metadata. Confirm reuse rights and add useful figure alt text. Record editorial versions in config/releases.json. Freeze approved submission/publication outputs in versioned storage outside ordinary source history; keep earlier editions intact.
