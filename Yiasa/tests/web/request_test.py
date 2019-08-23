import pytest
import sys
sys.path.append("web/")
import request
import requests


def test_get_request():
    req = request.get_request('https://www.google.com')
    assert(req.status_code) == 200

def test_get_request_requestresult():
    req = request.get_request('https://www.google.com')
    assert(type(req)) == request.RequestResult

def test_get_request_timed_out():
    url = "http://google.com"
    with pytest.raises(requests.exceptions.Timeout) as excinfo:
        req = request.get_request(url, timeout=0.001)
    excinfo.match(f'{url} timed out')