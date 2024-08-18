import typing
from collections.abc import Generator

import scrapy
from scrapy.http import Request, Response

from goweblogsscraper.items import GitHubPinnedLinkItem, GitHubRepoItem


class GithubSpider(scrapy.Spider):
    name = "github"
    allowed_domains: typing.ClassVar = ["github.com"]
    start_urls: typing.ClassVar = ["https://github.com/Maheshkumar-novice"]
    custom_settings: typing.ClassVar = {
        "ITEM_PIPELINES": {
            "goweblogsscraper.pipelines.JSONWriterPipeline": 300,
        }
    }

    def parse(self, response: Response) -> Generator[GitHubPinnedLinkItem | Request, None, None]:
        links = response.css(".js-pinned-items-reorder-list li a.Link::attr(href)").getall()
        if links:
            for link in links:
                item = GitHubPinnedLinkItem()
                item["link"] = link
                yield item

        respositories_link = response.css('nav a.UnderlineNav-item[data-tab-item="repositories"]::attr(href)').get()
        if respositories_link:
            yield response.follow(respositories_link, self.parse_repos)

    def parse_repos(self, response: Response) -> Generator[GitHubRepoItem | Request, None, None]:
        repos = response.css("#user-repositories-list li")
        if repos:
            for repo in repos:
                item = GitHubRepoItem()
                item["tags"] = repo.css("a.topic-tag.topic-tag-link::attr(href)").getall()
                item["link"] = repo.css("h3 a::attr(href)").get()
                yield item
        next_page = response.css(".paginate-container a.next_page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse_repos)
