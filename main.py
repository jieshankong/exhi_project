from scrapy.crawler import CrawlerProcess
from exhibitions.spiders.staedelmuseum import Spider2
...
from utils.notion_utils import push_to_notion

process = CrawlerProcess()

# Run spiders
process.crawl(Spider1)
process.crawl(Spider2)
...
process.start()

# Push data to Notion
push_to_notion()
