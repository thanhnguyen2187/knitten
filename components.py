import typing
from nicegui import ui

import global_state
import login
import sign_up
import yarns
import orders


@ui.refreshable
def header_buttons():
    with ui.row().classes(add="justify-between").bind_visibility_from(
        target_object=global_state.dict_,
        target_name="logged_in_user",
        backward=lambda value: value is not None and value["role"] == "owner",
    ):
        ui.button(text="Add New Product").on(
            "click",
            lambda _: ui.open(target="/edit-product/new"),
        )
        ui.button(text="Edit Materials").on(
            "click",
            lambda _: ui.open(target=yarns.page)
        )
        ui.button(text="View Orders").on(
            "click",
            lambda _: ui.open(target=orders.page)
        )

    with ui.row().classes(add="justify-between").bind_visibility_from(
        target_object=global_state.dict_,
        target_name="logged_in_user",
        backward=lambda value: value is not None and value["role"] == "customer",
    ):
        ui.button(text="View Cart").on(
            "click",
            lambda _: ui.open(target="/cart"),
        )


def handle_change_search():
    global_state.refresh_products()
    global_state.set_page(1)
    product_pagination.refresh()
    product_gallery.refresh()


@ui.refreshable
def search_bar():
    ui.input(label="Search for product...").bind_value_to(
        target_object=global_state.dict_,
        target_name="search_input",
    ).on(
        "change",
        lambda e: handle_change_search(),
    )


def handle_sort_change():
    global_state.sort_products()
    product_pagination.refresh()
    product_gallery.refresh()


def sort_select():
    ui.select(
        options={
            "name_asc": "Product Name Ascending (A - Z)",
            "name_desc": "Product Name Descending (Z - A)",
            "price_asc": "Cheapest to Most Expensive",
            "price_desc": "Most Expensive to Cheapest",
        },
        value="name_asc",
        on_change=lambda _: handle_sort_change()
    ).bind_value(
        target_object=global_state.dict_,
        target_name="products_sort_by",
    )


def create_handle_add_to_cart(product_id: str):
    def handle_add_to_cart(_):
        global_state.add_to_cart(product_id=product_id)
        ui.notify(
            message="Added product to cart",
            position="top-right",
        )

    return handle_add_to_cart


@ui.refreshable
def product_gallery():
    with ui.grid(columns=3):
        for product_record in global_state.get_products():
            with ui.card().classes(add="w-80"):
                ui.image(source=product_record["image_url"])
                with ui.card_section():
                    ui.link(
                        text=product_record["name"],
                        target="/product/" + product_record["id"],
                    )

                if global_state.get_user_role() == "customer":
                    ui.button(text="Add To Cart").on(
                        type="click",
                        handler=create_handle_add_to_cart(product_id=product_record["id"]),
                    )


def handle_change_page(
    action: typing.Literal['increase', 'decrease', 'first', 'last', 'custom'],
    value: int = 0,
):
    match action:
        case 'increase':
            global_state.set_page(global_state.dict_["page"] + 1)
        case 'decrease':
            global_state.set_page(global_state.dict_["page"] - 1)
        case 'first':
            global_state.set_page(1)
        case 'last':
            global_state.set_page(global_state.calculate_max_page())
        case 'custom':
            global_state.set_page(value=value)

    product_pagination.refresh()
    product_gallery.refresh()


@ui.refreshable
def product_pagination():
    with ui.row():
        ui.button("First").bind_enabled_from(
            target_object=global_state.dict_,
            target_name="page",
            backward=lambda value: value != 1,
        ).on(
            "click",
            lambda e: handle_change_page(action="first"),
        )
        ui.button("Previous").bind_enabled_from(
            target_object=global_state.dict_,
            target_name="page",
            backward=lambda value: value != 1,
        ).on(
            "click",
            lambda e: handle_change_page(action="decrease"),
        )

        ui.label().bind_text(
            target_object=global_state.dict_,
            target_name="page",
        )
        ui.label(text="/")
        ui.label(text=str(global_state.calculate_max_page()))

        ui.button("Next").bind_enabled_from(
            target_object=global_state.dict_,
            target_name="page",
            backward=lambda value: value != global_state.calculate_max_page(),
        ).on(
            "click",
            lambda e: handle_change_page(action="increase"),
        )
        ui.button("Last").bind_enabled_from(
            target_object=global_state.dict_,
            target_name="page",
            backward=lambda value: value != global_state.calculate_max_page(),
        ).on(
            "click",
            lambda e: handle_change_page(action="last"),
        )


def handle_log_out():
    global_state.dict_["logged_in_user"] = None
    footer.refresh()
    ui.open(target="/login")


@ui.refreshable
def footer():
    user_record = global_state.dict_["logged_in_user"]
    if user_record is None:
        with ui.row():
            ui.link(text="Sign up", target=sign_up.page)
            ui.link(text="Login", target=login.page)
    else:
        with ui.row():
            ui.label(text=f"Hello {user_record['full_name']}!")
            ui.link(text="Logout").on(
                "click",
                lambda e: handle_log_out()
            )
