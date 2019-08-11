import pytest
import rr

def test_answer():
    a = rr.get_request('http://google.com')
    assert(a.status_code) == 200