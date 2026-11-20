# Book bibliography

`../references.bib` is the maintained master BibLaTeX file. Quarto reads it using the project-level `bibliography`, `csl`, `citeproc` and `link-citations` settings in `_quarto.yml`. APA 7 is supplied locally in `apa.csl`; its authorship and licence are retained in the file.

The bibliography was consolidated from Better BibLaTeX exports of **BOOK RESEARCH METHODS**, **STORK RM Book**, and 21 exact matches to cited works elsewhere in the local Zotero library. Existing Better BibTeX citation keys are retained. Copies of the same work are consolidated; original Zotero item URIs and duplicate mappings are recorded in `../config/bibliography-manifest.json`. A citation key's trailing letter is a stable identifier, not a manually assigned author-date suffix: citeproc generates any displayed year suffixes.

`supplemental.bib` and `supplemental.json` contain eight entries added for identifiable handwritten citations. `reference-only.bib` and `reference-only.json` preserve fifteen additional identifiable works in the old reference lists. They are included in the master file, so do not add these files to the Quarto YAML a second time. Some reference-only entries are transcriptions of the manuscript rather than independently verified records; the audit distinguishes their status.

Only cited works appear in the rendered reference list. Uncited library records and reference-only entries remain available in the master database. `chapters/*.bib` are generated subsets containing the sources actually cited in each chapter, including its footnotes, tables and added handwritten citations. Standalone chapter review exports use these subsets and generate their own reference lists.

After adding or correcting an entry in the master file, keep its citation key stable and run:

```powershell
python scripts/chapter_bibliographies.py
python scripts/validate_citations.py
quarto render --to all
python scripts/validate_citations.py --rendered
```

The normal build script also regenerates and validates the chapter subsets. Builds do not require Zotero, a network connection, or a live auto-export. A future Zotero re-export should be reconciled against the manifest and `../config/bibliography-corrections.json`; do not overwrite the master file blindly, regenerate existing keys, or discard the supplements. No shared Zotero records or collections were changed during this migration.

The old reference lists, every source citation conversion, the registry checks and the remaining editorial questions are described in `../editorial/citation-audit.md` and its companion CSV files. The unmodified Word original and private source snapshots retain the original evidence.
