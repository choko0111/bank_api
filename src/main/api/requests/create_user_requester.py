# from http import HTTPStatus
# from requests import Response
# from src.main.api.models.create_user_request import CreateUserRequest
# from src.main.api.models.create_user_response import CreateUserResponse
# from src.main.api.requests.requester import CustomRequester
# import requests
#
#
#
# class CreateUserRequester(CustomRequester):
#     def post(self, create_user_request: CreateUserRequest) -> CreateUserResponse | Response:
#         url = f"{self.base_url}/admin/create"
#         response = requests.post(
#             url=url,
#             json=create_user_request.model_dump(),
#             headers=self.headers
#         )
#         self.response_spec(response)
#         if response.status_code in [HTTPStatus.CREATED, HTTPStatus.OK]:
#             return CreateUserResponse(**response.json())
#         return response
#
#     def delete(self, user_id: int):
#         url = f"{self.base_url}/admin/users/{user_id}"
#         response = requests.delete(
#             url=url,
#             headers=self.headers
#         )
#         self.response_spec(response)
