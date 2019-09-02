from bs4 import BeautifulSoup
import globvar

class Urls:
    def __init__(self):
        self.urls = set()
        self.emails = set()
        self.crawled_urls = set()
        # TODO: Maybe store fld here, so you don't have to pass it in extract_urls
    
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

    def extract_urls(self, text, fld):
        soup = BeautifulSoup(text, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a', href=True)]
        for url in urls:
            if url.startswith('mailto:'):
                self.add_emails(url[7:])
                continue

            if url.startswith('http') is False:
                url = url if url.startswith('/') else f'/{url}'
                url = f'{globvar.scheme}{fld}{url}'
                if url not in self.crawled_urls:
                    self.add_urls(url)
            else:
                if url not in self.crawled_urls:
                    self.add_urls(url)
    
    def __str__(self):
        return f'urls: {len(self.urls)}, emails: {len(self.emails)}'