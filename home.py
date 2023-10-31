from nicegui import ui

import components


@ui.page("/")
def page():
    ui.label(text="Knitten 🐱 - Yarn Knitting Management").classes(add="text-xl")

    components.search_bar()
    components.admin_buttons()
    components.product_gallery()
    components.product_pagination()
    components.footer()

