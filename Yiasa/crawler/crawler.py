from datetime import datetime
import uuid
import sys
import logging
sys.path.append('web/')
sys.path.append('utility/')
sys.path.append('database/')
import globvar
import request
import robot
import extractor
from pq import PoolQuery
import query

class Crawler:
    def __init__(self, fld, pool):
        self.creation_date = datetime.now()
        self.pool = pool
        self.scheme = 'https://'
        self.fld = fld
        self.id = uuid.uuid4().hex
        self.extractor = extractor.Extractor(self.fld)
        self.allow_redirects = True
        self.crawl_counter = 0
    
    def start_crawling(self):
        logging.info(f'{self.id}: Starting crawling on {self.scheme}{self.fld}')
        self.parse_robots()
        result = request.get_request(f'{self.scheme}{self.fld}', redirects=self.allow_redirects)
        print(result)
        print(self.extractor.robots)
        
        self.pool.put(PoolQuery(1, query.insert_table_domain, (self.scheme, 1, self.creation_date)))

        self.extractor.extract_urls(result.text)
        self.crawl()
    
    def crawl(self):
        print(self.extractor.urls)
        while len(self.extractor.urls) > 0:

            url = self.extractor.get_url()
            logging.info(f'{self.id} | Crawling: {url}')
            req = request.get_request(url, redirects=self.allow_redirects)
            self.extractor.extract_urls(req.text)
            self.crawl_counter += 1
            print(f'crawled: {self.crawl_counter} | queue: {len(self.extractor.urls)}')
        logging.info(f'{self.id}: Finished crawling {self.fld} with: {self.crawl_counter} crawled urls!')
        print(self.extractor.crawled_urls)
            

    def parse_robots(self):
        logging.info(f'{self.id}: Parsing robots.txt')
        url = f'{globvar.scheme}{self.fld}/robots.txt'
        try:
            req = request.get_request(url)
            if req.status_code != 404:
                self.extractor.robots.parse_robots(req.text)
        except:
            logging.error(f'Something went wrong parsing robots.txt url: {url}')

    def __str__(self):
        return f'{self.id} | {self.fld}'