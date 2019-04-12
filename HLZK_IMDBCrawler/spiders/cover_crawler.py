# coding=utf-8
import codecs
import csv
import datetime
import sys
import requests
import scrapy
from dateutil.parser import *
from scrapy import Request
from selenium import webdriver

from HLZK_IMDBCrawler.items import Book

# from urllib.parse import urlparse
reload(sys)
sys.setdefaultencoding('utf8')


class BookSpider(scrapy.Spider):
    name = "cover"
    allowed_domains = ["www.douban.com", "book.douban.com"]

    def __init__(self, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.douban.com/doulist/110601600']
        self.interval = 3
        option = webdriver.ChromeOptions()
        option.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.book_list = {}
        self.standard_time = datetime.datetime(year = 2018, month = 4, day = 1, hour = 0, minute = 0, second = 0)

    def destroy_browser(self):
        self.browser.quit()

    def compare_publish_time(self, time):
        book_time = parse(time, default = datetime.datetime.now().replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0))
        print(book_time)
        return book_time >= self.standard_time

    def strip(self, string):
        return string.replace(" ", "").replace("\t", "").replace("\n", "")

    def strip_book_id(self, url):
        return url.replace("https://book.douban.com/subject/", "").replace("http://book.douban.com/subject/", "").replace("/comments", "").replace("/", "")

    def parse(self, response):
        books = response.css("div.doulist-item")
        for book in books:
            link = book.css("div.title>a::attr(href)").extract()[0]
            _id = self.strip_book_id(link)
            self.book_list[_id] = Book(
                id = _id,
                title = self.strip(book.css("div.title>a::text").extract()[0]),
                link = link,
                cover_link = book.css("div.post img::attr(src)").extract()[0]
            )
            info = book.css("div.abstract::text").extract()
            for item in info:
                try:
                    (key, value) = self.strip(item).split(":")
                    if key == "ISBN":
                        self.book_list[_id]["isbn"] = value
                    if key == u"作者":
                        self.book_list[_id]["author"] = value
                    if key == u"出版年":
                        self.book_list[_id]["published_at"] = value
                    if key == u"出版社":
                        self.book_list[_id]["publisher"] = value
                    if key == u"页数":
                        self.book_list[_id]["page"] = value
                    if key == u"定价":
                        self.book_list[_id]["price"] = value.replace("元", "")
                    if key == u"装帧":
                        self.book_list[_id]["decoration"] = value
                    if key == u"原作名":
                        self.book_list[_id]["original_title"] = value
                    if key == u"丛书":
                        self.book_list[_id]["series"] = value
                    if key == u"出品方":
                        self.book_list[_id]["producer"] = value
                    if key == u"译者":
                        self.book_list[_id]["translator"] = value
                    if key == u"副标题":
                        self.book_list[_id]["subtitle"] = value
                except:
                    pass
            if "published_at" in self.book_list[_id] and not self.compare_publish_time(self.book_list[_id]["published_at"]):
                self.book_list.pop(_id)

        # parse next page of doulist
        next_page = response.css("span.next>a::attr(href)").extract()
        if len(next_page) != 0:
            yield Request(next_page[0], callback = self.parse)


    def execute_script(self):
        self.browser.execute_script("""
            $('#info br').before('<span>linebreak</span>');
            var text = $("#info").text();
            $('body').append($('<div id="basic-info">' + text + '</div>'));        
        """)

    def closed(self, reason):
        self.destroy_browser()
        self.save_result()
        print(reason)

    def save_result(self):
        with open('books.csv', 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            fieldnames = ["id", "title", "cover_link", "publisher", "author", "published_at"]
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for key in self.book_list:
                item = self.book_list[key]
                _item = {}
                for field in fieldnames:
                    if field in item:
                        _item[field] = item[field]
                    else:
                        _item[field] = ""
                writer.writerow(_item)
                import time
                time.sleep(1)
                with open("covers/" + _item["id"] + ".jpg", "wb") as f:
                    img_data = requests.get(_item["cover_link"]).content
                    f.write(img_data)
                    f.close()
            csvfile.close()
