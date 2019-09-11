import datetime
import requests
import sys
import threading
import time
sys.path.append('crawler/')
sys.path.append('utility/')
sys.path.append('web/')
sys.path.append('database/')
import globvar
import crawler
import robot
import utility
import request
import extractor
import logging
import pool
import query

p = pool.Pool('main.sql')

def main():
    utility.setup_logging()
    # p.database.setup_database()
    # dump()
    # test_full_fld_crawl()
    # multi_thread()

def multi_thread():
    t1 = threading.Thread(target=test_full_fld_crawl)
    t1.start()
    t2 = threading.Thread(target=test_full_fld_crawl2)
    t2.start()

    while True:
        print('lalala')
        print(f't1: {t1.is_alive()}')
        print(f't2: {t2.is_alive()}')
        time.sleep(1)

def dump():
    p.database.dump_database()

def test_full_fld_crawl2():
    url = 'google.com'
    fld = utility.get_fld(url)
    setup_db = p.database.setup_database()
    spider = crawler.Crawler(fld, p)
    spider.extractor.robots.rules["Disallow"].append("\S+/Partier/\S+")
    spider.extractor.robots.rules["Disallow"].append("/\S+.html")
    spider.extractor.robots.rules["Disallow"].append("/javascript")
    spider.extractor.robots.rules["Disallow"].append("\S+.cbv")
    spider.extractor.robots.rules["Disallow"].append("\S+2014")
    spider.extractor.robots.rules["Disallow"].append("\S+beta")
    print('Starting crawling')
    spider.start_crawling()

def test_full_fld_crawl():
    """ This is just a short website, that my bot can crawl through it's entirety fast,
        so I can use it as test """ 
    
    url = 'vg.no'
    fld = utility.get_fld(url)
    setup_db = p.database.setup_database()
    spider = crawler.Crawler(fld, p)
    spider.extractor.robots.rules["Disallow"].append("\S+/Partier/\S+")
    spider.extractor.robots.rules["Disallow"].append("/\S+.html")
    spider.extractor.robots.rules["Disallow"].append("/javascript")
    spider.extractor.robots.rules["Disallow"].append("\S+.cbv")
    spider.extractor.robots.rules["Disallow"].append("\S+2014")
    spider.extractor.robots.rules["Disallow"].append("\S+beta")
    print('Starting crawling')
    spider.start_crawling()

if __name__ == '__main__':
    main()