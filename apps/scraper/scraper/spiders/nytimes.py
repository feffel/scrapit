# -*- coding: utf-8 -*-
import re
import scrapy
import time

from apps.scraper.scraper import settings
from apps.scraper.scraper.utils import chrome
from apps.scraper.scraper.utils import format_date
from selenium.common.exceptions import NoSuchElementException


class NytimesSpider(scrapy.Spider):
    name = 'nytimes'
    allowed_domains = ['nytimes.com']
    start_urls = ['https://www.nytimes.com/search/*/newest/']
    articles_selector = '[class^="SearchResults-item"]'
    headline_selector = '[class^="Item-headline"]'
    url_xpath = 'div/div/a'
    img_selector = '[class^="Item-media"]'
    load_more_xpath = '//*[@id="site-content"]/div/div/div[2]/div[2]/div/button'
    domain = 'nytimes.com'
    date_regex = re.compile(r'.*([0-9]{4})/([0-9]{2})/([0-9]{2})/.*')
    MAX_ARTICLES = settings.MAX_ENTRIES
    MAX_AGE = settings.MAX_AGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = None

    def parse(self, response):
        self.driver = chrome()
        self.driver.get(response.url)
        load_more = self.driver.find_element_by_xpath(self.load_more_xpath)
        articles = self.driver.find_elements_by_css_selector(self.articles_selector)
        while len(articles) < self.MAX_ARTICLES:
            load_more.click()
            time.sleep(5)
            articles = self.driver.find_elements_by_css_selector(self.articles_selector)
        for article in articles[:self.MAX_ARTICLES]:
            yield self.parse_article(article)
        self.driver.close()

    def parse_article(self, article):
        item = {'domain': self.domain}
        item['headline'] = article.find_element_by_css_selector(self.headline_selector).text
        item['url'] = article.find_element_by_xpath(self.url_xpath).get_attribute('href')
        item['date'] = self.get_date(item['url'])
        try:
            item['img'] = article.find_element_by_css_selector(
                                                        self.img_selector).get_attribute('itemid')
        except NoSuchElementException:
            item['img'] = None
        return item

    def get_date(self, url):
        date_match = self.date_regex.match(url)
        return format_date(date_match.groups()[2],
                           date_match.groups()[1],
                           date_match.groups()[0])
