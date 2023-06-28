# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YunnanItem(scrapy.Item):
    # define the fields for your item here like:
    tablename = scrapy.Field()
    guid = scrapy.Field()
    title = scrapy.Field()
    publishTime = scrapy.Field()
    content = scrapy.Field()
    pass
