# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EthereumItem(scrapy.Item):
    Source = scrapy.Field()
    Pair = scrapy.Field()
    Price = scrapy.Field()
    Volume = scrapy.Field()
    Confidence = scrapy.Field()
    Updated = scrapy.Field()
    pass
