"""Cheap source/link checks. This is not a substitute for editorial proofing."""
from pathlib import Path
import json, re, sys, subprocess
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'config/publication.json').read_text(encoding='utf8'))
errors=[];warnings=[]
for ch in p['chapters']:
 f=R/ch['file']
 if not f.is_file():errors.append('Missing chapter '+ch['file']);continue
 s=f.read_text(encoding='utf8')
 if len(re.findall(r'^# ',s,re.M))!=1:errors.append(ch['id']+' must have one chapter heading')
 for href in re.findall(r'!\[[^\]]*\]\(([^)\s]+)',s):
  if not href.startswith(('http:','https:','data:')) and not (f.parent/href).is_file():errors.append(ch['id']+' missing image '+href)
 if re.search(r'\bLINK\b|\bTODO\b',s):warnings.append(ch['id']+' contains editorial link/text placeholders')
 if '\ufffd' in s:warnings.append(ch['id']+' contains a replacement character inherited from Word')
for k in ['book_doi','site_url','publication_date','license']:
 if p[k] is None:warnings.append(k+' pending')
print('\n'.join('WARNING: '+x for x in warnings))
print('\n'.join('ERROR: '+x for x in errors))
print(f"Checked {len(p['chapters'])} chapter sources; {len(errors)} errors.")
if (R/'references.bib').exists() and not errors:
 result=subprocess.run([sys.executable,str(R/'scripts/validate_citations.py')],cwd=R)
 if result.returncode:errors.append('Citation validation failed')
sys.exit(bool(errors))
