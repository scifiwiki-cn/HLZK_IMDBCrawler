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


class CelebrityStat(scrapy.Item):
    year = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    month = scrapy.Field()
    event = scrapy.Field()
    country = scrapy.Field()


class Book(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    original_title = scrapy.Field()
    link = scrapy.Field()
    cover_link = scrapy.Field()
    publisher = scrapy.Field()
    isbn = scrapy.Field()
    author = scrapy.Field()
    translator = scrapy.Field()
    producer = scrapy.Field()
    price = scrapy.Field()
    series = scrapy.Field()
    published_at = scrapy.Field()
    page = scrapy.Field()
    decoration = scrapy.Field()
    rating = scrapy.Field()
    rating_distribution = scrapy.Field()
    rater_count = scrapy.Field()
    short_review_count = scrapy.Field()
    long_review_count = scrapy.Field()
    has_previous_version = scrapy.Field()
    comments = scrapy.Field()
    reader_count = scrapy.Field()
