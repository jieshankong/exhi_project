# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ExhibitionsItem(scrapy.Item):
    url = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    date_start = scrapy.Field()
    date_end = scrapy.Field()
    date_str = scrapy.Field()
    date = scrapy.Field()
    venue = scrapy.Field()
    organizer_id = scrapy.Field()
    description = scrapy.Field()