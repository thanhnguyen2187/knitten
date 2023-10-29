from nicegui import ui
import global_state
import utilities
import admin_components


@ui.page("/login")
def page():
    ui.label("Sign In").classes(add="text-xl")
    input_username = ui.input(label="Username")
    input_password = ui.input(label="Password", password=True, password_toggle_button=True)
    with ui.row():
        ui.link(text="Forgot password?")

    with ui.row():
        ui.button(text="Login").on("click", lambda e: handle_login_click())
        ui.button(text="Sign Up").on("click", lambda e: global_state.set_logged_in(False))

    def handle_login_click():
        if not input_username.value:
            ui.notify("Username should not be blank!", position='top-right')
            return
        if not input_password.value:
            ui.notify("Password should not be blank!", position='top-right')
            return
        global_state.set_logged_in(True)
        utilities.redirect("/")
        # we need this since "simply" redirecting does not show the buttons as expected
        admin_components.buttons.refresh()
