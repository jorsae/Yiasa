import datetime
import sys
sys.path.append('web/')
import request

class Crawler():
    def __init__(self):
        self.creation_time = datetime.datetime.now()