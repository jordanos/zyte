# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import datetime

import scrapy


class BizItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    industry = scrapy.Field()
    location = scrapy.Field()
    asking_price = scrapy.Field()
    revenue = scrapy.Field()
    ebitda = scrapy.Field()
    cash_flow = scrapy.Field()
    agent_name = scrapy.Field()
    agent_company = scrapy.Field()
    agent_phone = scrapy.Field()
    website_url = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    deleted = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(BizItem, self).__init__(*args, **kwargs)
        self.setdefault("title", None)
        self.setdefault("description", None)
        self.setdefault("industry", None)
        self.setdefault("location", None)
        self.setdefault("asking_price", None)
        self.setdefault("revenue", None)
        self.setdefault("ebitda", None)
        self.setdefault("cash_flow", None)
        self.setdefault("agent_name", None)
        self.setdefault("agent_company", None)
        self.setdefault("agent_phone", None)
        self.setdefault("website_url", None)
        self.setdefault("created_at", str(datetime.now()))
        self.setdefault("updated_at", str(datetime.now()))
        self.setdefault("deleted", 0)
