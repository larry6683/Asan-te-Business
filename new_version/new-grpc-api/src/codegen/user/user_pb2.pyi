from error import error_pb2 as _error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "email", "user_type", "mailing_list_signup")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAILING_LIST_SIGNUP_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    user_type: str
    mailing_list_signup: bool
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., user_type: _Optional[str] = ..., mailing_list_signup: bool = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user", "errors")
    USER_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    user: User
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("email", "user_type", "mailing_list_signup")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAILING_LIST_SIGNUP_FIELD_NUMBER: _ClassVar[int]
    email: str
    user_type: str
    mailing_list_signup: bool
    def __init__(self, email: _Optional[str] = ..., user_type: _Optional[str] = ..., mailing_list_signup: bool = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("user", "errors")
    USER_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    user: User
    errors: _containers.RepeatedCompositeFieldContainer[_error_pb2.Error]
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_error_pb2.Error, _Mapping]]] = ...) -> None: ...
