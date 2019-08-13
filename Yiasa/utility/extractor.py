from bs4 import BeautifulSoup
import globvar

class Urls:
    def __init__(self):
        self.urls = set()
        self.emails = set()
    
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

    def __str__(self):
        return f'urls: {len(self.urls)}, emails: {len(self.emails)}'

def extract_urls(text, fld):
    valid_urls = set()
    valid_emails = set()
    soup = BeautifulSoup(text, 'html.parser')
    urls = [link.get('href') for link in soup.find_all('a', href=True)]
    for url in urls:
        if url.startswith('mailto:'):
            valid_emails.add(url[7:])
            continue

        if url.startswith('http') is False:
            url = url if url.startswith('/') else f'/{url}'
            url = f'{globvar.scheme}{fld}{url}'
            valid_urls.add(url)
        else:
            valid_urls.add(url)
    return valid_urls, valid_emails