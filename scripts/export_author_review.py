"""Split a reviewed DOCX without accepting revisions or losing comment threads.

The reviewed Word file is a private input. Outputs must stay outside the public
site and Git history. Quarto remains the maintained reading edition.
"""
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED
import argparse, copy, hashlib, json, posixpath, re
import xml.etree.ElementTree as E
from io import BytesIO

R = Path(__file__).resolve().parents[1]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
REL = '{http://schemas.openxmlformats.org/package/2006/relationships}'
CT = '{http://schemas.openxmlformats.org/package/2006/content-types}'
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
NS14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'
def xml(data):
    for _, (prefix, uri) in E.iterparse(BytesIO(data), events=['start-ns']):
        if not re.fullmatch(r'ns\d+', prefix): E.register_namespace(prefix, uri)
    return E.fromstring(data)
def dump(root):return E.tostring(root, encoding='utf-8', xml_declaration=True)
def text(node):return ''.join(x.text or '' for x in node.iter(W+'t'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def relpath(part):
    p=PurePosixPath(part); return str(p.parent/'_rels'/(p.name+'.rels'))
def resolved(part, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(part),target)).lstrip('/')
def revision_signatures(root):
    tags={W+n for n in ['ins','del','moveFrom','moveTo','pPrChange','rPrChange','tblPrChange','trPrChange','tcPrChange','sectPrChange','numberingChange']}
    # Attribute/text/descendant structure comparison is independent of XML prefix serialization.
    def sig(el):return (el.tag,sorted(el.attrib.items()),el.text,el.tail,[sig(x) for x in el])
    return [sig(x) for x in root.iter() if x.tag in tags]

def split(source,out):
    out.mkdir(parents=True, exist_ok=False)
    with ZipFile(source) as z: parts={n.replace('\\','/'):z.read(n) for n in z.namelist()}
    original=xml(parts['word/document.xml']);body=original.find(W+'body')
    starts=[i for i,e in enumerate(body) if re.fullmatch(r'CHAPTER\s+[1-9]\s*:',text(e).strip(),re.I)]
    if len(starts)!=9:raise ValueError(f'Expected 9 chapter starts, found {len(starts)}')
    ledger={'source':source.name,'source_sha256':digest(source),'chapters':[]}
    all_comment_ids=set()
    for n,start in enumerate(starts,1):
        stop=starts[n] if n<9 else len(body)
        doc=copy.deepcopy(original); dst=doc.find(W+'body');dst.clear()
        selected=list(body)[start:stop]
        for e in selected:
            if e.tag!=W+'sectPr':dst.append(copy.deepcopy(e))
        sect=body.find(W+'sectPr')
        if sect is not None:dst.append(copy.deepcopy(sect))
        work=dict(parts);work['word/document.xml']=dump(doc)
        trees={'word/document.xml':doc}
        for name,tag in [('footnotes','footnote'),('endnotes','endnote')]:
            part=f'word/{name}.xml'
            if part not in work:continue
            root=xml(work[part]); ids={e.get(W+'id') for e in doc.iter(W+tag+'Reference')}
            for e in list(root):
                if int(e.get(W+'id','0'))>0 and e.get(W+'id') not in ids:root.remove(e)
            work[part]=dump(root);trees[part]=root
        ids={e.get(W+'id') for root in trees.values() for e in root.iter() if e.tag in {W+'commentReference',W+'commentRangeStart',W+'commentRangeEnd'}}
        comments=xml(work['word/comments.xml'])
        # Modern Word reply chains use paraId/paraIdParent, rather than comment IDs.
        extended=xml(work['word/commentsExtended.xml']) if 'word/commentsExtended.xml' in work else None
        by_para={p.get(NS14+'paraId'):c.get(W+'id') for c in comments for p in c.iter(W+'p') if p.get(NS14+'paraId')}
        if extended is not None:
            changed=True
            while changed:
                changed=False
                for e in extended:
                    pair=[by_para.get(v) for k,v in e.attrib.items() if k.endswith(('}paraId','}paraIdParent'))]
                    if any(v in ids for v in pair):
                        for v in pair:
                            if v and v not in ids:ids.add(v);changed=True
        source_comments={c.get(W+'id'):copy.deepcopy(c) for c in comments if c.get(W+'id') in ids}
        for c in list(comments):
            if c.get(W+'id') not in ids:comments.remove(c)
        work['word/comments.xml']=dump(comments);trees['word/comments.xml']=comments
        para_ids={p.get(NS14+'paraId') for c in comments for p in c.iter(W+'p')}
        durable=set()
        for name in ['commentsExtended','commentsIds','commentsExtensible']:
            part=f'word/{name}.xml'
            if part not in work:continue
            root=xml(work[part])
            for e in list(root):
                pids=[v for k,v in e.attrib.items() if k.endswith('}paraId')]
                dids=[v for k,v in e.attrib.items() if k.endswith('}durableId')]
                if (pids and not any(v in para_ids for v in pids)) or (name=='commentsExtensible' and dids and not any(v in durable for v in dids)):root.remove(e)
                elif name=='commentsIds':durable.update(dids)
            work[part]=dump(root)
        all_comment_ids.update(ids)
        # Restrict document and notes relationships to this chapter's content.
        always={'styles','stylesWithEffects','settings','webSettings','fontTable','theme','numbering','footnotes','endnotes','comments','commentsExtended','commentsIds','commentsExtensible','people'}
        for part,tree in trees.items():
            rp=relpath(part)
            if rp not in work:continue
            root=xml(work[rp]);used={v for e in tree.iter() for k,v in e.attrib.items() if k.startswith(RID)}
            for e in list(root):
                kind=e.get('Type','').rsplit('/',1)[-1]
                if e.get('Id') not in used and kind not in always:root.remove(e)
            work[rp]=dump(root)
        # Keep reachable package parts, including nested diagram/chart/image dependencies.
        keep={'[Content_Types].xml','_rels/.rels'};queue=['']
        while queue:
            part=queue.pop();rp=relpath(part) if part else '_rels/.rels'
            if rp not in work:continue
            keep.add(rp)
            for e in xml(work[rp]):
                if e.get('TargetMode')=='External':continue
                target=resolved(part,e.get('Target',''))
                if target not in work:raise ValueError(f'Missing relationship target: {target}')
                if target not in keep:keep.add(target);queue.append(target)
        types=xml(work['[Content_Types].xml'])
        for e in list(types):
            if e.tag==CT+'Override' and e.get('PartName','').lstrip('/') not in keep:types.remove(e)
        work['[Content_Types].xml']=dump(types)
        # Open in markup view and continue tracking edits. Existing revisions are untouched.
        if 'word/settings.xml' in work:
            settings=xml(work['word/settings.xml'])
            for tag in ['trackRevisions','revisionView']:
                for e in list(settings.findall(W+tag)):settings.remove(e)
            E.SubElement(settings,W+'trackRevisions')
            v=E.SubElement(settings,W+'revisionView')
            for key in ['markup','comments','insDel','formatting','inkAnnotations']:v.set(W+key,'true')
            work['word/settings.xml']=dump(settings)
        filename=f'{n:02d}-'+Path(json.loads((R/'config/publication.json').read_text(encoding='utf8'))['chapters'][n-1]['file']).stem[3:]+'.docx'
        if n==1:filename='01-foundations-historical-review.docx'
        dest=out/filename
        with ZipFile(dest,'w',ZIP_DEFLATED) as z:
            for name in sorted(keep):z.writestr(name,work[name])
        # Exact revision structure and comment text/anchors must survive the export.
        reference=E.Element('selected')
        for e in selected:reference.append(copy.deepcopy(e))
        assert revision_signatures(reference)==revision_signatures(doc),f'Revisions changed in chapter {n}'
        with ZipFile(dest) as z:
            test=xml(z.read('word/comments.xml'))
            assert {c.get(W+'id') for c in test}==ids
            assert all(text(c)==text(source_comments[c.get(W+'id')]) for c in test)
        counts={tag:len(list(doc.iter(W+tag))) for tag in ['ins','del','commentRangeStart','commentRangeEnd','commentReference']}
        info={'number':n,'file':filename,'sha256':digest(dest),'comments':len(comments),**counts,'revision_integrity':'passed','comment_integrity':'passed','bytes':dest.stat().st_size}
        ledger['chapters'].append(info)
        print(f'{filename}: {len(comments)} comments; {counts["ins"]} insertions; {counts["del"]} deletions')
    source_ids={c.get(W+'id') for c in xml(parts['word/comments.xml'])}
    ledger['unanchored_or_frontmatter_comment_ids']=sorted(source_ids-all_comment_ids)
    (out/'word-review-manifest.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf8')
    return ledger

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();source=a.source.resolve();out=a.output.resolve()
    if out==R or not out.is_relative_to(R/'_review'):raise ValueError('Output must be a new private directory inside _review')
    original_hash=digest(source);split(source,out)
    assert digest(source)==original_hash,'Source was modified'
