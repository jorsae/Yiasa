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
import logging

utility.setup_logging()

print('program.py')
logging.info('asd')

url = 'asdasdasdasd.com'
fld = utility.get_fld(url)
spider = crawler.Crawler(fld)
spider.start_crawling()
print(crawler)