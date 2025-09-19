from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class UserErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_UNSPECIFIED: _ClassVar[UserErrorCode]
    ERROR_INVALID_PARAMETER: _ClassVar[UserErrorCode]
    ERROR_USER_NOT_FOUND: _ClassVar[UserErrorCode]
    ERROR_INVALID_ENTITY_TYPE: _ClassVar[UserErrorCode]
    ERROR_ENTITY_USER_NOT_FOUND: _ClassVar[UserErrorCode]
    ERROR_INVALID_PERMISSION_ROLE: _ClassVar[UserErrorCode]
    ERROR_OPERATION_FAILED: _ClassVar[UserErrorCode]
    ERROR_EMAIL_ALREADY_REGISTERED: _ClassVar[UserErrorCode]
    ERROR_USER_EMAIL_NOT_FOUND: _ClassVar[UserErrorCode]
    ERROR_USER_EMAIL_NOT_VERIFIED: _ClassVar[UserErrorCode]
    ERROR_USER_EMAIL_NOT_UNIQUE: _ClassVar[UserErrorCode]
    ERROR_INVALID_USER_ATTRIBUTES: _ClassVar[UserErrorCode]
ERROR_UNSPECIFIED: UserErrorCode
ERROR_INVALID_PARAMETER: UserErrorCode
ERROR_USER_NOT_FOUND: UserErrorCode
ERROR_INVALID_ENTITY_TYPE: UserErrorCode
ERROR_ENTITY_USER_NOT_FOUND: UserErrorCode
ERROR_INVALID_PERMISSION_ROLE: UserErrorCode
ERROR_OPERATION_FAILED: UserErrorCode
ERROR_EMAIL_ALREADY_REGISTERED: UserErrorCode
ERROR_USER_EMAIL_NOT_FOUND: UserErrorCode
ERROR_USER_EMAIL_NOT_VERIFIED: UserErrorCode
ERROR_USER_EMAIL_NOT_UNIQUE: UserErrorCode
ERROR_INVALID_USER_ATTRIBUTES: UserErrorCode
