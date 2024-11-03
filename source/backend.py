from colorama import Fore, Back, Style
from typing import Literal, TypeAlias
from getpass import getpass
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime

from ruamel.yaml import YAML
from ruamel.yaml import CommentedMap as OrderedDict
from ruamel.yaml import CommentedSeq as OrderedList

import string, secrets, hashlib, base64, os


BASEDIR = Path(__file__).resolve().parent.parent
KEYDIR = BASEDIR / 'key'
DBDIR = BASEDIR / 'db'

KEYFILE = KEYDIR / 'key.key'
DBFILE = DBDIR / 'passwords.yml'


ForegroundColor: TypeAlias = Literal['black', 'blue', 'cyan', 'green', 'lightblack_ex', 'lightblue_ex', 'lightcyan_ex', 'lightgreen_ex', 'lightmagenta_ex', 'lightred_ex', 'lightwhite_ex', 'lightyellow_ex', 'magenta', 'red', 'white', 'yellow']
BackgroundColor: TypeAlias = Literal['black', 'blue', 'cyan', 'green', 'lightblack_ex', 'lightblue_ex', 'lightcyan_ex', 'lightgreen_ex', 'lightmagenta_ex', 'lightred_ex', 'lightwhite_ex', 'lightyellow_ex', 'magenta', 'red', 'white', 'yellow']
FontWeight: TypeAlias = Literal['normal', 'bright', 'dim']

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

class Backend:

    @property
    def check_key(self):
        return self._check_key()
    @property
    def key_path(self):
        return KEYFILE
    @property
    def check_db(self):
        return self._check_db()
    @property
    def db_path(self):
        return os.path.basename(DBFILE)

    def save(self, token: bytes):
        if not self.check_key:
            Path(KEYDIR).mkdir()
            #Path(DBFILE).touch()

        with open(KEYFILE, 'wb') as file:
            file.write(token)

    def views_details(self, data: str):
        db = database()
        with open(DBFILE, 'r') as file:
            doc = db.load(file)

            get_item = []
            for item in doc['Body']:
                if item['password'] == data:
                    get_item = item
            
            details = dict.fromkeys(['Domínio', 'Usuário', 'Senha', 'Data de Registro'])
            details['Domínio'] = get_item['domain']
            details['Usuário'] = get_item['username']
            details['Senha'] = get_item['password']
            details['Data de Registro'] = datetime.fromisoformat(get_item['created_at']).strftime("%d/%m/%Y, %H:%M:%S")

            return details
        

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
        if not Path(DBDIR).exists():
            Path(DBDIR).mkdir()
        
        if not Path(DBFILE).exists():
            db = database()
            data = database_scope()

            with open(DBFILE, 'w') as db_file:
                db.dump(data, db_file)

class Console:
    "Customize the echo console"
    
    @classmethod
    def Write(cls, *values: object, fg: ForegroundColor = None, bg: BackgroundColor = None, weight: FontWeight = 'normal'):
        extra = []
        
        if fg: extra.append(getattr(Fore, fg.upper()))
        if bg: extra.append(getattr(Back, bg.upper()))
        if weight: extra.append(getattr(Style, weight.upper()))

        echo = print(*extra, *values, Style.RESET_ALL, sep=str().strip())
        return echo

    @classmethod
    def ReadLine(cls, prompt: object = "", password: bool = False):
        if password:
            return getpass(prompt)
        return input(prompt)
  
class Cryptography:
    AVAILABLE_STRING = string.ascii_lowercase + string.ascii_uppercase
    def __init__(self, key: bytes):
        if not isinstance(key, bytes):
            key.encode()
        
        self.fernet = Fernet(key)
    
    @classmethod
    def signature(cls):
        with open(KEYFILE, 'rb') as file:
            key = file.read()
        return key.decode()

    def encrypt(self, password: str):

        if not isinstance(password, bytes):
            password = password.encode()

        return self.fernet.encrypt(password)

    def decrypt(self, encrypt_pass: bytes):
        if not isinstance(encrypt_pass, bytes):
            encrypt_pass = encrypt_pass.encode()
        
        return self.fernet.decrypt(encrypt_pass)

    @classmethod
    def generate_key(cls):
        token = ''
        for _ in range(20):
            token += secrets.choice(cls.AVAILABLE_STRING)
        
        hash = hashlib.sha256(token.encode()).digest()
        key = base64.b64encode(hash)
        
        return key

class BaseModel:
    def __init__(self, *args):
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
        
