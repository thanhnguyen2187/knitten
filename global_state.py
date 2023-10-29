import persistence


dict_ = {
    "logged_in": False,
    "products": [],
    "search_input": "",
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
    return dict_["products"]
