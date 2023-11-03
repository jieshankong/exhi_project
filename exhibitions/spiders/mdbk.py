import scrapy
from exhibitions.items import ExhibitionsItem
from processing.db_check_utils import get_or_insert_organizer, host, database, user
import psycopg2

organizer_DETAILS = {
       "name": "Museum der bildenden Künste Leipzig",
       "city": "Leipzig",
       "country": "Germany"
}

class MdbkSpider(scrapy.Spider):
    name = "mdbk"
    allowed_domains = ["mdbk.de"]
    start_urls = [
    "https://mdbk.de/en/exhibitions/"
    ]

    def __init__(self, *args, **kwargs):
        super(MdbkSpider, self).__init__(*args, **kwargs)
        self.connection = psycopg2.connect(host=host, database=database, user=user)

    def parse(self, response):
        exhs = response.css('article.exhibition-preview.exhibition-preview--upcoming')
        for exh in exhs:
            relative_url = exh.css('a ::attr(href)').get()
            exh_url = 'https://mdbk.de/' + relative_url
            yield response.follow(exh_url, callback=self.pars_exh_page)
    
    def pars_exh_page(self, response):
        exh = response.css("div.exhibition-detail__info")
        exh_item = ExhibitionsItem()

        exh_item['url'] = response.url

        img_srcset = response.css('img::attr(data-srcset)').get()
        if img_srcset:
            # Handle case where srcset might not be in the expected format
            try:
                img_600 = img_srcset.split(',')[1].split()[0].strip()
                exh_item['img'] = 'https://mdbk.de' + img_600
            except IndexError:
                exh_item['img'] = None

        exh_item['title'] = exh.css("h3::text").get()

        try:
            exh_item['subtitle'] = exh.css("h4.exhibition-detail__subheading ::text").get(),
        except IndexError:
            exh_item['subtitle'] = None,

        exh_item['date_str'] = exh.css("h4.exhibition-detail__date ::text").get(),
        exh_item['venue'] = None,
        exh_item['organizer_id'] = get_or_insert_organizer(organizer_DETAILS, self.connection),

        try:
            text = response.css('div.exhibition-detail__text.text-with-slideshow__text.content-block')
            exh_item['description'] = ' '.join(text.css("p::text").extract()).strip(),
        except IndexError:
            exh_item['description'] = None,
        
        yield exh_item

    def close(self, spider, reason):
        # Close the database connection when the spider is closed
        self.connection.close()


# https://mdbk.de/site/assets/files/4244/g_2356_mdbk_2019_00013331_2_web.600x0.1695892087.jpg
# <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" data-srcset="/site/assets/files/4244/g_2356_mdbk_2019_00013331_2_web.300x0.1695892086.jpg 300w, /site/assets/files/4244/g_2356_mdbk_2019_00013331_2_web.600x0.1695892087.jpg 414w" width="300" height="507" alt="Werner Tübke, Remembrance of Sicily, 1974, Museum of Fine Arts Leipzig" class="lazyautosizes lazyloaded" data-sizes="auto" sizes="434px" srcset="/site/assets/files/4244/g_2356_mdbk_2019_00013331_2_web.300x0.1695892086.jpg 300w, /site/assets/files/4244/g_2356_mdbk_2019_00013331_2_web.600x0.1695892087.jpg 414w" style="width: 434px; height: 734px;">