import pytest
import sys
sys.path.append("web/")
import request

def test_answer():
    req = request.get_request('http://google.com')
    assert(req.status_code) == 200