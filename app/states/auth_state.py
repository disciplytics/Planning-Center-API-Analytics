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

    access_token: str | None = rx.LocalStorage(name="pco_access_token")
    is_authenticated: bool = False
    error_message: str = ""

    @rx.var
    def auth_url(self) -> str:
        """The URL to redirect the user to for authentication."""
        client_id = os.getenv("PLANNING_CENTER_APP_ID", "")
        redirect_uri_encoded = "http%3A%2F%2Flocalhost%3A3000%2Fcallback"
        scope_encoded = "people%20services"
        return f"{AUTHORIZE_URL}?client_id={client_id}&redirect_uri={redirect_uri_encoded}&response_type=code&scope={scope_encoded}"

    @rx.event
    async def handle_oauth_callback(self, code: str):
        """Exchange the authorization code for an access token."""
        self.error_message = ""
        client_id = os.getenv("PLANNING_CENTER_APP_ID", "")
        client_secret = os.getenv("PLANNING_CENTER_SECRET", "")
        try:
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
                response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.is_authenticated = True
            return rx.redirect("/settings")
        except httpx.HTTPStatusError as e:
            error_details = e.response.json()
            self.error_message = (
                f"API Error: {error_details.get('error_description', e.response.text)}"
            )
            logging.exception(f"OAuth Error: {self.error_message}")
        except Exception as e:
            self.error_message = f"An unexpected error occurred: {str(e)}"
            logging.exception("OAuth callback failed unexpectedly.")

    @rx.event
    def logout(self):
        """Log the user out by clearing the token."""
        self.access_token = None
        self.is_authenticated = False
        return rx.redirect("/login")

    @rx.event
    def on_load(self):
        """Event handler called when a page loads. Checks for auth code."""
        if self.access_token:
            self.is_authenticated = True
            return
        code = self.router.page.params.get("code")
        if code and self.router.page.path == "/callback":
            return AuthState.handle_oauth_callback(code)