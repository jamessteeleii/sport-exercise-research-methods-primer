"""Create an immutable author review round from checked proofs and Word history.

Only the reading site is public. The full package and chapter-specific ZIPs
contain private editorial markup and must be shared directly with the authors.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as E

from export_author_review import split

R = Path(__file__).resolve().parents[1]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args):
    subprocess.run([str(x) for x in args], cwd=R, check=True)


def zip_files(dest, files, root):
    with ZipFile(dest, 'w', ZIP_DEFLATED) as z:
        for f in sorted(files):
            z.write(f, f.relative_to(root).as_posix())


def html_copy(source, dest):
    run('quarto', 'pandoc', source, '--standalone', '--to=html',
        '--metadata=pagetitle:Author review instructions', '--output', dest)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--date', required=True, help='Review round YYYY-MM-DD')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--directory', type=Path, required=True)
    a = p.parse_args()
    out = a.directory.resolve()
    if not out.is_relative_to(R / '_review') or out.exists():
        raise ValueError('Choose a new directory within _review; earlier rounds are immutable')
    source = a.source.resolve()
    original_hash = sha(source)
    for script, extra in [('validate.py', []), ('validate_review.py', []),
                          ('validate_citations.py', ['--rendered'])]:
        run(sys.executable, R / 'scripts' / script, *extra)

    info = split(source, out / 'chapters')
    current = out / 'chapters/01-foundations-current-proof.docx'
    run('quarto', 'pandoc', 'chapters/01-foundations.qmd', '--from=markdown',
        '--to=docx', '--standalone', '--resource-path=chapters;.', '--citeproc',
        '--bibliography=bibliography/chapters/01-foundations.bib',
        '--csl=bibliography/apa.csl', '--metadata=link-citations:true',
        '--metadata=reference-section-title:References',
        '--lua-filter=scripts/book-formatting.lua',
        '--reference-doc=assets/review-reference.docx', '--output', current)
    # Enable future author edits; no historical revisions exist in this proof.
    with ZipFile(current) as z:
        parts = {n: z.read(n) for n in z.namelist()}
    settings = E.fromstring(parts['word/settings.xml'])
    for name in ['trackRevisions', 'revisionView']:
        for element in list(settings.findall(W + name)):
            settings.remove(element)
    E.SubElement(settings, W + 'trackRevisions')
    view = E.SubElement(settings, W + 'revisionView')
    for name in ['markup', 'comments', 'insDel', 'formatting']:
        view.set(W + name, 'true')
    parts['word/settings.xml'] = E.tostring(settings, encoding='utf-8', xml_declaration=True)
    with ZipFile(current, 'w', ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    doc = E.fromstring(parts['word/document.xml'])
    drawing = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
    assert len(list(doc.iter(drawing + 'blip'))) == 14, 'Chapter one must retain all 14 figures'

    shutil.copytree(R / '_book', out / 'html-site')
    pdf = out / f'research-methods-ses-author-review-{a.date}.pdf'
    shutil.copy2(R / '_book/research-methods-ses.pdf', pdf)
    for name in ['author-review-instructions.md', 'author-review-email.md']:
        shutil.copy2(R / 'editorial' / name, out / name)
    html_copy(out / 'author-review-instructions.md', out / 'author-review-instructions.html')
    publication = json.loads((R / 'config/publication.json').read_text(encoding='utf8'))
    issues = {
        1: 'Clarify the incomplete phrase "some underlying theoretical for which we wish to make inferences". Confirm the intended Bolt reference/edition where noted in the editorial review.',
        2: 'Confirm the remaining participant-recruitment cross-reference and the full McKay citation details.',
        3: 'Confirm the intended target of the opening research-question cross-reference.',
        4: 'Resolve the methodological use of the retracted Suresh randomisation overview: please supply a suitable replacement or an explicit editorial decision. The Stein retraction notice is cited as a retraction and is a separate case.',
        5: 'Check the hypothesis-testing table for inherited missing/corrupted symbols. Supply the intended confidence-interval app and causal-inference resource links.',
        6: 'Confirm the intended James Principles of Psychology edition and Bolt reference where queried; confirm the cross-reference to qualitative analysis.',
        7: 'Check the recreated first two diagrams, philosophical/inference cross-references and retained reference-only entries.',
        8: 'Confirm whether Figure 1 is missing or the sequence should begin at 1; the supplied sequence currently begins at 2. Confirm the remaining links to chapters 2 and 5.',
        9: 'Check figure numbering and external resource links in the clean proofs, including the writing-course URL.'
    }
    summary = [f'# Author review round {a.date}', '',
               'Prepared for contributing-author review. No files have been sent automatically. '
               'Send the dated PDF and instructions with the relevant chapter ZIP; '
               'retain the complete package as the editors\' record. Each chapter ZIP contains '
               'only that chapter\'s Word files and review notes.', '',
               'HTML: https://sportexercisemethods.org/', '',
               'PDF: https://sportexercisemethods.org/research-methods-ses.pdf', '',
               'The dated PDF is byte-identical to the PDF in the frozen HTML snapshot. '
               'The live site should be checked after deployment before circulation.', '',
               '| Chapter | Authors | File to edit | Comments | Insertions / deletions |',
               '| --- | --- | --- | ---: | ---: |']
    chapter_zips = out / 'chapter-packages'
    chapter_zips.mkdir()
    for chapter, history in zip(publication['chapters'], info['chapters'], strict=True):
        n = chapter['number']
        edit_file = current.name if n == 1 else history['file']
        summary.append(f'| {n}. {chapter["title"]} | {", ".join(chapter["authors"])} | '
                       f'`{edit_file}` | {history["comments"]} | {history["ins"]} / {history["del"]} |')
        note = out / 'chapters' / f'{n:02d}-review-notes.md'
        note.write_text(f'# Chapter {n} author review\n\nReview round: {a.date}\n\n'
                        f'**{chapter["title"]}**\n\nAuthors: {", ".join(chapter["authors"])}\n\n'
                        f'File to edit: `{edit_file}`.\n\n'
                        f'Reading proof: https://sportexercisemethods.org/{Path(chapter["file"]).with_suffix(".html").as_posix()}\n\n'
                        f'Please address every existing comment and tracked edit and check both clean reading proofs. '
                        f'Additional points identified during preparation: {issues[n]}\n\n'
                        'These are questions for review; no missing text, references or review decisions have been inferred.\n',
                        encoding='utf8')
        selected = [out / 'chapters' / history['file'], note,
                    out / 'author-review-instructions.md', out / 'author-review-instructions.html']
        if n == 1:
            selected.append(current)
        zip_files(chapter_zips / f'chapter-{n:02d}-author-review-{a.date}.zip', selected, out)
    summary += ['', 'Counts refer to the preserved historical files, including chapter one\'s context copy. '
                'Across these files all 479 insertions, 273 deletions and 128 chapter comment records survive. '
                'Two front-matter comments remain in the unchanged full-book review input.', '',
                'The current chapter one proof has tracking enabled for new edits and supersedes its historical text. '
                'The historical files retain Word formatting and citation fields; the clean proofs use the maintained '
                'book formatting and references. The current Word proof uses the original raster figures for Word '
                'compatibility; HTML/PDF use the checked white-margin crops.', '',
                'Word revisions, comments, anchors, relationships and ZIP integrity were checked. '
                'Desktop Word pagination and markup appearance still need a visual check before circulation. '
                'Author approval, final cover/rights and publication metadata remain pending.', '']
    (out / 'README.md').write_text('\n'.join(summary), encoding='utf8')
    html_copy(out / 'README.md', out / 'overview.html')

    for c in info['chapters']:
        assert sha(out / 'chapters' / c['file']) == c['sha256']
    assert sha(source) == original_hash
    assert sha(pdf) == sha(out / 'html-site/research-methods-ses.pdf')
    for path in (out / 'chapters').glob('*.docx'):
        with ZipFile(path) as z:
            assert z.testzip() is None
            settings = E.fromstring(z.read('word/settings.xml'))
            assert settings.find(W + 'trackRevisions') is not None
    files = sorted(x for x in out.rglob('*') if x.is_file())
    manifest = {
        'review_round': a.date, 'status': 'prepared; not sent; author approvals pending',
        'live_html_url': 'https://sportexercisemethods.org/',
        'live_pdf_url': 'https://sportexercisemethods.org/research-methods-ses.pdf',
        'reviewed_word_sha256': original_hash,
        'quarto_version': subprocess.check_output(['quarto', '--version'], text=True).strip(),
        'chapter_sources': [{'file': c['file'], 'sha256': sha(R / c['file']),
                             'approval': c['author_approval']} for c in publication['chapters']],
        'files': [{'file': f.relative_to(out).as_posix(), 'sha256': sha(f),
                   'bytes': f.stat().st_size} for f in files]
    }
    ledger = out / 'review-package-manifest.json'
    ledger.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
    zip_files(out / 'chapter-word-review-files.zip',
              [f for f in files if f.parent == out / 'chapters'] +
              [out / 'README.md', out / 'author-review-instructions.md',
               out / 'author-review-instructions.html', ledger], out)
    zip_files(out / 'author-review-package.zip', files + [ledger], out)
    zip_files(out / 'html-reading-proof.zip',
              [f for f in files if f.is_relative_to(out / 'html-site')], out / 'html-site')
    print(f'Prepared {out}; nine individual chapter ZIPs and full dated package; source inputs unchanged.')


if __name__ == '__main__':
    main()
