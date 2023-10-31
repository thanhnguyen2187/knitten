from nicegui import ui
import components
import global_state

global_state.refresh_products()
global_state.refresh_yarns()
global_state.update_users()

ui.label(text="Knitten 🐱 - Yarn Knitting Management").classes(add="text-xl")

components.search_bar()
components.admin_buttons()
components.product_gallery()
components.product_pagination()
components.footer()

ui.run(title="Knitten", favicon="🐱", dark=True)
