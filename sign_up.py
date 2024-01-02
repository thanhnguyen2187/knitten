import uuid

from nicegui import ui

import global_state
import persistence
import components


def handle_submit(username: str, full_name: str, password: str):
    persistence.insert_user({
        "id": str(uuid.uuid4()),
        "full_name": full_name,
        "username": username,
        "password": password,
    })

    global_state.refresh_users()
    ui.open(target="/login")
    # TODO: find a way to notify user that the registration succeeded
    ui.notify(
        message="Inserted user successfully!",
        position="top-right",
    )


@ui.page("/sign-up")
def page():
    ui.label("Sign Up").classes(add="text-xl")
    input_username = ui.input(
        label="Username",
        validation={
            "Blank input": lambda value: len(value) != 0,
            "Input should be less than 32 characters": lambda value: len(value) <= 32,
        },
    )
    input_full_name = ui.input(
        label="Full name",
        validation={
            "Blank input": lambda value: len(value) != 0,
            "Input should be less than 50 characters": lambda value: len(value) <= 50,
        },
    )
    input_password = ui.input(
        label="Password",
        password=True,
        password_toggle_button=True,
        validation={
            "Blank input": lambda value: len(value) != 0,
            "Input should be less than 32 characters": lambda value: len(value) <= 32,
        },
    )
    input_password_repeat = ui.input(
        label="Repeat password",
        password=True,
        password_toggle_button=True,
        validation={
            "Blank input": lambda value: len(value) != 0,
            "Unmatched password": lambda value: value == input_password.value,
        },
    )

    with ui.row():
        ui.button(
            text="Submit",
            on_click=lambda e: handle_submit(
                username=input_username.value,
                full_name=input_full_name.value,
                password=input_password.value,
            ),
        )
        ui.button(text="Reset")

    ui.link(text="Back", target="/login")

