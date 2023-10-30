import math

import persistence


dict_ = {
    "logged_in": False,
    "products": [],
    "search_input": "",
    "page": 1,
    "page_size": 6,
}


def set_logged_in(value: bool):
    dict_["logged_in"] = value


def update_products():
    products = persistence.get_all_products()
    products = [
        product
        for product in products
        if dict_["search_input"].lower() in product["name"].lower()
    ]
    dict_["products"] = products


def get_products():
    begin = (dict_["page"] - 1) * (dict_["page_size"])
    end = dict_["page"] * dict_["page_size"]
    return dict_["products"][begin:end]


def calculate_max_page():
    return math.ceil(len(dict_["products"]) / dict_["page_size"])


def set_page(value: int):
    dict_["page"] = value
