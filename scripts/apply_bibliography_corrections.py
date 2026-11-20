"""Apply documented bibliographic corrections without changing citation keys."""
from pathlib import Path
import json,subprocess,re
from chapter_bibliographies import entries
R=Path(__file__).resolve().parents[1]
master=R/'references.bib';text=master.read_text(encoding='utf8');bib=entries(text)
corrections=json.loads((R/'config/bibliography-corrections.json').read_text(encoding='utf8'))['entries']
parsed=json.loads(subprocess.run(['quarto','pandoc',str(master),'-f','biblatex','-t','csljson'],capture_output=True,text=True,encoding='utf8',check=True).stdout)
data={d['id']:d for d in parsed}
for key,changes in corrections.items():
 d=data[key]
 for name,value in changes.items():
  if name not in ['source','reason']:d[name]=value
 output=subprocess.run(['quarto','pandoc','-f','csljson','-t','biblatex'],input=json.dumps([d],ensure_ascii=False),capture_output=True,text=True,encoding='utf8',check=True).stdout.strip()
 text=text.replace(bib[key],output,1)
master.write_text(text,encoding='utf8')
print('Applied',len(corrections),'documented corrections; citation keys unchanged.')
