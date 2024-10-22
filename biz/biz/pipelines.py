import json

import requests

BIN_BASE_URL = "https://api.jsonbin.io/v3"
MASTER_KEY = ""
ACCESS_KEY = ""
COLLECTION_ID = ""


def save_json_to_cloud(data: dict) -> None:
    """Store json data on cloud

    Args:
        data (dict): _description_

    Yields:
        _type_: _description_
    """
    url = BIN_BASE_URL + "/b"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": MASTER_KEY,
        "X-Access-Key": ACCESS_KEY,
        "X-Collection-Id": COLLECTION_ID,
    }
    requests.post(url=url, headers=headers, json=data)


class LocalJsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open("items.json", "a")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class CloudJsonWriterPipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        data = json.dumps(dict(item))
        save_json_to_cloud(data)
        return item
