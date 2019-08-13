import requests
import sys
sys.path.append('crawler/')
sys.path.append('utility/')
sys.path.append('web/')
import crawler
import robot
import utility
import request
import extractor

print('program.py')

url = 'https://www.reddit.com/r/chess/comments/co2qg0/chess_event2019_gct_st_louis_rapid_blitz_is.json'
req = request.get_request('https://reddit.com/robots.txt')
robots = robot.Robots()
text = """
    user-agent: *
    Disallow: /*.json
"""
robots.parse_robots(req.text)
crawl = robots.can_crawl_url(url)
print(robots.rules)
print(crawl)