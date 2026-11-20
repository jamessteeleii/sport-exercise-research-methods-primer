# Citation and reference audit

Completed 29 October 2026. All **681 individual citations** in **551 citation groups** now use native Pandoc/Quarto citation keys and resolve to **488 cited works**. The master bibliography contains **658 records**; uncited library records and retained legacy references are available without being silently added to the book's works-cited list.

## Sources and reconstruction

The starting sources were the maintained nine Quarto chapters, the immutable Word draft, and scoped Better BibLaTeX/CSL exports from the local Zotero library. The exports contain 449 live bibliographic items from BOOK RESEARCH METHODS, 266 from STORK RM Book, and 21 additional exact matches to works cited in the draft. The group has chapter collections one to eight and an All collection; no chapter-nine collection was present. Group collection membership was used as supporting evidence, not assumed to be a complete or error-free inventory of each chapter.

736 exported Zotero records were consolidated to 635 sources, including 96 duplicate groups. Existing Better BibTeX citation keys were preserved. Word's 541 current-text citation fields and their structured metadata identified the intended works, including sources cited in footnotes. All 482 distinct embedded source records were matched to Zotero. The text migration replaced 537 matching citation occurrences, followed by a documented review of handwritten citations, duplicate author/year text, and quotation locators.

Eight entries were added for identifiable handwritten citations: Dolan et al. (2026), Franco et al. (2015), Zajonc (1965), Crossley (1996), the Human Tissue Act (2004), Einstein's letter to Thornton (1944), Newton's Principia (1687), and the James reprint dated 2000. Fifteen additional identifiable, uncited references from the original lists were retained as database entries. Their provenance is distinguished from verified Zotero and registry metadata.

The old reference-list inventory comprises 828 paragraphs representing 826 entries and two continuation fragments. Every paragraph has a documented match or continuation assignment in `reference-list-audit.csv`. The first chapter's imported list contained references from across the book; it was not treated as an accurate chapter-one-only bibliography. The complete old text remains in that CSV and the private source snapshots.

## Bibliography and rendering

`references.bib` is the maintained master. `_quarto.yml` declares `bibliography: references.bib`, the local APA 7 CSL style, `citeproc: true`, and `link-citations: true`. A single generated References chapter replaces the manually formatted lists. Citation suffixes, ordering, author presentation and reference formatting are generated from the database. Images, historical lifespan dates and ordinary dates are not misclassified as scholarly citations.

The nine files under `bibliography/chapters/` contain the sources actually cited in each chapter. The build script regenerates them and uses citeproc for standalone chapter Word review exports, so chapter reference lists are generated from the same master. Bibliography builds are local and do not depend on Zotero being open or on network access. The CSL licence and authorship are retained.

## Findings

The cited DOI inventory contains 321 distinct identifiers. Each was checked against Crossref or DataCite; rate-limited lookups were retried. Rajwani's exported DOI and page range were incorrect and have been corrected to DOI **10.1123/ssj.2020-0144**, volume 39(2), pages 205–215. The correction ledger also records Merton's title typo, Atkinson/Coffey/Delamont's coauthorship, Kuhn's sole authorship (Hacking supplied the introduction), the Belmont Report and NIH corporate authors, the Bacchieri/Della Cioppa chapter authors, Woodward's book type, and de Oliveira's complete author list and publication details. The publisher PDF establishes that the old list's 16 km/well-trained de Oliveira reference misdescribes the same work-based/recreationally-trained paper; no fictitious second work was retained.

**An editorial decision is required for Suresh (2011).** Chapter four recommends this randomisation overview, but it was retracted. Its Word field explicitly suppressed the retraction warning. The recommendation and citation remain available for the author/editor to review; no replacement source or substantive claim was invented. The Stein retraction notice in the same chapter is different: the surrounding text explicitly discusses that retraction, so its use is contextually appropriate.

Other review points include the James edition distinction, the malformed Eriksen preprint attribution, and independently checking the retained reference-only records before using them for new citations. Corrected legacy-list errors include Finlay's publication year, Spiegelberg's name/year, and the Strauss book title. Registry dates can describe an electronic or advance version rather than the cited print edition; mismatches were not used to change edition years automatically. For example, Rampinini's 2015 print date is supported by PubMed despite Crossref's 2014 online date.

`citation-issues.csv` distinguishes resolved corrections, contextual findings and remaining editorial actions. `bibliography-audit.csv` inventories all 658 entries, whether cited, chapter usage, creator/date/type, DOI status, provenance and missing metadata. Entries without DOIs are not described as failed DOI checks. A bibliographic audit does not establish that every cited work supports the author's claim; full content appraisal and author proof approval remain separate editorial work.

## Verification

- All 658 BibLaTeX entries round-trip through Pandoc with unique keys.
- All nine chapter bibliography subsets match their actual citation nodes.
- All 681 rendered HTML citation links reach existing reference anchors.
- The regenerated PDF's internal citation destinations were checked; representative text, table, quotation and reference pages were visually inspected.
- Chapter source checks preserve all 26 tables, 70 images, 20 mathematical expressions and 115 footnotes, together with the original headings and list structures apart from removal of the manual reference sections.
- The original Word SHA-256 remains `6d79f2e5f27ab77f2a6675e4f6e56e3557ce99f1eb06a96206612b1a773d3109`.
- No shared Zotero records, collections, original Word revisions, publication metadata, Git history or remote publication were changed.

The HTML/PDF reading edition is regenerated. Existing source placeholders and author approvals remain editorial matters; they were not resolved merely to obtain a clean build. The optional Word review workflow is wired to the new bibliography, but Word review files were not regenerated or visually approved in this audit.
