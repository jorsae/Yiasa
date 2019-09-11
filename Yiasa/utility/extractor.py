from datetime import datetime
from bs4 import BeautifulSoup
import globvar
import utility
import sys
sys.path.append("/crawler")
sys.path.append("/database")
import robot
import query
from pq import PoolQuery

class Extractor:
    def __init__(self, fld, pool):
        self.robots = robot.Robots()
        self.urls = set()
        self.emails = set()
        self.crawled_urls = set()
        self.new_fld = set()
        self.fld = fld
        self.pool = pool
    
    def get_url(self):
        url = self.urls.pop()
        self.crawled_urls.add(url)
        # TODO: Add crawled_url to table 'crawl_history'
        return url

    def add_new_fld(self, fld):
        if fld == self.fld:
            return True
        if fld not in self.new_fld:
            self.pool.put(PoolQuery(query.insert_table_crawl_queue, (fld, 1, datetime.now())))
            self.new_fld.add(fld)
            return False

    def check_url(self, url):
        if url.startswith('http'):
            fld = utility.get_fld(url)
            same_fld = self.add_new_fld(fld)
            if same_fld:
                self.add_url(url)
        else:
            url = url if url.startswith('/') else f'/{url}'
            url = f'{globvar.scheme}{self.fld}{url}'
            self.add_url(url)
    
    def add_url(self, url):
        if url not in self.crawled_urls and self.robots.can_crawl_url(url):
            # TODO: Add to pool
            self.urls.add(url)
    
    def add_email(self, email):
        if email not in self.emails:
            self.emails.add(email)
            # TODO: put to pool queue

    def extract_urls(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a', href=True)]
        for url in urls:
            if url.startswith('mailto:'):
                self.add_email(url[7:])
                continue
            
            self.check_url(url)
    
    def __str__(self):
        return f'urls: {len(self.urls)}, emails: {len(self.emails)}'