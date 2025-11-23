from src.main.api.requests.foundation.http_requester import HttpRequest
from src.main.api.requests.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequest):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec,
        )

    def post(self, model: BaseModel):
        response = self.crud_requester.post(model)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())