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
    url = 'google.com'
    fld = utility.get_fld(url)
    #spider = crawler.Crawler(fld)
    #spider.start_crawling()
    print(crawler)
    p = pool.Pool('main.sql')
    setup_db = p.database.setup_database()
    print(setup_db)
    
if __name__ == '__main__':
    main()