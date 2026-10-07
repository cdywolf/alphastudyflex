import hashlib,json
from .db import ROOT

def read(name):return json.loads((ROOT/'content'/f'{name}.json').read_text(encoding='utf-8'))
SOURCES=read('sources');CURRICULUM=read('curriculum');RULES=read('pedagogy');QUESTIONS=read('questions')
QMAP={q['id']:q for q in QUESTIONS}
PILOT_CHAPTERS=[c for c in CURRICULUM['chapters'] if c['state']=='pilot']
CHAPTER_IDS=[c['id'] for c in PILOT_CHAPTERS]
DEFAULT_CHAPTER=CHAPTER_IDS[0]
# Les identifiants de compétences et de séances sont uniques sur l'ensemble des chapitres pilotes.
SKILLS=[{**s,'chapter':c['id']} for c in PILOT_CHAPTERS for s in c['skills']]
SKILL_CHAPTER={s['id']:s['chapter'] for s in SKILLS}
LESSONS={l['id']:l for c in PILOT_CHAPTERS for l in c['lessons']}
def chapter_skills(chapter):return [s for s in SKILLS if s['chapter']==chapter]
def chapter_questions(chapter):return [q for q in QUESTIONS if q['chapter']==chapter]
def revision(q):
    # Le dictionnaire de séance est celui du curriculum, inchangé : les révisions déjà publiées restent valides.
    lesson=next(l for l in LESSONS.values() if l['skill']==q['skill'])
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
def ready(db,chapter=DEFAULT_CHAPTER):return all(is_published(db,q) for q in chapter_questions(chapter))
