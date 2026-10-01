import hashlib,hmac,secrets,time,re
from fastapi import HTTPException,Request
from .db import connect

def hash_password(password):
    salt=secrets.token_bytes(16);digest=hashlib.scrypt(password.encode(),salt=salt,n=16384,r=8,p=1)
    return salt.hex()+':'+digest.hex()
def verify_password(password,encoded):
    salt,wanted=encoded.split(':');actual=hashlib.scrypt(password.encode(),salt=bytes.fromhex(salt),n=16384,r=8,p=1)
    return hmac.compare_digest(actual.hex(),wanted)
def create_user(username,password,role='student'):
    if not re.fullmatch(r'[a-zA-Z0-9_-]{3,40}',username):raise ValueError('Identifiant : 3 à 40 lettres, chiffres, tirets ou underscores.')
    if not 10<=len(password)<=128:raise ValueError('Mot de passe : 10 à 128 caractères.')
    if role not in ['student','teacher']:raise ValueError('Rôle invalide.')
    with connect() as db:
        cur=db.execute('INSERT INTO users(username,password,role) VALUES(?,?,?) RETURNING id',(username.lower(),hash_password(password),role));return cur.fetchone()[0]

def current_user(request:Request):
    token=request.cookies.get('asf_session','')
    with connect() as db:
        row=db.execute('SELECT u.id,u.username,u.role FROM sessions s JOIN users u ON u.id=s.user_id WHERE token_hash=? AND expires>?',(hashlib.sha256(token.encode()).hexdigest(),int(time.time()))).fetchone()
    if not row:raise HTTPException(401,'Connecte-toi pour continuer.')
    return dict(row)
def teacher(request:Request):
    u=current_user(request)
    if u['role']!='teacher':raise HTTPException(403,'Cet espace est réservé aux enseignants.')
    return u
