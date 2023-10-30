from nicegui import ui
import login
import sign_up
import components
import global_state

global_state.update_products()
global_state.update_users()

ui.label(text="Knitten 🐱 - Yarn Knitting Management").classes(add="text-xl")

(
    ui
    .input(label="Search for product...")
    .bind_value_to(
        target_object=global_state.dict_,
        target_name="search_input",
    )
    .on(
        "change",
        lambda e: components.update_product_gallery(),
    )
)

components.admin_buttons()
components.product_gallery()

components.product_pagination()

with ui.row():
    ui.link(text="Login", target=login.page)
    ui.link(text="Sign up", target=sign_up.page)

ui.run(title="Knitten", favicon="🐱", dark=True)
