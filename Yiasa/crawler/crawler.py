from datetime import datetime
import uuid
import sys
import logging
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
        self.crawl_counter = 0
    
    def start_crawling(self):
        logging.info(f'{self.id}: Starting crawling on {self.scheme}{self.fld}')
        self.parse_robots()
        result = request.get_request(f'{self.scheme}{self.fld}', redirects=self.allow_redirects)
        print(result)
        print(self.robots)
        self.urls.extract_urls(result.text, self.fld)
        self.crawl()
    
    def crawl(self):
        while len(self.urls.urls) > 0:
            url = self.urls.get_url()
            logging.info(f'{self.id} | Crawling: {url}')
            req = request.get_request(url, redirects=self.allow_redirects)
            self.urls.extract_urls(req.text, self.fld)
            self.crawl_counter += 1
            print(f'crawled: {self.crawl_counter} | queue: {len(self.urls.urls)}')
        logging.info(f'{self.id}: Finished crawling {self.fld} with: {self.crawl_counter} crawled urls!')
            

    def parse_robots(self):
        logging.info(f'{self.id}: Parsing robots.txt')
        url = f'{globvar.scheme}{self.fld}/robots.txt'
        try:
            req = request.get_request(url)
            if req.status_code != 404:
                self.robots.parse_robots(req.text)
        except:
            logging.error(f'Something went wrong parsing robots.txt url: {url}')

    def __str__(self):
        return f'{self.id} | {self.fld}'