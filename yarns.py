import uuid

from nicegui import ui

import global_state
import persistence


def generate_row(yarn_record: dict):

    def handle_click_update():
        persistence.update_yarn(yarn_record=yarn_record)
        ui.notify(message="Updated record successfully", position="top-right")

    def handle_color_change(color: str):
        color_button.style(add=f"background-color: {color}!important")
        yarn_record["color"] = color

    def handle_click_delete():
        persistence.delete_yarn(id_=yarn_record["id"])
        ui.notify(message="Deleted record successfully", position="top-right")
        global_state.refresh_yarns()
        table.refresh()

    ui.input(label="Name").bind_value(
        target_object=yarn_record,
        target_name="name",
    )
    with ui.button(color=yarn_record["color"]) as color_button:
        ui.color_picker(on_pick=lambda e: handle_color_change(e.color), value=False)
    ui.number(
        min=0,
        suffix="VND",
        format="%d",
    ).bind_value(
        target_object=yarn_record,
        target_name="price_per_unit",
    )
    with ui.row():
        ui.button(text="Update").on(
            "click",
            lambda _: handle_click_update()
        )
        ui.button(
            text="Delete",
            color="deep-orange",
        ).on(
            "click",
            lambda _: handle_click_delete()
        )


@ui.refreshable
def table():

    def handle_click_add():
        persistence.insert_yarn(
            yarn_record={
                "id": str(uuid.uuid4()),
                "name": "",
                "color": "#ffffff",
                "price_per_unit": 20000,
            },
        )
        global_state.refresh_yarns()
        table.refresh()

    with ui.grid(columns=4):
        ui.label("Name").classes(add="text-bold")
        ui.label("Color").classes(add="text-bold")
        ui.label("Price").classes(add="text-bold")
        ui.label("Actions").classes(add="text-bold")

        for yarn_record in global_state.get_yarns():
            generate_row(yarn_record=yarn_record)

        ui.element()
        ui.element()
        ui.element()
        with ui.row():
            ui.button(text="Add").on(
                type="click",
                handler=lambda e: handle_click_add()
            )


@ui.page("/yarns")
def page():
    # do this to make sure that the unsaved changes are reset on page load
    global_state.refresh_yarns()
    ui.label("Yarns Management").classes(add="text-xl")
    table()

    ui.link(text="Back", target="/")
