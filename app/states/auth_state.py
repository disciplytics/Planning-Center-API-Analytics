import reflex as rx
import os
from typing import Optional
import httpx

API_BASE_URL = "https://api.planningcenteronline.com"
AUTHORIZE_URL = f"{API_BASE_URL}/oauth/authorize"
TOKEN_URL = f"{API_BASE_URL}/oauth/token"
REDIRECT_URI = "http://localhost:3000/callback"


class AuthState(rx.State):
    """Manages the authentication state of the application."""

    access_token: str | None = None
    is_authenticated: bool = False

    @rx.var
    def auth_url(self) -> str:
        """The URL to redirect the user to for authentication."""
        client_id = os.getenv("PLANNING_CENTER_APP_ID", "")
        return f"{AUTHORIZE_URL}?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code&scope=people services"

    @rx.event
    async def handle_oauth_callback(self, code: str):
        """Exchange the authorization code for an access token."""
        client_id = os.getenv("PLANNING_CENTER_APP_ID", "")
        client_secret = os.getenv("PLANNING_CENTER_SECRET", "")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": REDIRECT_URI,
                },
            )
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.is_authenticated = True
            return rx.redirect("/settings")
        else:
            print(f"Failed to get token: {response.text}")
            return rx.redirect("/login")

    @rx.event
    def logout(self):
        """Log the user out by clearing the token."""
        self.access_token = None
        self.is_authenticated = False
        return rx.redirect("/login")

    @rx.event
    def on_load(self):
        """Event handler called when a page loads. Checks for auth code."""
        code = self.router.page.params.get("code")
        if code:
            return AuthState.handle_oauth_callback(code)