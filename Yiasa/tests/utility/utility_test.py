import pytest
import sys
sys.path.append("utility/")
import utility

testdata_test_get_fld = [
    ("http://google.com", "google.com"),
    ("google.com", "google.com"),
    ("http://foo.bar?haha/whatever", "foo.bar"),
    ("https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url", "stackoverflow.com"),
    ("", "")
]
@pytest.mark.parametrize("url, expected", testdata_test_get_fld)
def test_get_fld(url, expected):
    fld = utility.get_fld(url)
    assert(fld) == expected