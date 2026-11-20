"""Synchronise confirmed identifiers and citation metadata without editing chapter prose."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'config/publication.json').read_text(encoding='utf8'))
def people(names): return [{'literal':a} for a in names]
def valid_doi(s): return isinstance(s,str) and re.fullmatch(r'10\.\d{4,9}/\S+',s) is not None
def citation(ch=None):
 doi=ch['doi'] if ch else p['book_doi']
 if doi is not None and not valid_doi(doi): raise ValueError('Use a bare assigned DOI (10.xxxx/...), not a guessed identifier or URL')
 if not doi or not p['publication_date']: return False
 base={'type':'chapter' if ch else 'book','title':ch['title'] if ch else p['title']+': '+p['subtitle'],'editor':people(p['editors']),'publisher':p['publisher'],'doi':doi,'issued':p['publication_date']}
 if ch:
  base.update({'author':people(ch['authors']),'container-title':p['title']+': '+p['subtitle'],'chapter-number':ch['number']})
  if ch['pages']:base['page']=ch['pages']
 return base
if p['status']=='published' and (not p['book_doi'] or any(not ch['doi'] for ch in p['chapters']) or not p['publication_date']):
 raise ValueError('Published status requires the confirmed date and all book/chapter DOIs')
for ch in p['chapters']:
 path=ROOT/ch['file'];body=path.read_text(encoding='utf8')
 if body.startswith('---\n'):body=re.sub(r'^---\n.*?\n---\n\s*','',body,count=1,flags=re.S)
 metadata={'citation':citation(ch),'google-scholar':bool(citation(ch))}
 path.write_text('---\n'+json.dumps(metadata,ensure_ascii=False,indent=2)+'\n---\n\n'+body,encoding='utf8')
bookmeta={'citation':citation(),'google-scholar':bool(citation())}
if p['publication_date']:bookmeta['date']=p['publication_date']
(ROOT/'config/book-metadata.yml').write_text(json.dumps(bookmeta,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
# Only update these known fields inside the existing book configuration.
config=(ROOT/'_quarto.yml').read_text(encoding='utf8')
for key,value in [('doi',p['book_doi']),('site-url',p['site_url'])]:
 config=re.sub(r'^  '+key+r':.*\n','',config,flags=re.M)
 if value:config=config.replace('book:\n','book:\n  '+key+': '+json.dumps(value)+'\n',1)
(ROOT/'_quarto.yml').write_text(config,encoding='utf8')
if p['publication_date'] and p['book_doi']:
 lines=['# Citation and publication information {.unnumbered}','','Edited by '+ ' and '.join(p['editors'])+'.','','*'+p['title']+': '+p['subtitle']+'*. '+p['publisher']+'. '+p['publication_date']+'.','','Book DOI: <https://doi.org/'+p['book_doi']+'>.','','## Chapter citations {.unnumbered}','']
 for ch in p['chapters']:
  lines+=['**'+str(ch['number'])+'. '+ch['title']+'**. '+', '.join(ch['authors'])+'.'+(' <https://doi.org/'+ch['doi']+'>.' if ch['doi'] else ' DOI pending.'),'']
 (ROOT/'backmatter/citation.qmd').write_text('\n'.join(lines),encoding='utf8')
print('Citation metadata synchronised; unknown identifiers remain absent.')
