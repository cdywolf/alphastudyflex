"""Règles explicites et traçables, sans score probabiliste de maîtrise."""
import json
from .content import SKILLS,DEFAULT_CHAPTER

def evidence(db,user_id,chapter=None):
    rows=db.execute('SELECT a.*,r.snapshot,r.mode FROM attempts a JOIN runs r ON r.id=a.run_id WHERE r.user_id=? AND r.completed=1 ORDER BY a.id',(user_id,)).fetchall()
    result=[]
    for skill in [s for s in SKILLS if chapter is None or s['chapter']==chapter]:
        obs=[]
        for row in rows:
            q=next(q for q in json.loads(row['snapshot']) if q['id']==row['question_id'])
            if q['skill']==skill['id']:obs.append((row,q))
        graded=[(r,q) for r,q in obs if r['score'] is not None]
        distinct={q['id'] for r,q in graded if r['score']==1 and not r['assisted']}
        open_success=any(q['kind']=='open' and r['score']==1 and not r['assisted'] for r,q in graded)
        recent=graded[-3:];has_recent_error=any(r['score']<1 for r,q in recent)
        if not graded:status='Non évalué'
        elif len(distinct)>=3 and not has_recent_error and (skill['dimension']!='methodologie' or open_success):status='Consolidé'
        elif len(distinct)>=2 and not has_recent_error:status='Acquis à confirmer'
        elif any(r['score']>0 for r,q in graded):status='En cours'
        else:status='À travailler'
        result.append({**skill,'status':status,'observations':len(graded),'independent_successes':len(distinct),'pending_reviews':sum(r['score'] is None for r,q in obs),'evidence_ids':[r['id'] for r,q in obs]})
    return result

def plan(db,user_id,chapter=DEFAULT_CHAPTER):
    skills=evidence(db,user_id,chapter)
    rank={'À travailler':0,'Non évalué':1,'En cours':2,'Acquis à confirmer':3,'Consolidé':4}
    ordered=sorted(enumerate(skills),key=lambda x:(rank[x[1]['status']],x[0]))
    by={s['id']:s for s in skills};sequence=[]
    def visit(s):
        for prerequisite in s['prerequisites']:
            if prerequisite in by and by[prerequisite]['status'] not in ['Acquis à confirmer','Consolidé']:
                visit(by[prerequisite])
        if s not in sequence:sequence.append(s)
    for _,s in ordered:visit(s)
    return [{**s,'reason':{'À travailler':'Reprendre les points qui ont posé problème.','Non évalué':'Recueillir une première preuve de compréhension.','En cours':'S’entraîner pour réussir sans aide.','Acquis à confirmer':'Vérifier la réussite sur une autre tâche.','Consolidé':'Entretenir cet acquis.'}[s['status']]} for s in sequence]

def run_result(db,run):
    snapshot=json.loads(run['snapshot']);attempts=db.execute('SELECT * FROM attempts WHERE run_id=? ORDER BY id',(run['id'],)).fetchall();by={a['question_id']:dict(a) for a in attempts}
    details=[]
    for q in snapshot:
        a=by.get(q['id'])
        if a:details.append(dict(question_id=q['id'],prompt=q['prompt'],skill=q['skill'],score=a['score'],assisted=bool(a['assisted']),feedback=a['feedback'],response=json.loads(a['response']),correct_answer=q['choices'][q['answer']] if q['kind']=='choice' else None,sources=q['sources']))
    graded=[a for a in attempts if a['score'] is not None]
    return dict(id=run['id'],mode=run['mode'],completed=bool(run['completed']),score=round(sum(a['score'] for a in graded),2),graded=len(graded),total=len(snapshot),pending=len(attempts)-len(graded),details=details)

def prerequisite_alerts(db,user_id,chapter):
    """Prérequis situés dans un autre chapitre et pas encore acquis : signalés, jamais imposés."""
    every={s['id']:s for s in evidence(db,user_id)}
    alerts=[]
    for s in [x for x in SKILLS if x['chapter']==chapter]:
        for pid in s.get('chapter_prerequisites',[]):
            p=every.get(pid)
            if p and p['status'] not in ['Acquis à confirmer','Consolidé'] and p['id'] not in [a['id'] for a in alerts]:
                alerts.append({'id':p['id'],'title':p['title'],'chapter':p['chapter'],'status':p['status'],'needed_for':s['title']})
    return alerts
