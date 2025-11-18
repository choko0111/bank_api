import requests
import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.requests_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpec
from src.main.api.requests.create_user_requester import CreateUserRequester


@pytest.mark.api
class TestLoginUser:
    def test_login_admin(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = LoginUserRequester(
            request_spec=RequestSpecs.unauthorized_headers(),
            response_spec=ResponseSpec.request_ok(),
        ).post(login_user_request)

        assert login_user_request.username == response.user.username

    def test_login_user(self):
        create_user_request = CreateUserRequest(username="Maxx3334", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpec.request_ok(),
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username="Maxx3334", password="Pas!sw0rd",)

        response = LoginUserRequester(
            request_spec=RequestSpecs.unauthorized_headers(),
            response_spec=ResponseSpec.request_ok(),
        ).post(login_user_request)

        assert login_user_request.username == response.user.username