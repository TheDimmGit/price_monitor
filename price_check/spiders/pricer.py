import scrapy
from db import urls_extract
from price_check.items import PriceCheckItem
from scrapy.loader import ItemLoader


class PricerSpider(scrapy.Spider):
    name = 'pricer'
    allowed_domains = ['https://store.steampowered.com/']
    start_urls = urls_extract()

    def parse(self, response):
        loader = ItemLoader(PriceCheckItem())
        loader.add_value('url', response.url)
        price = response.css('.discount_final_price::text').get().replace('₴', '')
        loader.add_value('price', price)
        yield loader.load_item()
