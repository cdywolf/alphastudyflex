import sqlite3
from app.db import initialize,connect,data_dir
from app.content import QUESTIONS,chapter_questions
from tests.test_flows import clients,finish,publish_all  # noqa: F401  (fixture partagée)

def publish(teacher,chapter):
    for q in chapter_questions(chapter):
        assert teacher.post('/api/teacher/questions/'+q['id']+'/publish',json={'confirmed':True,'note':'Validation de test, pas une validation humaine réelle.'}).status_code==200

def test_volcano_chapter_end_to_end_and_isolated_from_tectonics(clients):
    teacher,student,_=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic','chapter':'volcanoes'}).json()['id'];assert finish(student,rid,wrong=True)['score']==0
    for skill in ['v-eruptions','v-edifice','v-tectonics']:
        rid=student.post('/api/runs',json={'mode':'practice','chapter':'volcanoes','skill':skill}).json()['id'];finish(student,rid)
    pending=teacher.get('/api/teacher/overview').json()['pending'];assert [p['question']['id'] for p in pending]==['vp-t2']
    assert teacher.post('/api/teacher/reviews/'+str(pending[0]['id']),json={'score':2,'feedback':'Subduction, origine du magma et explosivité reliées.'}).status_code==200
    rid=student.post('/api/runs',json={'mode':'final','chapter':'volcanoes'}).json()['id'];assert finish(student,rid)['score']==6
    volcano=student.get('/api/dashboard?chapter=volcanoes').json()
    assert len(volcano['runs'])==5 and all(s['status']=='Consolidé' for s in volcano['skills'])
    assert {s['id'] for s in volcano['skills']}=={'v-eruptions','v-edifice','v-tectonics'}
    tectonics=student.get('/api/dashboard').json()
    assert tectonics['runs']==[] and all(s['status']=='Non évalué' for s in tectonics['skills'])
    # Le diagnostic de tectonique reste à faire : il n'est pas confondu avec celui du volcanisme.
    assert student.post('/api/runs',json={'mode':'practice','chapter':'tectonics','skill':'graph'}).status_code==409

def test_readiness_is_per_chapter(clients):
    teacher,student,_=clients;publish(teacher,'tectonics')
    assert student.post('/api/runs',json={'mode':'diagnostic','chapter':'volcanoes'}).status_code==409
    assert student.get('/api/lessons/v-edifice').status_code==409
    assert student.post('/api/runs',json={'mode':'diagnostic','chapter':'tectonics'}).status_code==200
    chapters={c['id']:c['ready'] for c in student.get('/api/dashboard').json()['pilot_chapters']}
    assert chapters=={'tectonics':True,'volcanoes':False}

def test_chapter_and_skill_validation(clients):
    teacher,student,_=clients;publish_all(teacher)
    assert student.post('/api/runs',json={'mode':'diagnostic','chapter':'seisms'}).status_code==404
    assert student.get('/api/dashboard?chapter=seisms').status_code==404
    student.post('/api/runs',json={'mode':'diagnostic','chapter':'volcanoes'})
    assert student.post('/api/runs',json={'mode':'practice','chapter':'volcanoes','skill':'graph'}).status_code==400
    lesson=student.get('/api/lessons/v-edifice')
    assert lesson.status_code==409  # diagnostic en cours : la séance attend la fin de l'évaluation

def test_cross_chapter_prerequisite_is_signalled_not_imposed(clients):
    teacher,student,_=clients;publish_all(teacher)
    alerts=student.get('/api/dashboard?chapter=volcanoes').json()['prerequisite_alerts']
    assert [(a['id'],a['chapter']) for a in alerts]==[('movement','tectonics')]
    assert student.post('/api/runs',json={'mode':'diagnostic','chapter':'volcanoes'}).status_code==200

def test_volcano_questions_do_not_expose_answers(clients):
    teacher,student,_=clients;publish_all(teacher)
    rid=student.post('/api/runs',json={'mode':'diagnostic','chapter':'volcanoes'}).json()['id']
    body=student.get('/api/runs/'+rid).json()
    assert body['chapter']=='volcanoes' and not {'answer','explanation','hints','criteria'}.intersection(body['question'])

def test_migration_from_schema_v1_keeps_existing_runs(tmp_path,monkeypatch):
    monkeypatch.setenv('ASF_DATA_DIR',str(tmp_path));monkeypatch.delenv('DATABASE_URL',raising=False);monkeypatch.setenv('ASF_ENV','development')
    raw=sqlite3.connect(data_dir()/'app.sqlite3')
    raw.executescript("""CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT NOT NULL, created_at TEXT);
    CREATE TABLE runs(id TEXT PRIMARY KEY,user_id INTEGER NOT NULL,mode TEXT NOT NULL,skill TEXT,question_ids TEXT NOT NULL,snapshot TEXT NOT NULL,completed INTEGER DEFAULT 0,created_at TEXT);
    CREATE TABLE schema_versions(version INTEGER PRIMARY KEY);INSERT INTO schema_versions VALUES(1);
    INSERT INTO users VALUES(1,'old','x','student',NULL);INSERT INTO runs VALUES('r1',1,'diagnostic',NULL,'[]','[]',1,NULL);""")
    raw.commit();raw.close()
    initialize();initialize()  # idempotent
    with connect() as db:
        assert db.execute('SELECT chapter FROM runs WHERE id=?',('r1',)).fetchone()['chapter']=='tectonics'
        assert [r['version'] for r in db.execute('SELECT version FROM schema_versions ORDER BY version').fetchall()]==[1,2]
