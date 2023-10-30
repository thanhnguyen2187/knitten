import typing
import math

import persistence


dict_ = {
    "logged_in_user": {
        "id": "",
        "username": "thanh",
        "password": "thanh",
        "full_name": "Thanh",
    },
    # "logged_in_user": None,
    "products": [],
    "users": [],
    "search_input": "",
    "page": 1,
    "page_size": 6,
}


def set_logged_in_user(record: dict):
    dict_["logged_in_user"] = record


def refresh_products():
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


def delete_product(id_: str):
    persistence.delete_product(id_=id_)


def update_product(product_record: dict):
    persistence.update_product(product_record=product_record)


def create_product(product_record: dict):
    persistence.insert_product(product_record=product_record)


def calculate_max_page():
    return math.ceil(len(dict_["products"]) / dict_["page_size"])


def set_page(value: int):
    dict_["page"] = value


def update_users():
    users = persistence.get_all_users()
    dict_["users"] = users


def find_user(
    username: str,
    password: str,
) -> typing.Optional[dict]:
    for user_record in dict_["users"]:
        if (
            user_record["username"] == username and
            user_record["password"] == password
        ):
            return user_record
    return None
