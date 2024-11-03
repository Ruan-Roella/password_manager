from .backend import BaseModel
from datetime import datetime

class Passwords(BaseModel):
    def __init__(self, domain = None, username = None, password = None):
        self.domain = domain
        self.username = username
        self.password = password
        self.created_at = datetime.now().isoformat("#", "seconds")