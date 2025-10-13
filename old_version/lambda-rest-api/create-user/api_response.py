import json
from log_utils import LogUtils

class ApiResponse:
    @staticmethod
    def create_response(status_code, body):
        response = {
            "statusCode": status_code,
            "headers": {
                "Content-Type": "application/json",
                "access-control-allow-origin": "*"
            },
            "body": json.dumps(body)
        }
        LogUtils.log_object('response', response)
        return response

    @staticmethod
    def create_error_list_response(status_code, errors):
        body = {
            "errors": [error.to_error_object() for error in errors]
        }
        return ApiResponse.create_response(status_code, body)

    @staticmethod
    def create_error_response(status_code, *errors):
        return ApiResponse.create_error_list_response(status_code, errors)

    @staticmethod
    def create_internal_error_response():
        return ApiResponse.create_response(500, {
            "error": "INTERNAL_ERROR"
        })