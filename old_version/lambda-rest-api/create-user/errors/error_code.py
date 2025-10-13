from enum import Enum

class ErrorCode(Enum):
    USER_NOT_FOUND = 100
    INVALID_USER_TYPE = 101
    ALREADY_REGISTERED_TO_BUSINESS = 102
    ALREADY_REGISTERED_TO_BENEFICIARY = 103
    UNSUPPORTED_ENTITY_TYPE = 104
    NAME_TAKEN = 105
    REGISTRATION_TYPE_MISMATCH = 106
    INSUFFICIENT_PERMISSION = 107
    USER_EMAIL_NOT_FOUND = 250
    USER_EMAIL_NOT_VERIFIED = 251
    USER_EMAIL_NOT_UNIQUE = 252
    INVALID_USER_ATTRIBUTES = 242
    EXPIRED_TOKEN = 401
    INVALID_TOKEN = 402
    RESOURCE_NOT_FOUND = 404
    INVALID_CREDENTIALS = 405
    INTERNAL_ERROR = 500
    INVALID_PARAMETER = 1000
    MISSING_QUERY_PARAMETER = 1001

    def to_message(self, value=None, entity_type=None, key=None) -> str:
        match(self):
            case ErrorCode.USER_NOT_FOUND:
                return f"User Id not found: {value}"
            case ErrorCode.INVALID_USER_TYPE:
                return f"Invalid user type: {value}"
            case ErrorCode.ALREADY_REGISTERED_TO_BUSINESS:
                return f"User already belongs to a business. id: {key} name: {value}."
            case ErrorCode.ALREADY_REGISTERED_TO_BENEFICIARY:
                return f"User already belongs to a beneficiary. id: {key} name: {value}."
            case ErrorCode.UNSUPPORTED_ENTITY_TYPE:
                return f"{entity_type} Registration not Supported"
            case ErrorCode.NAME_TAKEN:
                return f"{entity_type} Name already taken: {value}"
            case ErrorCode.REGISTRATION_TYPE_MISMATCH:
                return f"user type {value} cannot register as {entity_type}"
            case ErrorCode.INSUFFICIENT_PERMISSION:
                return f"user has insufficient permission. action: {key}.{f' must be a {value}' if value else ''}"
            case ErrorCode.USER_EMAIL_NOT_FOUND:
                return f"User email not found: {value}"
            case ErrorCode.USER_EMAIL_NOT_VERIFIED:
                return f"User email not verified: {value}"
            case ErrorCode.USER_EMAIL_NOT_UNIQUE:
                return f"User email already used: {value}"
            case ErrorCode.INVALID_USER_ATTRIBUTES:
                return f"Invalid User Attributes: {key}: {value}"
            case ErrorCode.EXPIRED_TOKEN:
                return f'Expired Token'
            case ErrorCode.INVALID_TOKEN:
                return f'Invalid Token'
            case ErrorCode.RESOURCE_NOT_FOUND:
                return "Resource Not Found"
            case ErrorCode.INVALID_CREDENTIALS:
                return "Invalid credentials"
            case ErrorCode.INTERNAL_ERROR:
                return "INTERNAL ERROR"
            case ErrorCode.INVALID_PARAMETER:
                return "Invalid Parameter"
            case _:
                return "unrecognized error"
        return "unrecognized error"