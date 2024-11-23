from ruamel.yaml import YAML
from ruamel.yaml import CommentedMap as OrderedDict
from ruamel.yaml import CommentedSeq as OrderedList

from source.core.conf import DATABASE

from typing import TypeAlias, Union
from os import PathLike

import os


StrOrBytesPath: TypeAlias = str | bytes | PathLike[str] | PathLike[bytes]

class Database:
    def __init__(self, filename: StrOrBytesPath) -> None:
        self.db = YAML()
        self.db.indent = 4
        self.db.block_seq_indent = 2
        self.name = filename

    @property
    def last_id(self):
        db = self.connect()
        id = 1
        
        if db['Body']:
            id = db['Body'][-1]['id'] + 1
        return id

    def __enter__(self):
        return self
    def __exit__(self, exc, exc_type, exc_traceback):
        return self

    def connect(self):
        with open(self.name, 'r') as db_file:
            return self.db.load(db_file.read())

    def create_all(self):

        table = OrderedDict({
            "Header": OrderedDict({
                "Type": DATABASE['FILE'],
                "Version": DATABASE['VERSION']
            }),
            "Body": OrderedList(),
            "Footer": OrderedList()
        })

        with open(self.name, 'w') as yaml_file:
            self.db.dump(table, yaml_file)

    def insert_into(self, tablename: str, data: dict):
        doc = self.connect()
        
        data['id'] = self.last_id
        table = str(tablename)
        value = OrderedDict(data)

        with open(self.name, 'w') as yaml_file:
            doc[table].append(value)

            self.db.dump(doc, yaml_file)

    def select_from(self, tablename: str, value: Union[str | list | tuple | None] = None):

        doc = self.connect()

        result = doc[tablename]

        if isinstance(value, str):
            ...

        if isinstance(value, Union[list | tuple]):
            return list(tuple(dct[v] for v in value) for dct in result)
        
        return result
