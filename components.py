from nicegui import ui
import global_state


@ui.refreshable
def admin_buttons():
    with ui.row().classes(add="justify-between").bind_visibility_from(
        target_object=global_state.dict_,
        target_name="logged_in",
    ):
        ui.button(text="Add new product")
        ui.button(text="Edit materials")


@ui.refreshable
def product_gallery():
    with ui.grid(columns=3):
        for product in global_state.get_products()[:6]:
            with ui.card().classes(add="w-80"):
                ui.image(source=product["image_url"])
                with ui.card_section():
                    ui.label(text=product["name"])


def update_product_gallery():
    global_state.update_products()
    product_gallery.refresh()
