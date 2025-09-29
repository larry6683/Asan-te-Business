from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_NONE: _ClassVar[ErrorCode]
    ERROR_INVALID_PARAMETER: _ClassVar[ErrorCode]
    ERROR_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_ALREADY_EXISTS: _ClassVar[ErrorCode]
    ERROR_DATABASE_ERROR: _ClassVar[ErrorCode]
    ERROR_INTERNAL: _ClassVar[ErrorCode]
ERROR_NONE: ErrorCode
ERROR_INVALID_PARAMETER: ErrorCode
ERROR_NOT_FOUND: ErrorCode
ERROR_ALREADY_EXISTS: ErrorCode
ERROR_DATABASE_ERROR: ErrorCode
ERROR_INTERNAL: ErrorCode

class Error(_message.Message):
    __slots__ = ("code", "message", "detail")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    message: str
    detail: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., message: _Optional[str] = ..., detail: _Optional[str] = ...) -> None: ...
