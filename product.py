from nicegui import ui
import components
import global_state
import persistence


def requirement_list(requirements: list):
    total = total_price(requirements=requirements)
    sum_unit = total_unit(requirements=requirements)
    with ui.grid(columns=7):
        for yarn_record in requirements:
            ui.label(text=yarn_record["name"])
            ui.button(color=yarn_record["color"])
            ui.label(text=yarn_record["price_per_unit"])
            ui.label(text="VND")
            ui.label(text="x")
            ui.label(text=yarn_record["count"])
            if yarn_record["count"] == 1:
                ui.label("ball")
            else:
                ui.label("balls")

        ui.label(text="Total").classes(add="text-lg")
        ui.element()
        ui.label(text=str(total)).classes(add="text-lg")
        ui.label(text="VND").classes(add="text-lg")
        ui.label(text=" ")
        ui.label(text=str(sum_unit)).classes(add="text-lg")
        if sum_unit == 1:
            ui.label("ball").classes(add="text-lg")
        else:
            ui.label("balls").classes(add="text-lg")


def total_price(requirements: list):
    result = 0
    for requirement in requirements:
        result += requirement["price_per_unit"] * requirement["count"]
    return result


def total_unit(requirements: list):
    result = 0
    for requirement in requirements:
        result += requirement["count"]
    return result


@ui.page("/product/{id_}")
def page(id_: str):
    product = global_state.get_product(id_=id_)
    ui.label(text=product["name"]).classes(add="text-2xl")
    with ui.row():
        ui.image(source=product["image_url"]).style(add="width: 400px")
        with ui.column():
            ui.label(text="Materials").classes(add="text-lg")
            requirements = persistence.get_product_yarns(product_id=id_)
            requirement_list(requirements=requirements)
            ui.label(text="Description").classes(add="text-lg")
            ui.markdown(content=product["description"])
            ui.label(text="Patterns").classes(add="text-lg")
            ui.markdown(content=product["patterns"])

    def handle_delete_product():
        global_state.delete_product(id_=id_)
        global_state.refresh_products()

        # Ensure that the current page does not become invalid after we remove
        # one product.
        #
        # For example:
        # - Our page size is 6, and
        # - There is precisely 13 products, then
        # - We are going to have 3 pages.
        # - Removing one product means the maximal page number becomes 2.
        #
        # If the current page number is 3, then we are going to have invalid
        # state on clicking "Back".
        #
        max_page = global_state.calculate_max_page()
        if global_state.get_page() >= max_page:
            global_state.set_page(max_page)

        components.product_pagination.refresh()
        components.product_gallery.refresh()
        ui.open(target="/")

    with ui.dialog() as dialog, ui.card():
        ui.label(text="Are you sure you want to delete this?")
        with ui.row():
            ui.button(text="Yes").on(
                "click",
                lambda _: handle_delete_product()
            )
            ui.button(text="No").on(
                "click",
                lambda _: dialog.close()
            )

    with ui.row().bind_visibility_from(
        target_object=global_state.dict_,
        target_name="logged_in_user",
        backward=lambda value: value is not None,
    ):
        ui.button(text="Edit Product").on(
            "click",
            lambda _: ui.open(target=f"/edit-product/{id_}"),
        )
        ui.button(text="Delete Product", color="deep-orange").on(
            "click",
            lambda _: dialog.open(),
        )

    ui.link(text="Back", target="/")

