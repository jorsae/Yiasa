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
        self.rowid = None
        self.thread_id = uuid.uuid4().hex
        self.extractor = extractor.Extractor(self.fld, self.pool)
        self.allow_redirects = True
        self.crawl_counter = 0
    
    def start_crawling(self):
        logging.info(f'{self.thread_id}: Starting crawling on {self.scheme}{self.fld}')
        self.parse_robots()
        result = request.get_request(f'{self.scheme}{self.fld}', redirects=self.allow_redirects)
        print(f'result: {result}')
        print(f'extractor: {self.extractor.robots}')
        
        self.pool.put(PoolQuery(query.insert_table_domain, (self.scheme, self.fld, 1, self.creation_date), priority=1))
        
        rowid = self.pool.database.query_get(query.get_id_domain, (self.fld, ))
        while rowid == []:
            rowid = self.pool.database.query_get(query.get_id_domain, (self.fld, ))
            time.sleep(1)
        self.rowid = rowid[0][0]

        self.extractor.extract_urls(result.text)
        self.crawl()
    
    def crawl(self):
        while len(self.extractor.urls) > 0:
            url = self.extractor.get_url()
            logging.info(f'{self.thread_id} | Crawling: {url}')
            req = request.get_request(url, redirects=self.allow_redirects)
            self.pool.put(PoolQuery(query.insert_table_crawl_history, req.to_tuple(self.rowid)))

            self.extractor.extract_urls(req.text)
            self.crawl_counter += 1
            print(f'id: {self.thread_id} | crawled: {self.crawl_counter} | queue: {len(self.extractor.urls)}')
        logging.info(f'{self.thread_id}: Finished crawling {self.fld} with: {self.crawl_counter} crawled urls!')
        print(self.extractor.crawled_urls)

    def parse_robots(self):
        logging.info(f'{self.thread_id}: Parsing robots.txt')
        url = f'{globvar.scheme}{self.fld}/robots.txt'
        try:
            req = request.get_request(url)
            if req.status_code != 404:
                self.extractor.robots.parse_robots(req.text)
        except:
            logging.error(f'Something went wrong parsing robots.txt url: {url}')

    def __str__(self):
        return f'{self.thread_id} | {self.fld}'