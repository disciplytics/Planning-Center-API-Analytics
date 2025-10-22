import reflex as rx
from typing import TypedDict, Optional
import httpx
import logging
from app.states.auth_state import AuthState, API_BASE_URL


class FieldDefinition(TypedDict):
    id: str
    name: str


class SettingsState(rx.State):
    """Manages application settings, including field definitions."""

    field_definitions: list[FieldDefinition] = []
    selected_field_ids: list[str] = rx.LocalStorage([], name="selected_field_ids")
    is_loading: bool = False

    async def _get_authed_client(self) -> httpx.AsyncClient | None:
        token = None
        async with self:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated or not auth_state.access_token:
                return None
            token = auth_state.access_token
        return httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"})

    @rx.event(background=True)
    async def on_load(self):
        """Load field definitions when the settings page loads."""
        async with self:
            self.is_loading = True
        yield SettingsState.fetch_field_definitions
        async with self:
            self.is_loading = False

    @rx.event(background=True)
    async def fetch_field_definitions(self):
        """Fetch all field definitions from the Planning Center API."""
        client = await self._get_authed_client()
        if client is None:
            return
        all_defs_data = []
        next_url = f"{API_BASE_URL}/people/v2/field_definitions?per_page=100"
        try:
            async with client:
                while next_url:
                    response = await client.get(next_url)
                    response.raise_for_status()
                    json_response = response.json()
                    all_defs_data.extend(json_response.get("data", []))
                    next_url = json_response.get("links", {}).get("next")
            async with self:
                self.field_definitions = sorted(
                    [
                        {"id": item["id"], "name": item["attributes"]["name"]}
                        for item in all_defs_data
                    ],
                    key=lambda x: x["name"],
                )
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching field definitions: {e}")
        except Exception as e:
            logging.exception(
                f"An unexpected error occurred while fetching field definitions: {e}"
            )

    @rx.event
    def toggle_field_definition(self, field_id: str):
        """Toggle the selection state of a field definition."""
        new_list = [i for i in self.selected_field_ids]
        if field_id in new_list:
            new_list.remove(field_id)
        else:
            new_list.append(field_id)
        self.selected_field_ids = new_list

    @rx.var
    def selected_field_count(self) -> int:
        """Returns the number of selected field definitions."""
        return len(self.selected_field_ids)