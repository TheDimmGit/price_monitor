import scrapy
from db import urls_extract
from price_check.items import PriceCheckItem
from scrapy.loader import ItemLoader
from scrapy.selector import Selector


class GogspiderSpider(scrapy.Spider):
    name = 'gogspider'
    allowed_domains = ['www.gog.com']
    store = 'GOG'
    start_urls = urls_extract(store)

    def parse(self, response):
        loader = ItemLoader(PriceCheckItem())
        loader.add_value('url', response.url)
        price = response.css('.product-actions-price span::text').get()
        loader.add_value('price', price)
        print(price)
        yield loader.load_item()