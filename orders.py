from nicegui import ui

import global_state


def handle_delete_row(id_: str):
    global_state.delete_order(id_=id_)
    orders_list.refresh()


def handle_edit_row(order: dict):
    global_state.update_order(order=order)
    ui.notify(message="Updated order's state")
    orders_list.refresh()


def order_row(order: dict):
    user = order["user"]
    with ui.column():
        ui.label(text=user["full_name"])
        ui.label(text=user["email"])
    with ui.column():
        ui.label().bind_text(
            target_object=order,
            target_name="date_created",
        )
    with ui.column():
        for product in order["products"]:
            ui.image(source=product["product_image_url"])
            with ui.row():
                ui.label(text=product["product_name"])
                ui.label(text="x")
                ui.label(text=product["product_count"])

    with ui.row():
        # ui.element()
        ui.label(text=order["price"]).classes(add="text-lg")
        ui.label(text="VND").classes(add="text-lg")

    ui.textarea(
        placeholder="The user did not provide anything else...",
    ).bind_value(
        target_object=order,
        target_name="user_message",
    ).disable()

    with ui.column():
        ui.select(
            options={
                "pending": "Pending",
                "processing": "Processing",
                "shipping": "Shipping",
                "done": "Done",
            },
            label="Status",
            value="waiting",
        ).bind_value(
            target_object=order,
            target_name="state",
        )

    with ui.row():
        ui.button(text="Save").on(
            type="click",
            handler=lambda _: handle_edit_row(order=order)
        )
        ui.button(text="Delete", color="deep-orange").on(
            type="click",
            handler=lambda _: handle_delete_row(id_=order["id"])
        )


def handle_sort_change():
    orders_list.refresh()


def header():
    with ui.row():
        ui.input(
            label="Customer Name Or Email",
            on_change=lambda _: orders_list.refresh(),
        ).bind_value(
            target_object=global_state.dict_,
            target_name="orders_customer",
        ).classes(add="w-48")
        ui.select(
            options={
                "date_desc": "Newest to Oldest",
                "date_asc": "Oldest to Newest",
                "price_desc": "Most Expensive to Cheapest",
                "price_asc": "Cheapest to Most Expensive",
            },
            label="Sort By",
            value="date_desc",
            on_change=lambda _: handle_sort_change(),
        ).bind_value(
            target_object=global_state.dict_,
            target_name="orders_sort_by",
        )
        ui.select(
            options={
                "pending": "Pending",
                "processing": "Processing",
                "shipping": "Shipping",
                "done": "Done",
            },
            label="Status",
            value="pending",
            clearable=True,
            on_change=lambda _: orders_list.refresh()
        ).bind_value(
            target_object=global_state.dict_,
            target_name="orders_state",
        )


@ui.refreshable
def orders_list():
    global_state.refresh_orders()
    global_state.sort_orders()
    orders = global_state.get_orders()
    with ui.grid(columns=7):
        ui.label(text="Customer").classes(add="text-lg")
        ui.label(text="Date Created").classes(add="text-lg")
        ui.label(text="Products").classes(add="text-lg")
        ui.label(text="Total").classes(add="text-lg")
        ui.label(text="User Message").classes(add="text-lg")
        ui.label(text="Status").classes(add="text-lg")
        ui.element()

        ui.separator().classes(add='col-span-full')

        for order in orders:
            order_row(order=order)


@ui.page("/orders")
def page():
    ui.label(text="Orders").classes(add="text-xl")
    header()
    orders_list()
    ui.link(text="Back", target="/")
