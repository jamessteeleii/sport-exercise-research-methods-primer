# Research Methods in Sport and Exercise Science

An Open Access Primer, edited by Eimear Dolan and James Steele, developed in association with STORK. This is an unpublished draft prepared for editorial review and final contributing-author sign-off.

## Quick start

Work in a local clone outside Dropbox/OneDrive, normally D:/projects/sport-exercise-research-methods-primer. The sources render without R, renv, targets, raw analysis data or execution caches.

Install Quarto 1.9.38 or a compatible newer release, with its bundled Pandoc and Typst. Python 3.12+ runs the metadata/validation scripts using the standard library. Install the optional PDF splitter dependency with `python -m pip install -r requirements.txt`. No system LaTeX installation is needed for the default PDF.

From the repository root in PowerShell:

```powershell
# Build the reading site and its downloadable whole-book PDF
.\scripts\build.ps1 -Target web

# Preview the built site
quarto preview --to html

# Generate clean Word reading copies (without historical review markup)
.\scripts\build.ps1 -Target review

# Build every output
.\scripts\build.ps1 -Target all

# Prepare whole-book and individual chapter PDFs without submitting anything
python scripts/export_submission.py --stage draft
```

If Windows blocks a downloaded script, inspect it before using `Unblock-File .\scripts\build.ps1`. The script does not change execution policy or publish anything. A custom Python executable can be supplied with `-Python 'C:/path/to/python.exe'`.

The low-level equivalent for the site/PDF is `python scripts/sync_metadata.py` followed by `quarto render --to all`. `quarto render --to html` alone does not create the PDF; use a complete build before sharing a site with the PDF link.

## Files

- `_quarto.yml`: whole-book HTML and Typst/PDF configuration, chapter order and navigation.
- `chapters/`: nine maintained chapter sources with native Quarto citations.
- `references.bib`: consolidated Better BibLaTeX bibliography; `_quarto.yml` controls APA 7 formatting and citation links.
- `bibliography/chapters/`: automatically generated chapter bibliography subsets for standalone review copies.
- `backmatter/references.qmd`: the generated whole-book reference list.
- `editorial/citation-audit.md`: citation audit, provenance, corrections and remaining editorial questions, with companion CSV inventories.
- `frontmatter/`: the imported foreword. `index.qmd` is the new site introduction.
- `assets/`: supplied concept cover, original extracted figures and browser-compatible derivatives, and the Word style reference.
- `config/publication.json`: confirmed metadata, pending DOIs, authors and approvals.
- `config/source-manifest.json`: immutable Word source identity and import audit.
- `editorial/author-review.csv`: review coordination; `editorial/workflow.md`: author review and OMP handoff.
- `editorial/private/`: untracked review records; never served on the website.
- `_book/`: generated site and whole-book PDF. `_review/`: generated Word copies. `_submission/`: exact PDF packages and hash manifests. All are ignored by Git.

## Editorial status and import limits

The original `Full-Book_241026.docx` remains unchanged, ignored by Git, and identified by checksum. Initial Quarto sources use its current-text view. This includes insertions and excludes deletions in the derivative only; no revisions have been editorially approved. Historical comments and revisions remain in the original and in private extraction records, rather than becoming public book content.

The original manual table of contents was replaced by generated navigation. Figures, tables, equations, footnotes, links and chapter reference lists were imported, but conversion is not a fidelity guarantee. Compare the rendered proofs against Word, especially dense tables, figure captions, mathematical symbols, placeholder links and affiliation text. Existing missing image alt text and replacement characters are recorded for review.

After the initial import, edit Quarto sources. Re-importing a returned Word document over them can lose changes and is not the author-review workflow. Maintain a deliberate editorial diff.

## Citations and references

The citation migration completed on 29 October 2026. Use `[@existingCitationKey]` for a parenthetical citation, `@existingCitationKey` for an author named in the sentence, and `[-@existingCitationKey]` for a year-only citation after an author already named in the prose. Include quotation locators in the citation, for example `[@existingCitationKey, p. 4]`. Keep existing keys stable when updating bibliography metadata.

The project uses `bibliography: references.bib`, the local APA 7 CSL style, `citeproc: true` and `link-citations: true`. It generates a single whole-book References section; standalone chapter review exports generate chapter reference lists from the same data. Run `python scripts/chapter_bibliographies.py` after adding citations or bibliography entries; the build script also does this. See `bibliography/README.md` for maintenance and `editorial/citation-audit.md` for the audit and remaining source questions. The optional Word review workflow is connected but was not regenerated as part of this audit.

## Publication metadata

Kinesiology Books will issue both book and chapter DOIs. Leave unknown values null in config/publication.json. Once confirmed, run scripts/sync_metadata.py; it refreshes chapter citation metadata, book citation metadata, the citation page and confirmed site-url/book DOI fields. Inspect changes and rebuild. Update CITATION.cff and the release ledger with the confirmed edition before a release. The editors are not substituted for the chapter authors.

The final PDF on the site must be the exact approved whole-book PDF uploaded to the press. scripts/export_submission.py derives individual chapter PDFs from it and records checksums and physical page ranges. See editorial/workflow.md for the author-approval gate and OMP metadata/proof sequence.

No domain, DOI, publication date, ISBN or licence has been invented. The supplied cover still contains concept text/names and must be replaced before publication. Author approvals are pending. The review deployment is opt-in as described below; press submission and final publication remain separate editorial decisions.

## Author review edition

Use `scripts/export_author_review.py` to split the reviewed whole-book Word file
when historical Track Changes and comments must be retained. The ordinary
`build.ps1 -Target review` exports above create clean reading copies. The splitter
refuses to overwrite an earlier export and checks revision and comment integrity.
Keep its inputs and outputs private and share the relevant chapter with its authors.

```powershell
python scripts/export_author_review.py --source 'Full-Book_241026 - For review.docx' --output _review/NEW-REVIEW-ROUND/chapters
```

For the 20 November 2026 round, chapter one has both a current proof reflecting
the separately integrated author revision and a clearly named historical review
copy. Proofread the current chapter; the historical file is retained for context.
Chapters two to nine preserve the reviewed Word file's comments and revisions.
The clean HTML/PDF use the maintained Quarto sources, including the chapter two edits.

Every HTML page displays a draft banner. The PDF includes the supplied placeholder
cover art and draft headers. Headings are unnumbered. See
[the review Pages setup guide](editorial/github-pages-review.md) for the opt-in
Actions deployment. Only `_book/` is published. The `PUBLISH_REVIEW` repository
variable is unset by default, so an initial review-branch push only builds and checks.

## Project rules

AGENTS.md contains the approved book-specific adaptation of the shared reproducible R project rules. The shared template is unchanged. Review editorial/rule-adaptations.md for the concrete exceptions: static Quarto builds, chapter review, editorial sign-off and press-issued DOIs replace R-analysis defaults where those defaults do not apply.
