from pathlib import Path

import os

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = {
    "DIR": BASE_DIR / 'data',
    "FILE": 'db.yaml',
    "VERSION": 1.0
}

DB_FILE = os.path.join(DATABASE['DIR'], DATABASE['FILE'])