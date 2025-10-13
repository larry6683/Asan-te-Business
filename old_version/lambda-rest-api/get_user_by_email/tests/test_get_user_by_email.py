import sys
# makes sure imports on lambda_handler work correctly
sys.path.append('../')

import lambda_function
from lambda_function import lambda_handler
from db.queries.app_user_query_response import AppUserQueryResponse
from db.codes.user_type_code import UserTypeCode
from api_response import ApiResponse
from errors.error_code import ErrorCode
from errors.error import Error

class Mocks:
    @staticmethod
    def get_event(email):
        return {
            'queryStringParameters': {
                'email': email
            }
        }
    
    @staticmethod
    def get_response_from_app_user(app_user: AppUserQueryResponse):
        return ApiResponse.create_response(
            200,
            {
                'data': {
                    'type': 'user',
                    'id': app_user.app_user_id,
                    'attributes': {
                        'email': app_user.email,
                        'userType': app_user.user_type_code.name
                    }
                }
            }
        )
    
    @staticmethod
    def get_not_found_response(email):
        error_code = ErrorCode.USER_EMAIL_NOT_FOUND
        return ApiResponse.create_error_response(
            404,
            Error.create_error(
                error_code,
                None,
                error_code.to_message(email)
            )
        )
    
    @staticmethod
    def get_internal_error_response():
        return ApiResponse.create_internal_error_response()

def test_get_user_success(monkeypatch):
    email = "email@email.com"
    event = Mocks.get_event(email)
    app_user = AppUserQueryResponse('id', email, UserTypeCode.BUSINESS.value)
    expected_response = Mocks.get_response_from_app_user(app_user)

    def mock_process_get_app_user(email):
        return app_user
    
    monkeypatch.setattr(lambda_function, 'process_get_app_user', mock_process_get_app_user)

    response = lambda_handler(event, None)
    assert response == expected_response

def test_get_user_not_found(monkeypatch):
    email = "email@email.com"
    event = Mocks.get_event(email)
    expected_response = Mocks.get_not_found_response(email)
    error_code = ErrorCode.USER_EMAIL_NOT_FOUND
    
    def mock_process_get_app_user(email):
        return error_code
    
    monkeypatch.setattr(lambda_function, 'process_get_app_user', mock_process_get_app_user)

    response = lambda_handler(event, None)
    assert response == expected_response

def test_get_internal_error_response(monkeypatch):
    email = "email@email.com"
    event = Mocks.get_event(email)
    expected_response = Mocks.get_internal_error_response()
    
    def mock_process_get_app_user(email):
        return ErrorCode.INTERNAL_ERROR
    
    monkeypatch.setattr(lambda_function, 'process_get_app_user', mock_process_get_app_user)

    response = lambda_handler(event, None)
    assert response == expected_response
