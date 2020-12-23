import scrapy


class PricerSpider(scrapy.Spider):
    name = 'pricer'
    allowed_domains = ['steam']
    start_urls = ['http://steam/']

    def parse(self, response):
        pass
