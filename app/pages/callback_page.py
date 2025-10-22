import reflex as rx
from app.states.auth_state import AuthState


def callback_page() -> rx.Component:
    """The callback page for handling OAuth authentication."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.spinner(class_name="h-12 w-12 text-teal-500"),
                rx.el.h2(
                    "Authenticating...",
                    class_name="text-2xl font-bold text-gray-800 mt-6",
                ),
                rx.el.p(
                    "Please wait while we connect to your Planning Center account.",
                    class_name="text-gray-600 mt-2",
                ),
                class_name="flex flex-col items-center justify-center p-12 bg-white rounded-2xl shadow-lg border border-gray-100",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.el.h3(
                        "Authentication Failed", class_name="font-bold text-red-600"
                    ),
                    rx.el.p(
                        AuthState.error_message, class_name="text-sm text-red-500 mt-2"
                    ),
                    rx.el.a(
                        "Try again",
                        href="/login",
                        class_name="mt-4 inline-block px-4 py-2 text-sm font-semibold text-white bg-teal-600 rounded-lg hover:bg-teal-700 transition-colors",
                    ),
                    class_name="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg text-center",
                ),
            ),
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 font-['Inter']",
    )