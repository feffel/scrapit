# -*- coding: utf-8 -*-
import json
import re
import scrapy

from apps.scraper.scraper import settings
from apps.scraper.scraper.utils import format_date
from scrapy.http import Request


class TechcrunchSpider(scrapy.Spider):
    name = 'techcrunch'
    allowed_domains = ['techcrunch.com']
    url = 'https://techcrunch.com/wp-json/tc/v1/magazine?page={}&_embed=true'
    domain = 'techcrunch.com'
    date_regex = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2}).*')
    MAX_ARTICLES = settings.MAX_ENTRIES
    MAX_AGE = settings.MAX_AGE

    def start_requests(self):
        yield Request(self.url.format(0),
                      callback=self.parse_json,
                      meta={'index': 0, 'count': 0})

    def parse_json(self, response):
        data = json.loads(response.text)
        if not data:
            return
        count = response.meta['count']
        for article in data[:self.MAX_ARTICLES-count]:
            count += 1
            yield self.extract_item(article)
        if count < self.MAX_ARTICLES:
            index = response.meta['index'] + 1
            yield Request(self.url.format(index),
                          callback=self.parse_json,
                          meta={'index': index, 'count': count})

    def extract_item(self, article):
        item = {'domain': self.domain}
        item['headline'] = article['title']['rendered']
        item['url'] = article['link']
        item['date'] = self.get_date(article['date'])
        try:
            item['img'] = article['_embedded']['wp:featuredmedia'][0]['source_url']
        except KeyError:
            item['img'] = None
        return item

    def get_date(self, date_text):
        date_match = self.date_regex.match(date_text)
        return format_date(date_match.groups()[2], date_match.groups()[1],
                           date_match.groups()[0])
