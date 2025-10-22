import reflex as rx
from typing import TypedDict
import httpx
import logging
from app.states.auth_state import AuthState, API_BASE_URL
from collections import defaultdict


class Person(TypedDict):
    id: str
    name: str
    status: str
    avatar: str


class Team(TypedDict):
    id: str
    name: str
    volunteer_count: int


class TeamPosition(TypedDict):
    id: str
    team_id: str
    person_id: str


class TeamComposition(TypedDict):
    name: str
    value: int


class PeopleState(rx.State):
    """Manages state for the people and teams analytics page."""

    all_people: list[Person] = []
    all_teams: list[Team] = []
    team_positions: list[TeamPosition] = []
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
        """Load all people and team data when the page loads."""
        async with self:
            self.is_loading = True
        yield PeopleState.fetch_all_people
        yield PeopleState.fetch_all_teams
        yield PeopleState.fetch_team_positions
        async with self:
            self.is_loading = False

    @rx.event(background=True)
    async def fetch_all_people(self):
        """Fetch all active people from the Planning Center API with pagination."""
        client = await self._get_authed_client()
        if client is None:
            return
        all_people_data = []
        next_url = f"{API_BASE_URL}/people/v2/people?where[status]=active&per_page=100"
        try:
            async with client:
                while next_url:
                    response = await client.get(next_url)
                    response.raise_for_status()
                    json_response = response.json()
                    all_people_data.extend(json_response.get("data", []))
                    next_url = json_response.get("links", {}).get("next")
            async with self:
                self.all_people = [
                    {
                        "id": item["id"],
                        "name": item["attributes"]["name"],
                        "status": item["attributes"]["status"],
                        "avatar": item["attributes"]["avatar"],
                    }
                    for item in all_people_data
                ]
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching people: {e}")
        except Exception as e:
            logging.exception(
                f"An unexpected error occurred while fetching people: {e}"
            )

    @rx.event(background=True)
    async def fetch_all_teams(self):
        """Fetch all teams from the Planning Center API with pagination."""
        client = await self._get_authed_client()
        if client is None:
            return
        all_teams_data = []
        next_url = f"{API_BASE_URL}/people/v2/teams?per_page=100"
        try:
            async with client:
                while next_url:
                    response = await client.get(next_url)
                    response.raise_for_status()
                    json_response = response.json()
                    all_teams_data.extend(json_response.get("data", []))
                    next_url = json_response.get("links", {}).get("next")
            async with self:
                self.all_teams = [
                    {
                        "id": item["id"],
                        "name": item["attributes"]["name"],
                        "volunteer_count": 0,
                    }
                    for item in all_teams_data
                ]
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching teams: {e}")
        except Exception as e:
            logging.exception(f"An unexpected error occurred while fetching teams: {e}")

    @rx.event(background=True)
    async def fetch_team_positions(self):
        """Fetch all team positions to link people to teams with pagination."""
        client = await self._get_authed_client()
        if client is None:
            return
        all_positions_data = []
        next_url = f"{API_BASE_URL}/people/v2/team_positions?per_page=100"
        try:
            async with client:
                while next_url:
                    response = await client.get(next_url)
                    response.raise_for_status()
                    json_response = response.json()
                    all_positions_data.extend(json_response.get("data", []))
                    next_url = json_response.get("links", {}).get("next")
            async with self:
                self.team_positions = [
                    {
                        "id": item["id"],
                        "team_id": item["relationships"]["team"]["data"]["id"],
                        "person_id": item["relationships"]["person"]["data"]["id"],
                    }
                    for item in all_positions_data
                    if item.get("relationships", {}).get("person")
                ]
        except httpx.HTTPStatusError as e:
            logging.exception(f"Error fetching team positions: {e}")
        except Exception as e:
            logging.exception(
                f"An unexpected error occurred while fetching team positions: {e}"
            )

    @rx.var
    def total_volunteers(self) -> int:
        """Returns the total number of active volunteers."""
        return len(self.all_people)

    @rx.var
    def total_teams(self) -> int:
        """Returns the total number of teams."""
        return len(self.all_teams)

    @rx.var
    def team_composition(self) -> list[TeamComposition]:
        """Calculates the number of volunteers per team."""
        if not self.all_teams or not self.team_positions:
            return []
        team_counts = defaultdict(int)
        team_id_to_name = {team["id"]: team["name"] for team in self.all_teams}
        active_person_ids = {person["id"] for person in self.all_people}
        for position in self.team_positions:
            if position["person_id"] in active_person_ids:
                team_name = team_id_to_name.get(position["team_id"])
                if team_name:
                    team_counts[team_name] += 1
        return sorted(
            [{"name": name, "value": count} for name, count in team_counts.items()],
            key=lambda x: x["value"],
            reverse=True,
        )