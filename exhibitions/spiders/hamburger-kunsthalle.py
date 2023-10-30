import scrapy
from exhibitions.items import ExhibitionsItem
from processing.db_check_utils import get_or_insert_organizer, host, database, user
import psycopg2

organizer_DETAILS = {
       "name": "Hamburger Kunsthalle",
       "city": "Hamburg",
       "country": "Germany"
}

class HamburgerkunsthalleSpider(scrapy.Spider):
    name = "hamburger-kunsthalle"
    allowed_domains = ["www.hamburger-kunsthalle.de"]
    start_urls = [
    "https://www.hamburger-kunsthalle.de/en/exhibitions/latest",
    "https://www.hamburger-kunsthalle.de/en/press/exhibitions/upcoming"
    ]

    def __init__(self, *args, **kwargs):
        super(HamburgerkunsthalleSpider, self).__init__(*args, **kwargs)
        self.connection = psycopg2.connect(host=host, database=database, user=user)

    def parse(self, response):
        exhs = response.css('div.teaser')
        for exh in exhs:
            relative_url = exh.css('a ::attr(href)').get()
            exh_url = 'https://www.hamburger-kunsthalle.de/' + relative_url
            yield response.follow(exh_url, callback=self.pars_exh_page)
    
    def pars_exh_page(self, response):
        exh = response.css("div.main-col")
        exh_item = ExhibitionsItem()

        exh_item['url'] = response.url,
        exh_item['title'] = exh.css('h1::text').get(),
        exh_item['subtitle'] = exh.css('div.title-suffix::text').get(),
        exh_item['date_start'] = response.css('time[itemprop="startDate"]::attr(datetime)').get(),
        exh_item['date_end'] = response.css('time[itemprop="endDate"]::attr(datetime)').get(),
        exh_item['venue'] = response.css('dt:contains("Venue") + dd::text').get(),
        exh_item['organizer_id'] = get_or_insert_organizer(organizer_DETAILS, self.connection),
        exh_item['description'] = ' '.join(exh.css("p::text").extract()).strip()

        yield exh_item

    def close(self, spider, reason):
        # Close the database connection when the spider is closed
        self.connection.close()