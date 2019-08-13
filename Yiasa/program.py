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

fld = utility.get_fld("https://github.com/jorsae/YiasaCrawler/blob/master/bot/spider.py")
#crawler = crawler.Crawler(fld)
#print(crawler)
#crawler.parse_robots()
#print(crawler.robots.rules)

fld = utility.get_fld(url)
req = request.get_request(url)
urls, emails = extractor.extract_urls(req.text, fld)
print(urls)