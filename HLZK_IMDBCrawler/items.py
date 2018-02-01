# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HlzkImdbcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SearchItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()
    douban = scrapy.Field()
    chtitle = scrapy.Field()
    douban_link = scrapy.Field()
    douban_rating = scrapy.Field()
    description = scrapy.Field()


class Celebrity(scrapy.Item):
    year = scrapy.Field()
    event = scrapy.Field()
    date = scrapy.Field()