from pathlib import Path

import os

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = {
    "DIR": 'data',
    "FILE": 'db.yaml',
    "VERSION": 1.0
}

DB_FILE = os.path.join(BASE_DIR, DATABASE['DIR'], DATABASE['FILE'])