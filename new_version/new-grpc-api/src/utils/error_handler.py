from codegen.error.error_pb2 import Error, ErrorCode

class ErrorHandler:
    
    @staticmethod
    def create_error(code: ErrorCode, message: str, detail: str = '') -> Error:
        return Error(code=code, message=message, detail=detail)
    
    @staticmethod
    def invalid_parameter(param_name: str) -> Error:
        return ErrorHandler.create_error(
            ErrorCode.ERROR_INVALID_PARAMETER,
            'Invalid parameter',
            f'Parameter "{param_name}" is invalid or missing'
        )
    
    @staticmethod
    def not_found(entity_type: str, identifier: str) -> Error:
        return ErrorHandler.create_error(
            ErrorCode.ERROR_NOT_FOUND,
            f'{entity_type} not found',
            f'{entity_type} with identifier "{identifier}" does not exist'
        )
    
    @staticmethod
    def already_exists(entity_type: str, field: str, value: str) -> Error:
        return ErrorHandler.create_error(
            ErrorCode.ERROR_ALREADY_EXISTS,
            f'{entity_type} already exists',
            f'{entity_type} with {field} "{value}" already exists'
        )
    
    @staticmethod
    def database_error(detail: str = '') -> Error:
        return ErrorHandler.create_error(
            ErrorCode.ERROR_DATABASE_ERROR,
            'Database operation failed',
            detail
        )
    
    @staticmethod
    def internal_error(detail: str = '') -> Error:
        return ErrorHandler.create_error(
            ErrorCode.ERROR_INTERNAL,
            'Internal server error',
            detail
        )
