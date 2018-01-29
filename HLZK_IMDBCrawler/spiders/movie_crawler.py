import codecs

import scrapy
import datetime
import csv
from selenium import webdriver

from HLZK_IMDBCrawler.items import SearchItem


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["www.imdb.com"]

    def __init__(self, start = None, end = None, rating = "7.5", *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        url_pattern = "http://www.imdb.com/search/title?title_type=feature,tv_movie,tv_series,tv_special,tv_miniseries,documentary,short&release_date=%d-%s,%d-%s&user_rating=%s,&genres=sci_fi"
        self.start_urls = []
        for i in range(1900, datetime.datetime.now().year + 1):
            self.start_urls.append(url_pattern % (i, start, i, end, rating))
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        option = webdriver.ChromeOptions()
        option.add_argument(
            "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36")
        self.browser = webdriver.Chrome(options = option, executable_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        self.item_list = []

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
            self.item_list.append(SearchItem(
                name = item_c.css(".lister-item-content h3.lister-item-header a::text").extract()[0],
                link = "http://www.imdb.com%s" % item_c.css(".lister-item-content h3.lister-item-header a::attr(href)").extract()[0],
                rating = clean(item_c.css(".lister-item-content .ratings-bar .ratings-imdb-rating::attr(data-value)").extract()),
                genre = clean(item_c.css(".lister-item-content h3.lister-item-header+p.text-muted .genre::text").extract()),
                runtime = clean(item_c.css(".lister-item-content h3.lister-item-header+p.text-muted .runtime::text").extract())
            ))

    def closed(self, reason):
        self.destroy_browser()
        self.save_result()
        print reason

    def save_result(self):
        with open('search_result.csv', 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            fieldnames = ['name', 'link', 'rating', 'genre', 'runtime']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for item in self.item_list:
                writer.writerow(item)
            csvfile.close()
