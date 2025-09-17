from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class AccountErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_UNSPECIFIED: _ClassVar[AccountErrorCode]
    ERROR_INVALID_PARAMETER: _ClassVar[AccountErrorCode]
    ERROR_RESOURCE_NOT_FOUND: _ClassVar[AccountErrorCode]
    ERROR_INVALID_ENTITY_TYPE: _ClassVar[AccountErrorCode]
    ERROR_ENTITY_USER_NOT_FOUND: _ClassVar[AccountErrorCode]
    ERROR_INVALID_PERMISSION_ROLE: _ClassVar[AccountErrorCode]
    ERROR_OPERATION_FAILED: _ClassVar[AccountErrorCode]
    ERROR_EMAIL_ALREADY_REGISTERED: _ClassVar[AccountErrorCode]
    ERROR_PARAMETER_MUST_BE_UNIQUE: _ClassVar[AccountErrorCode]
ERROR_UNSPECIFIED: AccountErrorCode
ERROR_INVALID_PARAMETER: AccountErrorCode
ERROR_RESOURCE_NOT_FOUND: AccountErrorCode
ERROR_INVALID_ENTITY_TYPE: AccountErrorCode
ERROR_ENTITY_USER_NOT_FOUND: AccountErrorCode
ERROR_INVALID_PERMISSION_ROLE: AccountErrorCode
ERROR_OPERATION_FAILED: AccountErrorCode
ERROR_EMAIL_ALREADY_REGISTERED: AccountErrorCode
ERROR_PARAMETER_MUST_BE_UNIQUE: AccountErrorCode
