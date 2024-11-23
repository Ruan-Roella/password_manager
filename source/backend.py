from source.db import Database
from source.settings import DATABASE, DB_FILE

from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

import os
import string
import secrets
import base64
import hashlib

def strftime(date: str):
    try:
        return datetime.fromisoformat(date).strftime("%d/%m/%Y, %H:%M:%S")
    except ValueError:
        return date

class Backend(Database):
    def __init__(self) -> None:
        super().__init__(filename=DB_FILE)

        if not Path(DB_FILE).exists():
            Path(DATABASE['DIR']).mkdir()
            self.create_all()
        
        
    def is_registred(self):
        db = self.connect()

        if db['Footer']:
            return True
        return False
    
    def pin_isvalid(self, pin):
        db = self.connect()
        db_pin = db['Footer'][0]['pin']
        
        if db_pin == self.set_pincode(pin):
            return True
        return False
    
    def set_pincode(self, pin):
        
        encrypt = hashlib.pbkdf2_hmac('SHA256', pin.encode(), b"pincode" * 4, 100_000)
        pincode = 'pbkdf2_hmac' + encrypt.hex()
        
        return pincode

    def get_password(self, id: int):
        db = self.connect()

        password = None
        for item in db['Body']:
            if item['id'] == id:
                password = item['password']
        return password

    def show_details(self, id: int):

        db = self.connect()

        result = []
        for item in db['Body']:
            if item['id'] == id:
                item['created_at'] = strftime(item['created_at'])
                result = item

        return list(filter(lambda val: not( val == id ), result.values()))

class Cryptography:
    AVAILABLE_STRING = string.ascii_lowercase + string.ascii_uppercase
    def __init__(self, key: bytes):
        if not isinstance(key, bytes):
            key.encode()
        
        self.fernet = Fernet(key)
    
    @classmethod
    def signature(cls):
        with Database(DB_FILE) as db:
            doc = db.connect()
            key = doc['Footer'][0]['key']
        return key

    def encrypt(self, password: bytes):

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


class PasswordGenerate:
    PIN_CODE = string.digits
    ALNUMERIC = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$"

    @classmethod
    def pin_code(cls, length: int):
        if not isinstance(length, int):
            length = int(length)
        
        key = [ secrets.choice(cls.PIN_CODE) for _ in range(length) ]
        scan = cls._verify_duplicate(key)
        pin = scan
        if len(scan) < length:
            current_len = length - len(scan)
            for _ in range(current_len):
                pin.add(secrets.choice(cls.PIN_CODE))
                break
        else:
            for k in key:
                pin.add(k)
                break
        return ''.join(p for p in pin)
    
    @classmethod
    def alnumeric(cls, length: int):
        if not isinstance(length, int):
            length = int(length)

        key = [ secrets.choice(cls.ALNUMERIC) for _ in range(length) ]

        alnum = cls._check_alnum(key)
        return ''.join(k for k in key)
        

    def _check_alnum(key: list):
        symbols = []
        numeric = []
        for k in key:
            if k in string.digits:
                numeric.append(k)
            if k in "!@#$":
                symbols.append(k)
        
        if len(symbols) < 1:
            del key[0]
            key.insert(0, secrets.choice("!@#$"))
        
        size = len(numeric)
        if size < 6:
            del key[1:size]
            for idx, num in enumerate(numeric, start=1):
                key.insert(idx, secrets.choice(string.digits))
                break
        return key
                
    def _verify_duplicate(_l: list):
        return set(list(_l))

