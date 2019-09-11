import pytest
import requests
import sys
sys.path.append("web/")
sys.path.append("crawler/")
sys.path.append("utility/")
import request
import robot


testdata_test_parse_robots = [
    ('https://www.vg.no/robots.txt', {'Allow':[], 'Disallow':['/tegneserier/salesposter']}),
    ('https://www.reddit.com/robots.txt', {'Allow': ['/partner_api/', '/', '/sitemaps/\\S+\\.xml'], 'Disallow': ['/\\S+\\.json', '/\\S+\\.json-compact', '/\\S+\\.json-html', '/\\S+\\.xml', '/\\S+\\.rss', '/\\S+\\.i', '/\\S+\\.embed', '/\\S+/comments/\\S+\\?\\S+sort=', '/r/\\S+/comments/\\S+/\\S+/c\\S+', '/comments/\\S+/\\S+/c\\S+', '/r/\\S+/submit\\$', '/r/\\S+/submit/\\$', '/message/compose\\S+', '/api', '/post', '/submit', '/goto', '/\\S+after=', '/\\S+before=', '/domain/\\S+t=', '/login', '/r/\\S+/user/', '/gold\\?']}),
    ('', {'Allow':[], 'Disallow':[]}),
    ('https://valleymap.xyz/robots.txt', {'Allow':[], 'Disallow':[]}),
]

@pytest.mark.parametrize("url,expected", testdata_test_parse_robots)
def test_parse_robots(url, expected):
    robots = robot.Robots()
    try:
        req = request.get_request(url)
        robots.parse_robots(req.text)
    except:
        pass
    assert(robots.rules) == expected

testdata_test_can_crawl = [
    ('https://www.reddit.com/r/chess/comments/co2qg0/chess_event2019_gct_st_louis_rapid_blitz_is.json', False),
    ('https://www.reddit.com/r/chess/pan+?^$?cake/co2qg0/chess_event2019_gct_st_louis_rapid_blitz_is.json', False),
    ('https://www.reddit.com/r/chess/comments/co2qg0/chess_event2019_gct_st_louis_rapid_blitz_is', True),
    ('https://www.reddit.com/r/chess/wits/co2qg0/chess_event2019_gct_st_louis_rapid_blitz_is', True)
]
@pytest.mark.parametrize("url, expected", testdata_test_can_crawl)
def test_can_crawl(url, expected):
    robots = robot.Robots()
    text = """
User-Agent: *
Disallow: /*.json
Disallow: /pan+?^$?cake/*
Disallow: /*.json-html
Disallow: /wits/*.xml
Disallow: /*.rss
    """
    robots.parse_robots(text)
    assert robots.can_crawl_url(url) == expected

def test_can_crawl_nothing():
    robots = robot.Robots()
    text = """
User-Agent: *
Disallow: /
"""
    robots.parse_robots(text)
    assert robots.can_crawl_url('reddit.com/r/asd') == False