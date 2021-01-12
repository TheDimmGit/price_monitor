import scrapy
from db import urls_extract
from price_check.items import PriceCheckItem
from scrapy.loader import ItemLoader
from scrapy.selector import Selector


class PricerSpider(scrapy.Spider):
    name = 'steamspider'
    allowed_domains = ['store.steampowered.com']
    store = 'Steam'
    start_urls = urls_extract(store)

    def parse(self, response):
        loader = ItemLoader(PriceCheckItem())
        loader.add_value('url', response.url)
        price_1 = response.css('.game_purchase_action').get()
        price_2 = price_1 if 'Add to Cart' in price_1 else response.css('.game_purchase_action').getall()[1]
        price_field = Selector(text=price_2)
        price = price_field.css('.game_purchase_price::text').get()
        if not price:
            price = price_field.css('.discount_final_price::text').get()
        print(price)
        loader.add_value('price', price.replace('₴', ''))
        yield loader.load_item()
