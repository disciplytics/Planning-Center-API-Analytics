import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.state import AppState
from app.states.people_state import PeopleState, Person, TeamComposition


def overview_metric_card(title: str, value: str, icon: str) -> rx.Component:
    """A card for displaying a single overview metric."""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-gray-500"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
            class_name="ml-4",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex items-center",
    )


def volunteer_card(person: Person) -> rx.Component:
    """Card to display a single volunteer."""
    return rx.el.div(
        rx.el.img(src=person["avatar"], class_name="h-16 w-16 rounded-full mx-auto"),
        rx.el.p(
            person["name"],
            class_name="mt-2 text-sm font-semibold text-gray-800 text-center",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm",
    )


def team_composition_chart(data: rx.Var[list[TeamComposition]]) -> rx.Component:
    """Chart to visualize team composition."""
    return rx.el.div(
        rx.el.h3(
            "Team Composition", class_name="text-lg font-semibold text-gray-700 mb-4"
        ),
        rx.recharts.responsive_container(
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    horizontal=False,
                    vertical=True,
                    stroke="#e5e7eb",
                ),
                rx.recharts.x_axis(
                    type_="number", tick_line=False, axis_line=False, stroke="#a1a1aa"
                ),
                rx.recharts.y_axis(
                    type_="category",
                    data_key="name",
                    tick_line=False,
                    axis_line=False,
                    stroke="#a1a1aa",
                ),
                rx.recharts.tooltip(content_style={"borderRadius": "16px"}),
                rx.recharts.bar(data_key="value", fill="#14b8a6", radius=[0, 4, 4, 0]),
                data=data,
                layout="horizontal",
                margin={"left": 100, "right": 20, "top": 20, "bottom": 20},
            ),
            height=400,
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
    )


def people_page() -> rx.Component:
    """The people and teams analytics page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.cond(
                    PeopleState.is_loading,
                    rx.el.div(
                        rx.spinner(size="3"),
                        class_name="flex justify-center items-center h-[80vh]",
                    ),
                    rx.el.div(
                        rx.el.div(
                            overview_metric_card(
                                "Total Volunteers",
                                PeopleState.total_volunteers.to_string(),
                                "users",
                            ),
                            overview_metric_card(
                                "Total Teams",
                                PeopleState.total_teams.to_string(),
                                "shield",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Volunteer Roster",
                                    class_name="text-lg font-semibold text-gray-700 mb-4",
                                ),
                                rx.el.div(
                                    rx.foreach(PeopleState.all_people, volunteer_card),
                                    class_name="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4",
                                ),
                                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
                            ),
                            team_composition_chart(PeopleState.team_composition),
                            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6",
                        ),
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