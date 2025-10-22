import reflex as rx
from app.states.state import AppState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.dashboard import dashboard
from app.pages.login import login_page
from app.pages.settings import settings_page
from app.pages.people_page import people_page
from app.states.people_state import PeopleState
from app.states.settings_state import SettingsState


def index() -> rx.Component:
    """The main page of the app."""
    return rx.el.div(
        rx.cond(
            AuthState.is_authenticated,
            rx.fragment(
                sidebar(),
                rx.el.main(
                    header(),
                    dashboard(),
                    class_name=rx.cond(
                        AppState.is_sidebar_open,
                        "transition-all duration-300 ease-in-out ml-64",
                        "transition-all duration-300 ease-in-out ml-20",
                    ),
                ),
            ),
            login_page(),
        ),
        class_name=rx.cond(
            AppState.theme == "dark",
            "font-['Inter'] bg-gray-900 min-h-screen dark",
            "font-['Inter'] bg-gray-50 min-h-screen",
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=AppState.on_load)
app.add_page(
    people_page, route="/people", on_load=[AppState.on_load, PeopleState.on_load]
)
app.add_page(index, route="/teams", on_load=AppState.on_load)
app.add_page(
    settings_page, route="/settings", on_load=[AppState.on_load, SettingsState.on_load]
)
app.add_page(login_page, route="/login")
app.add_page(lambda: rx.fragment(), route="/callback", on_load=AuthState.on_load)