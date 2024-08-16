# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pathlib import Path

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from goweblogsscraper.items import BlogItem


class BlogPipeline:
    def process_item(self, item: BlogItem, _spider: scrapy.Spider) -> BlogItem:
        item = ItemAdapter(item=item)

        if not item.get("title"):
            msg = f"Missing title in {item}"
            raise DropItem(msg)
        if not item.get("content"):
            msg = f"Missing content in {item}"
            raise DropItem(msg)

        filename = f"blog_{item['title'].replace(' ', '_')}.html"
        file_path = Path("scraped_blogs") / filename

        Path.mkdir(Path(__file__).parent, exist_ok=True)

        with Path(file_path).open("wb") as f:
            f.write(item["content"])

        item["file_path"] = file_path

        return item
