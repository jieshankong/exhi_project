import scrapy
from exhibitions.items import ExhibitionsItem
from processing.db_check_utils import get_or_insert_organizer, host, database, user
import psycopg2

organizer_DETAILS = {
       "name": "Städel Museum",
       "city": "Frankfurt am Main",
       "country": "Germany"
}

class StaedelmuseumSpider(scrapy.Spider):
    name = "staedelmuseum"
    allowed_domains = ["www.staedelmuseum.de"]
    start_urls = ["https://www.staedelmuseum.de"]

    def __init__(self, *args, **kwargs):
        super(StaedelmuseumSpider, self).__init__(*args, **kwargs)
        self.connection = psycopg2.connect(host=host, database=database, user=user)

    def parse(self, response):
        exh_urls = response.css('li.stScroller__item.exhibitions a:not([href*="permanent"])::attr(href)').extract()
        for exh_url in exh_urls:
            yield response.follow(exh_url, callback=self.pars_exh_page)
    
    def pars_exh_page(self, response):
        exh_item = ExhibitionsItem()
        exh_item['url'] = response.url,
        
        title_parts = response.css('h1::text').getall()
        exh_item['title'] = ' '.join(part.strip() for part in title_parts),

        try:
            exh_item['subtitle'] = response.css('h1 span::text').get(),
        except IndexError:
            exh_item['subtitle'] = None,
        
        exh_item['date_str'] = response.css('h1 + p::text').get()
        exh_item['venue'] = None
        exh_item['organizer_id'] = get_or_insert_organizer(organizer_DETAILS, self.connection),
        
        if response.css('p.lead::text').get() == None:
            exh_item['description'] = response.css('div.stTypo p::text').get()
        else:
            exh_item['description'] = response.css('p.lead::text').get()
        
        yield exh_item
    
    def close(self, spider, reason):
        self.connection.close()