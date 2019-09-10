import requests
from datetime import datetime

class RequestResult(object):
    def __init__(self, url, text, elapsed_time, status_code, date, content_type, content_length, new_location):
        self.FLD_Id = None
        self.URLS_Id = None
        self.url = url
        self.text = text
        self.elapsed_time = elapsed_time
        self.status_code = status_code
        self.date = date
        self.content_type = content_type
        self.content_length = content_length if content_length != None else 0
        self.new_location = new_location
    
    @classmethod
    def by_request(cls, request, date):
        contentType = parse_headers(request.headers, 'Content-Length')
        contentLength = parse_headers(request.headers, 'Content-Type')
        new_location = parse_headers(request.headers, 'Location')
        return cls(request.url, request.text, request.elapsed, request.status_code, datetime.now(), contentType, contentLength, new_location)
    
    def to_tuple(self, rowid):
        return (rowid, self.url, self.elapsed_time.microseconds, self.status_code, self.date, self.content_type, self.content_length, )

    def __str__(self):
        return f'{self.url} {self.date} {self.elapsed_time.microseconds} | {self.status_code} {self.content_type} {self.content_length}'

def get_request(url, timeout=3, redirects=False):
    try:
        request = requests.get(url, timeout=timeout, allow_redirects=redirects)
    except requests.exceptions.Timeout as timeout:
        raise requests.exceptions.Timeout(f'{url} timed out')
    except Exception as e:
        raise Exception(e)
    
    contentType = parse_headers(request.headers, 'Content-Type')
    contentLength = parse_headers(request.headers, 'Content-Length')
    new_location = parse_headers(request.headers, 'Location')
    return RequestResult(request.url, request.text, request.elapsed, request.status_code, datetime.now(), contentType, contentLength, new_location)

def parse_headers(headers, value):
    try:
        return headers[value]
    except:
        return None