import pytest
import sys
sys.path.append("web/")
sys.path.append("crawler/")
import request
import robot


testdata_test_parse_robots = [
    ('https://www.vg.no/robots.txt', {'Allow':[], 'Disallow':['/tegneserier/salesposter']})
]

@pytest.mark.parametrize("url,expected", testdata_test_parse_robots)
def test_parse_robots(url, expected):
    req = request.get_request(url)
    robots = robot.Robots()
    robots.parse_robots(req.text)
    assert(robots.rules) == expected