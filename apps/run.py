import os
import sys


sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'scrapit.settings'

import django
django.setup()


from apps.scraper.scraper.spiders import (a2go, ahram, masrawy, nytimes,
                                          offers_plus, techcrunch, washington)
from apps.scraper.scraper import settings as my_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


spiders = [a2go.A2goSpider, ahram.AhramSpider(), masrawy.MasrawySpider(),
           nytimes.NytimesSpider(), offers_plus.OffersPlusSpider(),
           techcrunch.TechcrunchSpider(), washington.WashingtonSpider()]
crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
process = CrawlerProcess(settings=crawler_settings)
for spider in spiders:
    process.crawl(spider)
process.start()
