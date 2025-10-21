import reflex as rx
from app.states.state import AppState, Metric, ChartData, Insight, MetricTrend


def metric_card(metric: Metric) -> rx.Component:
    """A card for displaying a single metric with trend indicator."""
    trend = AppState.metric_trends.get(
        metric["title"], {"change": "", "direction": "neutral"}
    )
    trend_color = rx.cond(
        trend["direction"] == "up",
        "text-green-500",
        rx.cond(trend["direction"] == "down", "text-red-500", "text-gray-500"),
    )
    trend_icon = rx.cond(
        trend["direction"] == "up",
        "arrow-up",
        rx.cond(trend["direction"] == "down", "arrow-down", "minus"),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.p(metric["title"], class_name="text-sm font-medium text-gray-500"),
            rx.icon(metric["icon"], class_name=f"h-6 w-6 {metric['color']}"),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.el.p(metric["value"], class_name="text-3xl font-bold text-gray-800"),
            rx.cond(
                trend["change"] != "",
                rx.el.div(
                    rx.icon(trend_icon, class_name=f"h-4 w-4 {trend_color}"),
                    rx.el.span(
                        trend["change"],
                        class_name=f"text-sm font-semibold {trend_color}",
                    ),
                    class_name="flex items-center gap-1 mt-1",
                ),
            ),
            class_name="flex items-baseline gap-2 mt-2",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg transition-shadow duration-300",
    )


def insight_card(insight: Insight) -> rx.Component:
    """A card for displaying a single automated insight."""
    return rx.el.div(
        rx.icon(insight["icon"], class_name=f"h-6 w-6 {insight['color']}"),
        rx.el.p(insight["text"], class_name="text-sm text-gray-700 font-medium ml-4"),
        class_name="flex items-center bg-gray-100/80 p-4 rounded-xl border border-gray-200",
    )


def chart_card(
    title: str, chart_data: rx.Var[list[ChartData]], line_color: str
) -> rx.Component:
    """A card for displaying a chart."""
    return rx.el.div(
        rx.el.h3(
            title, class_name="text-lg font-semibold text-gray-700 mb-4 px-6 pt-6"
        ),
        rx.recharts.responsive_container(
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", horizontal=True, vertical=False
                ),
                rx.recharts.x_axis(
                    data_key="name", tick_line=False, axis_line=False, stroke="#A1A1AA"
                ),
                rx.recharts.y_axis(tick_line=False, axis_line=False, stroke="#A1A1AA"),
                rx.recharts.tooltip(content_style={"borderRadius": "16px"}),
                rx.recharts.line(
                    type="monotone",
                    data_key="pv",
                    stroke=line_color,
                    stroke_width=2,
                    dot=False,
                ),
                data=chart_data,
            ),
            height=300,
        ),
        class_name="bg-white rounded-2xl border border-gray-100 shadow-sm",
    )


def dashboard() -> rx.Component:
    """The main dashboard content."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p("Last updated:", class_name="text-sm text-gray-500"),
                rx.el.p(
                    AppState.last_updated,
                    class_name="text-sm font-semibold text-gray-700",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-4 w-4"),
                "Refresh",
                on_click=AppState.update_dashboard_metrics,
                class_name="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-teal-600 rounded-lg shadow-sm hover:bg-teal-700 transition-colors",
                disabled=AppState.dashboard_loading,
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.cond(
            AppState.dashboard_loading,
            rx.el.div(
                rx.spinner(class_name="h-8 w-8 text-teal-600"),
                class_name="flex justify-center items-center h-64",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(AppState.metrics, metric_card),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Insights",
                        class_name="text-lg font-semibold text-gray-700 mt-8 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(AppState.insights, insight_card),
                        class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
                    ),
                    class_name=rx.cond(
                        AppState.insights.length() > 0, "block", "hidden"
                    ),
                ),
                rx.el.div(
                    chart_card(
                        "Service Attendance", AppState.service_chart_data, "#14b8a6"
                    ),
                    chart_card("Team Engagement", AppState.team_chart_data, "#6366f1"),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8",
                ),
            ),
        ),
        class_name="p-6 max-w-7xl mx-auto",
    )