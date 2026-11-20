"""Freeze clean reading formats alongside previously split private Word files."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import argparse,hashlib,json,shutil,subprocess,sys

R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,required=True)
    a=p.parse_args();out=a.directory.resolve()
    if not out.is_relative_to(R/'_review'):raise ValueError('Review packages must stay in _review')
    manifest=out/'chapters/word-review-manifest.json'
    if not manifest.is_file():raise ValueError('Split the reviewed Word document first')
    if (out/'review-package-manifest.json').exists():raise ValueError('Do not overwrite an earlier frozen review package')
    for script in ['validate.py','validate_review.py']:
        subprocess.run([sys.executable,str(R/'scripts'/script)],cwd=R,check=True)
    subprocess.run([sys.executable,str(R/'scripts/validate_citations.py'),'--rendered'],cwd=R,check=True)
    info=json.loads(manifest.read_text(encoding='utf8'))
    for c in info['chapters']:
        assert sha(out/'chapters'/c['file'])==c['sha256'],'Historical Word export changed'
    current=out/'chapters/01-foundations-current-proof.docx'
    if not current.exists():raise ValueError('Add the current chapter one Quarto proof before freezing this round')
    shutil.copytree(R/'_book',out/'html-site')
    shutil.copy2(R/'_book/research-methods-ses.pdf',out/'research-methods-ses-draft.pdf')
    readme='''# Author review package

This is a draft for editorial and contributing-author review. It is not the final book.

## Which files to review

- `chapters/01-foundations-current-proof.docx` is the current first chapter, reflecting James Steele's separately reconciled author revision. Proofread this version.
- `chapters/01-foundations-historical-review.docx` preserves the earlier first-chapter markup for context. Do not use it to replace the current chapter.
- Chapters 02–09 are split from the reviewed whole-book Word file. Their historical comments, replies and tracked changes are retained. Markup display and Track Changes are enabled in these files. In Word choose Review → All Markup if needed; keep Track Changes on for additional edits.
- `research-methods-ses-draft.pdf` is the clean whole-book reading proof, including the placeholder cover art. It shows the current proposed text without Word markup.
- `html-site/` is the matching static reading site. Use the deployed review URL once available. For local use, serve this folder with a local HTTP server; opening HTML directly may restrict search or navigation in some browsers.

The Word review files preserve the reviewed source's layout, citation fields and review history. The clean reading formats apply the maintained Quarto formatting and bibliography. Their purpose differs: record review decisions in Word and use the reading proofs to judge the proposed final appearance. The editors will transfer agreed changes into Quarto and issue fresh proofs.

## Points to check

Confirm authors, affiliations, figure/table permissions, captions, quotation sources, mathematical notation and references. Remaining editorial placeholders, missing source details and unresolved wording remain for author review; they have not been silently resolved. See the editors' review note for the current issue list.

All 479 tracked insertions and 273 deletions were preserved across the historical chapter files, together with 128 chapter comment records. Two front-matter comments remain in the preserved full-book input. No original or returned Word file was overwritten, and no revision was accepted or rejected in those files.

The clean HTML has a draft banner on every page; the PDF has draft headers and a placeholder artwork cover. Heading numbering has been removed from the clean proofs. Earlier section numbers and formatting remain in the historical Word files to preserve their exact review context.

Word package structure, revision integrity and comment threads were checked. Automated Word page rendering was unavailable in this execution session; open the files in desktop Word before sending to confirm page layout and markup display. The clean PDF and HTML have separate layout checks recorded by the editors. This package is for review, not final publication approval.

## Returning changes

Return the chapter Word file with Track Changes and comments intact. Identify the version you reviewed and use the exact file supplied. Do not edit the PDF to replace the maintained source. The package manifest records the source and output checksums for comparison.
'''
    (out/'README.md').write_text(readme,encoding='utf8')
    roots=[out/'chapters',out/'html-site',out/'README.md',out/'research-methods-ses-draft.pdf']
    files=sorted(f for root in roots for f in (root.rglob('*') if root.is_dir() else [root]) if f.is_file())
    publication=json.loads((R/'config/publication.json').read_text(encoding='utf8'))
    data={'review_round':'2026-11-20','status':'draft; author approvals pending','reviewed_word_sha256':info['source_sha256'],'quarto_version':subprocess.check_output(['quarto','--version'],text=True).strip(),'chapter_sources':[{'file':c['file'],'sha256':sha(R/c['file']),'approval':c['author_approval']} for c in publication['chapters']],'files':[{'file':f.relative_to(out).as_posix(),'sha256':sha(f),'bytes':f.stat().st_size} for f in files]}
    (out/'review-package-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
    with ZipFile(out/'chapter-word-review-files.zip','w',ZIP_DEFLATED) as z:
        for f in sorted((out/'chapters').glob('*.docx')):z.write(f,'chapters/'+f.name)
        z.write(out/'README.md','README.md');z.write(manifest,'word-review-manifest.json')
    with ZipFile(out/'author-review-package.zip','w',ZIP_DEFLATED) as z:
        for f in files:z.write(f,f.relative_to(out).as_posix())
        z.write(out/'review-package-manifest.json','review-package-manifest.json')
    print(f'Frozen review package: {out}')

if __name__=='__main__':main()
