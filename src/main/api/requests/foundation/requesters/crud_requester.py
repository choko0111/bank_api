import requests
from typing import TypeVar, Optional
from requests import Response
from src.main.configs.config import Config
from src.main.api.requests.foundation.http_requester import HttpRequest
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.foundation.crud_endpoint import CrudEndpoint
from http import HTTPStatus


T = TypeVar('T', bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpoint):
    def post(self, model: Optional[T]) -> Response:
        body = model.model_dump() if model is not None else ""

        response = requests.post(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
