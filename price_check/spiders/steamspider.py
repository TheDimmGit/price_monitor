import scrapy
from db import store_urls_extract
from price_check.items import PriceCheckItem
from scrapy.loader import ItemLoader
from scrapy.selector import Selector


class PricerSpider(scrapy.Spider):
    name = 'steam'
    allowed_domains = ['store.steampowered.com']
    store = 'Steam'
    start_urls = store_urls_extract(store)

    def parse(self, response: scrapy.http.Request) -> None:
        loader = ItemLoader(PriceCheckItem())
        loader.add_value('url', response.url)
        price_1 = response.css('.game_purchase_action').get()
        lst = (response.css('.game_purchase_action span::text').getall())
        final_price = 0
        if 'Add to Cart' in lst:
            if lst[0] == 'Add to Cart':
                price_field = response.css('.game_purchase_action')
            elif lst[1] == 'Add to Cart':
                price_field = response.css('.game_purchase_action').getall()[1]
                price_field = Selector(text=price_field)
            else:
                price_field = None
            price = price_field.css('.game_purchase_price::text').get()
            if not price:
                price = price_field.css('.discount_final_price::text').get()
            final_price = int(''.join([i for i in price if i.isdigit()]))
        elif lst[0] == 'Play Game':
            final_price = 0

        loader.add_value('price', final_price)
        yield loader.load_item()
