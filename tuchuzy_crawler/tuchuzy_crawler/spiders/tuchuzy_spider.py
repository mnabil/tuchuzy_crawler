import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tuchuzy_crawler.items import TuchuzyCrawlerItem
import csv


class MySpider(CrawlSpider):
    name = 'tuchuzy'
    allowed_domains = ['tuchuzy.com']

    # Reading list of xpaths from CSV
    with open("tuchuzy_crawler/spiders/spider_xpaths/{0}_xpath.csv".format(name), 'r') as f:
        # reading xpath csv data into dictionary to use
        xpath_info = csv.DictReader(f)
        for row in xpath_info:
            xpath_info = row
            break

    def start_requests(self):
        """start request link

        Yields:
            [scrapy.Request]: First Request with AUD only
                              Change to USD or other currencies if needed
                              #currencies usually change on different servers/origin
                              depending on the country of machine running crawler
        """
        url = 'https://www.tuchuzy.com'
        yield scrapy.Request(url=url, cookies={'cart_currency': 'AUD'})

    rules = (
        # Extract links matching 'category' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('.*/collections/.*',
             '.*/collections/.*\?page='), deny=(".*/vendors/.*"))),
        # Extracting pagination as well , ex: page=1, page=2 in categories
        Rule(LinkExtractor(allow=('.*/collections/.*', '.*/collections/.*\?page='),
             deny=([".*/vendors/.*", '.+\.atom', '.+\.oembed']), tags=('link'), attrs=('href'))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('.*/products/.*', )), callback='parse_item'),
    )

    def parse_item(self, response):
        """called on links that needs parsing

        Args:
            response (scrapy.Response): response object

        Yields:
            item: scrapy.Item()
        """
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = TuchuzyCrawlerItem()

        item['url'] = response.url
        item['product_name'] = response.xpath(
            self.xpath_info['product_name']).extract_first()
        item['brand'] = response.xpath(
            self.xpath_info['brand']).extract_first()
        item['category'] = ">>".join(response.xpath(
            self.xpath_info['category']).re('/collections/(.+)?'))  # FIXME: update
        item['images'] = response.xpath(self.xpath_info['images']).extract()
        price = response.xpath(self.xpath_info['price']).extract_first()
        sale_price = response.xpath(
            self.xpath_info['sale_price']).extract_first()
        item['price'] = self.wrap_price([',', '.', 'AUD', 'USD', '$'], price)
        item['sale_price'] = self.wrap_price(
            [',', '.', 'AUD', 'USD', '$'], sale_price)
        item['in_stock'] = bool(response.xpath(
            self.xpath_info['in_stock']).extract_first() == 'http://schema.org/InStock')
        yield item

    def wrap_price(self, rep_list, price):
        """replaces list of strings in a string with nothing 
            (Doesn't need to be in pipeline)

        Args:
            rep_list (list): strings to be replaces
            price (string): string which we replace in

        Returns:
            (string): string after replacements
        """
        [price.replace(item, '') for item in rep_list]
        for item in rep_list:
            price = price.replace(item, '')
        price = price.strip()
        return price


# NOTES
# sitemaps in case we need sitemap crawler #SITEMAP IS A LOT FASTER THAN MOST CRAWLERS
# https://www.tuchuzy.com/sitemap_products_1.xml?from=4125014982716&to=4126387863612
# https://www.tuchuzy.com/sitemap_products_2.xml?from=4126388125756&to=6541721239612

# some backup parsed data present in [type="application/json"] tag

# DIDN'T FIND ANY INTERNAL API REQUESTS CONTAINING FURTHER DATA

#PRICE CLEANING could be done with Scrapy.Selector.re or using pipelines (was not needed)
# i tend to avoid using Regex in terms of speed

# Required fields
# - Product Name [Titlecase]
# - Brand [Uppercase]
# - Category [Separate categories by >> ]
# - Image links [ These should be the largest size images you are able to obtain]
# - Price [Remove '$' and return in decimals i.e $99.95 should be returned as 9995 ]
# - Sale Price [If available, remove '$' and return in decimals i.e $99.95 should be returned as 9995 ]
