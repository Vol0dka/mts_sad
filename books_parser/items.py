# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksParserItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    genre = scrapy.Field()
    director = scrapy.Field()
    country = scrapy.Field()
    year = scrapy.Field()
    IMDB_id = scrapy.Field()
    IMDB_link = scrapy.Field()
