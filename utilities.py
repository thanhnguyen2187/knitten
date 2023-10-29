from nicegui import ui


def redirect(url: str):
    ui.run_javascript(code=f"window.location.replace('{url}')")
