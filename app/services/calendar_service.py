from google_auth_oauthlib.flow import Flow

from app.core.config import settings

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

_pending_code_verifiers: dict[str, str] = {}


class GooggleCalendarSerivce:

    @staticmethod
    def save_code_verifier(state: str, code_verifier: str) -> None:
        _pending_code_verifiers[state] = code_verifier

    @staticmethod
    def pop_code_verifier(state: str) -> str | None:
        return _pending_code_verifiers.pop(state, None)

    @staticmethod
    def create_flow():


        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [
                        settings.google_redirect_uri
                    ],
                }
            },
            scopes=SCOPES,
        )


        flow.redirect_uri = settings.google_redirect_uri

        return flow


