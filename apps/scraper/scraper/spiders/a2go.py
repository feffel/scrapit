# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dateutil.parser import parse


class A2goSpider(CrawlSpider):
    name = '2go'
    allowed_domains = ['2go-eg.com']
    start_urls = ['http://2go-eg.com/']
    name = '2go'
    allowed_domains = ['2go-eg.com']
    start_urls = ['http://www.2go-eg.com/golden_vouchers_list']
    headline_xpath = '//*[@id="ProductDetails"]/div/h2/text()'
    img_xpath = '//*[@id="wrapper"]/section/div/div/div[1]/div[1]/a/img/@src'
    date_xpath = '//*[@id="wrapper"]/section/div/div/div[1]/ul/li[1]/a/span/text()'
    date_regex = re.compile(r'Valid till (.*)')
    domain = '2go-eg.com'

    rules = (
        Rule(LinkExtractor(allow=r'.*2go-eg\.com/golden_vouchers/.*',
                           restrict_xpaths=['//*[@id="wrapper"]/section/div/div'],
                           unique=True),
             callback='parse_offer', follow=True),
    )

    def parse_offer(self, response):
        item = {'domain': self.domain, 'url': response.url}
        # import ipdb;ipdb.set_trace()
        item['headline'] = self.get_headline_text(response)
        item['date'] = self.get_date(response)
        item['img'] = response.xpath(self.img_xpath).extract()[0]
        return item

    def get_headline_text(self, response):
        header = response.xpath('//*[@id="wrapper"]/section/div/div/div[1]/h1')
        main_text = header.xpath('text()').extract()[0]
        extra_text = header.xpath('span/text()').extract()
        return ''.join([main_text] + extra_text)

    def get_date(self, response):
        date_text = response.xpath(self.date_xpath).extract()[0]
        stripped_date = self.date_regex.match(date_text).groups()[0]
        return parse(stripped_date).date()
