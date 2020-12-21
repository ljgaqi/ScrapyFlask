# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JavbusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jav_sn=scrapy.Field()
    jav_name=scrapy.Field()
    jav_time=scrapy.Field()
    jav_date=scrapy.Field()
    jav_open_date=scrapy.Field()
    jav_url=scrapy.Field()
    image_urls=scrapy.Field()
    jav_cili=scrapy.Field()

