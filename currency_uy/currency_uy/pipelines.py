# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json


class CurrencyUyPipeline:
    result = {}

    def process_item(self, item, spider):
        exchange_house = self.result.setdefault(spider.name, [])

        values = item.__dict__['_values']
        values['buy'] = round(float(values['buy'].replace(',', '.')), 2)
        values['sell'] = round(float(values['sell'].replace(',', '.')), 2)

        exchange_house.append(values)
        return item

    def close_spider(self, spider):
        with open('result.json', 'w') as f:
            f.write(json.dumps(self.result, indent=4))
