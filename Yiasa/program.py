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


def main():
    utility.setup_logging()
    url = 'jensenfilene.net'
    fld = utility.get_fld(url)
    print(crawler)
    p = pool.Pool('main.sql')
    setup_db = p.database.setup_database()
    print(setup_db)
    spider = crawler.Crawler(fld)
    spider.extractor.robots.rules["Disallow"].append("\S+/Partier/\S+")
    spider.extractor.robots.rules["Disallow"].append("/\S+.html")
    spider.extractor.robots.rules["Disallow"].append("/javascript")
    spider.extractor.robots.rules["Disallow"].append("\S+.cbv")
    spider.extractor.robots.rules["Disallow"].append("\S+2014")
    spider.start_crawling()
    
if __name__ == '__main__':
    main()