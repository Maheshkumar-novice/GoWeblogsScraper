# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class BlogItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    content = scrapy.Field(output_processor=TakeFirst())
    file_path = scrapy.Field()
