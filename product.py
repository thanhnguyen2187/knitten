from nicegui import ui
import global_state


@ui.page("/product/{id_}")
def page(id_: str):
    product = global_state.get_product(id_=id_)
    ui.label(text=product["name"]).classes(add="text-xl")
    with ui.row():
        ui.image(source=product["image_url"]).style(add="width: 400px")
        with ui.column():
            ui.label(text="Materials: ...")
            ui.label(text="Price: ...")
            ui.label(text="Description: ...")
            ui.label(text="Patterns: ...")

    ui.button("Edit Product").bind_visibility_from(
        target_object=global_state.dict_,
        target_name="logged_in",
    )
    ui.link(text="Back", target="/")
