# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from apps.main.models import ScrapContent
from django.db import IntegrityError
from scrapy.exceptions import DropItem
import json


class ScraperAppPipeline(object):
    # def __init__(self, *args, **kwargs):
    #     self.items = []

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
    #     )

    # def close_spider(self, spider):
    #     item = ScrapContent()
    #     item.unique_id = self.unique_id
    #     item.data = json.dumps(self.items)
    #     item.save()

    def process_item(self, item, spider):
        try:
            item = ScrapContent.objects.create(
                headline=item['headline'],
                url=item['url'],
                img=item['img'],
                date=item['date'],
                domain=item['domain']
            )
        except IntegrityError:
            raise DropItem()
        return item
