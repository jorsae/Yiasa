from datetime import datetime
import uuid
import time
import sys
import logging
sys.path.append('web/')
sys.path.append('utility/')
sys.path.append('database/')
import utility
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
        self.fld = fld
        self.rowid = None
        self.thread_id = uuid.uuid4().hex
        self.extractor = extractor.Extractor(self.fld, self.pool)
        self.crawl_counter = 0
    
    def add_to_domain_database(self):
        rowid = self.pool.database.query_get(query.get_id_domain, (self.fld, ))
        updateRow = True
        # FLD does not exist in domain, insert it
        while rowid == []:
            updateRow = False
            self.pool.database.query(query.insert_table_domain, (globvar.scheme, self.fld, 1, self.creation_date, self.creation_date))
            rowid = self.pool.database.query_get(query.get_id_domain, (self.fld, ))
        self.rowid = rowid[0][0]

        if updateRow:
            self.pool.database.query(query.update_table_domain, (self.creation_date, self.rowid))
    
    def start_crawling(self):
        url = f'{globvar.scheme}{self.fld}'
        logging.info(f'{self.thread_id}: Starting crawling on {url}')

        self.add_to_domain_database()
        self.parse_robots()

        req = self.send_request(url)
        if req == None:
            logging.info(f'{self.thread_id}: {url} could not be crawled. Stopping crawler...')
            return

        self.extractor.extract_urls(req.text)
        self.crawl()
    
    def send_request(self, url, depth=globvar.REDIRECT_MAX_DEPTH):
        req = request.get_request(url, redirects=globvar.ALLOW_REDIRECTS)
        self.pool.put(PoolQuery(query.insert_table_crawl_history, req.to_tuple(self.rowid)))
        i = 0
        while (300 <= req.status_code < 400) and i <= depth:
            if utility.same_fld(utility.get_fld(req.new_location), self.fld):
                req = request.get_request(req.new_location, redirects=globvar.ALLOW_REDIRECTS)
                self.pool.put(PoolQuery(query.insert_table_crawl_history, req.to_tuple(self.rowid)))
            else:
                # TODO: Log error message here.
                return None
            i +=1
        
        if 300 <= req.status_code < 400:
            return None
        else:
            return req

    def crawl(self):
        while len(self.extractor.urls) > 0:
            url = self.extractor.get_url()
            logging.info(f'{self.thread_id} | Crawling: {url}')

            req = self.send_request(url)
            if req != None:
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