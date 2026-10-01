"""Ingestion locale reprise page par page. Aucun texte OCR n'est validé automatiquement."""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path
import fitz
from docx import Document

ROOT = Path(__file__).resolve().parents[1]

def extract_page(job):
    source, number, dest, language, fingerprint = job
    target = dest / f"page-{number:04d}.json"
    if target.exists():
        old = json.loads(target.read_text(encoding='utf-8'))
        if old.get('source_sha256') == fingerprint and old.get('extractor_version') == 1 and (old.get('method') != 'ocr' or old.get('language') == language):
            return old['method']
    with fitz.open(source) as pdf:
        page = pdf[number-1]
        text = page.get_text(sort=True).strip()
        images = len(page.get_images())
        method = 'native'
        confidence = None
        if len(text) < 60:
            if not shutil.which('tesseract'):
                method = 'ocr_required'
            else:
                with tempfile.TemporaryDirectory() as td:
                    image = Path(td)/'page.png'
                    page.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(image)
                    env = dict(os.environ, OMP_THREAD_LIMIT='1')
                    result = subprocess.run(['tesseract',str(image),'stdout','-l',language,'--psm','3'],env=env,capture_output=True,text=True,timeout=120)
                    if result.returncode:
                        method = 'ocr_failed';text = '';confidence = result.stderr[-500:]
                    else:
                        text = result.stdout.strip();method = 'ocr'
        # Les blocs natifs conservent les coordonnées ; le texte OCR reste lié à sa page.
        blocks = [dict(bbox=list(b[:4]),text=b[4]) for b in page.get_text('blocks') if b[6] == 0] if method=='native' else []
    record = dict(pdf_page=number,printed_page=None,text=text,method=method,language=language if method=='ocr' else None,source_sha256=fingerprint,extractor_version=1,embedded_images=images,blocks=blocks,validation='pending',warning=confidence)
    temp=target.with_suffix('.tmp');temp.write_text(json.dumps(record,ensure_ascii=False,indent=2), encoding='utf-8');temp.replace(target)
    return method

def word_record(source, dest):
    if source.suffix.lower()=='.doc':
        if not shutil.which('soffice'):
            return dict(method='conversion_required',blocks=[])
        with tempfile.TemporaryDirectory() as td:
            profile=(Path(td)/'profile').as_uri()
            subprocess.run(['soffice',f'-env:UserInstallation={profile}','--headless','--convert-to','docx','--outdir',td,str(source)],capture_output=True,check=True,timeout=120)
            return word_record(next(Path(td).glob('*.docx')),dest)
    doc=Document(source)
    blocks=[]
    # Preserve paragraph/table order, headings and row/column relationships.
    from docx.oxml.ns import qn
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    for index,node in enumerate(doc.element.body):
        if node.tag==qn('w:p'):
            p=Paragraph(node,doc)
            if p.text.strip():blocks.append(dict(id=f'b{index}',type='paragraph',style=p.style.name,text=p.text))
        elif node.tag==qn('w:tbl'):
            table=Table(node,doc)
            blocks.append(dict(id=f'b{index}',type='table',rows=[[c.text for c in row.cells] for row in table.rows]))
    return dict(method='docx',blocks=blocks,validation='pending',pagination='not_available_for_word_blocks')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-dir',required=True,type=Path);parser.add_argument('--output',type=Path,default=ROOT/'data/processed');parser.add_argument('--workers',type=int,default=4);parser.add_argument('--ocr-lang',default='fra');args=parser.parse_args()
    manifest=json.loads((ROOT/'content/sources.json').read_text(encoding='utf-8'));summary=[]
    args.output.mkdir(parents=True,exist_ok=True)
    for row in manifest:
        source=args.source_dir/row['filename'];dest=args.output/row['id'];dest.mkdir(exist_ok=True)
        if not source.exists():summary.append(dict(id=row['id'],status='missing'));continue
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        if digest!=row['sha256']:
            summary.append(dict(id=row['id'],status='hash_mismatch'));continue
        print('Processing',row['id'],flush=True)
        if source.suffix.lower()=='.pdf':
            with fitz.open(source) as pdf:count=len(pdf)
            jobs=[(source,i,dest,args.ocr_lang,digest) for i in range(1,count+1)]
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                methods=list(pool.map(extract_page,jobs))
            stats={m:methods.count(m) for m in sorted(set(methods))}
            summary.append(dict(id=row['id'],status='extracted' if not any(m in stats for m in ['ocr_required','ocr_failed']) else 'incomplete',pages=count,methods=stats,pedagogical_validation='pending'))
        else:
            record=word_record(source,dest);record['source_sha256']=digest
            (dest/'document.json').write_text(json.dumps(record,ensure_ascii=False,indent=2), encoding='utf-8')
            summary.append(dict(id=row['id'],status='extracted' if record['method']=='docx' else 'incomplete',blocks=len(record['blocks']),pedagogical_validation='pending'))
        (args.output/'coverage.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2), encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
    if any(r['status']!='extracted' for r in summary):raise SystemExit(2)
if __name__=='__main__':main()
