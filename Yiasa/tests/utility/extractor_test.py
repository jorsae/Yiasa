import pytest
import requests
import sys
sys.path.append('utility/')
sys.path.append('web/')
import crawler
import utility
import request
import extractor

testdata_test_extractor_urls = [
    ('https://reddit.com', {'http://github.com/reddit/reddit/wiki/API'}, set()),
]

@pytest.mark.parametrize("url, expected_urls, expected_emails", testdata_test_extractor_urls)
def test_extractor_urls(url, expected_urls, expected_emails):
    fld = utility.get_fld(url)
    req = request.get_request(url)

    urls, emails = extractor.extract_urls(req.text, fld)
    assert(urls) == expected_urls
    assert(emails) == expected_emails