import hashlib,json
from .db import ROOT

def read(name):return json.loads((ROOT/'content'/f'{name}.json').read_text(encoding='utf-8'))
SOURCES=read('sources');CURRICULUM=read('curriculum');RULES=read('pedagogy');QUESTIONS=read('questions')
QMAP={q['id']:q for q in QUESTIONS}
SKILLS=CURRICULUM['chapters'][0]['skills']
def revision(q):
    lesson=next(l for l in CURRICULUM['chapters'][0]['lessons'] if l['skill']==q['skill'])
    refs=[s for s in SOURCES if s['id'] in {r['id'] for r in q['sources']}]
    payload={'question':q,'lesson':lesson,'rules':RULES,'sources':refs}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def public_question(q):
    return {k:q[k] for k in ['id','kind','prompt','choices','skill','document']}
def sources_for(q):
    return [{**s,'title':next(x['filename'] for x in SOURCES if x['id']==s['id'])} for s in q['sources']]
def is_published(db,q):
    row=db.execute('SELECT status FROM publications WHERE question_id=? AND revision=?',(q['id'],revision(q))).fetchone()
    return bool(row and row['status']=='published')
def ready(db):return all(is_published(db,q) for q in QUESTIONS)
