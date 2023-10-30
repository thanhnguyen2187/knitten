import math

import persistence


dict_ = {
    "logged_in": False,
    "products": [],
    "users": [],
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


def get_product(id_: str) -> dict:
    product = next(
        product
        for product in dict_["products"]
        if product["id"] == id_
    )
    return product


def calculate_max_page():
    return math.ceil(len(dict_["products"]) / dict_["page_size"])


def set_page(value: int):
    dict_["page"] = value


def update_users():
    users = persistence.get_all_users()
    dict_["users"] = users


def user_exist(
    username: str,
    password: str,
) -> bool:
    for user_record in dict_["users"]:
        if (
            user_record["username"] == username and
            user_record["password"] == password
        ):
            return True
    return False
