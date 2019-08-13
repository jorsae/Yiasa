from datetime import datetime
import uuid
import sys
sys.path.append('web/')
import request

class Crawler:
    def __init__(self, fld):
        self.creation_date = datetime.now()
        self.fld = fld
        self.id = uuid.uuid4().hex
    
    def __str__(self):
        return f'{self.id} | {self.fld}'