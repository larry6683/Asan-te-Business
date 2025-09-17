import account_error_code_pb2 as _account_error_code_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountError(_message.Message):
    __slots__ = ("error_code", "detail")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    error_code: _account_error_code_pb2.AccountErrorCode
    detail: str
    def __init__(self, error_code: _Optional[_Union[_account_error_code_pb2.AccountErrorCode, str]] = ..., detail: _Optional[str] = ...) -> None: ...
