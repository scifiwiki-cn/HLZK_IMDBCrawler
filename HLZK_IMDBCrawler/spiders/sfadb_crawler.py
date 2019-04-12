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


class SfadbSpider(scrapy.Spider):
    name = "sfadb"
    allowed_domains = ["www.sfadb.com"]

    def __init__(self, *args, **kwargs):
        super(SfadbSpider, self).__init__(*args, **kwargs)
        self.base_url = "http://www.sfadb.com"
        self.start_urls = ['http://www.sfadb.com/Hugo_Awards_2019']
        self.interval = 3
        option = webdriver.ChromeOptions()
        option.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.award_list = {}

    def strip(self, string):
        return string.replace(" ", "").replace("\t", "").replace("\n", "")

    def parse(self, response):

        years_link = response.css("#menunav a::attr(href)").extract()
        _years = response.css("#menunav a::text").extract()
        years = []
        for i in range(len(_years)):
            years.append({
                "year": self.strip(_years[i]),
                "link": self.base_url + "/" + years_link[i]
            })
        for item in years:
            self.award_list[item["year"]] = {}
            yield Request(item["link"], callback = self.parse_year)
            break

    def parse_year(self, response):
        year_data = self.award_list[response.url[-4:]]
        categories = response.css(".categoryblock")
        for category in categories:
            if len(category.css(".category::text").extract()) != 0:
                cname = self.strip(category.css(".category::text").extract()[0])
            else:
                cname = self.strip(category.css(".category > span::text").extract()[0])
            if cname not in year_data:
                year_data[cname] = []
            item_containers = category.css('ul>li')
            for item_container in item_containers:
                year_data[cname].append("".join(item_container.css("::text").extract()))
        pass

    def closed(self, reason):
        self.destroy_browser()
        self.save_result()
        print(reason)

    def destroy_browser(self):
        self.browser.quit()

    def save_result(self):
        category_data = self.year2category()
        pass

    def year2category(self):
        category_data = {}
        for year in self.award_list:
            for category in self.award_list[year]:
                if category not in category_data:
                    category_data[category] = {}
                category_data[category][year] = self.award_list[year][category]
        return category_data