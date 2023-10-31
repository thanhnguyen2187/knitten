import uuid

from nicegui import ui
import global_state
import components
import persistence


def yarn_row(
    yarn_options: dict,
    product_yarn_record: dict,
    yarn_map: dict,
):
    ui.select(
        options=yarn_options,
        value=product_yarn_record["yarn_id"],
        on_change=lambda e: handle_select_change(e.value)
    )
    color_button = ui.button(color=product_yarn_record["yarn_color"])

    def handle_select_change(yarn_id: str):
        color_button.style(add=f"background-color: {yarn_map[yarn_id]['color']}!important")
        product_yarn_record["yarn_id"] = yarn_id
        product_yarn_record["yarn_price_per_unit"] = yarn_map[yarn_id]["price_per_unit"]

    with ui.row():
        ui.label(text=product_yarn_record["yarn_price_per_unit"])
        ui.label(text="VND")

    ui.number(
        label="Count",
        min=1,
        format="%d",
    ).classes(add="w-12").bind_value(
        target_object=product_yarn_record,
        target_name="yarn_count",
    )

    def handle_click_save():
        persistence.update_product_yarn(record=product_yarn_record)
        ui.notify(message="Updated record successfully.", position="top-right")

    def handle_click_delete():
        persistence.delete_product_yarn(id_=product_yarn_record["id"])
        ui.notify(message="Deleted record successfully.", position="top-right")
        yarn_list.refresh()

    with ui.row():
        ui.button(icon="save").on(
            type="click",
            handler=lambda _: handle_click_save()
        )
        ui.button(icon="delete", color="deep-orange").on(
            type="click",
            handler=lambda _: handle_click_delete()
        )


@ui.refreshable
def yarn_list(product_id: str):
    yarn_records = global_state.get_yarns()
    products_yarns = persistence.get_product_yarns(product_id=product_id)
    yarn_map = {
        record["id"]: record
        for record in yarn_records
    }
    yarn_options = {
        record["id"]: record["name"]
        for record in yarn_records
    }
    ui.label(text="Materials").classes(add="text-lg")

    def handle_click_add():
        persistence.insert_product_yarn(
            record={
                "id": str(uuid.uuid4()),
                "product_id": product_id,
                "yarn_id": yarn_records[0]["id"],
                "yarn_count": 1,
            },
        )
        ui.notify(
            message="Created record successfully.",
            position="top-right",
        )
        yarn_list.refresh()

    with ui.grid(columns=5):
        for products_yarn in products_yarns:
            yarn_row(
                yarn_options=yarn_options,
                product_yarn_record=products_yarn,
                yarn_map=yarn_map,
            )

        ui.element()
        ui.element()
        ui.element()
        ui.element()
        with ui.row():
            ui.button(icon="add").on(
                "click",
                lambda _: handle_click_add()
            )



@ui.page("/edit-product/{id_}")
def page(id_: str):
    product_record = {}
    if id_ == "new":
        product_record = {
            "id": str(uuid.uuid4()),
            "name": "Product name",
            "description": "",
            "patterns": "",
            "image_url": "https://placehold.co/600x400",
        }
    else:
        product_record = global_state.get_product(id_=id_)

    def handle_edit_product():
        global_state.update_product(product_record=product_record)
        global_state.refresh_products()
        components.product_gallery.refresh()
        ui.open(target=f"/product/{product_record['id']}")

    def handle_create_product():
        global_state.create_product(product_record=product_record)
        global_state.refresh_products()

        # A small UX improvement where we always navigate to the latest page
        # that contains the newly-created product.
        global_state.set_page(global_state.calculate_max_page())

        components.product_pagination.refresh()
        components.product_gallery.refresh()
        ui.open(target=f"/product/{product_record['id']}")

    with ui.row():
        ui.image().style(add="width: 400px").bind_source_from(
            target_object=product_record,
            target_name="image_url",
        )
        with ui.column():
            ui.input(label="Name").bind_value(
                target_object=product_record,
                target_name="name",
            ).style(add="width: 200px")
            ui.input(label="Image URL").bind_value(
                target_object=product_record,
                target_name="image_url",
            ).style(add="width: 200px")
            ui.textarea(label="Description").bind_value(
                target_object=product_record,
                target_name="description",
            ).style(add="width: 240px")
            ui.textarea(label="Patterns").bind_value(
                target_object=product_record,
                target_name="patterns",
            ).style(add="width: 240px")
        with ui.column():
            yarn_list(product_record["id"])

    if id_ == "new":
        ui.button(text="Create").on(
            type="click",
            handler=lambda _: handle_create_product()
        )
        ui.link(text="Back", target="/")
    else:
        ui.button(text="Save").on(
            type="click",
            handler=lambda _: handle_edit_product()
        )
        ui.link(text="Back", target=f"/product/{id_}")

