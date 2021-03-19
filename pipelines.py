# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem


class TuchuzyDuplicatesPipe:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.ids_seen:
            raise DropItem("Duplicate item found: {0}".format(item))
        else:
            self.ids_seen.add(item['url'])
            return item


class TuchuzyValidationPipeline:
    req_fields = ['url', 'product_name', 'brand',
                  'category', 'images', 'price', 'in_stock']

    def process_item(self, item, spider):
        # Do sanity check on the item if missing one or more required field
        if any([item.get(field, '') == None or item.get(field, '') == '' for field in self.req_fields]):
            raise DropItem(
                "Item is not Valid , missing one or more of required_fields Item :: {0}".format(item))
        return item


class TuchuzyAddReailerDataPipeline:
    """
        Adding Necessary Fields
    """
    def process_item(self, item, spider):
        item.update({"retailer_short_id": "tu", "retailer_code": "au-tuchuzy",
                    "retailer_display_domain": "tuchuzy.com", "free_returns": False, "returns_period": 21})
        return item
