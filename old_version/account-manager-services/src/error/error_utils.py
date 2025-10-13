import logging
from config.config import Config
from utils.enum_utils import EnumUtils
from codegen.error.account_error_code_pb2 import AccountErrorCode as ErrorCode
from codegen.error.account_error_pb2 import AccountError as Error

class ErrorUtils:
    @staticmethod
    def create_error(error_code, detail=""):
        return Error(error_code=EnumUtils.get_enum_name(ErrorCode, error_code), detail=detail)
    
    @staticmethod
    def get_error_name(error_code):
        return EnumUtils.get_enum_name(ErrorCode, error_code)
    
    @staticmethod
    def create_parameter_error(detail):
        return ErrorUtils.create_error(ErrorCode.ERROR_INVALID_PARAMETER, detail=detail)
    
    @staticmethod
    def create_required_parameter_error(parameter_name):
        return ErrorUtils.create_parameter_error(detail=f"parameter: \'{parameter_name}\' is required")
    
    @staticmethod
    def create_enforce_parameter_uniqueness_error(parameter_name: str, parameter_value: str):
        return ErrorUtils.create_parameter_error(f"parameter: \'{parameter_name}\' with value \'{parameter_value}\' must be unique within existing data")

    @staticmethod
    def create_resource_not_found_error(resource_name: str, resource_id: str):
        return ErrorUtils.create_error(error_code=ErrorCode.ERROR_RESOURCE_NOT_FOUND, detail=f"\'{resource_name}\' with id \'{resource_id}\' not found")

    @staticmethod
    def create_operation_failed_error(method, additional_detail="", exception: Exception=None):
        detail=f"Failed operation: {method.__name__ if callable(method) else method}"
        if (detail and Config.get_logging_config()["level"] == "DEBUG"):
            detail += f" - {additional_detail}"
            logging.exception(exception)
        return ErrorUtils.create_error(ErrorCode.ERROR_OPERATION_FAILED, detail=detail)