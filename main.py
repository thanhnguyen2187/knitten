from nicegui import ui
import login
import sign_up
import admin_components

ui.label(text="Knitten 🐱 - Yarn Knitting Management").classes(add="text-xl")

ui.input(label="Search for product...")

admin_components.buttons()

with ui.grid(columns=3):
    with ui.card().classes(add="w-80"):
        ui.image('https://http.cat/images/100.jpg')
        with ui.card_section():
            ui.label("Name product 1")
    with ui.card():
        ui.image('https://http.cat/images/101.jpg')
        with ui.card_section():
            ui.label("Name product 2")
    with ui.card():
        ui.image('https://http.cat/images/102.jpg')
        with ui.card_section():
            ui.label("Name product 3")
    with ui.card():
        ui.image('https://http.cat/images/103.jpg')
        with ui.card_section():
            ui.label("Name product 4")
    with ui.card():
        ui.image('https://http.cat/images/200.jpg')
        with ui.card_section():
            ui.label("Name product 5")
    with ui.card():
        ui.image('https://http.cat/images/201.jpg')
        with ui.card_section():
            ui.label("Name product 6")
ui.button("Show more")

with ui.row():
    ui.link(text="Login", target=login.page)
    ui.link(text="Sign up", target=sign_up.page)

ui.run(title="Knitten", favicon="🐱")
