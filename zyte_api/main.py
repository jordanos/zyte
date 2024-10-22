import asyncio
import os

from dotenv import load_dotenv

from zyte_api import AsyncZyteAPI

load_dotenv()  # take environment variables from .env.

API_KEY = os.environ.get("ZYTE_API_KEY", None)
if API_KEY is None:
    raise ValueError("Zyte API_KEY is not set.")

client = AsyncZyteAPI(api_key=API_KEY)


async def get_listings(url: str):
    api_response = await client.get(
        {
            "url": url,
            "httpResponseBody": True,
            "productList": True,
            "productListOptions": {"extractFrom": "httpResponseBody"},
        }
    )
    listings = api_response["productList"]
    # we can get the detail page url, offer and title
    return listings


def parse_detail(product: dict):
    biz_item = {
        "title": None,
        "description": None,
        "industry": None,
        "location": None,
        "asking_price": None,
        "revenue": None,
        "ebitda": None,
        "cash_flow": None,
        "agent_name": None,
        "agent_company": None,
        "agent_phone": None,
        "website_url": None,
        "created_at": None,
        "updated_at": None,
        "deleted": 0,
    }

    custom = product["customAttributes"]["values"]

    biz_item["title"] = product["product"]["name"]
    biz_item["description"] = product["product"]["description"]
    biz_item["asking_price"] = custom["asking_price"]
    biz_item["cash_flow"] = custom["cash_flow"]
    # TODO: populate remaning fields

    return biz_item


async def get_detail(url: str):
    api_response = await client.get(
        {
            "url": url,
            "product": True,
            "productOptions": {"extractFrom": "httpResponseBody"},
            "customAttributes": {
                "asking_price": {
                    "type": "string",
                    "description": "The asking price or offer of the product or business",
                },
                "cash_flow": {
                    "type": "string",
                    "description": "The cash flow of the product or business listing",
                },
                # add more custom fields that aren't in the product detail
            },
        }
    )
    return api_response


async def get_biz_details(listings_url: str):
    products = await get_listings(url=listings_url)
    products = products["products"]
    details = []
    for p in products:
        detail = await get_detail(url=p["url"])
        details.append(parse_detail(detail))
        # only get the first listing or now
        break
    return details


async def main():
    listing_details = await get_biz_details(
        "https://www.bizbuysell.com/building-and-construction-established-businesses-for-sale/"
    )
    print(listing_details)


asyncio.run(main())
