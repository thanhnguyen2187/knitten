from nicegui import ui
import global_state
import components


@ui.page("/login")
def page():
    ui.label("Sign In").classes(add="text-xl")
    input_username = ui.input(label="Username")
    input_password = ui.input(label="Password", password=True, password_toggle_button=True)

    ui.button(text="Login").on("click", lambda e: handle_login_click())
    with ui.row():
        ui.link(text="Sign up", target="/sign-up")

    def handle_login_click():
        if not input_username.value:
            ui.notify("Username should not be blank!", position="top-right")
            return
        if not input_password.value:
            ui.notify("Password should not be blank!", position="top-right")
            return

        user_record = global_state.find_user(
            username=input_username.value,
            password=input_password.value,
        )
        if user_record is not None:
            global_state.set_logged_in_user(record=user_record)
            ui.open(target="/")
            # we need this since redirecting does not show the buttons as expected
            components.header.refresh()
            components.footer.refresh()
        else:
            ui.notify("Wrong username or password", position="top-right")
