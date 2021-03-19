# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TuchuzyCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    product_name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()
    in_stock = scrapy.Field()
    retailer_short_id = scrapy.Field()
    retailer_code = scrapy.Field()
    retailer_display_domain = scrapy.Field()
    free_returns = scrapy.Field()
    returns_period = scrapy.Field()
