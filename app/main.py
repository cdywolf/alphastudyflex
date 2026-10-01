from __future__ import annotations
from contextlib import asynccontextmanager
import hashlib,json,os,secrets,sqlite3,time
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse
from fastapi import FastAPI,Request,HTTPException,Depends
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field,ConfigDict,StrictInt,StrictStr
from .db import ROOT,data_dir,connect,initialize
from .auth import create_user,verify_password,current_user,teacher,hash_password
from .content import QUESTIONS,QMAP,CURRICULUM,RULES,SOURCES,SKILLS,revision,public_question,ready,is_published
from .engine import evidence,plan,run_result

@asynccontextmanager
async def lifespan(app):
    if (os.environ.get('RENDER') or os.environ.get('ASF_ENV')=='production') and os.environ.get('ASF_SECURE_COOKIE')!='1':
        raise RuntimeError('ASF_SECURE_COOKIE=1 est obligatoire en hébergement HTTPS.')
    initialize();yield
app=FastAPI(title='AlphaStudyFlex',version='0.1.1',lifespan=lifespan)

@app.middleware('http')
async def request_security(request,call_next):
    if request.method in ['POST','PUT','PATCH','DELETE']:
        origin=request.headers.get('origin')
        if origin and urlparse(origin).netloc!=request.headers.get('host'):
            return JSONResponse({'detail':'Origine non autorisée.'},403)
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='same-origin'
    response.headers['X-Frame-Options']='DENY'
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    if request.url.path.startswith('/api'):response.headers['Cache-Control']='no-store'
    return response

class StrictModel(BaseModel):model_config=ConfigDict(extra='forbid')
class Credentials(StrictModel):username:str=Field(min_length=3,max_length=40);password:str=Field(min_length=10,max_length=128)
class Setup(Credentials):setup_token:str=Field(min_length=24,max_length=256)
class Profile(StrictModel):goal:str=Field(default='',max_length=250);minutes:int=Field(default=20,ge=10,le=60)
class Start(StrictModel):mode:Literal['diagnostic','practice','final'];skill:Literal['arguments','graph','movement']|None=None
class Answer(StrictModel):question_id:str;response:StrictInt|StrictStr
class Hint(StrictModel):question_id:str
class Publish(StrictModel):confirmed:bool;note:str=Field(min_length=5,max_length=1000)
class Review(StrictModel):score:Literal[0,1,2];feedback:str=Field(min_length=10,max_length=2000)

ATTEMPTS={}
def rate_limit(request):
    now=time.time();key=request.client.host if request.client else 'local'
    for ip in list(ATTEMPTS):
        ATTEMPTS[ip]=[t for t in ATTEMPTS[ip] if now-t<300]
        if not ATTEMPTS[ip]:ATTEMPTS.pop(ip,None)
    recent=ATTEMPTS.setdefault(key,[])
    if len(recent)>=30:raise HTTPException(429,'Trop de tentatives. Réessaie dans quelques minutes.')
    recent.append(now)

@app.get('/api/health')
def health():return {'status':'ok','version':'0.1.1','tutor':'curated','scope':'local_pilot'}
@app.post('/api/setup')
def setup_teacher(body:Setup,request:Request):
    import re
    rate_limit(request)
    expected=os.environ.get('ASF_SETUP_TOKEN','')
    if len(expected)<24 or not secrets.compare_digest(body.setup_token,expected):raise HTTPException(403,'Code d’installation incorrect ou configuration déjà fermée.')
    if not re.fullmatch(r'[a-zA-Z0-9_-]{3,40}',body.username):raise HTTPException(400,'Identifiant invalide.')
    with connect() as db:
        db.lock(987432)
        if db.execute("SELECT id FROM users WHERE role='teacher'").fetchone():raise HTTPException(409,'Le compte enseignant initial existe déjà.')
        if db.execute('SELECT id FROM users WHERE username=?',(body.username.lower(),)).fetchone():raise HTTPException(409,'Identifiant déjà utilisé.')
        db.execute('INSERT INTO users(username,password,role) VALUES(?,?,?)',(body.username.lower(),hash_password(body.password),'teacher'))
    return {'created':True}
@app.post('/api/register')
def register(body:Credentials,request:Request):
    rate_limit(request)
    expected=os.environ.get('ASF_INVITE_CODE','')
    if (os.environ.get('RENDER') or os.environ.get('ASF_ENV')=='production') and not expected:
        raise HTTPException(403,'Les inscriptions ne sont pas encore ouvertes.')
    if expected and not secrets.compare_digest(request.headers.get('X-Invite-Code',''),expected):
        raise HTTPException(403,'Le code d’invitation de la classe est requis.')
    try:create_user(body.username,body.password,'student')
    except ValueError as e:raise HTTPException(400,str(e))
    except Exception as e:
        if isinstance(e,sqlite3.IntegrityError) or getattr(e,'sqlstate',None)=='23505':raise HTTPException(409,'Cet identifiant est déjà utilisé.')
        raise
    return {'created':True}
@app.post('/api/login')
def login(body:Credentials,request:Request):
    rate_limit(request)
    with connect() as db:
        row=db.execute('SELECT * FROM users WHERE username=?',(body.username.lower(),)).fetchone()
        if not row or not verify_password(body.password,row['password']):raise HTTPException(401,'Identifiant ou mot de passe incorrect.')
        token=secrets.token_urlsafe(32);db.execute('DELETE FROM sessions WHERE expires<=?',(int(time.time()),))
        db.execute('INSERT INTO sessions VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),row['id'],int(time.time())+28800))
    response=JSONResponse({'id':row['id'],'username':row['username'],'role':row['role']})
    response.set_cookie('asf_session',token,httponly=True,samesite='strict',secure=os.environ.get('ASF_SECURE_COOKIE')=='1',max_age=28800)
    return response
@app.post('/api/logout')
def logout(request:Request):
    with connect() as db:db.execute('DELETE FROM sessions WHERE token_hash=?',(hashlib.sha256(request.cookies.get('asf_session','').encode()).hexdigest(),))
    response=JSONResponse({'ok':True});response.delete_cookie('asf_session');return response
@app.get('/api/me')
def me(user=Depends(current_user)):return user
@app.get('/api/dashboard')
def dashboard(user=Depends(current_user)):
    with connect() as db:
        runs=db.execute('SELECT * FROM runs WHERE user_id=? ORDER BY created_at,id',(user['id'],)).fetchall()
        profile=db.execute('SELECT goal,minutes FROM profiles WHERE user_id=?',(user['id'],)).fetchone()
        return dict(user=user,ready=ready(db),profile=dict(profile) if profile else {'goal':'Comprendre la tectonique des plaques','minutes':20},skills=evidence(db,user['id']),plan=plan(db,user['id']),runs=[run_result(db,r) if r['completed'] else {'id':r['id'],'mode':r['mode'],'completed':False} for r in runs],chapters=[{k:v for k,v in c.items() if k not in ['skills','lessons']} for c in CURRICULUM['chapters']])
@app.put('/api/profile')
def profile(body:Profile,user=Depends(current_user)):
    with connect() as db:db.execute('INSERT INTO profiles(user_id,goal,minutes) VALUES(?,?,?) ON CONFLICT(user_id) DO UPDATE SET goal=excluded.goal,minutes=excluded.minutes',(user['id'],body.goal,body.minutes))
    return {'ok':True}
@app.get('/api/lessons/{skill}')
def lesson(skill:str,user=Depends(current_user)):
    item=next((l for l in CURRICULUM['chapters'][0]['lessons'] if l['id']==skill),None)
    if not item:raise HTTPException(404,'Séance introuvable.')
    with connect() as db:
        if not ready(db) and user['role']!='teacher':raise HTTPException(409,'Ce parcours attend une validation pédagogique.')
        active=db.execute("SELECT id FROM runs WHERE user_id=? AND completed=0 AND mode IN ('diagnostic','final')",(user['id'],)).fetchone()
        if active:raise HTTPException(409,'Termine ton évaluation avant de consulter la séance.')
    return item

def get_run(db,rid,uid):
    row=db.execute('SELECT * FROM runs WHERE id=? AND user_id=?',(rid,uid)).fetchone()
    if not row:raise HTTPException(404,'Parcours introuvable.')
    return row

def next_question(db,run):
    answered={r[0] for r in db.execute('SELECT question_id FROM attempts WHERE run_id=?',(run['id'],))}
    return next((q for q in json.loads(run['snapshot']) if q['id'] not in answered),None)

@app.post('/api/runs')
def start(body:Start,user=Depends(current_user)):
    with connect() as db:
        db.lock(user['id'])
        if not ready(db):raise HTTPException(409,'L’enseignant doit valider le contenu du pilote avant de l’ouvrir.')
        active=db.execute('SELECT * FROM runs WHERE user_id=? AND completed=0',(user['id'],)).fetchone()
        if active:return {'id':active['id'],'resumed':True}
        diagnostic=db.execute("SELECT id FROM runs WHERE user_id=? AND mode='diagnostic' AND completed=1",(user['id'],)).fetchone()
        if body.mode=='diagnostic' and diagnostic:return {'id':diagnostic['id'],'resumed':True}
        if body.mode!='diagnostic' and not diagnostic:raise HTTPException(409,'Commence par le diagnostic.')
        if body.mode=='practice' and body.skill is None:raise HTTPException(400,'Choisis une compétence.')
        if body.mode=='final':
            practiced={r[0] for r in db.execute("SELECT DISTINCT skill FROM runs WHERE user_id=? AND mode='practice' AND completed=1",(user['id'],))}
            if practiced!={s['id'] for s in SKILLS}:raise HTTPException(409,'Termine une séance pour chacune des trois compétences avant le bilan final.')
        questions=[q for q in QUESTIONS if q['mode']==body.mode and (body.mode!='practice' or q['skill']==body.skill)]
        rid=secrets.token_hex(16)
        db.execute('INSERT INTO runs(id,user_id,mode,skill,question_ids,snapshot) VALUES(?,?,?,?,?,?)',(rid,user['id'],body.mode,body.skill,json.dumps([q['id'] for q in questions]),json.dumps(questions,ensure_ascii=False)))
    return {'id':rid,'resumed':False}
@app.get('/api/runs/{rid}')
def run(rid:str,user=Depends(current_user)):
    with connect() as db:
        r=get_run(db,rid,user['id']);q=next_question(db,r)
        count=db.execute('SELECT count(*) FROM attempts WHERE run_id=?',(rid,)).fetchone()[0]
        return dict(id=rid,mode=r['mode'],completed=bool(r['completed']),answered=count,total=len(json.loads(r['snapshot'])),question=public_question(q) if q else None,result=run_result(db,r) if r['completed'] else None)
@app.post('/api/runs/{rid}/hint')
def hint(rid:str,body:Hint,user=Depends(current_user)):
    with connect() as db:
        r=get_run(db,rid,user['id'])
        if r['mode']!='practice':raise HTTPException(403,'Les indices sont disponibles pendant l’entraînement.')
        q=next_question(db,r)
        if not q or q['id']!=body.question_id:raise HTTPException(409,'Cette question n’est pas active.')
        row=db.execute('SELECT used FROM hints WHERE run_id=? AND question_id=?',(rid,q['id'])).fetchone();used=row['used'] if row else 0
        if not q['hints']:raise HTTPException(404,'Aucun indice disponible.')
        index=min(used,len(q['hints'])-1)
        db.execute('INSERT INTO hints VALUES(?,?,?) ON CONFLICT(run_id,question_id) DO UPDATE SET used=excluded.used',(rid,q['id'],index+1))
        return {'hint':q['hints'][index],'index':index+1,'total':len(q['hints'])}
@app.post('/api/runs/{rid}/answer')
def answer(rid:str,body:Answer,user=Depends(current_user)):
    with connect() as db:
        db.lock(user['id'])
        r=get_run(db,rid,user['id']);q=next_question(db,r)
        if not q or q['id']!=body.question_id:raise HTTPException(409,'Question déjà traitée ou non active.')
        assisted=db.execute('SELECT used FROM hints WHERE run_id=? AND question_id=?',(rid,q['id'])).fetchone() is not None
        if q['kind']=='choice':
            if type(body.response) is not int or not 0<=body.response<len(q['choices']):raise HTTPException(400,'Choisis une réponse valide.')
            score=1.0 if body.response==q['answer'] else 0.0;feedback=q['explanation']
        else:
            if not isinstance(body.response,str) or not 5<=len(body.response.strip())<=2000:raise HTTPException(400,'Écris une réponse de 5 à 2000 caractères.')
            score=None;feedback='Ta réponse sera évaluée par l’enseignant selon les critères annoncés.'
        db.execute('INSERT INTO attempts(run_id,question_id,response,score,assisted,feedback) VALUES(?,?,?,?,?,?)',(rid,q['id'],json.dumps(body.response),score,int(assisted),feedback))
        completed=next_question(db,r) is None
        if completed:db.execute('UPDATE runs SET completed=1 WHERE id=?',(rid,))
        return dict(saved=True,completed=completed,score=score if r['mode']=='practice' else None,feedback=feedback if r['mode']=='practice' else 'Réponse enregistrée. Les résultats seront présentés à la fin.',sources=q['sources'] if r['mode']=='practice' else [])
@app.get('/api/teacher/overview')
def overview(user=Depends(teacher)):
    with connect() as db:
        users=db.execute("SELECT id,username FROM users WHERE role='student'").fetchall()
        pending=db.execute('SELECT a.id,a.response,a.question_id,r.snapshot,u.username FROM attempts a JOIN runs r ON r.id=a.run_id JOIN users u ON u.id=r.user_id WHERE a.score IS NULL').fetchall()
        reviews=[]
        for r in pending:
            q=next(q for q in json.loads(r['snapshot']) if q['id']==r['question_id'])
            reviews.append(dict(id=r['id'],username=r['username'],response=json.loads(r['response']),question=q))
        return dict(learners=[dict(id=u['id'],username=u['username'],skills=evidence(db,u['id'])) for u in users],pending=reviews,ready=ready(db))
@app.get('/api/teacher/content')
def teacher_content(user=Depends(teacher)):
    with connect() as db:return dict(questions=[{**q,'published':is_published(db,q),'revision':revision(q)} for q in QUESTIONS],rules=RULES,curriculum=CURRICULUM)
@app.post('/api/teacher/questions/{qid}/publish')
def publish(qid:str,body:Publish,user=Depends(teacher)):
    q=QMAP.get(qid)
    if not q:raise HTTPException(404,'Question introuvable.')
    if not body.confirmed:raise HTTPException(400,'La vérification pédagogique doit être confirmée.')
    with connect() as db:
        db.execute("INSERT INTO publications(question_id,revision,reviewer_id,status) VALUES(?,?,?,'published') ON CONFLICT(question_id,revision) DO UPDATE SET reviewer_id=excluded.reviewer_id,status='published',reviewed_at=CURRENT_TIMESTAMP",(qid,revision(q),user['id']))
        db.execute('INSERT INTO review_log(teacher_id,action,object_id,detail) VALUES(?,?,?,?)',(user['id'],'publish',qid,body.note))
    return {'ok':True}
@app.post('/api/teacher/reviews/{aid}')
def review(aid:int,body:Review,user=Depends(teacher)):
    with connect() as db:
        a=db.execute('SELECT a.*,r.snapshot FROM attempts a JOIN runs r ON r.id=a.run_id WHERE a.id=?',(aid,)).fetchone()
        if not a:raise HTTPException(404,'Réponse introuvable.')
        q=next(q for q in json.loads(a['snapshot']) if q['id']==a['question_id'])
        if q['kind']!='open':raise HTTPException(400,'Cette réponse utilise une correction automatique.')
        db.execute('UPDATE attempts SET score=?,feedback=?,reviewed_by=? WHERE id=?',(body.score/2,body.feedback,user['id'],aid))
        db.execute('INSERT INTO review_log(teacher_id,action,object_id,detail) VALUES(?,?,?,?)',(user['id'],'grade',str(aid),json.dumps(body.model_dump())))
    return {'ok':True}
@app.get('/api/teacher/sources')
def source_list(user=Depends(teacher)):
    p=data_dir()/'processed/coverage.json'
    if p.exists():coverage=json.loads(p.read_text(encoding='utf-8'))
    else:
        with connect() as db:coverage=[json.loads(r['body']) for r in db.execute('SELECT body FROM corpus_coverage').fetchall()]
    return [{**s,'extraction':next((x for x in coverage if x['id']==s['id']),{'status':'not_extracted'})} for s in SOURCES]
@app.get('/api/teacher/sources/{sid}')
def source_detail(sid:str,page:int=1,user=Depends(teacher)):
    s=next((s for s in SOURCES if s['id']==sid),None)
    if not s or page<1:raise HTTPException(404,'Source introuvable.')
    root=data_dir()/'processed'/sid
    p=root/f'page-{page:04d}.json' if s['pages'] else root/'document.json'
    if p.exists():content=json.loads(p.read_text(encoding='utf-8'))
    else:
        with connect() as db:record=db.execute('SELECT body FROM corpus_pages WHERE source_id=? AND page_key=?',(sid,p.name)).fetchone()
        if not record:raise HTTPException(404,'Cette source n’a pas encore été importée. Utilise le script de synchronisation du corpus.')
        content=json.loads(record['body'])
    return {'source':s,'content':content}

app.mount('/static',StaticFiles(directory=ROOT/'web'),name='static')
@app.get('/')
def index():return FileResponse(ROOT/'web/index.html')
