from bs4 import BeautifulSoup
import globvar
import utility
import sys
sys.path.append("/crawler")
import robot

class Urls:
    def __init__(self, fld):
        self.robots = robot.Robots()
        self.urls = set()
        self.emails = set()
        self.crawled_urls = set()
        self.new_fld = set()
        self.fld = fld
    
    def get_url(self):
        url = self.urls.pop()
        self.crawled_urls.add(url)
        return url

    def add_data(self, urls, emails):
        self.add_urls(urls)
        self.add_emails(emails)

    def add_emails(self, emails):
        if type(emails) == set:
            self.emails = self.emails.union(emails)
        elif type(emails) == str:
            self.emails.add(emails)
    
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
                if self.fld == fld:
                    if url not in self.crawled_urls and self.robots.can_crawl_url(url):
                        print(url)
                        self.add_urls(url)
                else:
                    self.new_fld.add(fld)
                    print(f'found new fld: {fld} | {len(self.new_fld)}')
            else:
                url = url if url.startswith('/') else f'/{url}'
                url = f'{globvar.scheme}{self.fld}{url}'
                if url not in self.crawled_urls and self.robots.can_crawl_url(url):
                    print(url)
                    self.add_urls(url)
    
    def __str__(self):
        return f'urls: {len(self.urls)}, emails: {len(self.emails)}'