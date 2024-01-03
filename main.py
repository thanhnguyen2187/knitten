from nicegui import ui
import global_state

# import to make the pages work
import home
import product
import edit_product
import cart

global_state.refresh_products()
global_state.refresh_yarns()
global_state.refresh_users()


ui.run(title="Knitten", favicon="🐱", dark=True)
