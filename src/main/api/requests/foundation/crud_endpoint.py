from requests import Response
from typing import Optional, Protocol
from src.main.api.models.base_model import BaseModel
from typing import TypeVar

T = TypeVar("T", BaseModel, Response)

class CrudEndpoint(Protocol):
    def post(self, model:  Optional[T]) -> BaseModel | Response:...
    def get(self, user_id: Optional[BaseModel] = None) -> BaseModel | Response:...
    def delete(self, user_id: int) -> BaseModel | Response:...
