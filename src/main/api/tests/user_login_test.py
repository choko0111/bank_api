import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.foundation.requesters.validated_crud_requester import ValidateCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.foundation.endpoint import Endpoint



@pytest.mark.api
class TestUserLogin:
    @pytest.mark.parametrize("auth_request_admin", [(LoginUserRequest(username="admin", password="123456"))])
    def test_login_admin(self, auth_request_admin, api_manager: ApiManager):
        response_auth_admin = api_manager.admin_steps.login_user(auth_request_admin)

        assert auth_request_admin.username == response_auth_admin.user.username
        assert response_auth_admin.user.role == "ROLE_ADMIN"

    def test_login_user(self, create_user_request, api_manager: ApiManager):
        response_auth_user = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response_auth_user.user.username
        assert response_auth_user.user.role == "ROLE_USER"