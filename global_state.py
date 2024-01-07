import typing
import math

import persistence


dict_ = {
    # "logged_in_user": None,
    "logged_in_user": {
        "id": "fa39c270-4a9e-47de-bcef-1d137c201e3b",
        "role": "owner",
        "username": "knitten",
        "email": "admin@knitten.k",
        "full_name": "Knitten Admin",
        "password": "knitten",
    },
    # "logged_in_user": {
    #     "id": "dabad991-9573-4835-ad9c-f8e606e6a025",
    #     "role": "customer",
    #     "username": "customer",
    #     "email": "customer@customer.c",
    #     "full_name": "Customer",
    #     "password": "customer",
    # },
    "user_cart": {},
    "products": [],
    "products_sort_by": "name_asc",
    "users": [],
    "yarns": [],
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
    for product in products:
        product["price"] = persistence.get_product_price(id_=product["id"])
    dict_["products"] = products
    sort_products()


def sort_products():
    by = dict_["products_sort_by"]
    products = dict_["products"]
    match by:
        case "name_asc":
            products.sort(key=lambda product: product["name"])
        case "name_desc":
            products.sort(key=lambda product: product["name"], reverse=True)
        case "price_asc":
            products.sort(key=lambda product: product["price"])
        case "price_desc":
            products.sort(key=lambda product: product["price"], reverse=True)


def refresh_yarns():
    yarns = persistence.get_all_yarns()
    dict_["yarns"] = yarns


def get_products():
    begin = (dict_["page"] - 1) * (dict_["page_size"])
    end = dict_["page"] * dict_["page_size"]
    return dict_["products"][begin:end]


def get_yarns():
    return dict_["yarns"]


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


def get_page() -> int:
    return dict_["page"]


def refresh_users():
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


def add_to_cart(product_id: str):
    if product_id in dict_["user_cart"]:
        dict_["user_cart"][product_id] += 1
    else:
        dict_["user_cart"][product_id] = 1


def get_cart_products():
    products = [
        get_product(product_id)
        for product_id in dict_["user_cart"]
    ]
    return products


def get_user_role():
    if dict_["logged_in_user"]:
        # noinspection PyUnresolvedReferences
        return dict_["logged_in_user"]["role"]

    return None


def place_order(user_message: str):
    persistence.insert_order(
        cart=dict_["user_cart"],
        user_id=dict_["logged_in_user"]["id"],
        user_message=user_message,
    )
    dict_["user_cart"] = {}
