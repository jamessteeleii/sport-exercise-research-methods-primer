"""Check bibliography integrity and, optionally, every rendered citation target."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
import argparse,json,re,subprocess,sys
from chapter_bibliographies import entries
R=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.citations=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='a' and a.get('role')=='doc-biblioref':self.citations.append(a.get('href',''))
def main():
 p=argparse.ArgumentParser();p.add_argument('--rendered',action='store_true');args=p.parse_args()
 subprocess.run([sys.executable,str(R/'scripts/chapter_bibliographies.py'),'--check'],check=True,cwd=R)
 bib=(R/'references.bib').read_text(encoding='utf8');raw=entries(bib)
 result=subprocess.run(['quarto','pandoc','references.bib','-f','biblatex','-t','csljson'],capture_output=True,text=True,encoding='utf8',check=True,cwd=R)
 parsed=json.loads(result.stdout);ids=[d['id'] for d in parsed]
 if len(ids)!=len(set(ids)) or set(ids)!=raw.keys():raise ValueError('Bibliography does not round-trip through Pandoc')
 if re.search(r'(?mi)^\s*(?:file|abstract|annotation|note)\s*=',bib) or re.search(r'[A-Z]:[\\/]|/Users/|/home/',bib):raise ValueError('Private fields or local paths in bibliography')
 if any(re.search(r'(?m)^## References Chapter',f.read_text(encoding='utf8')) for f in (R/'chapters').glob('*.qmd')):raise ValueError('Manual reference list remains')
 summary={'bibliography_entries':len(ids),'roundtrip':'passed','rendered_links':None}
 if args.rendered:
  site=R/'_book';pages={}
  for f in site.rglob('*.html'):
   x=Links();x.feed(f.read_text(encoding='utf8'));pages[f.resolve()]=x
  count=0
  for file,page in pages.items():
   for href in page.citations:
    u=urlsplit(href);target=(file.parent/unquote(u.path)).resolve() if u.path else file
    if target not in pages or unquote(u.fragment) not in pages[target].ids:raise ValueError(f'Broken citation target in {file.name}: {href}')
    count+=1
  manifest=json.loads((R/'config/bibliography-manifest.json').read_text(encoding='utf8'))
  if count<manifest['citation_groups']:raise ValueError('Rendered site contains fewer links than citation groups')
  if not (site/'research-methods-ses.pdf').is_file():raise ValueError('Downloadable PDF is missing')
  if any('editorial' in f.parts or 'private' in f.parts for f in site.rglob('*')):raise ValueError('Private editorial files in site')
  summary['rendered_links']=count
 (R/'config/citation-validation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
 print(f'Bibliography passed: {len(ids)} unique parsed entries.'+(f' All {count} rendered citation links resolve.' if args.rendered else ''))
if __name__=='__main__':main()
