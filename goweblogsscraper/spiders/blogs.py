import typing
from collections.abc import Generator

import scrapy
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader

from goweblogsscraper.items import BlogItem


class BlogsSpider(scrapy.Spider):
    name = "blogs"
    allowed_domains: typing.ClassVar = ["maheshkumar-novice.github.io"]
    start_urls: typing.ClassVar = ["https://maheshkumar-novice.github.io/GoWeblogs"]

    def parse(self, response: Response) -> Generator[Request, None, None]:
        blog_link = response.xpath("//nav/a[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]")
        if blog_link:
            yield response.follow(blog_link.attrib["href"], self.parse_blog)

    def parse_blog(self, response: Response) -> Generator[Request, None, None]:
        yield from response.follow_all(css=".blog-posts li a", callback=self.parse_blog_content)

    def parse_blog_content(self, response: Response) -> Generator[BlogItem, None, None]:
        item_loader = ItemLoader(item=BlogItem(), response=response)
        item_loader.add_css("title", "#main-content :nth_child(1)::text")
        item_loader.add_value("content", response.body)
        yield item_loader.load_item()
