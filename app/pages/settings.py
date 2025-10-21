import reflex as rx
from app.states.state import AppState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar
from app.components.header import header


def settings_page() -> rx.Component:
    """The settings page for the application."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "API Connection", class_name="text-xl font-bold text-gray-800"
                    ),
                    rx.el.p(
                        "Manage your connection to the Planning Center API.",
                        class_name="text-gray-500 mt-1",
                    ),
                    rx.el.div(
                        rx.cond(
                            AuthState.is_authenticated,
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "check_check",
                                        class_name="h-5 w-5 text-green-500",
                                    ),
                                    rx.el.p(
                                        "Connected to Planning Center",
                                        class_name="font-medium text-gray-700",
                                    ),
                                    class_name="flex items-center gap-2",
                                ),
                                rx.el.button(
                                    "Disconnect",
                                    on_click=AuthState.logout,
                                    class_name="px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors",
                                ),
                                class_name="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "circle_x", class_name="h-5 w-5 text-red-500"
                                    ),
                                    rx.el.p(
                                        "Not Connected to Planning Center",
                                        class_name="font-medium text-gray-700",
                                    ),
                                    class_name="flex items-center gap-2",
                                ),
                                rx.el.a(
                                    "Connect",
                                    href=AuthState.auth_url,
                                    class_name="px-4 py-2 text-sm font-semibold text-white bg-teal-600 rounded-lg hover:bg-teal-700 transition-colors",
                                ),
                                class_name="flex items-center justify-between p-4 bg-red-50 border border-red-200 rounded-lg",
                            ),
                        ),
                        class_name="mt-6",
                    ),
                    class_name="bg-white p-8 rounded-2xl border border-gray-100 shadow-sm",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Preferences", class_name="text-xl font-bold text-gray-800"
                    ),
                    rx.el.p(
                        "Customize the application appearance and behavior.",
                        class_name="text-gray-500 mt-1",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Theme", class_name="font-medium text-gray-700"
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("sun", class_name="h-5 w-5"),
                                    "Light",
                                    on_click=lambda: AppState.set_theme("light"),
                                    class_name=rx.cond(
                                        AppState.theme == "light",
                                        "inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-teal-600 rounded-l-lg",
                                        "inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-l-lg",
                                    ),
                                ),
                                rx.el.button(
                                    rx.icon("moon", class_name="h-5 w-5"),
                                    "Dark",
                                    on_click=lambda: AppState.set_theme("dark"),
                                    class_name=rx.cond(
                                        AppState.theme == "dark",
                                        "inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-teal-600 rounded-r-lg",
                                        "inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-r-lg",
                                    ),
                                ),
                                class_name="flex",
                            ),
                            class_name="flex items-center justify-between",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Data Sync Interval",
                                class_name="font-medium text-gray-700",
                                html_for="sync-interval",
                            ),
                            rx.el.select(
                                rx.el.option("5 minutes", value="5"),
                                rx.el.option("15 minutes", value="15"),
                                rx.el.option("30 minutes", value="30"),
                                rx.el.option("1 hour", value="60"),
                                rx.el.option("Manual", value="0"),
                                id="sync-interval",
                                on_change=AppState.set_sync_interval,
                                default_value=AppState.sync_interval,
                                class_name="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500",
                            ),
                            class_name="flex items-center justify-between mt-4",
                        ),
                        class_name="mt-6",
                    ),
                    class_name="bg-white p-8 rounded-2xl border border-gray-100 shadow-sm mt-6",
                ),
                class_name="p-6 max-w-4xl mx-auto",
            ),
            class_name=rx.cond(
                AppState.is_sidebar_open,
                "transition-all duration-300 ease-in-out ml-64",
                "transition-all duration-300 ease-in-out ml-20",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )