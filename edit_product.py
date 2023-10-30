from nicegui import ui
import global_state
import components


@ui.page("/edit-product/{id_}")
def page(id_: str):
    product = global_state.get_product(id_=id_)

    def handle_edit_product():
        global_state.update_product(product_record=product)
        components.update_product_gallery()
        components.update_product_pagination()
        ui.open(target=f"/product/{id_}")

    with ui.row():
        ui.image().style(add="width: 400px").bind_source_from(
            target_object=product,
            target_name="image_url",
        )
        with ui.column():
            ui.input(label="Name").bind_value(
                target_object=product,
                target_name="name",
            ).style(add="width: 200px")
            ui.input(label="Image URL").bind_value(
                target_object=product,
                target_name="image_url",
            ).style(add="width: 200px")
            ui.textarea(label="Description").bind_value(
                target_object=product,
                target_name="description",
            ).style(add="width: 240px")
            ui.textarea(label="Patterns").bind_value(
                target_object=product,
                target_name="patterns",
            ).style(add="width: 240px")

    ui.button(text="Save").on(
        type="click",
        handler=lambda _: handle_edit_product()
    )
    # TODO: fix a bug where clicking "Back" in here and "Back" in the product
    #       page leads to inconsistent state
    ui.link(text="Back", target=f"/product/{id_}")
