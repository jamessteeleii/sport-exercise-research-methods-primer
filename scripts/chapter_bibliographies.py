"""Derive chapter BibLaTeX files from actual Pandoc citation nodes in the sources."""
from pathlib import Path
import argparse,collections,json,re,subprocess,hashlib,sys
R=Path(__file__).resolve().parents[1]
def walk(x):
 if isinstance(x,dict):
  if x.get('t')=='Cite':yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def entries(s):
 pairs=[(m.group(1),m.group(0).strip()) for m in re.finditer(r'(?ms)^@\w+\{([^,]+),.*?(?=^@\w+\{|\Z)',s)]
 if len(dict(pairs))!=len(pairs):raise ValueError('Duplicate bibliography keys')
 return dict(pairs)
def chapter_citations(path):
 result=subprocess.run(['quarto','pandoc',str(path),'-f','markdown','-t','json'],capture_output=True,text=True,encoding='utf8',check=True)
 groups=list(walk(json.loads(result.stdout)))
 keys=[ci['citationId'] for n in groups for ci in n['c'][0] if not ci['citationId'].startswith(('sec-','fig-','tbl-','eq-','lst-'))]
 return keys,len(groups)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 master=(R/'references.bib').read_text(encoding='utf8');bib=entries(master);prefix=master[:re.search(r'(?m)^@\w+\{',master).start()]
 p=json.loads((R/'config/publication.json').read_text(encoding='utf8'));manifest=json.loads((R/'config/bibliography-manifest.json').read_text(encoding='utf8'))
 allkeys=[];groups=0
 for ch in p['chapters']:
  path=R/ch['file'];keys,count=chapter_citations(path);allkeys+=keys;groups+=count;missing=set(keys)-bib.keys()
  if missing:raise ValueError(f'{path.name}: missing bibliography keys {sorted(missing)}')
  dest=R/'bibliography/chapters'/(path.stem+'.bib');expected=prefix+'\n\n'.join(bib[k] for k in sorted(set(keys),key=str.casefold))+'\n'
  if args.check:
   if not dest.exists() or dest.read_text(encoding='utf8')!=expected:raise ValueError(f'Regenerate chapter bibliography: {dest.name}')
  else:
   dest.write_text(expected,encoding='utf8')
   manifest['chapters'][path.stem]={'keys':sorted(set(keys)),'count':len(set(keys)),'citation_groups':count,'citation_occurrences':len(keys),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 if not args.check:
  manifest['cited_sources']=len(set(allkeys));manifest['citation_groups']=groups;manifest['citation_occurrences']=len(allkeys)
  (R/'config/bibliography-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(f'Checked nine chapter bibliographies: {len(set(allkeys))} sources, {groups} citation groups, {len(allkeys)} individual citations.')
if __name__=='__main__':main()
