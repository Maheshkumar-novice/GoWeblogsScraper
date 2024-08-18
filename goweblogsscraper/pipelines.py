# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from pathlib import Path

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from goweblogsscraper.items import BlogItem, GitHubPinnedLinkItem, GitHubRepoItem


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

        Path.mkdir(Path(Path.cwd()) / "scraped_blogs", exist_ok=True)

        with Path(file_path).open("wb") as f:
            f.write(item["content"])

        item["file_path"] = file_path

        return item


class JSONWriterPipeline:
    def open_spider(self, _spider: scrapy.Spider) -> None:
        self.file = Path(Path.cwd() / "github_data.jsonl").open("w")  # noqa: SIM115

    def close_spider(self, _spider: scrapy.Spider) -> None:
        self.file.close()

    def process_item(self, item: GitHubPinnedLinkItem | GitHubRepoItem, _spider: scrapy.Spider) -> GitHubPinnedLinkItem:
        line = ItemAdapter(item).asdict()
        if isinstance(item, GitHubPinnedLinkItem):
            line["type"] = "pinned_link"
        else:
            line["type"] = "repo"
        line = json.dumps(line, sort_keys=True) + "\n"
        self.file.write(line)
        return item
