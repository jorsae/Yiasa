import pytest
import requests
import sys
import os
sys.path.append('utility/')
sys.path.append('web/')
sys.path.append('database/')
import crawler
import utility
import request
import extractor
import pool

dbFile = 'tests/utility/pytest_extractor.sql'
p = pool.Pool(db_file=dbFile)
ext = None
urls = None
data = ''

@pytest.fixture(scope='function', autouse=True)
def read_file(request):
    global data, urls, ext
    ext = extractor.Extractor('fld.com', p)
    p.database.setup_database()
    p.disable_processing = True
    urls = {'https://fld.com/arg',
                'http://fld.com/pancake/wut',
                'https://fld.com/pancake/wut'
                }
    with open('tests/utility/extractor_test_website.html') as f:
        data = f.read()

def test_emails():
    ext.extract_urls(data)
    assert(ext.emails) == {'asdaspoap@gmail.com'}

def test_urls():
    ext.extract_urls(data)
    assert(ext.urls) == urls

def test_urls_pop():
    urls.pop()

    ext.extract_urls(data)
    ext.get_url()
    assert(ext.urls) == urls

def test_crawled_urls():
    url = urls.pop()

    ext.extract_urls(data)
    ext.get_url()
    assert(ext.crawled_urls) == {url}

def test_duplicate_new_fld():
    expected = {'wikileaksorwhatever.com', 'antibiotics.com'}
    ext.extract_urls(data)
    ext.extract_urls(data)
    assert(ext.new_fld) == expected