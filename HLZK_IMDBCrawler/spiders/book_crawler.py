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
    name = "book"
    allowed_domains = ["www.douban.com", "book.douban.com"]

    def __init__(self, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        # self.start_urls = ['https://www.douban.com/doulist/110601600']
        self.start_urls = ['https://www.douban.com/doulist/110601600/?start=25&sort=seq&playable=0&sub_type=']
        self.interval = 3
        option = webdriver.ChromeOptions()
        option.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.book_list = {}

    def destroy_browser(self):
        self.browser.quit()

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
                comments = {},
                title = self.strip(book.css("div.title>a::text").extract()[0]),
                link = link,
                rater_count = book.css("div.rating span:last-child::text").extract()[0].replace("(", "").replace("人评价)", "")
            )
            rating = book.css("div.rating span.rating_nums::text").extract()
            if len(rating) != 0 and len(self.strip(rating[0])) != 0:
                self.book_list[_id]["rating"] = rating[0]
            yield Request(self.book_list[_id]["link"], callback = self.parse_book)
            break
        # parse next page of doulist
        # next_page = response.css("span.next>a::attr(href)").extract()
        # if len(next_page) != 0:
        #     yield Request(next_page[0], callback = self.parse)

    def parse_book(self, response):
        book = self.book_list[self.strip_book_id(response.url)]

        # 基本信息
        info = self.strip(response.css("div#basic-info::text").extract()[0].encode(encoding = "utf-8")).split("linebreak")
        for property in info[:-1]:
            try:
                (key, value) = property.split(":")
                if key == "ISBN":
                    book["isbn"] = value
                if key == u"作者":
                    book["author"] = value
                if key == u"出版年":
                    book["published_at"] = value
                if key == u"页数":
                    book["page"] = value
                if key == u"定价":
                    book["price"] = value.replace("元", "")
                if key == u"装帧":
                    book["decoration"] = value
                if key == u"原作名":
                    book["original_title"] = value
                if key == u"丛书":
                    book["series"] = value
                if key == u"出品方":
                    book["producer"] = value
                if key == u"译者":
                    book["translator"] = value
                if key == u"副标题":
                    book["subtitle"] = value
            except:
                pass

        # 封面图片地址
        book["cover_link"] = response.css("#mainpic>a>img::attr(src)").extract()[0]

        # 评分分布
        rating_star = response.css("span.starstop::text").extract()
        rating_ratio = response.css("span.rating_per::text").extract()
        if len(rating_star) == 5:
            rating_distribution = {}
            for i in range(5):
                rating_distribution[self.strip(rating_star[i].replace("星", ""))] = rating_ratio[i]
            book["rating_distribution"] = rating_distribution

        # 详细短评（取得评分用户情况）
        rater_count = response.css(".rating_sum a[href='collections'] span::text").extract()
        if len(rater_count) != 0:
            book["rater_count"] = rater_count[0]
            yield Request("http://book.douban.com/subject/%s/comments" % book["id"], callback = self.parse_comment)
        # 详细长评（取得评分用户情况）

    def parse_comment(self, response):
        query = parse_qs(urlparse(url = response.url + "?p=2").query)
        book = self.book_list[self.strip_book_id(response.url)]
        comment_ids = response.css("#comments>ul>li::attr(data-cid)").extract()
        user_links = response.css("#comments>ul>li .comment .comment-info>a:first-child::attr(href)").extract()
        userids = [link.replace("https://www.douban.com/people/", "").replace("/", "") for link in user_links]
        stars = response.css("#comments>ul>li .comment .rating::attr(title)").extract()
        contents = response.css("#comments>ul>li .comment .comment-content .short::text").extract()
        for i in range(len(comment_ids)):
            pass

        #pagination
        next_page = response.css("ul.comment-paginator>li.p:last-child")
        if len(next_page.css("a.page-disabled").extract()) == 0:
            if "p" in query:
                yield Request("http://book.douban.com/subject/%s/comments?p=%d" % (book["id"], int(query["p"][0]) + 1), callback = self.parse_comment)
            else:
                yield Request("http://book.douban.com/subject/%s/comments?p=%d" % (book["id"], 2), callback = self.parse_comment)


    def parse_commenter(self, response):
        pass


    def execute_script(self):
        self.browser.execute_script("""
            $('br').before('<span>linebreak</span>');
            var text = $("#info").text();
            $('body').append($('<div id="basic-info">' + text + '</div>'));        
        """)



    def closed(self, reason):
        self.destroy_browser()
        self.save_result()
        print(reason)

    def save_result(self):
        print(self.book_list)
        pass