# coding=utf-8
import codecs
import os
import scrapy
import datetime
import csv

from scrapy import Request
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class IdeaSpider(scrapy.Spider):
    name = "idea"
    allowed_domains = ["www.writepop.com"]

    def __init__(self, *args, **kwargs):
        super(IdeaSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.writepop.com/category/1001-story-ideas"]
        option = webdriver.ChromeOptions()
        option.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.item_list = []
        self.count = 0
        self.file = None
        if not os.path.exists("ideas"):
            os.mkdir("ideas")

    def destroy_browser(self):
        self.browser.quit()

    def parse(self, response):
        result_list = response.css("#post-476 .entry ul>li")
        for item in result_list[:-1]:
            # print item.css("a::attr(href)").extract()[0]
            yield Request(item.css("a::attr(href)").extract()[0], callback = self.parse_ideas)

    def parse_ideas(self, response):

        def get_tag_name(html):
            return html[1:html.find(">")]

        import re
        pattern = re.compile("[^a-zA-Z0-9.…(!)]")
        pattern_2 = re.compile(" +")
        category = re.sub(pattern = pattern, string = response.css(".entry h2::text").extract()[0].replace("/", "or"), repl = " ")
        category = re.sub(pattern = pattern_2, string = category, repl = " ").lstrip().rstrip()
        # print category
        if not os.path.exists("ideas/%s" % category):
            os.mkdir("ideas/%s" % category)
        contents = response.css(".entry>*")
        for item in contents:
            if get_tag_name(item.extract()) == "h3" and len(item.xpath("./text()").extract()) != 0:
                if self.file is not None and not self.file.closed:
                    self.file.close()
                filename = re.sub(pattern = pattern, string = item.xpath("./text()").extract()[0], repl = " ")
                filename = re.sub(pattern = pattern_2, string = filename, repl = " ").lstrip().rstrip()
                self.file = open("ideas/%s/%s.txt" % (category, filename), "wb")
            elif get_tag_name(item.extract()) == "ul":
                unfinish = True
                while unfinish:
                    try:
                        if item.css("ul") is not None:
                            contents = item.css("ul").css("li::text").extract()
                        else:
                            contents = item.css("li::text").extract()
                        print category, len(contents), type(contents)
                        self.count += len(contents)
                        unfinish = False
                    except IOError:
                        unfinish = True
                        continue
                for content in contents:
                    self.file.write(content + "\n\n")

    def closed(self, reason):
        self.destroy_browser()
        print self.count
        print reason