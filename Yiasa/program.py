import requests
import sys
sys.path.append('crawler/')
sys.path.append('utility/')
sys.path.append('web/')
sys.path.append('database/')
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
    dump()
    #test_full_fld_crawl()

def dump():
    p.database.dump_database()

def test_full_fld_crawl():
    """ This is just a short website, that my bot can crawl through it's entirety fast,
        so I can use it as test """ 
    
    url = 'jensenfilene.net'
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