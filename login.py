from nicegui import ui
import global_state
import components


@ui.page("/login")
def page():
    ui.label("Sign In").classes(add="text-xl")
    input_username = ui.input(label="Username")
    input_password = ui.input(label="Password", password=True, password_toggle_button=True)
    with ui.row():
        ui.link(text="Forgot password?")

    ui.button(text="Login").on("click", lambda e: handle_login_click())

    def handle_login_click():
        if not input_username.value:
            ui.notify("Username should not be blank!", position="top-right")
            return
        if not input_password.value:
            ui.notify("Password should not be blank!", position="top-right")
            return

        if global_state.user_exist(username=input_username.value, password=input_password.value):
            global_state.set_logged_in(True)
            ui.open(target="/")
            # we need this since redirecting does not show the buttons as expected
            components.admin_buttons.refresh()
        else:
            ui.notify("Wrong username or password", position="top-right")
