import json
import time
from random import randint
from typing import Iterable, Optional

import scrapy
from curl_cffi import requests as curl_requests

# useful for handling different item types with a single interface
from scrapy.http import HtmlResponse

from biz.items import BizItem


class BizSpider(scrapy.Spider):
    name = "bsp"
    start_urls = [
        "https://www.google.com",
    ]

    def __init__(self, url=None, *args, **kwargs):
        super(BizSpider, self).__init__(*args, **kwargs)
        self.url = url

    def get_url(self) -> str:
        # check is the url arg is supplied if and use it or the default
        if self.url:
            return self.url
        else:
            return "https://www.bizbuysell.com/restaurants-and-food-established-businesses-for-sale/"

    def get_cffi_response(self, url: str) -> HtmlResponse:
        """Use ccfi to bypass TLS fingerpint blocking

        Args:
            url (str): _description_

        Returns:
            HtmlResponse: _description_
        """
        request = scrapy.Request(url)
        response = curl_requests.get(
            request.url,
            headers=request.headers.to_unicode_dict(),
            impersonate="chrome124",
        )
        if response.status_code >= 400:
            raise ValueError(
                f"Got error in response. status code {response.status_code}"
            )
        # Create an HtmlResponse object
        response = HtmlResponse(
            url=request.url,
            body=response.content,  # Raw content (bytes)
            encoding=response.encoding,
            request=request,
            status=response.status_code,
        )
        return response

    def parse(self, re: HtmlResponse) -> Iterable[BizItem]:
        """Gets called by default after the first request is processed

        Args:
            re (_type_): _description_

        Yields:
            _type_: _description_
        """
        response = self.get_cffi_response(self.get_url())
        # get the listing items from html doc
        search_results_raw = response.xpath(
            '//head//script[@type="application/ld+json" and @data-stype="searchResultsPage"]/text()'
        ).get()
        search_results = json.loads(search_results_raw)
        listing_items = search_results["about"]
        # for each listing item get the detail and save the result
        counter = 0
        # TODO: remove selecting the first 5 only, it's added because of blocking issues for now
        listing_items = listing_items[:5]

        for ls in listing_items:
            item = ls["item"]
            if item["@type"] != "Product":
                continue
            biz_item = self.get_biz_item(item)
            try:
                # go to detail page url
                item_res = self.get_cffi_response(item["url"])
                # parse and populate detail
                biz_item = self.populate_detail(biz_item, item_res)
            except Exception:
                # detail page is deleted or not found
                biz_item["deleted"] = 1
            # random sleeps to protect from rate limiting
            time.sleep(randint(3, 6))
            counter += 1
            if counter % 5 == 0:
                # long delay between 5 results because of rate limiting
                # if ip rotation is enabled this can be ommited
                # time.sleep(10)
                pass
            yield biz_item

    def populate_detail(self, biz_item: BizItem, response: HtmlResponse) -> BizItem:
        # add missing attributes from detail page
        product_data = self.get_product_dict(response)
        if product_data is None:
            return biz_item
        # add full description
        biz_item["description"] = product_data["description"]
        # populate finance details
        finance_data = self.get_finance_detail(response)
        for k, v in finance_data.items():
            biz_item[k] = v
        # populate agent details
        agent_data = self.get_agent_detail(response)
        for k, v in agent_data.items():
            biz_item[k] = v
        return biz_item

    def get_metadata(self, item: dict) -> dict:
        url_paths = self.get_url().split("/")
        url_paths.reverse()
        url_paths.remove("")

        data = {
            "title": item["name"],
            "description": item["description"],
            "industry": url_paths[0],
            "website_url": item["url"],
        }
        if item["offers"]["availableAtOrFrom"]:
            address = item["offers"]["availableAtOrFrom"]["address"]
            locality = address["addressLocality"]
            data["location"] = (
                f'{locality}{"," if locality is not None else ""}{address["addressRegion"]}'
            )

        return data

    def get_biz_item(self, item: dict) -> BizItem:
        """Initialize biz item and populate it with basic data such as title

        Args:
            item (dict): _description_

        Returns:
            BizItem: _description_
        """
        biz_item = BizItem()
        # populate the metadata
        metadata = self.get_metadata(item)
        for k, v in metadata.items():
            biz_item[k] = v
        return biz_item

    def get_finance_detail(self, response: HtmlResponse) -> dict:
        finance_data = {
            "asking_price": "",
            "revenue": "",
            "ebitda": "",
            "cash_flow": "",
        }
        asking_selector = response.xpath(
            "//p[contains(@class, 'asking')]//span[@class='normal flex-center g4']/text()"
        )
        cash_selector = response.xpath(
            "//p[span[contains(text(), 'Cash Flow')]]//span[@class='normal flex-center g4']/text()"
        )
        revenue_selector = response.xpath(
            "//p[span[contains(text(), 'Gross Revenue')]]//span[@class='normal flex-center g4']/text()"
        )
        ebitda_selector = response.xpath(
            "//p[span[contains(text(), 'EBITDA')]]//span[@class='normal flex-center g4']/text()"
        )

        finance_data["asking_price"] = asking_selector.get().strip()
        finance_data["cash_flow"] = cash_selector.get().strip()
        finance_data["revenue"] = revenue_selector.get().strip()
        finance_data["ebitda"] = ebitda_selector.get().strip()
        return finance_data

    def get_agent_detail(self, response: HtmlResponse) -> dict:
        agent_data = {"agent_name": "", "agent_company": "", "agent_phone": ""}
        p = self.get_product_dict(response)
        if p is None:
            return agent_data
        if "offeredBy" in p["offers"]:
            offered_by = p["offers"]["offeredBy"]
            agent_data["agent_name"] = offered_by["name"]
            agent_data["agent_company"] = offered_by["worksFor"]["name"]
            phone_selector = response.xpath(
                '//span[contains(@class, "ctc_phone")]/a/span[@class="text-dec-h"]/text()'
            )
            agent_data["agent_phone"] = phone_selector.get()

        return agent_data

    def get_product_dict(self, response: HtmlResponse) -> Optional[dict]:
        selector = response.xpath('//head//script[@type="application/ld+json"]/text()')
        for s in selector:
            data = json.loads(s.get())
            if data["@type"] == "Product":
                return data
        return None
