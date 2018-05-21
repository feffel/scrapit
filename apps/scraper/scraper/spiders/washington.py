# -*- coding: utf-8 -*-
import re
import time

from scraper import settings
from scraper.utils import format_date, chrome
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from selenium.common.exceptions import NoSuchElementException


class WashingtonSpider(CrawlSpider):
    name = 'washington'
    allowed_domains = ['washingtonpost.com']
    start_urls = ['https://www.washingtonpost.com/']
    articles_selector = '[class^="story-list-story"]'
    lnk_xpath = 'div[1]/div[1]/h3/a'
    img_xpath = 'div[3]/a/img'
    more_btn_selector = '[class^="button pb-loadmore"]'
    domain = 'washingtonpost.com'
    date_regex = re.compile(r'.*/([0-9]{4})/([0-9]{2})/([0-9]{2})/.*')
    MAX_ARTICLES = settings.MAX_ENTRIES
    MAX_AGE = settings.MAX_AGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = 0

    def parse(self, response):
        extractor = LinkExtractor(
                        allow=r'^https://.*\.com/[^/]*/$',
                        restrict_xpaths=['//*[@id="sections-menu-wide"]'],
                    )
        links = extractor.extract_links(response)
        self.categories = len(links)
        for i, link in enumerate(links):
            yield Request(link.url,
                          callback=self.parse_category,
                          meta={'category_index': i})

    def get_categyory_limit(self, meta):
        limit = self.MAX_ARTICLES // self.categories
        if meta['category_index'] < self.MAX_ARTICLES % self.categories:
            limit += 1
        return limit

    def parse_category(self, response):
        driver = chrome()
        driver.get(response.url)
        limit = self.get_categyory_limit(response.meta)
        count = 0
        more_btn = driver.find_element_by_css_selector(self.more_btn_selector)
        articles = driver.find_elements_by_css_selector(self.articles_selector)
        seen = set()
        while count < limit:
            for article in articles[:limit-count]:
                item = self.extract_data(article)
                count += 1 if item else 0
                yield item
            time.sleep(2)
            more_btn.click()
            articles = driver.find_elements_by_css_selector('[class^="story-list-story"]')
            articles = list(set(articles) - seen)
            seen = set(articles)
        driver.close()

    def get_date(self, link):
        date_match = self.date_regex.match(link)
        return format_date(date_match.groups()[2], date_match.groups()[1],
                           date_match.groups()[0])

    def extract_data(self, article):
        item = {'domain': self.domain}
        try:
            lnk = article.find_element_by_xpath(self.lnk_xpath)
            item['headline'] = lnk.get_attribute('text')
            item['url'] = lnk.get_attribute('href')
            try:
                item['img'] = article.find_element_by_xpath(self.img_xpath).get_attribute('src')
            except NoSuchElementException:
                item['img'] = None
        except NoSuchElementException:
            return
        item['date'] = self.get_date(item['url'])
        return item
