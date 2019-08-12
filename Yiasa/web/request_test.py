import pytest
import request

def test_answer():
    a = request.get_request('http://google.com')
    assert(a.status_code) == 200