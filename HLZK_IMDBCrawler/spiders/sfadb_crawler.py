# coding=utf-8
import codecs
# from urllib.parse import urlparse

import scrapy
import datetime
import csv

from scrapy import Request
from selenium import webdriver
from urlparse import urlparse, parse_qs
from HLZK_IMDBCrawler.items import Celebrity, Book
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class BookSpider(scrapy.Spider):
    name = "sfadb"
    allowed_domains = ["www.sfadb.com"]

    def __init__(self, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        self.base_url = "http://www.sfadb.com"
        self.start_urls = ['']
        self.interval = 3
        option = webdriver.ChromeOptions()
        option.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.award_list = {}

    def strip(self, string):
        return string.replace(" ", "").replace("\t", "").replace("\n", "")

    def parse_year(self, response):
        years_link = response.css("#menunav a::attr(href)").extract()
        years = response.css("#menunav a::text").extract()
        result = []
        for i in range(len(years)):
            result.append({
                "year": self.strip(years[i]),
                "link": self.base_url + "/" + years_link[i]
            })
        return result

    def parse(self, response):
        years = self.parse_year(response)
        for item in years:
            self.award_list[item["year"]] = {}
            yield Request(item["link"], callback = self.parse_year)

    def parse_year(self, response):
        pass

    def closed(self, reason):
        self.destroy_browser()
        self.save_result()
        print(reason)

    def destroy_browser(self):
        self.browser.quit()

    def save_result(self):
        pass