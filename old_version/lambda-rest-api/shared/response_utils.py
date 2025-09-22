import json
from log_utils import LogUtils
from errors.error_code import ErrorCode
from utils import Utils

class ResponseUtils:
    @staticmethod
    def create_response(status_code, body):
        if not isinstance(body, dict):
            body = Utils.obj_to_dict(body)
        
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

    # @staticmethod
    # def create_error_list_response(status_code, errors):
    #     body = {
    #         "errors": [error.to_error_object() for error in errors]
    #     }
    #     return ResponseUtils.create_response(status_code, body)

    # @staticmethod
    # def create_error_response(status_code, *errors):
    #     return ResponseUtils.create_error_list_response(status_code, errors)

    @staticmethod
    def create_internal_error_response():
        # instead of going through the motions
        # of using the ApiError objects, just make the correct structure here
        error_code = ErrorCode.INTERNAL_ERROR
        return ResponseUtils.create_response(
            500,
            {
                "errors": [
                    {
                        "status": "500",
                        "code": error_code.value,
                        "title": error_code.name,
                        "detail": error_code.to_message()
                    }
                ]
            }
        )