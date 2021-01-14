# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from db import new_price

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PriceCheckPipeline:

    def process_item(self, item):
        new_price(item['price'][0], item['url'][0])
        return item
