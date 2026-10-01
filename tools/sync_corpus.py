"""Transférer uniquement le corpus extrait dans la base configurée (locale ou Neon)."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.db import connect,initialize,ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--processed-dir',type=Path,default=ROOT/'data/processed');args=parser.parse_args()
    coverage=json.loads((args.processed_dir/'coverage.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'content/sources.json').read_text(encoding='utf-8'));allowed={s['id']:s for s in manifest}
    initialize();total=0
    with connect() as db:
        for item in coverage:
            sid=item['id']
            if sid not in allowed:raise ValueError('Source inconnue : '+sid)
            for p in sorted((args.processed_dir/sid).glob('*.json')):
                record=json.loads(p.read_text(encoding='utf-8'))
                if record.get('source_sha256')!=allowed[sid]['sha256']:raise ValueError('Empreinte incorrecte : '+str(p))
                db.execute('INSERT INTO corpus_pages(source_id,page_key,body) VALUES(?,?,?) ON CONFLICT(source_id,page_key) DO UPDATE SET body=excluded.body',(sid,p.name,p.read_text(encoding='utf-8')));total+=1
            db.execute('INSERT INTO corpus_coverage(source_id,body) VALUES(?,?) ON CONFLICT(source_id) DO UPDATE SET body=excluded.body',(sid,json.dumps(item)))
    print(f'{len(coverage)} sources synchronisées, {total} enregistrements. Aucune validation pédagogique automatique.')
if __name__=='__main__':main()
