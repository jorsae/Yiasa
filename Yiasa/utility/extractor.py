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
        return url

    def add_new_fld(self, fld):
        if fld not in self.new_fld:
            self.pool.put(PoolQuery(1, query.insert_table_crawl_queue, (fld, 1, datetime.now())))
            self.new_fld.add(fld)

    def add_urls(self, urls):
        if type(urls) == set:
            self.urls = self.urls.union(urls)
        elif type(urls) == str:
            self.urls.add(urls)

    def extract_urls(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a', href=True)]
        for url in urls:
            if url.startswith('mailto:'):
                self.add_emails(url[7:])
                continue
            
            if url.startswith('http'):
                fld = utility.get_fld(url)
                if fld == self.fld:
                    if url not in self.crawled_urls and self.robots.can_crawl_url(url):
                        self.add_urls(url)
                else:
                    self.add_new_fld(fld)
            else:
                url = url if url.startswith('/') else f'/{url}'
                url = f'{globvar.scheme}{self.fld}{url}'
                if url not in self.crawled_urls and self.robots.can_crawl_url(url):
                    self.add_urls(url)
    
    def __str__(self):
        return f'urls: {len(self.urls)}, emails: {len(self.emails)}'