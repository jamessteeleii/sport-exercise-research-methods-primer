"""Split the exact whole-book PDF and record hashes; never upload to the press."""
import argparse,json,hashlib,subprocess
from pathlib import Path
from pypdf import PdfReader,PdfWriter
R=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--stage',choices=['draft','submission','final-proofs'],default='draft');args=a.parse_args()
p=json.loads((R/'config/publication.json').read_text(encoding='utf8'))
if args.stage!='draft':
 for ch in p['chapters']:
  actual=hashlib.sha256((R/ch['file']).read_bytes()).hexdigest()
  if ch['author_approval']!='approved' or ch['approved_source_sha256']!=actual or not ch['approved_date']:
   raise SystemExit('Obtain and record author approval for the exact source of '+ch['id'])
if args.stage=='final-proofs' and (not p['book_doi'] or not p['publication_date'] or any(not ch['doi'] for ch in p['chapters'])):
 raise SystemExit('Final proofs require the confirmed book/chapter DOIs and publication date.')
source=R/'_book/research-methods-ses.pdf'
reader=PdfReader(source)
destinations={}
def outline(items,level=0):
 for item in items:
  if isinstance(item,list):outline(item,level+1)
  elif level==0:destinations[item.title.strip()]=reader.get_destination_page_number(item)
outline(reader.outline)
starts=[]
for ch in p['chapters']:
 matches=[page for title,page in destinations.items() if ch['title'].casefold() in title.casefold()]
 if len(matches)!=1:raise SystemExit('Cannot uniquely locate PDF bookmark for '+ch['id'])
 starts.append(matches[0])
if starts!=sorted(set(starts)):raise SystemExit('Chapter bookmarks are not in order.')
tail=[page for title,page in destinations.items() if title.casefold()=='references' or 'citation and publication information' in title.casefold()]
end=tail[0] if tail else len(reader.pages)
out=R/'_submission'/args.stage;out.mkdir(exist_ok=True,parents=True)
(out/source.name).write_bytes(source.read_bytes())
entries=[]
for i,ch in enumerate(p['chapters']):
 stop=starts[i+1] if i+1<len(starts) else end
 writer=PdfWriter()
 for page in reader.pages[starts[i]:stop]:writer.add_page(page)
 file=out/(Path(ch['file']).stem+'.pdf')
 with file.open('wb') as f:writer.write(f)
 entries.append({'chapter_id':ch['id'],'file':file.name,'pdf_physical_pages':[starts[i]+1,stop],'note':'Physical PDF positions. Confirm displayed page labels for the OMP Pages field.'})
manifest={'stage':args.stage,'book':source.name,'chapter_ranges':entries,'quarto':subprocess.check_output(['quarto','--version'],text=True).strip(),'files':[{'name':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(out.glob('*.pdf'))],'source_files':[{'file':ch['file'],'sha256':hashlib.sha256((R/ch['file']).read_bytes()).hexdigest()} for ch in p['chapters']]}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('Prepared '+str(out)+'; no submission or publication performed.')
