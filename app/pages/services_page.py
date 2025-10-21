import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.state import AppState
from app.states.services_state import ServicesState, Plan


def service_card(plan: Plan) -> rx.Component:
    """A card displaying information about a single service plan."""
    filled_ratio = plan["filled_positions_count"] / rx.cond(
        plan["team_positions_count"] > 0, plan["team_positions_count"], 1
    )
    return rx.el.div(
        rx.el.div(
            rx.el.p(plan["short_dates"], class_name="font-semibold text-gray-800"),
            rx.el.p(plan["dates"], class_name="text-sm text-gray-500"),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.p(
                plan["series_title"], class_name="text-sm font-medium text-gray-600"
            )
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name=f"h-2 rounded-full bg-teal-500",
                    style={"width": f"{filled_ratio * 100}%"},
                ),
                class_name="w-full bg-gray-200 rounded-full h-2",
            ),
            rx.el.p(
                f"{plan['filled_positions_count']} / {plan['team_positions_count']} positions filled",
                class_name="text-xs text-gray-500 mt-1 text-right",
            ),
            class_name="mt-4",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:shadow-lg transition-shadow duration-300 flex flex-col",
    )


def services_page() -> rx.Component:
    """The services analytics page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Upcoming Services",
                        class_name="text-xl font-bold text-gray-800",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("All Service Types", value="all"),
                            rx.foreach(
                                ServicesState.service_types,
                                lambda st: rx.el.option(st["name"], value=st["id"]),
                            ),
                            class_name="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.cond(
                    ServicesState.is_loading,
                    rx.el.div(
                        rx.spinner(size="3"),
                        class_name="flex justify-center items-center h-96",
                    ),
                    rx.el.div(
                        rx.foreach(ServicesState.upcoming_plans, service_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                    ),
                ),
                class_name="p-6 max-w-full mx-auto",
            ),
            class_name=rx.cond(
                AppState.is_sidebar_open,
                "transition-all duration-300 ease-in-out ml-64",
                "transition-all duration-300 ease-in-out ml-20",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )