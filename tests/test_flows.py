import json,os
import pytest
from fastapi.testclient import TestClient
from app.main import app,ATTEMPTS
from app.db import initialize,connect
from app.auth import create_user
from app.content import QUESTIONS,QMAP,revision,is_published

@pytest.fixture
def clients(tmp_path,monkeypatch):
    monkeypatch.setenv('ASF_DATA_DIR',str(tmp_path));monkeypatch.setenv('ASF_ENV','development');monkeypatch.delenv('RENDER',raising=False);monkeypatch.delenv('ASF_INVITE_CODE',raising=False)
    if os.environ.get('TEST_DATABASE_URL'):monkeypatch.setenv('DATABASE_URL',os.environ['TEST_DATABASE_URL'])
    else:monkeypatch.delenv('DATABASE_URL',raising=False)
    initialize()
    with connect() as db:
        for table in ['review_log','attempts','hints','runs','profiles','publications','sessions','users','corpus_pages','corpus_coverage']:db.execute('DELETE FROM '+table)
    ATTEMPTS.clear()
    create_user('teacher','Teacher-test-2026','teacher');create_user('learner','Learner-test-2026');create_user('other','Another-test-2026')
    with TestClient(app) as teacher,TestClient(app) as student,TestClient(app) as other:
        assert teacher.post('/api/login',json={'username':'teacher','password':'Teacher-test-2026'}).status_code==200
        assert student.post('/api/login',json={'username':'learner','password':'Learner-test-2026'}).status_code==200
        assert other.post('/api/login',json={'username':'other','password':'Another-test-2026'}).status_code==200
        yield teacher,student,other

def publish_all(teacher):
    for q in QUESTIONS:assert teacher.post('/api/teacher/questions/'+q['id']+'/publish',json={'confirmed':True,'note':'Validation de test, pas une validation humaine réelle.'}).status_code==200

def finish(student,rid,wrong=False):
    while True:
        body=student.get('/api/runs/'+rid).json()
        if body['completed']:return body['result']
        q=QMAP[body['question']['id']]
        response='Les roches se forment à la dorsale et s’éloignent ensuite avec les plaques.' if q['kind']=='open' else ((q['answer']+1)%len(q['choices']) if wrong else q['answer'])
        r=student.post('/api/runs/'+rid+'/answer',json={'question_id':q['id'],'response':response});assert r.status_code==200,r.text

def test_end_to_end_assessment_review_and_persistence(clients):
    teacher,student,_=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic'}).json()['id'];r=finish(student,rid,wrong=True);assert r['score']==0
    for skill in ['arguments','graph','movement']:
        rid=student.post('/api/runs',json={'mode':'practice','skill':skill}).json()['id'];finish(student,rid)
    pending=teacher.get('/api/teacher/overview').json()['pending'];assert len(pending)==1
    assert teacher.post('/api/teacher/reviews/'+str(pending[0]['id']),json={'score':2,'feedback':'Observation et mécanisme correctement reliés.'}).status_code==200
    rid=student.post('/api/runs',json={'mode':'final'}).json()['id'];assert finish(student,rid)['score']==6
    dashboard=student.get('/api/dashboard').json();assert len(dashboard['runs'])==5
    assert all(s['status']=='Consolidé' for s in dashboard['skills'])
    student.post('/api/logout');student.post('/api/login',json={'username':'learner','password':'Learner-test-2026'})
    assert len(student.get('/api/dashboard').json()['runs'])==5

def test_publication_gate_and_revision_invalidation(clients):
    teacher,student,_=clients
    assert student.post('/api/runs',json={'mode':'diagnostic'}).status_code==409
    publish_all(teacher)
    with connect() as db:
        assert is_published(db,QUESTIONS[0])
        changed={**QUESTIONS[0],'prompt':'Nouvelle formulation'}
        assert not is_published(db,changed)

def test_answers_not_exposed_and_assessment_hints_blocked(clients):
    teacher,student,_=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic'}).json()['id'];q=student.get('/api/runs/'+rid).json()['question']
    assert not {'answer','explanation','hints','criteria'}.intersection(q)
    assert student.post('/api/runs/'+rid+'/hint',json={'question_id':q['id']}).status_code==403
    assert student.get('/api/lessons/arguments').status_code==409
    r=student.post('/api/runs/'+rid+'/answer',json={'question_id':q['id'],'response':0}).json();assert r['score'] is None and r['sources']==[]

def test_role_and_student_isolation(clients):
    teacher,student,other=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic'}).json()['id']
    assert student.get('/api/teacher/content').status_code==403
    assert student.get('/api/teacher/sources').status_code==403
    assert other.get('/api/runs/'+rid).status_code==404
    assert other.post('/api/runs/'+rid+'/answer',json={'question_id':'d-a1','response':0}).status_code==404

def test_double_submission_and_bad_values(clients):
    teacher,student,_=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic'}).json()['id']
    assert student.post('/api/runs/'+rid+'/answer',json={'question_id':'d-a1','response':999}).status_code==400
    assert student.post('/api/runs/'+rid+'/answer',json={'question_id':'d-a1','response':True}).status_code==422
    body={'question_id':'d-a1','response':1};assert student.post('/api/runs/'+rid+'/answer',json=body).status_code==200
    assert student.post('/api/runs/'+rid+'/answer',json=body).status_code==409

def test_hints_are_recorded_and_do_not_count_as_independent(clients):
    teacher,student,_=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic'}).json()['id'];finish(student,rid,wrong=True)
    rid=student.post('/api/runs',json={'mode':'practice','skill':'arguments'}).json()['id']
    assert student.post('/api/runs/'+rid+'/hint',json={'question_id':'p-a1'}).status_code==200
    finish(student,rid)
    skill=student.get('/api/dashboard').json()['skills'][0];assert skill['independent_successes']==1

def test_final_requires_practice_and_active_run_resumes(clients):
    teacher,student,_=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic'}).json()['id']
    assert student.post('/api/runs',json={'mode':'practice','skill':'graph'}).json()['id']==rid
    finish(student,rid)
    assert student.post('/api/runs',json={'mode':'final'}).status_code==409

def test_csrf_and_session_revocation(clients):
    _,student,_=clients
    assert student.post('/api/logout',json={},headers={'Origin':'https://attacker.example'}).status_code==403
    assert student.post('/api/logout',json={}).status_code==200
    assert student.get('/api/me').status_code==401

def test_signup_cannot_elevate_and_requires_invite(clients,monkeypatch):
    _,student,_=clients
    payload={'username':'new-user','password':'New-password-2026','role':'teacher'}
    assert student.post('/api/register',json=payload).status_code==422
    monkeypatch.setenv('ASF_INVITE_CODE','Class-invite');payload.pop('role')
    assert student.post('/api/register',json=payload).status_code==403
    assert student.post('/api/register',json=payload,headers={'X-Invite-Code':'Class-invite'}).status_code==200

def test_remote_corpus_fallback_and_scope(clients):
    teacher,_,_=clients
    record={'pdf_page':1,'text':'Extrait de test','validation':'pending'}
    with connect() as db:
        db.execute('INSERT INTO corpus_pages VALUES(?,?,?)',('manual-apef','page-0001.json',json.dumps(record)))
        db.execute('INSERT INTO corpus_coverage VALUES(?,?)',('manual-apef',json.dumps({'id':'manual-apef','status':'extracted'})))
    assert teacher.get('/api/teacher/sources/manual-apef').json()['content']['text']=='Extrait de test'
    assert len(teacher.get('/api/teacher/sources').json())==17
    assert teacher.get('/api/teacher/sources/unknown').status_code==404

def test_first_teacher_setup_is_secret_and_single_use(clients,monkeypatch):
    teacher,student,_=clients
    monkeypatch.setenv('ASF_SETUP_TOKEN','installation-test-secret-2026')
    with connect() as db:
        db.execute('DELETE FROM sessions')
        db.execute('DELETE FROM users')
    body={'username':'new-teacher','password':'Teacher-setup-2026','setup_token':'incorrect-test-secret-2026'}
    assert student.post('/api/setup',json=body).status_code==403
    body['setup_token']='installation-test-secret-2026'
    assert student.post('/api/setup',json=body).status_code==200
    body['username']='second-teacher'
    assert student.post('/api/setup',json=body).status_code==409
    assert teacher.post('/api/login',json={'username':'new-teacher','password':'Teacher-setup-2026'}).json()['role']=='teacher'

def test_hosting_refuses_ephemeral_sqlite(monkeypatch):
    monkeypatch.delenv('DATABASE_URL',raising=False)
    monkeypatch.setenv('ASF_ENV','production')
    with pytest.raises(RuntimeError,match='DATABASE_URL'):
        with connect():pass
