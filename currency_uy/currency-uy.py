#!/usr/bin/env python3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

setting = get_project_settings()
setting.set('LOG_LEVEL', 'ERROR')
# Following line commented in favour of CurrencyUyPipeline (will now group values).
#setting.set('FEEDS', {'result.json': {'format': 'json', 'store_empty': False, 'encoding': 'utf8', 'indent': 0}}) # CurrencyUyPipeline will group values 

process = CrawlerProcess(setting)

for spider_name in process.spider_loader.list():
    print(f'Running spider {spider_name}.')
    process.crawl(spider_name)

process.start()
