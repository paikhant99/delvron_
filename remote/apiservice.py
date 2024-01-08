import requests

from business.models import Item, Product

URL = "http://192.168.1.8:8000/"
ITEMS = "items/"
GET_PRODUCTS = "get_products/"
NEW_PRODUCT = "new_product"


class ApiService:
    """
    Class that will be in later versions.
    """

    def get_items_response(self):
        try:
            _response = requests.get(URL + ITEMS)
            return [Item(*json_data.values()) for json_data in _response.json()]
        except requests.RequestException as e:
            raise e

    def get_products_response(self):
        try:
            _response = requests.get(URL + GET_PRODUCTS)
            return [Product(*list(json_data.values())[:4], item=Item(*list(json_data.values())[4].values())) for json_data in _response.json()]
        except requests.RequestException as e:
            raise e

    def post_product(self, _item_id, _local_price, _distributor_price, _distributor_set_qty):
        #todo implement post method for calling new product
        requests.post(URL+NEW_PRODUCT)
