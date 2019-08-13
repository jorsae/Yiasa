import requests
import sys
sys.path.append('crawler/')
sys.path.append('utility/')
sys.path.append('web/')
import crawler
import robot
import utility
import request

fld = utility.get_fld("https://github.com/jorsae/YiasaCrawler/blob/master/bot/spider.py")
crawler = crawler.Crawler(fld)
print(crawler)
try:
    req = request.get_request("http://google.com", timeout=0.001)
except requests.exceptions.Timeout as e:
    print(f'Timeout: {e}')


req = request.get_request('http://vg.no/robots.txt')
req = request.get_request('https://www.reddit.com/robots.txt')
robots = robot.Robots()
robots.parse_robots(req.text)
print(robots.rules)