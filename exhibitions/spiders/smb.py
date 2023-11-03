import scrapy
from exhibitions.items import ExhibitionsItem
from processing.db_check_utils import get_or_insert_organizer, host, database, user
import psycopg2

organizer_DETAILS = {
       "name": "Staatliche Museen zu Berlin",
       "city": "Berlin",
       "country": "Germany"
}

class SmbSpider(scrapy.Spider):
    name = "smb"
    allowed_domains = ["www.smb.museum"]
    start_urls = ["https://www.smb.museum/en/exhibitions/current/",
                  "https://www.smb.museum/en/exhibitions/preview/"
                  ]

    def __init__(self, *args, **kwargs):
        super(SmbSpider, self).__init__(*args, **kwargs)
        self.connection = psycopg2.connect(host=host, database=database, user=user)
    
    def parse(self, response):
        exhs = response.css('div.smbExhibitionsList')
        for exh in exhs:
        # Check if the text "Permanent exhibition" exists in the paragraph text
            if 'Permanent exhibition' in exh.css('p ::text').get(''):
                continue

            relative_url = exh.css('h4 a ::attr(href)').get()
            exh_url = 'https://www.smb.museum' + relative_url
            yield response.follow(exh_url, callback=self.pars_exh_page)

    
    def pars_exh_page(self, response):
        exh = response.css("div.col-md-8")
        exh_item = ExhibitionsItem()

        exh_item['url'] = response.url,

        relative_img = exh.css('picture.lazyloading source[data-srcset]::attr(data-srcset)').get()
        exh_item['img'] = 'https://www.smb.museum' + relative_img

        exh_item['title'] = exh.css('h2 ::text')[0].get(),

        try:
            exh_item['subtitle'] = exh.css('h2 ::text')[1].get(),
        except IndexError:
            exh_item['subtitle'] = None,

        exh_item['date_str'] = exh.css('p::text').get(),
        exh_item['venue'] = exh.css('a::text').get(),
        exh_item['organizer_id'] = get_or_insert_organizer(organizer_DETAILS, self.connection),
        exh_item['description'] = exh.css('p + div p::text').get(),

        yield exh_item

    def close(self, spider, reason):
        # Close the database connection when the spider is closed
        self.connection.close()