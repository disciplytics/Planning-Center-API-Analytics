import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    """The login page for the application."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("church", class_name="h-12 w-12 text-teal-500"),
                rx.el.h1(
                    "PCO Analytics", class_name="text-3xl font-bold text-gray-800"
                ),
                class_name="flex flex-col items-center gap-4",
            ),
            rx.el.p(
                "Connect your Planning Center account to get started.",
                class_name="text-gray-600 mt-2 text-center",
            ),
            rx.el.a(
                rx.icon("link", class_name="h-5 w-5"),
                "Connect to Planning Center",
                href=AuthState.auth_url,
                class_name="mt-8 inline-flex items-center gap-2 justify-center px-6 py-3 font-semibold text-white bg-teal-600 rounded-lg shadow-md hover:bg-teal-700 transition-all duration-200",
            ),
            class_name="bg-white p-12 rounded-2xl shadow-lg border border-gray-100 max-w-md w-full",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 font-['Inter']",
    )