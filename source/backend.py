from colorama import Fore, Back, Style
from typing import Literal, TypeAlias
from getpass import getpass
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime


import string, secrets, hashlib, base64, os



KEYDIR = BASEDIR / 'key'
DBDIR = BASEDIR / 'db'

KEYFILE = KEYDIR / 'key.key'
DBFILE = DBDIR / 'passwords.yml'



__version__ = 1.0

def database():
    db = YAML()
    db.indent = 4
    db.block_seq_indent = 2
    
    return db

def database_scope():
    scope = OrderedDict({
        "Header": OrderedDict({
            "Type": 'passwords_db',
            "Version": __version__
        }),


        "Body": None
    })
    return scope

def emojis(unicode: str):
    try:
        return chr(int(unicode, 16))
    except:
        return 'x'

def strftime(date: str):
    try:
        return datetime.fromisoformat(date).strftime("%d/%m/%Y, %H:%M:%S")
    except ValueError:
        return date

class Backend:

    @property
    def check_key(self):
        return self._check_key()
    @property
    def check_db(self):
        return self._check_db()
    @property
    def key_path(self):
        return KEYFILE
    @property
    def create_db(self):
        return self._create_db()
    @property
    def db_path(self):
        return os.path.basename(DBFILE)

    def save(self, token: bytes):
        if not self.check_key:
            Path(KEYDIR).mkdir()

        with open(KEYFILE, 'wb') as file:
            file.write(token)

    def views_details(self, data: str):
        db = database()
        with open(DBFILE, 'r') as file:
            doc = db.load(file)

            get_item = []
            for item in doc['Body']:
                if item['password'] == data:
                    item['created_at'] = strftime(item['created_at'])
                    get_item = item
            
            return list(filter(lambda s: not( s == data ), get_item.values()))

    def select_from_db(self, id: int = None):
        db = database()
        with open(DBFILE,'r', encoding='utf-8') as dbfile:
            query = db.load(dbfile.read())

            result = [ (idx, q['domain'], q['username'], q['password']) for idx, q in enumerate(query['Body'], start=1) ]
            if id:
                return [ (domain, password) for idx, domain, _, password in result if idx == id ][0]
            return result


    def _check_key(self):
        try:
            with open(KEYFILE, 'r') as file:
                key = file.readlines()
        
            if key:
                return True
            return False
        except FileNotFoundError:
            return False

    def _check_db(self):
        db = database()
        with open(DBFILE, 'r') as file:
            doc = db.load(file.read())

            try:
                if doc['Body']:
                    return True
                return False
            except KeyError:
                return False

    def _create_db(self):
        if not Path(DBDIR).exists():
            Path(DBDIR).mkdir()
        
        if not Path(DBFILE).exists():
            db = database()
            data = database_scope()

            with open(DBFILE, 'w') as db_file:
                db.dump(data, db_file)


  




class BaseModel:
    def __init__(self):
        r"""
            A database model

            :param domain: Estes são os nomes de domínio que você salvará

                e.g; `Youtube`

            :param username: The current domain login username

            :param password: The current domain login password
        """

    def __setattr__(self, name, value):

        if isinstance(value, bytes):
            value = value.decode()

        if value == "":
            value = None
        self.__dict__[name] = value

    def save(self):

        db = database()
        data = OrderedList([
            OrderedDict(self.__dict__)
        ])
#
        with open(DBFILE, 'a') as file:
            db.dump(data, file)
        
