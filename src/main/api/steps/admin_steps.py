from src.main.api.models.comparison_models.model_assertions import ModelAssertions
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.foundation import endpoint
from src.main.api.requests.foundation.requesters.validated_crud_requester import ValidateCrudRequester
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.base_step import BaseSteps
from src.main.api.requests.foundation.requesters.crud_requester import CrudRequester
from src.main.api.requests.foundation.endpoint import Endpoint


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)
        ModelAssertions(create_user_request, response).match()

        self.created_obj.append(response)
        return response

    def invalid_create_user(self, create_user_request: CreateUserRequest, expected_status_code: int):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.request_expected_status(expected_status_code)
        ).post(create_user_request)

    def delete_user(self, user_id: int):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            endpoint=Endpoint.ADMIN_DELETE_USER,
            response_spec=ResponseSpecs.request_ok()
        ).delete(user_id)

    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.unauth_headers(),
            endpoint=Endpoint.USER_LOGIN,
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response
