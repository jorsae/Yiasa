import sys
sys.path.append('crawler/')
sys.path.append('utility/')
import crawler
import utility

crawler = crawler.Crawler()
print(crawler.creation_time)