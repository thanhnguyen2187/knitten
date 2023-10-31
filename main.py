from nicegui import ui
import global_state

# import for side effect
import home
# import product
import edit_product

global_state.refresh_products()
global_state.refresh_yarns()
global_state.update_users()


ui.run(title="Knitten", favicon="🐱", dark=True)
