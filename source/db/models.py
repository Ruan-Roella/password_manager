from typing import Self
from datetime import datetime

from .base import Database
from source.settings import DB_FILE

class BaseModel:
    instance = None

    def __new__(cls, **values) -> Self:
        cls.instance = dict.fromkeys(cls.__annotations__.keys())
        
        for value in values:
            cls.instance[value] = values[value]
        
        return super().__new__(cls)

    def save(self):
        self.instance['created_at'] = datetime.now().isoformat("#", 'seconds')
        
        with Database(DB_FILE) as db:
            db.insert_into(self, self.instance)


    def __repr__(self) -> str:
        if isinstance(self, Users):
            return 'Footer'
        return 'Body'


class Users(BaseModel):
    id: int
    pin: int
    key: str
    created_at: datetime

class Passwords(BaseModel):
    id: int
    domain: str
    description: str
    password: str
    created_at: datetime