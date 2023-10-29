from nicegui import ui
import login
import sign_up
import admin_components


ui.input(label="Search for product...")

admin_components.buttons()

with ui.grid(columns=2):
    with ui.card():
        ui.image('https://picsum.photos/id/684/800/600')
        with ui.card_section():
            ui.label("Name product 1")
    with ui.card():
        ui.image('https://picsum.photos/id/684/800/600')
        with ui.card_section():
            ui.label("Name product 2")
    with ui.card():
        ui.image('https://picsum.photos/id/684/800/600')
        with ui.card_section():
            ui.label("Name product 3")
    with ui.card():
        ui.image('https://picsum.photos/id/684/800/600')
        with ui.card_section():
            ui.label("Name product 4")
    ui.element("div")
    ui.button("Show more")

with ui.row():
    ui.link(text="Login", target=login.page)
    ui.link(text="Sign up", target=sign_up.page)

ui.run(title="Knitten")
