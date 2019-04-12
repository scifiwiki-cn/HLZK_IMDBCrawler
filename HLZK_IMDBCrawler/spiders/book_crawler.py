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
        self.start_urls = ['https://www.douban.com/doulist/110601600']
        # self.start_urls = ['https://www.douban.com/doulist/110601600/?start=25&sort=seq&playable=0&sub_type=']
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
            # break
        # parse next page of doulist
        next_page = response.css("span.next>a::attr(href)").extract()
        if len(next_page) != 0:
            yield Request(next_page[0], callback = self.parse)

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
                if key == u"出版社":
                    book["publisher"] = value
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

        readers_count = response.css("#collector p.pl>a::text").extract()
        book["reader_count"] = sum([int(item.replace("人想读", "").replace("人在读", "").replace("人读过", "")) for item in readers_count])

        # yield Request("http://book.douban.com/subject/%s/comments" % book["id"], callback = self.parse_comment)
        # 详细长评（取得评分用户情况）

    def parse_comment(self, response):
        querystring = urlparse(url = response.url).query
        query = parse_qs(querystring)
        book = self.book_list[self.strip_book_id(response.url.replace("?" + querystring, ""))]
        star_map = {u"力荐": 5, u"推荐": 4, u"还行": 3, u"较差": 2, u"很差": 1}
        comments = response.css("#comments>ul>li")
        comment_ids = response.css("#comments>ul>li::attr(data-cid)").extract()
        user_links = response.css("#comments>ul>li .comment .comment-info>a:first-child::attr(href)").extract()
        userids = [link.replace("https://www.douban.com/people/", "").replace("/", "") for link in user_links]
        contents = response.css("#comments>ul>li .comment .comment-content .short::text").extract()
        for i in range(len(comment_ids)):
            book["comments"][userids[i]] = {
                "userid": userids[i],
                "content": contents[i],
                "userinfo": {}
            }
            star = comments[i].css(".comment .rating::attr(title)").extract()
            if len(star) != 0:
                book["comments"][userids[i]]["star"] = star_map[star[0]]
            yield Request("https://www.douban.com/people/%s?bid=%s&uid=%s" % (userids[i], book["id"], userids[i]), callback = self.parse_commenter)
        #pagination
        next_page = response.css("ul.comment-paginator>li.p:last-child")
        if len(next_page.extract()) != 0 and len(next_page.css("a.page-disabled").extract()) == 0:
            if "p" in query:
                yield Request("http://book.douban.com/subject/%s/comments?p=%d" % (book["id"], int(query["p"][0]) + 1), callback = self.parse_comment)
            else:
                yield Request("http://book.douban.com/subject/%s/comments?p=%d" % (book["id"], 2), callback = self.parse_comment)


    def parse_commenter(self, response):
        querystring = urlparse(url = response.url).query
        query = parse_qs(querystring)
        userinfo = self.book_list[query["bid"]]["comment"][query["pid"]]["userinfo"]

        dramastat = response.css("#drama span.pl>a::text").extract()

        for stat in dramastat:
            userinfo["drama"] = {}
            if stat.find("部想看") != -1:
                userinfo["drama"]["want"] = self.strip(stat.replace("部想看", ""))
            if stat.find("部看过") != -1:
                userinfo["drama"]["have"] = self.strip(stat.replace("部看过", ""))

        bookstat = response.css("#book span.pl>a::text").extract()

        for stat in bookstat:
            userinfo["book"] = {}
            if stat.find("本想读") != -1:
                userinfo["book"]["want"] = self.strip(stat.replace("本想读", ""))
            if stat.find("本在读") != -1:
                userinfo["book"]["doing"] = self.strip(stat.replace("本在读", ""))
            if stat.find("本读过") != -1:
                userinfo["book"]["have"] = self.strip(stat.replace("本读过", ""))

        moviestat = response.css("#movie span.pl>a::text").extract()

        for stat in moviestat:
            userinfo["movie"] = {}
            if stat.find("部想看") != -1:
                userinfo["movie"]["want"] = self.strip(stat.replace("部想看", ""))
            if stat.find("部在看") != -1:
                userinfo["movie"]["doing"] = self.strip(stat.replace("部在看", ""))
            if stat.find("部看过") != -1:
                userinfo["movie"]["have"] = self.strip(stat.replace("部看过", ""))

        musicstat = response.css("#music span.pl>a::text").extract()

        for stat in musicstat:
            userinfo["music"] = {}
            if stat.find("张想听") != -1:
                userinfo["music"]["want"] = self.strip(stat.replace("张想听", ""))
            if stat.find("张在听") != -1:
                userinfo["music"]["doing"] = self.strip(stat.replace("张在听", ""))
            if stat.find("张听过") != -1:
                userinfo["music"]["have"] = self.strip(stat.replace("张听过", ""))

        gamestat = response.css("#game span.pl>a::text").extract()

        for stat in gamestat:
            userinfo["game"] = {}
            if stat.find("想玩") != -1:
                userinfo["game"]["want"] = self.strip(stat.replace("想玩", ""))
            if stat.find("在玩") != -1:
                userinfo["game"]["doing"] = self.strip(stat.replace("在玩", ""))
            if stat.find("玩过") != -1:
                userinfo["game"]["have"] = self.strip(stat.replace("玩过", ""))

        pass

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
            fieldnames = ["id", "title", "subtitle", "original_title", "link", "cover_link", "publisher", "isbn", "author", "translator", "producer", "price", "series", "published_at", "page", "decoration", "rating", "score5", "score4", "score3", "score2", "score1", "rater_count", "short_review_count", "long_review_count", "has_previous_version", "reader_count"]
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
                for i in range(1, 6):
                    if "rating_distribution" in item:
                        _item["score" + str(i)] = item["rating_distribution"][str(i)]
                    else:
                        _item["score" + str(i)] = ""
                writer.writerow(_item)
            csvfile.close()
