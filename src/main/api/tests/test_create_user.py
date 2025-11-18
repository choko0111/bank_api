import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.requests_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpec


@pytest.mark.api
class TestCreateUser:
    def test_create_valid_user(self):
        create_user_request = CreateUserRequest(username="Max13333", password="Pas!sw0rd", role="ROLE_USER")

        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpec.request_ok(),
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpec.request_ok(),
        ).delete(response.id)

    @pytest.mark.parametrize(
        "username, password, status_code",
        [
            ("Max121", "Pas!sw0rd",  409),
            ("Maxx2", "123", 400)
        ]
    )
    def test_create_invalid_user(self, username, password, status_code):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpec.request_expected_status(status_code),
        ).post(create_user_request)
