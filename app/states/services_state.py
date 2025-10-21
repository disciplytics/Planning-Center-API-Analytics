import reflex as rx
from typing import TypedDict, Any
import httpx
import logging
from app.states.auth_state import AuthState, API_BASE_URL


class ServiceType(TypedDict):
    id: str
    name: str


class Plan(TypedDict):
    id: str
    series_title: str | None
    plan_title: str | None
    dates: str
    short_dates: str
    team_positions_count: int
    filled_positions_count: int
    service_type: str


class ServicesState(rx.State):
    """Manages the state for the services page."""

    service_types: list[ServiceType] = []
    upcoming_plans: list[Plan] = []
    is_loading: bool = False

    async def _get_authed_client(self) -> httpx.AsyncClient | None:
        async with self:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated or not auth_state.access_token:
                return None
            return httpx.AsyncClient(
                headers={"Authorization": f"Bearer {auth_state.access_token}"}
            )

    @rx.event(background=True)
    async def on_load(self):
        """Load service types and upcoming plans when the page loads."""
        async with self:
            self.is_loading = True
        yield ServicesState.fetch_service_types
        yield ServicesState.fetch_upcoming_services
        async with self:
            self.is_loading = False

    @rx.event(background=True)
    async def fetch_service_types(self):
        """Fetch all service types from the Planning Center API."""
        client = await self._get_authed_client()
        if client is None:
            async with self:
                return rx.redirect("/login")
            return
        try:
            async with client:
                response = await client.get(f"{API_BASE_URL}/services/v2/service_types")
                response.raise_for_status()
                data = response.json()["data"]
                async with self:
                    self.service_types = [
                        {"id": item["id"], "name": item["attributes"]["name"]}
                        for item in data
                    ]
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching service types: {e}")

    @rx.event(background=True)
    async def fetch_upcoming_services(self):
        """Fetch upcoming service plans from the Planning Center API."""
        client = await self._get_authed_client()
        if client is None:
            async with self:
                return rx.redirect("/login")
            return
        try:
            async with client:
                response = await client.get(
                    f"{API_BASE_URL}/services/v2/plans?filter=future"
                )
                response.raise_for_status()
                data = response.json()["data"]
                async with self:
                    self.upcoming_plans = [
                        {
                            "id": item["id"],
                            "series_title": item["attributes"].get("series_title"),
                            "plan_title": item["attributes"].get("plan_title"),
                            "dates": item["attributes"]["dates"],
                            "short_dates": item["attributes"]["short_dates"],
                            "team_positions_count": item["attributes"]["total_needed"],
                            "filled_positions_count": item["attributes"][
                                "total_confirmed"
                            ],
                            "service_type": item["relationships"]["service_type"][
                                "data"
                            ]["id"],
                        }
                        for item in data
                    ]
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching upcoming plans: {e}")