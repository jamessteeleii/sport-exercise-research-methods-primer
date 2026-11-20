# Approved adaptations of the shared research rules

The shared rules in D:/projects/agent_instructions/AGENTS.md remain unchanged. The root AGENTS.md contains the book-specific rules approved by the editors on 26 October 2026 for this repository only.

| Shared rule area | Book-specific rule | Reason |
| --- | --- | --- |
| Default R project, renv and targets scaffold | Apply only if substantive R computations are added | The imported text and assets form a static edited book |
| Pipeline execution requires separate delegation | Permit ordinary direct Quarto rendering for verification | Static renders do not execute an analytical pipeline; execution is disabled |
| manuscript/ as the default single-paper layout | Keep _quarto.yml at root and one qmd per chapter | Supports whole-book and chapter review exports from the same source |
| Zenodo stage lifecycle | Use a book editorial lifecycle and Kinesiology Books identifiers | The publisher provides book and chapter DOIs; no duplicate minting |
| A single manuscript citation | Separate editor/book and author/chapter metadata | An edited volume must preserve individual chapter attribution |
| Generic generated output policy | Keep Word reviews private; archive exact approved PDFs with hashes | Review copies can contain confidential comments; PDF identity matters for submission |
| Generic verification | Add author sign-off against chapter hashes, visual proofing, link and asset checks | A successful conversion does not establish author approval or layout fidelity |

Retain local clones outside cloud sync, small reviewable source changes, declared dependencies, relative paths, immutable inputs, secret protection, release integrity and the prohibition on unrequested commits/pushes/publication.
