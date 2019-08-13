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
crawler.parse_robots()
print(crawler.robots.rules)