# -*- coding: utf-8 -*-
import re
import scrapy

from scraper import settings
from scraper.utils import format_date
from scrapy.http import Request


class AhramSpider(scrapy.Spider):
    name = 'ahram'
    allowed_domains = ['gate.ahram.org.eg']
    url = 'http://gate.ahram.org.eg/OuterMore/2/{}.aspx'
    articles_xpath = '//*[contains(@id, "ContentPlaceHolder1_dlNewsContentUrgent_divOuterNews")]/div/div[2]/a/@href'
    headline_xpath = '//*[@id="ContentPlaceHolder1_divTitle"]/h1/text()'
    img_xpath = '//*[@id="ContentPlaceHolder1_divMainImage"]/img/@src'
    date_xpath = '//*[@id="ContentPlaceHolder1_divdate"]/h4/text()[1]'
    domain = 'ahram.org.eg'
    date_regex = re.compile(r'([0-9]{1,2})-([0-9]{1,2})-([0-9]{4})')
    MAX_ARTICLES = settings.MAX_ENTRIES
    ARTICLES_PER_PAGE = 30
    MAX_AGE = settings.MAX_AGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        pages_to_load = int(self.MAX_ARTICLES / self.ARTICLES_PER_PAGE)
        if self.MAX_ARTICLES // self.ARTICLES_PER_PAGE > 0:
            pages_to_load += 1
        for i in range(pages_to_load):
            yield Request(self.url.format(i*self.ARTICLES_PER_PAGE),
                          callback=self.parse_outer,
                          meta={'count': i*self.ARTICLES_PER_PAGE})

    def get_date(self, response):
        date = response.xpath(self.date_xpath).extract()
        date_match = self.date_regex.match(date[0])
        return format_date(date_match.groups()[0], date_match.groups()[1],
                           date_match.groups()[2])

    def parse_outer(self, response):
        self.logger.warning(response.url)
        count = response.meta['count']
        atricles = response.xpath(self.articles_xpath).extract()
        for article_url in atricles:
            count += 1
            if count > self.MAX_ARTICLES:
                break
            yield Request(article_url, callback=self.parse_item)

    def parse_item(self, response):
        item = {
            'url': response.url,
            'domain': self.domain
        }
        item['headline'] = response.xpath(self.headline_xpath).extract()[0]
        item['date'] = self.get_date(response)
        item['img'] = response.xpath(self.img_xpath).extract()[0]
        return item
