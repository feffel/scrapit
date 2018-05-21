# -*- coding: utf-8 -*-
import scrapy

from apps.scraper.scraper import settings
from dateutil.parser import parse
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor


class OffersPlusSpider(scrapy.Spider):
    name = 'offers-plus'
    allowed_domains = ['offers-plus.com']
    start_urls = ['http://offers-plus.com/']
    url = 'http://www.offers-plus.com/categories.php?category=Clothing-%2C-Shoes-%26-Apparel&page={}&sort=newest'
    headline_xpath = '//*[@id="ProductDetails"]/div/h2/text()'
    img_selector = '[class^="ProductThumb"]'
    img_xpath = 'a/img/@src'
    date_grid_selector = '[class^="ProductDetailsGrid"]'
    date_xpath = 'dd[5]/text()'
    domain = 'offers-plus.com'
    MAX_ENTRIES = settings.MAX_ENTRIES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extractor = LinkExtractor(
                            allow=r'.*/products\.php\?product=.*',
                            restrict_xpaths=['//*[@id="frmCompare"]/ul'],
                            unique=True
                        )

    def start_requests(self):
        meta = {'index': 1, 'count': 0}
        yield Request(self.url.format(meta['index']),
                      callback=self.parse_outer,
                      meta=meta)

    def parse_outer(self, response):
        count = response.meta['count']
        entries_links = self.extractor.extract_links(response)
        limit = self.MAX_ENTRIES - count
        limit = limit if limit > 0 else 0
        for entry in entries_links[:limit]:
            yield Request(entry.url,
                          callback=self.parse_coupon)
        count += len(entries_links)
        if len(entries_links) == 0 or count > self.MAX_ENTRIES:
            return
        meta = {'index': response.meta['index']+1, 'count': count}
        yield Request(self.url.format(meta['index']),
                      callback=self.parse_outer,
                      meta=meta)

    def parse_coupon(self, response):
        item = {'domain': self.domain, 'url': response.url}
        item['headline'] = response.xpath(self.headline_xpath).extract()[0]
        item['date'] = self.get_date(response)
        item['img'] = response.css(self.img_selector).xpath(self.img_xpath).extract()[0]
        yield item

    def get_date(self, response):
        date_grid = response.css(self.date_grid_selector)
        date_text = date_grid.xpath(self.date_xpath).extract()[0]
        try:
            return parse(date_text).date()
        except TypeError:
            return None
