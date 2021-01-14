import scrapy
import requests
import json
from db import store_urls_extract
from price_check.items import PriceCheckItem
from scrapy.loader import ItemLoader


class GogspiderSpider(scrapy.Spider):
    name = 'gogspider'
    allowed_domains = ['www.gog.com']
    store = 'GOG'
    start_urls = store_urls_extract(store)

    def parse(self, response: scrapy.http.Request) -> None:
        r = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/dollar_info?json').text
        usd = json.loads(r)[0]['rate']
        loader = ItemLoader(PriceCheckItem())
        loader.add_value('url', response.url)
        price = round((float(response.css('.product-actions-price span::text').getall()[1])*usd))
        loader.add_value('price', price)
        print(price)
        print(usd)
        yield loader.load_item()
