# coding=utf-8
import codecs

import scrapy
import datetime
import csv

from scrapy import Request
from selenium import webdriver

from HLZK_IMDBCrawler.items import Celebrity, CelebrityStat
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class MovieSpider(scrapy.Spider):
    name = "celebrity_stat"
    allowed_domains = ["www.scifi-wiki.com"]

    def __init__(self, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        url_pattern = "http://www.scifi-wiki.com/wiki/%d月%d日"
        self.start_urls = []
        self.interval = 0
        start = datetime.datetime.now().replace(year = 2016, month = 1, day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
        end = datetime.datetime.now().replace(year = 2016, month = 12, day = 31, hour = 0, minute = 0, second = 0, microsecond = 0)
        while start <= end:
            try:
                self.start_urls.append(url_pattern % (start.month, start.day))
                try:
                    start = start.replace(day = start.day + 1)
                except ValueError:
                    start = start.replace(month = start.month + 1, day = 1)
            except ValueError:
                break
        option = webdriver.ChromeOptions()
        option.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.item_list = []

    def destroy_browser(self):
        self.browser.quit()

    def parse(self, response):

        def clear_html(html):
            import re
            html = html.replace('<td class="timeline-content">', "")
            html = html.replace("</td>", "")
            html = re.sub(r"<sup(.*?)>(.*?)</sup>", "", html)
            html = html.replace("</a>", "")
            html = html.replace("<b>", "")
            html = html.replace("</b>", "")
            html = re.sub(r"<a(.*?)>", "", html)
            html = html.replace("&amp;", ":")
            return html

        result_list = response.css("table.scifi-calendar-timeline tbody tr")
        for item_c in result_list:
            _date = "".join(response.css("#firstHeading::text").extract()).replace("　", "").replace(" ", "")
            item = CelebrityStat(
                name = "",
                year = item_c.css("td.timeline-year::text").extract()[0].replace("　", ""),
                month = _date[:_date.find(u'月')],
                date = _date[_date.find('月') + 1:_date.find('日')],
                event = clear_html("".join(item_c.css("td.timeline-content").extract())),
                country = ""
            )
            if item["event"].find("出生") != -1:
                clist = [u'中国', u'美国', u'英国', u'加拿大', u'俄罗斯', u'澳大利亚', u'日本', u'挪威', u'法国', u'德国', u'巴西', u'阿根廷']
                for country in clist:
                    if item['event'][:len(country)] == country:
                        item['country'] = country
                        break
                self.item_list.append(item)

    def closed(self, reason):
        self.destroy_browser()
        self.save_result()
        print reason

    def save_result(self):
        with open('celebrity_stat.csv', 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            fieldnames = ['year', 'month', "date", "name", 'country', 'event']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for item in self.item_list:
                writer.writerow(item)
            csvfile.close()
