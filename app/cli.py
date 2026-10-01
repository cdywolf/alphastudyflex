import argparse,getpass,sqlite3
from .db import initialize
from .auth import create_user

def main():
    parser=argparse.ArgumentParser();subs=parser.add_subparsers(dest='command',required=True)
    user=subs.add_parser('create-user');user.add_argument('--username',required=True);user.add_argument('--role',choices=['student','teacher'],default='teacher')
    args=parser.parse_args();initialize()
    password=getpass.getpass('Mot de passe (10 caractères minimum) : ')
    if password!=getpass.getpass('Confirmer : '):raise SystemExit('Les mots de passe diffèrent.')
    try:create_user(args.username,password,args.role)
    except (ValueError,sqlite3.IntegrityError) as e:raise SystemExit(str(e))
    print('Compte créé. Lance : python -m uvicorn app.main:app --host 127.0.0.1 --port 8000')
if __name__=='__main__':main()
