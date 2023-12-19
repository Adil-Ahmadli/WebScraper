# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class ProductscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field in field_names:
            if field!= "other_image_urls":
                value = adapter.get(field)
                if value is not None:
                    adapter[field] = value.strip()

        value = adapter.get("price_without_discount")
        if value is None:
            adapter["price_without_discount"] = 0.0
        else:
            value = value.replace(' TL', '')
            value = value.replace(',', '.')
            adapter["price_without_discount"] = float(value)

        value = adapter.get("price")
        if value is None:
            adapter["price"] = adapter.get("price_without_discount")
        else:
            value = value.replace(' TL', '')
            value = value.replace(',', '.')
            adapter["price"] = float(value)

        value = adapter.get("rating_score")
        if value is None:
            adapter["rating_score"] = 0

        value = adapter.get("review_count")
        if value is None:
            adapter["review_count"] = 0

        return item


class ExcelExportPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        data = pd.DataFrame(self.items)
        data.to_excel('data.xlsx', index=False)
