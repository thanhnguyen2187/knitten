from nicegui import ui


@ui.page("/product/{id_}")
def page(id_: str):
    ui.label("Hello world")
    ui.label(id_)
