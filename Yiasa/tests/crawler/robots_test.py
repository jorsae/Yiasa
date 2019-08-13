import pytest
import sys
sys.path.append("web/")
sys.path.append("crawler/")
import request
import robot


testdata_test_parse_robots = [
    ('https://www.vg.no/robots.txt', {'Allow':[], 'Disallow':['/tegneserier/salesposter']}),
    ('https://www.reddit.com/robots.txt', {'Allow':['/partner_api/', '/', '/sitemaps/*.xml'], 'Disallow':['/*.json', '/*.json-compact', '/*.json-html', '/*.xml', '/*.rss', '/*.i', '/*.embed', '/*/comments/*?*sort=', '/r/*/comments/*/*/c*', '/comments/*/*/c*', '/r/*/submit$', '/r/*/submit/$', '/message/compose*', '/api', '/post', '/submit', '/goto', '/*after=', '/*before=', '/domain/*t=', '/login', '/r/*/user/', '/gold?']})
]

@pytest.mark.parametrize("url,expected", testdata_test_parse_robots)
def test_parse_robots(url, expected):
    req = request.get_request(url)
    robots = robot.Robots()
    robots.parse_robots(req.text)
    assert(robots.rules) == expected