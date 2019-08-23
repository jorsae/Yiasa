import requests
from datetime import datetime

class RequestResult():
    def __init__(self, url, elapsed_time, status_code, date, content_type, content_length):
        self.FLD_Id = None
        self.URLS_Id = None
        self.url = url
        self.elapsed_time = elapsed_time
        self.status_code = status_code
        self.date = date
        self.content_type = content_type
        self.content_length = content_length
    
    def __str__(self):
        return f'{self.url} {self.date} {self.elapsed_time} | {self.status_code} {self.content_type} {self.content_length}'

def get_request(url, timeout=3, redirects=False):
    try:
        request = requests.get(url, timeout=timeout, allow_redirects=redirects)
    except requests.exceptions.Timeout as timeout:
        raise requests.exceptions.Timeout(f'{url} timed out')
    except Exception as e:
        raise Exception(e)
    
    contentType = parse_headers(request.headers, 'Content-Type')
    contentLength = parse_headers(request.headers, 'Content-Length')
    return RequestResult(request.url, request.elapsed, request.status_code, datetime.now(), contentType, contentLength)

def parse_headers(headers, value):
    try:
        return headers[value]
    except:
        return None