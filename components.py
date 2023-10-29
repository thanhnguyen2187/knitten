from nicegui import ui
from global_state import dict_


@ui.refreshable
def buttons():
    with ui.row().classes(add="justify-between").bind_visibility_from(
        target_object=dict_,
        target_name="logged_in",
    ):
        ui.button(text="Add new product")
        ui.button(text="Edit materials")
