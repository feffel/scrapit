from apps.scraper.scraper.spiders import (a2go, ahram, masrawy, nytimes,
                                          offers_plus, techcrunch, washington)
from apps.scraper.scraper import settings as my_settings
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


class Command(BaseCommand):
    help = 'Runs the spiders to scrap some content'

    def handle(self, *args, **options):
        spiders = [a2go.A2goSpider, ahram.AhramSpider(), masrawy.MasrawySpider(),
                   nytimes.NytimesSpider(), offers_plus.OffersPlusSpider(),
                   techcrunch.TechcrunchSpider(), washington.WashingtonSpider()]
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        for spider in spiders:
            process.crawl(spider)
        process.start()
        self.stdout.write(self.style.SUCCESS('Successfully scraped available websites'))
