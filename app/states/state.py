import reflex as rx
from typing import TypedDict
import httpx
import logging
from datetime import datetime, timedelta


class NavItem(TypedDict):
    name: str
    icon: str
    route: str


class Metric(TypedDict):
    title: str
    value: str
    icon: str
    color: str


class ChartData(TypedDict):
    name: str
    uv: int
    pv: int


class MetricTrend(TypedDict):
    change: str
    direction: str


class Insight(TypedDict):
    text: str
    icon: str
    color: str


class AppState(rx.State):
    """The main application state."""

    active_page: str = "Dashboard"
    is_sidebar_open: bool = True
    theme: str = rx.LocalStorage("light", name="theme")
    sync_interval: str = rx.LocalStorage("15", name="sync_interval")
    dashboard_loading: bool = False
    last_updated: str = "Never"
    previous_metrics: list[Metric] = []
    nav_items: list[NavItem] = [
        {"name": "Dashboard", "icon": "layout-dashboard", "route": "/"},
        {"name": "Services", "icon": "calendar-days", "route": "/services"},
        {"name": "People", "icon": "users", "route": "/people"},
        {"name": "Teams", "icon": "shield", "route": "/teams"},
        {"name": "Settings", "icon": "settings", "route": "/settings"},
    ]
    metrics: list[Metric] = [
        {
            "title": "Total Volunteers",
            "value": "0",
            "icon": "users",
            "color": "text-teal-500",
        },
        {
            "title": "Upcoming Services",
            "value": "0",
            "icon": "calendar",
            "color": "text-indigo-500",
        },
        {
            "title": "Open Positions",
            "value": "0",
            "icon": "user-plus",
            "color": "text-amber-500",
        },
        {
            "title": "New Members",
            "value": "0",
            "icon": "user-check",
            "color": "text-green-500",
        },
    ]
    service_chart_data: list[ChartData] = []
    team_chart_data: list[ChartData] = []
    metric_trends: dict[str, MetricTrend] = {}
    insights: list[Insight] = []
    metric_trends: dict[str, MetricTrend] = {}
    insights: list[Insight] = []

    async def _get_authed_client(self) -> httpx.AsyncClient | None:
        from app.states.auth_state import AuthState

        token = None
        async with self:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated or not auth_state.access_token:
                return None
            token = auth_state.access_token
        return httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"})

    @rx.event
    def set_active_page(self, page: str):
        """Set the active page."""
        self.active_page = page

    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar open/closed."""
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_theme(self):
        """Toggle the theme between light and dark."""
        self.theme = "dark" if self.theme == "light" else "light"

    @rx.event
    def set_sync_interval(self, interval: str):
        """Set the data sync interval."""
        self.sync_interval = interval

    @rx.event(background=True)
    async def on_load(self):
        """Check auth and load dashboard data."""
        from app.states.auth_state import AuthState

        is_authed = False
        async with self:
            auth_state = await self.get_state(AuthState)
            is_authed = auth_state.is_authenticated
        if not is_authed:
            if self.router.page.path not in ["/login", "/callback"]:
                yield rx.redirect("/login")
                return
            return
        async with self:
            self.dashboard_loading = True
        yield AppState.update_dashboard_metrics
        async with self:
            self.dashboard_loading = False

    def _calculate_trends(self):
        if not self.previous_metrics:
            self.metric_trends = {
                m["title"]: {"change": "", "direction": "neutral"} for m in self.metrics
            }
            return
        trends = {}
        prev_map = {
            m["title"]: int(m["value"].replace(",", "")) for m in self.previous_metrics
        }
        for metric in self.metrics:
            title = metric["title"]
            current_value = int(metric["value"].replace(",", ""))
            prev_value = prev_map.get(title, 0)
            if prev_value > 0:
                change = (current_value - prev_value) / prev_value * 100
                direction = "up" if change > 0 else "down"
                trends[title] = {
                    "change": f"{abs(change):.1f}%",
                    "direction": direction,
                }
            else:
                trends[title] = {"change": "", "direction": "neutral"}
        self.metric_trends = trends

    def _generate_insights(self):
        insights = []
        for metric in self.metrics:
            if metric["title"] == "Open Positions" and int(metric["value"]) > 0:
                insights.append(
                    {
                        "text": f"{metric['value']} positions need filling across upcoming services.",
                        "icon": "alert-circle",
                        "color": "text-amber-600",
                    }
                )
            if metric["title"] == "New Members" and int(metric["value"]) > 0:
                insights.append(
                    {
                        "text": f"{metric['value']} new people joined in the last 30 days.",
                        "icon": "party-popper",
                        "color": "text-green-600",
                    }
                )
        self.insights = insights

    def _calculate_trends(self):
        if not self.previous_metrics:
            self.metric_trends = {
                m["title"]: {"change": "", "direction": "neutral"} for m in self.metrics
            }
            return
        trends = {}
        prev_map = {
            m["title"]: int(m["value"].replace(",", "")) for m in self.previous_metrics
        }
        for metric in self.metrics:
            title = metric["title"]
            current_value = int(metric["value"].replace(",", ""))
            prev_value = prev_map.get(title, 0)
            if prev_value > 0:
                change = (current_value - prev_value) / prev_value * 100
                direction = "up" if change > 0 else "down"
                trends[title] = {
                    "change": f"{abs(change):.1f}%",
                    "direction": direction,
                }
            else:
                trends[title] = {"change": "", "direction": "neutral"}
        self.metric_trends = trends

    def _generate_insights(self):
        insights = []
        for metric in self.metrics:
            if metric["title"] == "Open Positions" and int(metric["value"]) > 0:
                insights.append(
                    {
                        "text": f"{metric['value']} positions need filling across upcoming services.",
                        "icon": "alert-circle",
                        "color": "text-amber-600",
                    }
                )
            if metric["title"] == "New Members" and int(metric["value"]) > 0:
                insights.append(
                    {
                        "text": f"{metric['value']} new people joined in the last 30 days.",
                        "icon": "party-popper",
                        "color": "text-green-600",
                    }
                )
        self.insights = insights

    @rx.event(background=True)
    async def update_dashboard_metrics(self):
        """Fetch all metrics for the dashboard from the Planning Center API."""
        from app.states.auth_state import API_BASE_URL

        async with self:
            self.dashboard_loading = True
        client = await self._get_authed_client()
        if client is None:
            async with self:
                self.dashboard_loading = False
            return
        try:
            async with client:
                people_res = await client.get(
                    f"{API_BASE_URL}/people/v2/people?where[status]=active&per_page=1"
                )
                people_res.raise_for_status()
                total_volunteers = (
                    people_res.json().get("meta", {}).get("total_count", 0)
                )
                plans_res = await client.get(
                    f"{API_BASE_URL}/services/v2/plans?filter=future"
                )
                plans_res.raise_for_status()
                plans_data = plans_res.json()["data"]
                upcoming_services_count = len(plans_data)
                open_positions = sum(
                    (
                        plan["attributes"].get("needed_positions_count", 0)
                        for plan in plans_data
                    )
                )
                thirty_days_ago = (
                    datetime.utcnow() - timedelta(days=30)
                ).isoformat() + "Z"
                new_members_res = await client.get(
                    f"{API_BASE_URL}/people/v2/people?where[created_at][gt]={thirty_days_ago}"
                )
                new_members_res.raise_for_status()
                new_members_count = (
                    new_members_res.json().get("meta", {}).get("total_count", 0)
                )
            async with self:
                self.previous_metrics = self.metrics
                self.metrics = [
                    {
                        "title": "Total Volunteers",
                        "value": f"{total_volunteers:,}",
                        "icon": "users",
                        "color": "text-teal-500",
                    },
                    {
                        "title": "Upcoming Services",
                        "value": str(upcoming_services_count),
                        "icon": "calendar",
                        "color": "text-indigo-500",
                    },
                    {
                        "title": "Open Positions",
                        "value": str(open_positions),
                        "icon": "user-plus",
                        "color": "text-amber-500",
                    },
                    {
                        "title": "New Members",
                        "value": str(new_members_count),
                        "icon": "user-check",
                        "color": "text-green-500",
                    },
                ]
                self.last_updated = datetime.utcnow().strftime("%b %d, %Y %I:%M %p UTC")
                self._calculate_trends()
                self._generate_insights()
                self.dashboard_loading = False
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching dashboard metrics: {e}")
            async with self:
                self.dashboard_loading = False
                self.dashboard_loading = False