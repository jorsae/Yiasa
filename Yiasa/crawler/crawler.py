from datetime import datetime
import uuid
import sys
sys.path.append('web/')
sys.path.append('utility/')
import globvar
import request
import robot

class Crawler:
    def __init__(self, fld):
        self.creation_date = datetime.now()
        self.fld = fld
        self.id = uuid.uuid4().hex
        self.robots = robot.Robots()
    
    def parse_robots(self):
        url = f'{globvar.scheme}{self.fld}/robots.txt'
        try:
            req = request.get_request(url)
            if req.status_code != 404:
                self.robots.parse_robots(req.text)
        except:
            pass

    def __str__(self):
        return f'{self.id} | {self.fld}'