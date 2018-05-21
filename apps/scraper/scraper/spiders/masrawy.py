# -*- coding: utf-8 -*-
import scrapy

from apps.scraper.scraper import settings
from datetime import date
from scrapy.http import Request


class MasrawySpider(scrapy.Spider):
    name = 'masrawy'
    allowed_domains = ['masrawy.com']
    url = 'http://www.masrawy.com/listing/ArchiveMore?archiveDate={}-{}-{}&categoryId=0&pageIndex={}'
    articles_selector = '[class^="mix "]'
    headline_xpath = 'a[1]/div[2]/p//text()'
    url_xpath = 'a[1]/@href'
    img_xpath = 'a[1]/div[1]/img/@src'
    domain = 'masrawy.com'
    MAX_ARTICLES = settings.MAX_ENTRIES
    MAX_AGE = settings.MAX_AGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.driver = None
        self.seen = set()

    def start_requests(self):
        self.counter = 0
        self.seen = set()
        day = date.today()
        index = 1
        yield Request(self.url.format(day.year, day.month, day.day, index),
                      callback=self.parse_outer,
                      meta={'day': day, 'index': index})

    def parse_outer(self, response):
        articles = response.css(self.articles_selector)
        new_articles = self.filter_articles(articles)
        for article in new_articles:
            if self.counter >= self.MAX_ARTICLES:
                return
            yield self.extract_data(article, response.meta['day'])
        meta = response.meta
        meta['articles_found'] = len(new_articles)
        yield self.next_page(response.meta)

    def next_page(self, meta):
        if meta['articles_found'] > 0:
            meta['index'] += 1
        else:
            meta['index'] = 1
            meta['day'] = meta['day'].replace(day=meta['day'].day-1)
            if (date.today() - meta['day']).days >= self.MAX_AGE:
                return
        day = meta['day']
        return Request(self.url.format(day.year, day.month, day.day, meta['index']),
                       callback=self.parse_outer,
                       meta=meta)

    def extract_data(self, article, date):
        self.counter += 1
        item = {
            'domain': self.domain,
            'date': date
        }
        item['headline'] = article.xpath(self.headline_xpath).extract()[0]
        item['url'] = 'http://{}{}'.format(self.domain, article.xpath(self.url_xpath).extract()[0])
        item['img'] = article.xpath(self.img_xpath).extract()[0]
        return item

    def filter_articles(self, articles):
        article_ids = [a.xpath('@postid').extract()[0] for a in articles]
        new_article_ids = set(article_ids) - self.seen
        new_articles = [x for x in articles if x.xpath('@postid').extract()[0] in new_article_ids]
        self.seen = self.seen | set(new_article_ids)
        return new_articles
