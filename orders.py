from nicegui import ui


@ui.page("/orders")
def page():
    ui.label(text="Orders").classes(add="text-xl")
    with ui.row():
        ui.input(label="Customer Name Or Email").classes(add="w-48")
        ui.select(
            options={
                "waiting": "Waiting",
                "processed": "Processed",
                "shipping": "Shipping",
                "done": "Done",
                "all": "All",
            },
            label="Status",
            value="waiting",
        ).classes(add="w-28")
    with ui.grid(columns=5):
        ui.label(text="Customer").classes(add="text-lg")
        ui.label(text="Products").classes(add="text-lg")
        ui.label(text="Total").classes(add="text-lg")
        ui.label(text="Status").classes(add="text-lg")
        ui.element()

        ui.separator().classes(add='col-span-full')

        with ui.column():
            ui.label(text="Customer name")
            ui.label(text="email@email.com")
        ui.label(text="Three")
        ui.label(text="Four")
        ui.select(
            options={
                "waiting": "Waiting",
                "processed": "Processed",
                "shipping": "Shipping",
                "done": "Done",
                "all": "All",
            },
            label="Status",
            value="waiting",
        )
        with ui.row():
            ui.button(text="Save")
            ui.button(text="Delete", color="deep-orange")
