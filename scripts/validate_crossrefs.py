"""Check chapter caption sequences and the actual rendered cross-reference targets.

Uses only the standard library. PDF annotation checks can additionally be run
with the project's optional pypdf dependency during proof inspection.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import json
import re

R = Path(__file__).resolve().parents[1]
LABEL = re.compile(r'(table|figure)-(ch\d+)-(\d+)')


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = Counter()
        self.links = []
        self.tables = []
        self.table = None
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids[a['id']] += 1
        if tag == 'a':
            self.anchor = [a.get('href', ''), '']
        if tag == 'table':
            self.table = {'headers': 0, 'text': ''}
        if tag == 'th' and self.table is not None:
            self.table['headers'] += 1

    def handle_data(self, data):
        if self.anchor is not None:
            self.anchor[1] += data
        if self.table is not None:
            self.table['text'] += data

    def handle_endtag(self, tag):
        if tag == 'a' and self.anchor is not None:
            self.links.append(self.anchor)
            self.anchor = None
        if tag == 'table' and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def main():
    manifest = json.loads((R/'config/crossref-manifest.json').read_text(encoding='utf8'))
    typ = (R/'index.typ').read_text(encoding='utf8')
    expected = set()
    links = 0
    for chapter, info in manifest['chapters'].items():
        page = Page()
        html = (R/'_book'/info['file']).with_suffix('.html')
        page.feed(html.read_text(encoding='utf8'))
        for kind in ('table', 'figure'):
            numbers = info[kind+'s']
            assert numbers == list(range(1, len(numbers)+1)), f'{chapter}: gap in {kind} sequence'
            for number in numbers:
                target = f'{kind}-{chapter}-{number}'
                expected.add(target)
                assert page.ids[target] == 1, f'{chapter}: missing/duplicate HTML caption {target}'
                assert typ.count('<'+target+'>') >= 1, f'Missing PDF caption {target}'
                assert len(re.findall(r'(?<!link\()<' + target + r'>', typ)) == 1, f'Duplicate PDF caption {target}'
        for target, text in page.links:
            if '#' not in target:
                continue
            match = LABEL.fullmatch(target.split('#')[-1])
            if not match:
                continue
            links += 1
            number = re.search(r'\d+', text)
            assert number and number[0] == match[3], f'Caption/link number mismatch: {text}: {target}'
        for table in page.tables:
            # Argument panels and the weather/sky figure pair have no column
            # heading row; all genuine data/comparison tables must have one.
            panel = ('Modus ponens' in table['text'] or
                     ('Weather app' in table['text'] and 'Sky overhead' in table['text']))
            assert table['headers'] or panel, f'{chapter}: table lacks header cells: {table["text"][:90]}'
    actual = set(re.findall(r'id="((?:table|figure)-ch\d+-\d+)"', '\n'.join(
        p.read_text(encoding='utf8') for p in (R/'_book/chapters').glob('*.html'))))
    assert actual == expected, f'Unexpected/missing caption targets: {actual ^ expected}'
    for target in re.findall(r'#link\(<((?:table|figure)-ch\d+-\d+)>\)', typ):
        assert target in expected, f'Unresolved PDF cross-reference {target}'
    print(f'Cross-reference checks passed: {len(expected)} chapter-local numbered captions; '
          f'{links} HTML table/figure links; PDF labels/links; table headers.')
    for exception in manifest['exceptions']:
        if 'editorial decision' in exception['reason']:
            print(f'EDITORIAL: {exception["chapter"]}: {exception["text"]}: {exception["reason"]}')


if __name__ == '__main__':
    main()
