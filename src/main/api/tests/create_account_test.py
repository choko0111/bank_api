import pytest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, create_user_request, api_manager):
        response_create_account = api_manager.user_steps.create_account(create_user_request)

        assert response_create_account.balance == 0
