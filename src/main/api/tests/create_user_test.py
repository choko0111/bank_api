import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize("create_user_request", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.create_user(create_user_request)
        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

    @pytest.mark.parametrize(
        "username, password, expected_status",
        [
            ("1", "Pas1sw0rd", 400),
            ("Max1113", "Pas!sw0", 400),
            ("Md303", "Passsw0rd", 400),
            ("MD304", "pas!sw0rd", 400),
            ("Maax03", "Pas!swwrd", 400)
        ]
    )
    def test_create_user_invalid_password(self, api_manager: ApiManager, username: str, password: str, expected_status: int):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.invalid_create_user(create_user_request, expected_status)

    def test_create_user_invalid_username(self, create_user_request: CreateUserRequest, api_manager: ApiManager):
        api_manager.admin_steps.invalid_create_user(create_user_request, expected_status_code=409)

