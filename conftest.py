from src.main.api.fixtures.admin_fixture import *
from src.main.api.fixtures.api_fixture import *
from src.main.api.fixtures.object_fixture import *



@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def api_manager(created_obj):
    return ApiManager(created_obj)

@pytest.fixture
def created_obj():
    objects: List[Any] = []
    yield objects
    clean_users(objects)

def clean_users(objects: List[Any]):
    api_manager = ApiManager()
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f"Error in delete user_id: {u}")

