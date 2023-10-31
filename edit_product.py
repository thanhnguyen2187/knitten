import uuid

from nicegui import ui
import global_state
import components


@ui.refreshable
def yarn_list():
    yarn_records = global_state.get_yarns()
    yarn_map = {
        record["id"]: record
        for record in yarn_records
    }
    yarn_options = {
        record["id"]: record["name"]
        for record in yarn_records
    }
    yarn_colors = {
        record["id"]: record["color"]
        for record in yarn_records
    }
    ui.label(text="Materials").classes(add="text-lg")

    state = {}
    with ui.grid(columns=5):
        ui.select(
            options=yarn_options,
            value=yarn_records[0]["id"],
            on_change=lambda e: color_button.style(add=f"background-color: {yarn_colors[e.value]}!important")
        ).bind_value(
            target_object=state,
            target_name="yarn_id",
        )
        color_button = ui.button(color="red")
        with ui.row():
            ui.label(text="20000")
            ui.label(text="VND")
        ui.number(
            label="Count",
            min=1,
            format="%d",
            value=1,
        ).classes(add="w-12")
        with ui.row():
            ui.button(icon="save")
            ui.button(icon="delete")

        ui.select(
            options=["red", "green", "blue"],
            value="green",
        )
        ui.button(color="green")
        with ui.row():
            ui.label(text="20000")
            ui.label(text="VND")
        ui.number(
            label="Count",
            min=1,
            format="%d",
            value=1,
        ).classes(add="w-12")
        with ui.row():
            ui.button(icon="save")
            ui.button(icon="delete")

        ui.element()
        ui.element()
        ui.element()
        ui.element()
        with ui.row():
            ui.button(icon="add")



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
            yarn_list()

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

