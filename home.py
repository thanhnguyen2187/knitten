from nicegui import ui
from fastapi.responses import RedirectResponse

import components
import global_state


@ui.page("/")
def page():
    if not global_state.dict_["logged_in_user"]:
        return RedirectResponse('/login')

    ui.label(text="Knitten 🐱 - Yarn Knitting Management").classes(add="text-xl")

    components.search_bar()
    components.header()
    components.product_gallery()
    components.product_pagination()
    components.footer()

