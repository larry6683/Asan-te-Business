from typing import Self
from .error_code import ErrorCode

class Error():
    def __init__(self, error_code: ErrorCode, error_message, field=None, value=None):
        self.error_code = error_code
        self.error_message = error_message
        self.field = field
        self.value = value
        
    def to_error_object(self):
        error = {
            "errorCode": self.error_code.value,
            "errorType": self.error_code.name,
            "message": self.error_message
        }
        if self.field:
            error['field'] = self.field
        if self.value:
            error['value'] = self.value
        return error

    @staticmethod
    def create_error(error_code: ErrorCode, field: str, error_message: str) -> Self:
        return Error(error_code, error_message, field)

    @staticmethod
    def create_invalid_parameter_error(field: str, error_message: str, value=None) -> Self:
        return Error(ErrorCode.INVALID_PARAMETER, error_message, field, value)

    @staticmethod
    def create_internal_error() -> Self:
        return Error(ErrorCode.INTERNAL_ERROR, "Internal Error", None)