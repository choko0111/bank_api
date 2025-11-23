from src.main.api.classes import api_manager
from src.main.api.requests.foundation.endpoint import Endpoint
from src.main.api.requests.foundation.requesters.validated_crud_requester import ValidateCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_step import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_created()
        ).post(create_user_request)
        return response