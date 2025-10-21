import reflex as rx
from app.states.state import AppState, NavItem


def nav_item(item: NavItem) -> rx.Component:
    """A single navigation item."""
    return rx.el.a(
        rx.el.div(
            rx.icon(item["icon"], class_name="h-5 w-5"),
            rx.el.span(
                item["name"],
                class_name=rx.cond(
                    AppState.is_sidebar_open,
                    "opacity-100 transition-opacity duration-300 ease-in-out",
                    "opacity-0",
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        href=item["route"],
        on_click=lambda: AppState.set_active_page(item["name"]),
        class_name=rx.cond(
            AppState.active_page == item["name"],
            "flex items-center px-4 py-3 text-sm font-semibold text-white bg-teal-600 rounded-lg transition-colors duration-200",
            "flex items-center px-4 py-3 text-sm font-medium text-gray-200 hover:bg-gray-700 rounded-lg transition-colors duration-200",
        ),
    )


def sidebar() -> rx.Component:
    """The navigation sidebar."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("church", class_name="h-8 w-8 text-teal-400"),
                rx.el.h1(
                    "PCO Analytics",
                    class_name=rx.cond(
                        AppState.is_sidebar_open,
                        "text-xl font-bold text-white transition-opacity duration-300 ease-in-out",
                        "opacity-0",
                    ),
                ),
                class_name="flex items-center gap-3 p-4",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.foreach(AppState.nav_items, nav_item),
                    class_name="flex flex-col gap-2",
                ),
                class_name="flex-1 px-4",
            ),
            rx.el.div(
                rx.el.div(class_name="flex-grow border-t border-gray-700"),
                rx.el.a(
                    rx.el.div(
                        rx.el.img(
                            src="https://api.dicebear.com/9.x/initials/svg?seed=Admin",
                            class_name="h-10 w-10 rounded-full border-2 border-gray-600",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Admin User",
                                class_name="font-semibold text-white text-sm",
                            ),
                            rx.el.p(
                                "admin@example.com", class_name="text-xs text-gray-400"
                            ),
                            class_name=rx.cond(
                                AppState.is_sidebar_open,
                                "flex flex-col transition-opacity duration-300 ease-in-out",
                                "opacity-0",
                            ),
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    href="#",
                    class_name="flex items-center p-4 text-white hover:bg-gray-700 transition-colors duration-200",
                ),
                class_name="mt-auto",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=rx.cond(
            AppState.is_sidebar_open,
            "h-screen bg-gray-800 text-white shadow-2xl transition-width duration-300 ease-in-out fixed left-0 top-0 z-50 w-64",
            "h-screen bg-gray-800 text-white shadow-2xl transition-width duration-300 ease-in-out fixed left-0 top-0 z-50 w-20",
        ),
    )