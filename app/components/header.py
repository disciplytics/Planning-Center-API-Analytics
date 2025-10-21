import reflex as rx
from app.states.state import AppState


def header() -> rx.Component:
    """The header component."""
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="h-6 w-6 text-gray-600"),
                on_click=AppState.toggle_sidebar,
                class_name="p-2 rounded-full hover:bg-gray-200 transition-colors",
            ),
            rx.el.h2(
                AppState.active_page, class_name="text-2xl font-bold text-gray-800"
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Search...",
                    class_name="w-full bg-transparent focus:outline-none text-gray-700 placeholder-gray-500",
                ),
                rx.icon("search", class_name="h-5 w-5 text-gray-500"),
                class_name="flex items-center bg-gray-100 border border-gray-200 rounded-lg px-4 py-2 w-64",
            ),
            rx.el.button(
                rx.icon("bell", class_name="h-6 w-6 text-gray-600"),
                class_name="p-2 rounded-full hover:bg-gray-200 transition-colors",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex justify-between items-center p-4 bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-40",
    )