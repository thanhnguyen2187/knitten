from nicegui import ui
import components
import global_state


@ui.page("/product/{id_}")
def page(id_: str):
    product = global_state.get_product(id_=id_)
    ui.label(text=product["name"]).classes(add="text-xl")
    with ui.row():
        ui.image(source=product["image_url"]).style(add="width: 400px")
        with ui.column():
            ui.label(text="Materials").classes(add="text-lg")
            ui.label(text="Price").classes(add="text-lg")
            ui.label(text="Description").classes(add="text-lg")
            ui.markdown(content=product["description"])
            ui.label(text="Patterns").classes(add="text-lg")

    def handle_delete_product():
        global_state.delete_product(id_=id_)
        components.update_product_gallery()
        components.update_product_pagination()
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

    with ui.row():
        ui.button(text="Edit Product").bind_visibility_from(
            target_object=global_state.dict_,
            target_name="logged_in_user",
            backward=lambda value: value is not None,
        )
        ui.button(
            text="Delete Product",
            color="deep-orange",
        ).bind_visibility_from(
            target_object=global_state.dict_,
            target_name="logged_in_user",
            backward=lambda value: value is not None,
        ).on(
            "click",
            lambda _: dialog.open(),
        )

    ui.link(text="Back", target="/")

