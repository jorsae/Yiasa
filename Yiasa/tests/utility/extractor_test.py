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
    ('http://wikileaksorwhatever.com/', {'www.hbo.com'}, set()),
]

@pytest.mark.parametrize("url, expected_urls, expected_emails", testdata_test_extractor_urls)
def test_extractor_urls(url, expected_urls, expected_emails):
    fld = utility.get_fld(url)
    req = request.get_request(url)

    ext = extractor.Extractor(fld)

    ext.extract_urls(req.text)
    assert(ext.new_fld) == expected_urls
    assert(ext.emails) == expected_emails

def test_urls_add_duplicate_urls():
    testdata = {'https://reddit.com'}
    fld = utility.get_fld('https://reddit.com')

    ext = extractor.Extractor(fld)
    ext.add_urls(testdata)
    ext.add_urls(testdata)
    assert(ext.urls) == testdata

def test_urls_add_multiple_sets():
    testdata1 = {'https://reddit.com', 'https://google.com'}
    testdata2 = {'https://amazon.com', 'https://youtube.com'}
    expected = {'https://reddit.com', 'https://google.com', 'https://amazon.com', 'https://youtube.com', 'https://google.com.au'}

    urls = extractor.Extractor("")
    urls.add_urls(testdata1)
    urls.add_urls(testdata2)
    urls.add_urls('https://google.com.au')
    assert(urls.urls) == expected

def test_emails_add_duplicate_emails():
    testdata = {'test@example.com'}
    urls = extractor.Extractor("")
    urls.add_emails(testdata)
    urls.add_emails(testdata)
    assert(urls.emails) == testdata

def test_emails_add_multiple_sets():
    testdata1 = {'test@example.com', 'wormslayer@gmail.com'}
    testdata2 = {'barb@house.com.au', 'arrrrrg@hotmail.no'}
    expected = {'test@example.com', 'wormslayer@gmail.com', 'barb@house.com.au', 'arrrrrg@hotmail.no', 'citron@co.uk'}

    urls = extractor.Extractor("")
    urls.add_emails(testdata1)
    urls.add_emails(testdata2)
    urls.add_emails('citron@co.uk')
    assert(urls.emails) == expected