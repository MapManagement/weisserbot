import requests
from bot.utils import secrets


def get_oauth(scope: str) -> str:
    try:
        response = requests.post(secrets.tokenurl + scope)
        response.raise_for_status()
        json_response = response.json()
        return json_response["access_token"]

    except Exception:
        return "error"
