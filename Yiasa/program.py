import sys
sys.path.append('crawler/')
sys.path.append('utility/')
import crawler
import utility

fld = utility.get_fld("https://github.com/jorsae/YiasaCrawler/blob/master/bot/spider.py")
crawler = crawler.Crawler(fld)
print(crawler)