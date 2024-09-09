# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class NdBusinessesItem(scrapy.Item):
    # Fields for the items to be scraped
    business_id = scrapy.Field()
    business_name = scrapy.Field()
    filing_type = scrapy.Field()
    owner_name = scrapy.Field()
    commercial_registered_agent = scrapy.Field()
    registered_agent = scrapy.Field()

    def __setitem__(self, key, value):
        # Dynamically add fields when they are not predefined
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(NdBusinessesItem, self).__setitem__(key, value)
