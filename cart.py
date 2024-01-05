from nicegui import ui

import global_state
import persistence
import product as product_page


def handle_remove_product(user_cart: dict, product_id: str):
    user_cart.pop(product_id)
    product_list.refresh()


def product_row(
    user_cart: dict,
    products: [dict],
    product: dict,
    products_yarns: [dict],
    product_yarns: [dict],
):
    ui.image(source=product["image_url"])
    ui.label(text=product["name"])
    ui.markdown(content=product["description"])

    with ui.row():
        material_price = ui.label(text=product_page.total_price(product_yarn_records=product_yarns))
        ui.label(text="VND")

    with ui.row():
        ui.label(text="x")
        count = (
            ui.number(label="Count", min=1)
            .bind_value(
                target_object=user_cart,
                target_name=product["id"],
                forward=lambda value: int(value),
            )
            .on(
                type="change",
                handler=lambda _: total_cart_price.refresh(
                    user_cart=user_cart,
                    products=products,
                    products_yarns=products_yarns,
                )
            )
            .classes(add="w-20")
        )
        ui.label(text="=")

    with ui.row():
        ui.label().bind_text_from(
            target_object=count,
            target_name="value",
            backward=lambda count_value: count_value * int(material_price.text)
        )
        ui.label(text="VND")
    with ui.row():
        ui.button(text="Remove", color="deep-orange").on(
            type="click",
            handler=lambda e: handle_remove_product(
                user_cart=user_cart,
                product_id=product["id"],
            )
        )


def add_products_price(products: [dict], products_yarns: [dict]):
    for product in products:
        product_yarns = products_yarns[product["id"]]
        product["price"] = product_page.total_price(product_yarn_records=product_yarns)


def calculate_total_cart_price(user_cart: dict, products: [dict]) -> int:
    total = 0
    for product in products:
        count = user_cart[product["id"]]
        total += count * product["price"]

    return total


@ui.refreshable
def total_cart_price(user_cart: dict, products: [], products_yarns: []):
    add_products_price(products=products, products_yarns=products_yarns)
    total = calculate_total_cart_price(user_cart=user_cart, products=products)
    with ui.row():
        ui.label(text=str(total)).classes(add="text-lg")
        ui.label(text="VND").classes(add="text-lg")


@ui.refreshable
def product_list():
    user_cart = global_state.dict_["user_cart"]
    products = global_state.get_cart_products()
    products_yarns = {
        product["id"]: persistence.get_product_yarns(product_id=product["id"])
        for product in products
    }

    for product in products:
        product_yarns = products_yarns[product["id"]]
        product["price"] = product_page.total_price(product_yarn_records=product_yarns)

    with ui.grid(columns=7):

        ui.label(text="Image").classes(add="text-lg")
        ui.label(text="Name").classes(add="text-lg")
        ui.label(text="Description").classes(add="text-lg")
        ui.label(text="Price").classes(add="text-lg")
        ui.element()
        ui.label(text="Total").classes(add="text-lg")
        ui.element()

        for product in products:
            product_yarns = products_yarns[product["id"]]
            product_row(
                user_cart=user_cart,
                products=products,
                product=product,
                products_yarns=products_yarns,
                product_yarns=product_yarns,
            )

        ui.element()
        ui.element()
        ui.element()
        ui.element()
        ui.element()
        total_cart_price(
            user_cart=user_cart,
            products=products,
            products_yarns=products_yarns,
        )
        ui.element()

    if len(user_cart) > 0:
        text_area_user_message = ui.textarea(
            placeholder=(
                "Do you want to provide additional information "
                "(your phone number or current address etc.)?"
            )
        )
        ui.button(text="Place Order").on(
            type="click",
            handler=lambda _: handle_place_order(user_message=text_area_user_message.value),
        )


def handle_place_order(user_message: str):
    global_state.place_order(user_message=user_message)
    ui.notify(
        message="Your order has been placed successfully. We'll contact you soon!",
        position="top-right",
    )
    product_list.refresh()


@ui.page("/cart")
def page():
    ui.label(text="Cart").classes(add="text-xl")
    product_list()
    ui.link(text="Back", target="/")
