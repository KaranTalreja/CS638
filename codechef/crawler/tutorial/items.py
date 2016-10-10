# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Question(scrapy.Item):
    index = scrapy.Field()
    problem_code = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    submissions_page = scrapy.Field()
    description = scrapy.Field()
    input_text = scrapy.Field()
    output_text = scrapy.Field()
    date_added = scrapy.Field()
    time_limit = scrapy.Field()
    source_limit = scrapy.Field()
    tags = scrapy.Field()
    editorial_page = scrapy.Field()
    success_count = scrapy.Field()
    accuracy = scrapy.Field()
