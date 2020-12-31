# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PriceCheckItem(scrapy.Item):
    url = scrapy.Field()
    price = scrapy.Field()
