from ..auth import auth_pb2 as _auth_pb2
from ..error import user_error_pb2 as _user_error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateUserRequest(_message.Message):
    __slots__ = ("user",)
    class User(_message.Message):
        __slots__ = ("email", "user_type", "mailing_list_signup")
        EMAIL_FIELD_NUMBER: _ClassVar[int]
        USER_TYPE_FIELD_NUMBER: _ClassVar[int]
        MAILING_LIST_SIGNUP_FIELD_NUMBER: _ClassVar[int]
        email: str
        user_type: str
        mailing_list_signup: bool
        def __init__(self, email: _Optional[str] = ..., user_type: _Optional[str] = ..., mailing_list_signup: bool = ...) -> None: ...
    USER_FIELD_NUMBER: _ClassVar[int]
    user: CreateUserRequest.User
    def __init__(self, user: _Optional[_Union[CreateUserRequest.User, _Mapping]] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("user", "errors")
    class User(_message.Message):
        __slots__ = ("id", "email", "user_type")
        ID_FIELD_NUMBER: _ClassVar[int]
        EMAIL_FIELD_NUMBER: _ClassVar[int]
        USER_TYPE_FIELD_NUMBER: _ClassVar[int]
        id: str
        email: str
        user_type: str
        def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., user_type: _Optional[str] = ...) -> None: ...
    USER_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    user: CreateUserResponse.User
    errors: _containers.RepeatedCompositeFieldContainer[_user_error_pb2.UserError]
    def __init__(self, user: _Optional[_Union[CreateUserResponse.User, _Mapping]] = ..., errors: _Optional[_Iterable[_Union[_user_error_pb2.UserError, _Mapping]]] = ...) -> None: ...
