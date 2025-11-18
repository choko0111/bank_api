import requests

from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.configs.config import Config


class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "accept": "application/json",
        }

    @staticmethod
    def unauthorized_headers():
        return {
            "headers": RequestSpecs.base_headers(),
            "base_url": Config.fetch("backendUrl"),
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f"{Config.fetch("backendUrl")}auth/token/login",
            json=request.model_dump()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return {
                "headers": headers,
                "base_url": Config.fetch("backendUrl")
            }
        raise Exception("Failed to authenticate")
