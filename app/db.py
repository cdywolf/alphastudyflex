from __future__ import annotations
import os,sqlite3
from pathlib import Path
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parents[1]

def data_dir():
    p=Path(os.environ.get('ASF_DATA_DIR',ROOT/'data')).resolve();p.mkdir(parents=True,exist_ok=True);return p

class Row(dict):
    def __getitem__(self,key):return list(self.values())[key] if isinstance(key,int) else super().__getitem__(key)
class Result:
    def __init__(self,cursor):self.cursor=cursor
    def fetchone(self):
        r=self.cursor.fetchone();return Row(r) if r is not None else None
    def fetchall(self):return [Row(r) for r in self.cursor.fetchall()]
    def __iter__(self):return iter(self.fetchall())
class Postgres:
    def __init__(self,connection):self.connection=connection
    def execute(self,sql,params=()):return Result(self.connection.execute(sql.replace('?', '%s'),params))
    def executescript(self,sql):
        for statement in sql.split(';'):
            if statement.strip():self.connection.execute(statement)
    def lock(self,key):self.connection.execute('SELECT pg_advisory_xact_lock(%s)',(key,))
class SQLite:
    def __init__(self,connection):self.connection=connection
    def execute(self,sql,params=()):return self.connection.execute(sql,params)
    def executescript(self,sql):return self.connection.executescript(sql)
    def lock(self,key):self.connection.execute('BEGIN IMMEDIATE')

@contextmanager
def connect():
    url=os.environ.get('DATABASE_URL')
    if url:
        import psycopg
        from psycopg.rows import dict_row
        raw=psycopg.connect(url,connect_timeout=10,row_factory=dict_row)
        db=Postgres(raw)
    else:
        if os.environ.get('RENDER') or os.environ.get('ASF_ENV')=='production':
            raise RuntimeError('DATABASE_URL est obligatoire en hébergement. SQLite local serait perdu au redémarrage.')
        raw=sqlite3.connect(data_dir()/'app.sqlite3',timeout=10);raw.row_factory=sqlite3.Row;raw.execute('PRAGMA foreign_keys=ON');db=SQLite(raw)
    try:
        yield db;raw.commit()
    except BaseException:
        raw.rollback();raise
    finally:raw.close()

def initialize():
    schema=SCHEMA
    with connect() as db:
        if isinstance(db,Postgres):
            db.lock(987431)
            schema=schema.replace('INTEGER PRIMARY KEY','SERIAL PRIMARY KEY').replace('DEFAULT CURRENT_TIMESTAMP','DEFAULT (CURRENT_TIMESTAMP::text)')
        else:db.execute('PRAGMA journal_mode=WAL')
        db.executescript(schema)
        db.execute('INSERT INTO schema_versions(version) VALUES(1) ON CONFLICT(version) DO NOTHING')
        # Version 2 : un parcours appartient à un chapitre ; les parcours existants restent en tectonique.
        if not db.execute('SELECT version FROM schema_versions WHERE version=2').fetchone():
            db.execute("ALTER TABLE runs ADD COLUMN chapter TEXT NOT NULL DEFAULT 'tectonics'")
            db.execute('INSERT INTO schema_versions(version) VALUES(2)')

SCHEMA = r"""


        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('student','teacher')), created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS sessions(token_hash TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id) ON DELETE CASCADE, expires INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS publications(question_id TEXT NOT NULL, revision TEXT NOT NULL, reviewer_id INTEGER REFERENCES users(id), status TEXT NOT NULL, reviewed_at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(question_id,revision));
        CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY,user_id INTEGER NOT NULL REFERENCES users(id),mode TEXT NOT NULL,skill TEXT,question_ids TEXT NOT NULL,snapshot TEXT NOT NULL,completed INTEGER DEFAULT 0,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,run_id TEXT REFERENCES runs(id),question_id TEXT NOT NULL,response TEXT NOT NULL,score REAL,assisted INTEGER NOT NULL DEFAULT 0,feedback TEXT,reviewed_by INTEGER REFERENCES users(id),created_at TEXT DEFAULT CURRENT_TIMESTAMP,UNIQUE(run_id,question_id));
        CREATE TABLE IF NOT EXISTS hints(run_id TEXT REFERENCES runs(id),question_id TEXT,used INTEGER NOT NULL,PRIMARY KEY(run_id,question_id));
        CREATE TABLE IF NOT EXISTS profiles(user_id INTEGER PRIMARY KEY REFERENCES users(id),goal TEXT NOT NULL DEFAULT '',minutes INTEGER NOT NULL DEFAULT 20);
        CREATE TABLE IF NOT EXISTS review_log(id INTEGER PRIMARY KEY,teacher_id INTEGER REFERENCES users(id),action TEXT NOT NULL,object_id TEXT NOT NULL,detail TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);


CREATE TABLE IF NOT EXISTS schema_versions(version INTEGER PRIMARY KEY);
CREATE TABLE IF NOT EXISTS corpus_pages(source_id TEXT NOT NULL,page_key TEXT NOT NULL,body TEXT NOT NULL,PRIMARY KEY(source_id,page_key));
CREATE TABLE IF NOT EXISTS corpus_coverage(source_id TEXT PRIMARY KEY,body TEXT NOT NULL);
"""
