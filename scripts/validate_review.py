"""Check the public review edition without reading private editorial inputs."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json,re

R=Path(__file__).resolve().parents[1]
SITE=(R/'_book').resolve()
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=[];self.banners=0;self.attributions=0;self.heading='';self.headings=[];self.capture=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if tag in ['a','img','link','script']:
            u=a.get('href') or a.get('src')
            if u:self.links.append(u)
        classes=a.get('class','').split()
        if tag=='div' and 'draft-banner' in classes:self.banners+=1
        if 'quote-attribution' in classes:self.attributions+=1
        if tag in ['h1','h2','h3','h4','h5','h6']:self.capture=True;self.heading=''
    def handle_data(self,data):
        assert not re.search(r'\+[-=]{12,}|\|[:=]{12,}|={30}',data),'Unparsed grid table border in HTML'
        if self.capture:self.heading+=data
    def handle_endtag(self,tag):
        if tag in ['h1','h2','h3','h4','h5','h6']:
            if self.capture:self.headings.append(self.heading.strip())
            self.capture=False

def main():
    pages={}
    for f in SITE.rglob('*.html'):
        p=Page();p.feed(f.read_text(encoding='utf8'));pages[f.resolve()]=p
    assert len(pages)==13,f'Expected 13 book pages, found {len(pages)}'
    for f,p in pages.items():
        assert p.banners==1,f'Missing or duplicate draft banner in {f.name}'
        assert not any(re.match(r'^\d+(?:\.\d+)*\.?\s',h) for h in p.headings),f'Numbered heading in {f.name}'
        for href in p.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            target=(SITE/unquote(u.path.lstrip('/'))).resolve() if u.path.startswith('/') else (f.parent/unquote(u.path)).resolve() if u.path else f
            assert target.is_relative_to(SITE),f'Link escapes site: {href}'
            assert target.exists(),f'Missing local target: {f.name}: {href}'
            if u.fragment and target in pages:assert unquote(u.fragment) in pages[target].ids,f'Missing anchor: {f.name}: {href}'
    first=pages[(SITE/'chapters/01-foundations.html').resolve()]
    assert first.attributions==5,f'Expected 5 quotation attributions, found {first.attributions}'
    pdf=SITE/'research-methods-ses.pdf'
    assert pdf.is_file() and pdf.read_bytes().startswith(b'%PDF-'),'Whole-book PDF missing'
    for f in SITE.rglob('*'):
        parts=set(f.relative_to(SITE).parts)
        assert not parts.intersection({'editorial','private','_review','work','.git'}),f'Private path in site: {f}'
        assert f.suffix.lower() not in {'.docx','.docm'},f'Word file in public site: {f}'
    publication=json.loads((R/'config/publication.json').read_text(encoding='utf8'))
    assert publication['status']=='draft','Review workflow is for a draft edition'
    print(f'Review checks passed: {len(pages)} draft banners; unnumbered headings; all local links/assets and anchors; five quote attributions; clean PDF download; no private files.')

if __name__=='__main__':main()
