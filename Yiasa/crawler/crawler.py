from datetime import datetime
import uuid
import sys
sys.path.append('web/')
sys.path.append('utility/')
import globvar
import request
import robot
import extractor

class Crawler:
    def __init__(self, fld):
        self.creation_date = datetime.now()
        self.scheme = 'https://'
        self.fld = fld
        self.id = uuid.uuid4().hex
        self.robots = robot.Robots()
        self.urls = extractor.Urls()
        self.allow_redirects = True
    
    def start_crawling(self):
        self.parse_robots()
        result = request.get_request(f'{self.scheme}{self.fld}', redirects=self.allow_redirects)
        print(result)
        urls, emails = extractor.extract_urls(result.text, self.fld)
        print(urls)
        print(emails)
        print(f'{len(urls)}{len(emails)}')

    def parse_robots(self):
        url = f'{globvar.scheme}{self.fld}/robots.txt'
        try:
            req = request.get_request(url)
            if req.status_code != 404:
                self.robots.parse_robots(req.text)
        except:
            # TODO: log error
            pass

    def __str__(self):
        return f'{self.id} | {self.fld}'