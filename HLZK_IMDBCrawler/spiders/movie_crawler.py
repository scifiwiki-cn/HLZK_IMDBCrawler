# coding=utf-8
import codecs

import scrapy
import datetime
import csv

from scrapy import Request
from selenium import webdriver

from HLZK_IMDBCrawler.items import SearchItem


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["www.imdb.com", "movie.douban.com"]

    def __init__(self, start = None, end = None, rating = "7.5", filter = True, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        url_pattern = "http://www.imdb.com/search/title?title_type=feature,tv_movie,tv_series,tv_special,tv_miniseries,documentary,short&release_date=%d-%s,%d-%s&user_rating=%s,&genres=sci_fi"
        self.start_urls = []
        for i in range(2015, datetime.datetime.now().year + 1):
            self.start_urls.append(url_pattern % (i, start, i, end, rating))
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        option = webdriver.ChromeOptions()
        option.add_argument(
            "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.item_list = {}
        self.filter = filter

    def destroy_browser(self):
        self.browser.quit()

    def parse(self, response):

        def clean(value):
            result = None
            try:
                result = value[0]
            except:
                result = ""
            return result

        result_list = response.css(".lister-list .lister-item.mode-advanced")
        for item_c in result_list:
            item_id = item_c.css(".lister-item-content h3.lister-item-header a::attr(href)").extract()[0].replace("/title/", "").replace("/?ref_=adv_li_tt", "")
            self.item_list[item_id] = SearchItem(
                name = item_c.css(".lister-item-content h3.lister-item-header a::text").extract()[0],
                link = "http://www.imdb.com%s" % item_c.css(".lister-item-content h3.lister-item-header a::attr(href)").extract()[0],
                rating = clean(item_c.css(".lister-item-content .ratings-bar .ratings-imdb-rating::attr(data-value)").extract()),
                genre = clean(item_c.css(".lister-item-content h3.lister-item-header+p.text-muted .genre::text").extract()),
                runtime = clean(item_c.css(".lister-item-content h3.lister-item-header+p.text-muted .runtime::text").extract())
            )

            if filter:
                yield Request("https://movie.douban.com/subject_search?search_text=%s" % item_id, callback = self.parse_douban)

    def parse_douban(self, response):
        item_id = response.url.replace("https://movie.douban.com/subject_search?search_text=", "")
        try:
            item = response.css(".sc-dnqmqq.eXEXeG div:first-child")
            if item.css(".item-root .detail .pl::text").extract()[0] != "(暂无评分)":
                self.item_list[item_id]["douban"] = item.css(".item-root>a::attr(href)").extract()[0]
                self.item_list[item_id]["chtitle"] = item.css(".item-root .detail .title>a::text").extract()[0]
                self.item_list[item_id]["douban_rating"] = item.css(".item-root .detail .rating .rating_nums::text").extract()[0]
                self.item_list[item_id]["douban_link"] = item.css(".item-root .detail .title>a::attr(href)").extract()[0]
                yield Request(self.item_list[item_id]["douban_link"], callback = self.parse_douban_detail)
            else:
                self.item_list.pop(item_id)
        except Exception, e:
            self.item_list.pop(item_id)

    def parse_douban_detail(self, response):
        item_id = response.css("#info>a[href^='http://www.imdb.com/title']::text").extract()[0]
        self.item_list[item_id]["description"] = response.css("#link-report span[property='v:summary']::text").extract()[0]

    def closed(self, reason):
        self.destroy_browser()
        self.save_result()
        print reason

    def save_result(self):
        with open('search_result.csv', 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            fieldnames = ['name', 'link', 'rating', 'genre', 'runtime', 'douban', 'chtitle', 'douban_rating', 'douban_link', "description"]
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for item in self.item_list:
                writer.writerow(self.item_list[item])
            csvfile.close()
