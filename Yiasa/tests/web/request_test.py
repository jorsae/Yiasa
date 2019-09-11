import pytest
import sys
sys.path.append("web/")
import request
import requests
from datetime import datetime


def test_get_request():
    req = request.get_request('https://www.google.com')
    assert(req.status_code) == 200

def test_get_request_requestresult():
    req = request.get_request('https://www.google.com')
    assert(type(req)) == request.RequestResult

def test_requestresult_by_request():
    r = requests.get('https://www.google.com')
    req = request.RequestResult.by_request(r, datetime.now())
    assert(type(req)) == request.RequestResult

def test_get_request_timed_out():
    url = "http://google.com"
    req = request.get_request(url, timeout=0.001)
    assert(req.status_code) == 0