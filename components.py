from nicegui import ui
import global_state
import product
import typing


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
        for product_record in global_state.get_products():
            with ui.card().classes(add="w-80"):
                ui.image(source=product_record["image_url"])
                with ui.card_section():
                    ui.link(
                        text=product_record["name"],
                        target="/product/" + product_record["id"],
                    )
                    ui.label(text=product_record["description"])


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


def update_product_gallery():
    global_state.update_products()
    product_gallery.refresh()
    global_state.set_page(1)
    product_pagination.refresh()
